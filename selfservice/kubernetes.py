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

import shlex, subprocess

class Kubernetes:
    """Kubernetes managment"""
    
    timeout = 2
    
    def __init__(self, apiserver, token, config):
        """Constructor
        
        Args:
            apiserver (String): Kubernetes API uri
            token (String): Kubernetes token
            config (Config): configuration
        """
        self.apiserver = apiserver
        self.token = token
        self.config = config
    
    def deploy_services(self, services, owner, name, ns, branch):
        """Deploy services
        
        Args:
            services (List): List of services to deploy
            owner (String): The owner (eg: CLOUD)
            name (String): The repo name (eg: selfservice-init)
            ns (String): The namespace (eg: cloudselfservice-init)
            branch (String): The branch (eg: master)
        
        Returns:
            bool, Dict. The result and details
        """
        
        # Generate and apply all configurations (ServiceInstance and ServiceBinding)
        #
        # "kubectl --kubeconfig=/dev/null --insecure-skip-tls-verify=true --token='%s' --server='%s' -n %s apply -f %s" % (self.token, self.apiserver, ns, "file.yaml")
                
        result = True
        details = { "missing" : [],
                    "deployed" : [],
                    "failed" : []
                  }
        
        # Generate and apply all configurations (ServiceInstance and ServiceBinding)
        for service in services:
            if not self.config.is_template_exists(service):
                print("Missing templates for %s" % service)
                details["missing"].append(service)
                result = False
                continue
        
            # set templates modifier for instance and binding
            instance_modifier, binding_modifier = self.config.get_template_modifiers(service, services[service], owner, name, ns, branch)
            
            # load template for instance and binding
            try:
                k8s_instance = self.config.load_instance_template(service, instance_modifier)
                k8s_binding = self.config.load_binding_template(service, binding_modifier)
            except:
                print("Failed to load templates for %s" % service)
                details["failed"].append(service)
                result = False
                continue
        
            # Apply the configuration
            k8s_apply = k8s_instance + "\n---\n" + k8s_binding
            
            command_line = "kubectl --kubeconfig=/dev/null --insecure-skip-tls-verify=true --token='%s' --server='%s' -n %s apply -f -" % (self.token, self.apiserver, ns)
            args = shlex.split(command_line)
            
            print("Applying resources for %s" % service)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output, output_err = proc.communicate(input=k8s_apply.encode())
            
            if proc.returncode != 0:
                print("Failed to apply resources for %s" % service)
                print("output : %s\noutput_err : %s" % (output, output_err))
                result = False
                details["failed"].append(service)
                continue
            
            details["deployed"].append(service)
        
        return (result, details)
    
