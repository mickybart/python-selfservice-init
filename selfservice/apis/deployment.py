# Copyright (c) 2018 Yellow Pages Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Deployment module

API to deploy services for a specific repository
"""

from flask import request
from flask_restplus import Namespace, Resource, fields
import requests
from selfservice.kubernetes import Kubernetes
import selfservice.settings as settings

api = Namespace('deployment', description='Deploying services for Kubernetes Service Catalog')

model_deploy_for = api.model('Deploy for', {
    'owner': fields.String(required=True, description='The project', example='CLOUD'),
    'name': fields.String(required=True, description='The repo name', example='selfservice-init'),
    'branch': fields.String(required=True, description='The branch', example='master'),
    'ns': fields.String(required=True, description='The namespace', example='cloudselfservice-init'),
    'apiserver': fields.String(required=True, description='The kubernetes API', example='http://localhost'),
    'token': fields.String(required=True, description='The kubernetes token'),
})

@api.route('/')
class Deployment(Resource):
    err_msg_get_deployment_requests = "Failed to get deployment requests"
    
    @api.doc('deployment')
    @api.response(201, 'Services successfully deployed.')
    @api.response(409, 'Services partially or not deployed.')
    @api.expect(model_deploy_for, validate=True)
    def post(self):
        '''Configure services for the repo'''
        
        data = request.json
        
        owner = data["owner"]
        name = data["name"]
        branch = data["branch"]
        ns = data["ns"]
        apiserver = data["apiserver"]
        token = data["token"]
        
        try:
            deployment_requests = self.get_deployment_requests(owner, name)
        except:
            api.abort(409, self.err_msg_get_deployment_requests)
        
        result, details = Kubernetes(apiserver, token, settings.config).deploy_services(
                                                                      deployment_requests,
                                                                      owner,
                                                                      name,
                                                                      ns,
                                                                      branch)
        
        if result:
            return {"deployed" : True, "details" : details}, 201
        else:
            return {"deployed" : False, "details" : details}, 409

    def get_deployment_requests(self, owner, name):
        """Get deployment requests for the owner/name
        
        Args:
            owner (String): The owner (eg: CLOUD)
            name (String): The repo name (eg: selfservice-init)
        
        Returns:
            dict: List of services to deploy
            
        Raises:
            Exception: Issue to contact the external provisions service
        """
        try:
            print("Trying to get deployment requests for %s/%s" % (owner, name))
            
            r = requests.get(settings.config.get_uri_provisions(owner, name), allow_redirects=True, timeout=2, headers={})
            
            if r.status_code != 200:
                print(self.err_msg_get_deployment_requests)
                raise Exception(r.text)
            
            deployment_requests = r.json()["data"]
            print("deployment requests : %s" % str(deployment_requests))
            
            return deployment_requests
        except:
            raise
        finally:
            if r:
                r.connection.close()
