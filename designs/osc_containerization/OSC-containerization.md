# OSC Containerization

We want to deploy OSC as a container i.e as a docker image. This allows us to deploy OSC service along with other similar services on a single host. This also allows easier management of OSC lifecycle(Upgrades, HA etc)

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

##### Persistent data
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

To allow easy launch and usage of OSC, we will have default data(which includes the keystore, truststore, vmidcServer.conf and plugins) which will be copied(NOT overwritten) to the docker volume on startup.

In a production environment, it is expected that the default data will not be needed. The secure information like the keystore and truststore should be setup with strong non-default passwords and these passwords are passed in via environment variables as described below.

##### Life cycle management
Remove restart and shutdown operations possbile via OSC UI
Remove inplace upgrade of OSC via server upgrade bundles

##### CLI/Restricted Shell
Remove restricted shell. Restricted shell is no longer applicable as we will be using standard base containers.
Note: It is technically feasible to have a restricted shell if we build up the OSC container image from scratch. For now, this is out of scope.

##### Network/Ip address management
Remove network management functionality. Setting custom IP address within a docker container does not make sense as the IP is not exposed outside of the container.

We can expose OSC endpoints as a virtual ip from the host or use different ports to expose OSC

##### Secure information
The passwords to access keystore, truststore and entries within them are currently part of properties file embedded within the source code as part of `security.properties` within the osc-server project. Since the restricted shell is no longer available to secure this information it is no longer secure in a production environment.

For container based deployment, the best practises are to pass such information as an docker secret or through environmental variables.

Docker Secrets are available only to swarm services, so this is not an option for standalone containers.

We can pass in this password information via environmental variables. OSC will fallback to using the properties file with the default password if the environmental variable is not set.

We will use the same keys within the `security.properties` like `keystore.password` `truststore.password` `aesctr.password` for passing in the environmental variables.

Example Command to start a docker OSC container with environment variables is:

`docker run -p 443:443 -p 8090:8090 -dit --mount source=osc-vol,target=/opt/vmidc/bin/data -e keystore.password=PASSWORD arvindn05:osc`

##### TLS Certificate sourcing

See below on how certificates are sourced in ODL:

>The OpenDayLight (ODL) uses Karaf distribution for sourcing the TLS certificates (based on the link https://wiki.opendaylight.org/view/OpenDaylight_OpenFlow_Plugin:_TLS_Support). 
In this solution, various TLS certificates are generated in the relevant format and stored in specific “PATH” as described in the configuration files (*.xml). The configuration files contains various information about the certificates, location of these certification and security algorithms used etc.
As part of ODL installation, Karaf distribution reads these configuration files and source the new certificates to ODL, so that new certificates gets installed / copied in ODL and used in the new session. All of these are automated as part of Karaf custom command set defined as part of ODL definition.

The sourcing of OSC certificates shall follow the similar scheme,but without using the Karaf Distribution. The OSC certificates like internal certificate (containing internal key and public key), other public certificates (used for authenticating with security manager, openstack clients etc) are sourced as a separate *.p12/*.jks certificates and sourced in a specific folder.
As part of OSC deployment / installation, the relevant deployment scripts shall pick up the new certificates and translates this to the one single truststore and sourced to OSC.

### POC Implementation

###### Scope
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

## Tests
N/A

## References
### [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)