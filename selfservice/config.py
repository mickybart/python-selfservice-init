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

"""
config module

Permit to manage global configurations
"""

import json

class Config:
    """Configuration for module and sub-modules
    
    This class can be overriden and so adapted by every compagnies.
        
    Constructor
    
    Args:
        uri_provisions (string): Uri to list provisions requests for the service
    """
    
    templates = {}
    
    def __init__(self, uri_provisions):
        self.uri_provisions = uri_provisions
        
    def load_json(json_file):
        """Load JSON file
        
        Args:
            json_file (str): filename of a json file
            
        Returns:
            dict: content of the file
        """
        try:
            with open(json_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def get_uri_provisions(self, owner, name):
        """Get the url of the provisions service
        
        Args:
            owner (String): The owner (eg: CLOUD)
            name (String): The repo name (eg: selfservice-init)
        
        Returns:
            String: The provisions service uri
        """
        return self.uri_provisions % (owner, name)
    
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
        
        instance_modifier = ()
        binding_modifier = ()
        
        return instance_modifier, binding_modifier
    
    def is_template_exists(self, template):
        """Check if a template is available
        
        Args:
            template (String):  Template name
            
        Returns:
            bool: True if the template exist.
        """
        return template in self.templates

    def load_template(self, template, kind, modifier):
        """Load a template
        
        Args:
            template (String): Template name
            kind (String): instance or binding
            modifier (List of String): Parameters for the template
            
        Returns:
            String: The template content or an empty string
        """
        with open(self.templates[template][kind], mode="r") as f:
            return f.read() % modifier
            
        return ""
    
    def load_instance_template(self, template, modifier):
        """Load an instance template
        
        see load_template
        """
        return self.load_template(template, "instance", modifier)
    
    def load_binding_template(self, template, modifier):
        """Load a binding template
        
        see load_template
        """
        return self.load_template(template, "binding", modifier)

    
    
    
