# OSC Containerization 

This document outlines the design and configuration changes needed to deploy OSC as a Docker container. This allows us to deploy OSC service along with other similar services on a single host. This also allows easier management of OSC lifecycle (Upgrades, HA etc).  
Th process of building and deploying the OSC container image for protecting an OpenStack environment will leverage the projects [Kolla](https://github.com/openstack/kolla) and [TripleO](https://docs.openstack.org/tripleo-docs/latest/). This document will also describe the intended changes that must be upstreamed to those projects in order to support the build and deployment of OSC as a new service.   

## Assignees
Arvind Nadendla https://github.com/arvindn05  


## Background

OSC containerization for deployment allows greater flexibility on mixing services on same host.

For example, in case of openstack we can co-locate osc on the controller node with the other controller services like keystone, nova etc. We can follow the same lifecycle as those services and utilize similar mechanisms for upgrades, data persistence, HA etc

It also simplifies packaging and distribution.

## Constraints and Assumptions

##### Constraint
- Support migrating current OSC installation to container based installation.

##### Assumption
- OSC will be deployed as a container only. The Virtual Machine appliance model will not be supported going forward.
- For migration of VM-based OSC to container based OSC, some manual steps maybe required. Scripts should be provided in this case. For example, copying the database/keystore to the modified location etc

## Design Changes

### Persistent data
Persistent data stored by OSC will need to be decoupled and managed outside the lifecycle of the container.

The following data will need to be decoupled from the lifecycle of the OSC container:
- H2 database
- Keystore
- Truststore
- Plugins
- Service Function catalog image files
- Log file
- vmidcServer.conf

This data would need to be exposed in docker volumes to the OSC container.

### Life cycle management
Remove restart and shutdown operations possbile via OSC UI
Remove inplace upgrade of OSC via server upgrade bundles

### CLI/Restricted Shell
Remove restricted shell. Restricted shell is no longer applicable as we will be using standard base containers.
Note: It is technically feasible to have a restricted shell if we build up the OSC container image from scratch. For now, this is out of scope.

### Network/Ip address management
Remove network management functionality. Setting custom IP address within a docker container does not make sense as the IP is not exposed outside of the container.

We can expose OSC endpoints as a virtual ip from the host or use different ports to expose OSC

### POC Implementation

#### Scope
- Create docker files for OSC
- Use Docker volume to store persistent data and decouple from OSC code
	- Moved log files to persistent volume
	- Moved Database to persisent volume
	- Moved Plugins to persistent volume
- Launch different OSC containers and make sure they are using the same persistent data

Code is available [here](https://github.com/arvindn05/osc-core/tree/docker)

### REST API
N/A

### OSC SDKs

#### VNF Security Manager SDK
N/A

#### SDN Controller SDK
N/A

### OSC Entities
N/A

### OSC UI
- Remove restart option under Manage -> Server -> Summary
- Remove restart option under Manage -> Server -> Summary
- Remove exposing IP Address management functionality under Manage -> Server -> Network. Setting NAT Ip is still applicable to expose virtual IP of OSC to external entities for callbacks etc
- Remove option to Upgrade server under Manage -> Server -> Maintainence

### OSC Synchronization Tasks
N/A

## OSC Kolla Container  
In order for OSC to be available in the [TripleO docker repository](https://hub.docker.com/u/tripleoupstream/) it must build as part of the OpenStack Kolla.  The main requirement for this is the presence of a Docker file template `Dockerfile.j2` for OSC upstreamed to the [Kolla docker folder](https://github.com/openstack/kolla/tree/master/docker).  Below is the initial intended OSC Docker template file to be reviewed with the Kolla team:

```
FROM {{ namespace }}/{{ image_prefix }}base:{{ tag }}
	
LABEL maintainer="{{ maintainer }}" name="{{ image_name }}" build-date="{{ build_date }}"
	
{% block osc_header %}{% endblock %}
{% import "macros.j2" as macros with context %}
    
{{ macros.configure_user(name='osc') }}
	
	
# Copy OSC opt folder to container
COPY . /
EXPOSE 8090 443  # How to provide these parameters as part of the deployment?
WORKDIR /opt/vmidc/bin/
RUN chmod +x vmidc.sh 

# Run OSC in console mode, otherwise container exists immediately
CMD ["/opt/vmidc/bin/vmidc.sh", "--console", "--start"]
```

See details on how to [add a new service to Kolla here](https://docs.openstack.org/kolla/latest/contributor/CONTRIBUTING.html#adding-a-new-service).
> Note: Upstream these changes to Kolla will likely require an [OpenStack blueprint](https://blueprints.launchpad.net/kolla).   

> Questions for the Kolla team:
> How different types of parameters can be passed to the container for launching?  
> How to test the template locally? Do we need a Kolla deployment?  Can we have the OSC binaries on a local repository?  
> What is the schedule to having the blueprint approved and what are the requirements?  
> Other than the Jinja2 file above are there other files we must provide when upstreaming? For instance see PR https://review.openstack.org/#/c/416369/  
> Are thee any specific storage restriction? How to ensure volumes are mounted correctly in the host when needed by the container?  
> Is there anything specific for [ansible](https://github.com/openstack/kolla-ansible) or [kubernetes](https://github.com/openstack/kolla-kubernetes) we need to produce?  

## OSC TripleO Service
In order to the OSC service to be deployed as part of TripleO it must be registered as a service in the [TripleO service](designs/osc_containerization/OSC-containerization.md) for that changes to the tripleo-heat-templates must be done. The main configuration file needed will be a yaml file `services/osc-service.yaml`. This file will be similar to the [ODL template](designs/osc_containerization/OSC-containerization.md).

> Questions for the Kolla/TripleO team:  
> Which environment is needed to test the OSC service deployment with TripleO?  
> Is a bluebrint needed for the changes in TripleO or can the Kolla blueprint above cover it all?  


## Tests
N/A

## References
### [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)