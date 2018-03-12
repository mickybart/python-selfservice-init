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

from selfservice.config import Config
import re

class CustomConfig(Config):
    """Custom Config"""
    
    regex_ns_dev = re.compile(".*-develop$")
    regex_ns_qa = re.compile(".*-qa$")
    
    mongo_clusters = {
        "dev" : "ypcloud-io-dev",
        "qa" : "ypcloud-io-qa",
        "prod" : "ypcloud-io-prod"
        }
    
    templates = {
        "mongo" : {
            "instance" : "templates/selfservice-atlas-instance.yaml",
            "binding" : "templates/selfservice-atlas-binding.yaml"
            },
        "mysql" : {
            "instance" : "templates/selfservice-rds-instance.yaml",
            "binding" : "templates/selfservice-rds-binding.yaml"
            }
        }
        
    def get_template_modifiers(self, service, service_details, owner, name, ns, branch):
        """Get modifiers to apply on the template
        
        Args:
            service (string): Name of the service
            service_details (dict): Details about the service setup
            owner (String): The owner (eg: CLOUD)
            name (String): The repo name (eg: selfservice-init)
            ns (String): The namespace (eg: cloudselfservice-init)
            branch (String): The branch (eg: master)
        
        Returns:
            list, list: instance modifier, binding modifier
        """
        
        # set templates modifier for instance and binding
        if service == "mongo":
            instance_modifier = (ns, self.get_mongo_cluster(self.get_ns_environment(ns)) , ns)
            binding_modifier = (ns)
        elif service == "mysql":
            instance_modifier = (ns, owner + self.get_ns_environment(ns) , name)
            binding_modifier = (ns)
        else:
            return super().get_template_modifiers(service, service_details, owner, name, ns, branch)
        
        return instance_modifier, binding_modifier
    
    def get_ns_environment(self, ns):
        """Extract the environment from a namespace
        
        Args:
            ns (String): The namespace in Kubernetes
            
        Returns:
            String: The environment (eg: dev, qa or prod)
        """
        if self.regex_ns_dev.match(ns) is not None:
            return "dev"
        elif self.regex_ns_qa.match(ns) is not None:
            return "qa"
        else:
            return "prod"
    
    def get_mongo_cluster(self, env):
        """Get the mongo cluster
        
        Args:
            env (String): Environment (dev, qa or prod)
        
        Returns:
            Dict: The mongo cluster or None if not available
        """
        return self.mongo_clusters.get(env, None)
