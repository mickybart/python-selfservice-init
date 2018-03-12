Docker
------

This part can be extracted to a new project to manage your own deployment
with custom Config and secrets management.

Create an image
^^^^^^^^^^^^^^^

.. code:: bash
    
    export VERSION=1
    docker build -t selfservice-init:$VERSION .

secret.json
^^^^^^^^^^^

Check the README.rst on the root of the project.

templates
^^^^^^^^^

A templates folder need to be added and to fit with your custom config.
Please read README.rst on the templates folder.
