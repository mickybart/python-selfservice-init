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

"""Application module

Provide the app Flask object.
"""

from flask import Flask
from .apiv1 import blueprint as api1
import selfservice.settings as settings

class App:
    """Core of the application
    
    Constructor
    
    Args:
        config (Config): configuration of the application
    """
    
    def __init__(self, config):
        # init the settings module
        settings.init(config)
        
        self.app = Flask(__name__)
        self.app.register_blueprint(api1)
    
    def run(self, host='0.0.0.0'):
        """Start the application
        
        Keyword Arguments:
            host (string): IP to bind
        """
        self.app.run(host=host)
