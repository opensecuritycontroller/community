# OSC Kolla Container
[Kolla](#kolla-home) is an OpenStack project that provides production-ready containers and deployment tools for operating OpenStack clouds. This document outlines the contributions to be up streamed to Kolla so that the OSC image is present in the [Kolla container repository](#kolla-container-repos).   
> Note: There other options for OSC packaging and distribution that might work with TripleO. Before we update this document with more details we must determine whether this is the most appropriate choice.  

## Assignees
Emanoel Xavier - https://github.com/emanoelxavier

## Background

The purpose of this work is to facilitate the deployment and configuration of OSC by [TripleO](#tripleo-osc-design). TripleO directly picks up container images from the Kolla repository. Having an OSC container image built as a Kolla container will therefore facilitate this integration and keep it consistent with other services supported by TripleO.  

## Constraints and Assumptions

## Design Changes

This proposed design builds the OSC Kolla container image directly from the [OSC source code on GitHub](#osc-code). There are multiple ways to achieve this:
1. **Using multi-stage build:** the `osc` container starts from an existing Kolla image, for instance the `Kolla base` container and adds the jdk, git, maven and everything we need to build OSC. This container then uses a [multi-stage](#docker-multi-stage) approach to clone the OSC source then build the OSC binaries discarding what is no longer needed (build tools, source code, etc). After building the OSC binaries the container then runs the OSC service.  
2. **Using Kolla scripts to get and build the OSC source code:** This means the OSC binaries will be present on the environment building the `osc` container and must be copied into the container image. 


### OSC Kolla Container  
The OSC Kolla container will be up streamed to the folder `docker/osc` in the [Kolla source repository](#kolla-source) as the file `Dockerfile.j2`:
```
FROM {{ namespace }}/{{ image_prefix }}osc-base:{{ tag }}
	
LABEL maintainer="{{ maintainer }}" name="{{ image_name }}" build-date="{{ build_date }}"
	
{% block osc_header %}{% endblock %}
{% import "macros.j2" as macros with context %}
    
{{ macros.configure_user(name='osc') }}
	
	
EXPOSE 8090 443  # How to provide these parameters as part of the deployment?
WORKDIR /opt/vmidc/bin/
RUN chmod +x vmidc.sh 

# Run OSC in console mode, otherwise container exists immediately
CMD ["/opt/vmidc/bin/vmidc.sh", "--console", "--start"]
```

> Note: The file above assumes this container is built upon an `osc-base` image that already has the OSC binaries. Depending whether we implement Option 1 or 2 this file will need additional changes either using a multi-stage build or copying the binaries from the machine running docker build.  

> Note: Upstream these changes to Kolla will likely require an [OpenStack blueprint](#kolla-blueprint).   

See details on how to [add a new service to Kolla here](#kolla-adding-service).  

### OSC Container Base  
TODO: Details on the j2 file for the OSC base container. Must contain the OSC binaries, base OS, jre, etc. Consider support for multiple OS distros.   

### OSC Build Container  
TODO: Details on the j2 file for a container able to clone and build OSC. Must contain everything needed to clone and build the OSC source code.  

### Kolla OSC Build  
TODO: Details on how Kolla scripts can build OSC from the source code.  This is an alternative to using the **OSC Build Container** .  

## Tests  
TBD

## References
### [TripleO OSC Design](../../tripleo/osc-tripleo.md)  
### [Kolla Home](https://wiki.openstack.org/wiki/Kolla)
### [OSC Code](https://github.com/opensecuritycontroller/osc-core)  
### [Kolla Container Repos](https://hub.docker.com/r/kolla/)  
### [Kolla Blueprint](https://blueprints.launchpad.net/kolla)  
### [Kolla Adding Service](https://docs.openstack.org/kolla/latest/contributor/CONTRIBUTING.html#adding-a-new-service)
### [Docker Multi Stage](https://docs.docker.com/engine/userguide/eng-image/multistage-build/#use-multi-stage-builds)



