Templates
=========

Usage
-----

A template is set with 2 yaml files that will be used by kubernetes :

- ServiceInstance (selfservice-<name of the service>-instance.yaml)
- ServiceBinding (selfservice-<name of the service>-binding.yaml)

Those templates need to be set in a custom config (see an example into docker/config.py).

This is up to you to define the location, service name and how to modify those templates with parameters available to selfservice.

Service Catalog / Broker
------------------------

A template is associated to a broker registered in kubernetes service catalog.

All parameters on those templates will depend of those needed by the broker itself.
