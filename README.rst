Self Service
============

Self-service to create ServiceBinding and ServiceInstance for Kubernetes (DevOps)

`Code documentation (sphinx) <https://mickybart.github.io/python-selfservice-init/>`__

Docker
------

The docker folder provides everything to create an image of this service.

selfservice module
------------------

Installation
^^^^^^^^^^^^

This package is available for Python 3.5+.

Install the development version from github:

.. code:: bash

    pip3 install git+https://github.com/mickybart/python-selfservice-init.git

Prerequisite
^^^^^^^^^^^^

Examples in this README are using the secret.json file to inject the provisions uri that will provide the configuration of a service.
Of course you can use any other solution provided by your infrastructure.

.. code:: python
    
    # Secrets structure
    #
    secrets = {
        "provisions" : { "list" : "https://<url>/%s/%s" }
    }

Quick start
^^^^^^^^^^^

.. code:: python

    from selfservice.config import Config
    from selfservice.app import App
    
    secrets = Config.load_json("secret.json")
    
    config = Config(secrets["provisions"]["list"])
    
    App(config).run()

Custom Config
^^^^^^^^^^^^^

The class Config is the main way to customize self service.
This class will permit to define how to use templates that you will create.

Please read the Code documentation for more details.

You can find a complete example in the docker folder.

Error Types
-----------


Internal Notes
--------------

`Code documentation (sphinx) <https://mickybart.github.io/python-selfservice-init/>`__

Bugs or Issues
--------------

Please report bugs, issues or feature requests to `Github
Issues <https://github.com/mickybart/python-selfservice-init/issues>`__
