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

"""apiv1 module

Expose selfservice APIs
"""

from flask import Blueprint
from flask_restplus import Api

from .apis.health import api as ns_health
from .apis.deployment import api as ns1

blueprint = Blueprint('apiv1', __name__)
api = Api(blueprint,
    title='selfservice-init',
    version='1.0',
    description='Deploy ServiceInstance and ServiceBinding into Kubernetes',
    doc=False
)

api.add_namespace(ns1)
api.add_namespace(ns_health, path='/')

#
# we need to expose swagger.yaml and not only the default swagger.json for compatibility reason
#
from flask import Response
from flask_restplus import Namespace, Resource
import yaml, json

ns_swagger_yaml = Namespace('swagger.yaml', description='swagger.yaml')

@ns_swagger_yaml.route('swagger.yaml')
@ns_swagger_yaml.doc(False)
class SwaggerYaml(Resource):
    def get(self):
        '''swagger.yaml'''
        return Response(yaml.safe_dump(json.loads(json.dumps(api.__schema__)), default_flow_style=False), mimetype="application/yaml")
    
api.add_namespace(ns_swagger_yaml, path='/')
