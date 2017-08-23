# OSC Container Support - VNF Deployment
This document describes the design changes needed for OSC to support deployments of container VNFs on a Kubernetes(K8s) cluster.  The deployed VNF instances will be used to protect the network traffic between workload containers present on the cluster.  

## Assignees
Emanoel Xavier - https://github.com/emanoelxavier

## Background
OSC currently supports protection of workloads hosted on VM based virtualized environments. This work expands OSC to also control security on container based environments orchestrated by [Kubernetes](#kubernetes-home). The adoption of container technologies is becoming more and more widespread due to its benefits such as easy maintainability, reusability, and minimal overhead with K8s being one of the most popular container orchestrators.  
For the first release of the OSC containers support the focus will be mostly on the integration points between OSC, the virtualization environment (K8s) and the software defined network(SDN) controller services needed to discovering the workloads to be protected, deploying the security VNFs and performing traffic redirection through a demonstrable E2E flow.  

## Constraints and Assumptions

### OVN with SFC for Kubernetes
To perform the redirection through a container VNF using OVN the container must be on the same Kubernetes node as the protected pod. For this reason OSC may need to deploy one pod (container) per node in the cluster. There may be a way to configure a Deployment in K8s to indicate every node must have a given container. If not, this might still be possible with a single deployment: OSC can create one deployment with multiple pod specs using node selectors. Each spec would select an specific node. This approach requires further investigation and must be addressed when the integration with OVN is planned.  

### Nuage SDN for Kubernetes
Nuage does not present a restriction with respect to where the container VNF should be deployed. 


## Design Changes
The implementation of this feature will require changes on the OSC entities and operations involved on the definition and registration of VNF images; deployment specification; and monitoring of container VNFs. 

### Container VNF Images
In order for a user to deploy a VM VNF using OSC they must register the image file of the VNF along with some additional metadata. For container VNFs this model will be further simplified.  The image for the container is not necessary as it will be retrieved by the virtualization platform from a Docker registry, the user will simply need to provide the metadata needed for OSC to match the VNF with the supported security manager and virtualization platform versions and create the [K8s Deployment object](#kubernetes-deployment).
This new model is implemented by a couple of new **POST** REST APIs to create the existing types `ApplianceDTO` and `ApplianceSoftwareVersionDTO`. The choice of using two APIs instead of a single one to create both objects is consistent with the existing APIs to GET and DELETE these resources, this also allows the clients to manage appliances and their software versions independently.  

### REST API  

#### Appliance
The resource `/api/server/v1/catalog/{applianceId}/` will have a create/POST API implemented by the class `ApplianceApis`.  This API implementation will make use of the new service `AddApplianceService`.  


#### Appliance Software Version
The resource `/api/server/v1/catalog/{applianceId}/versions/{ApplianceSoftwareVersionId}` will have a create/POST API implemented by the class `ApplianceApis`.  This API implementation will make use of the new service `AddApplianceSoftwareVersionService`.  
In addition to that, the object `ApplianceSoftwareVersionDto` will include a new field: `imagePullSecretName`. This optional field can be used for clients to provide the name of the secret to be used by Kubernetes to [retrieve images from a private Docker registry](#private-docker-registry). 


```java
ApplianceSoftwareVersionDto {
id (integer, optional),
parentId (integer, optional),
swVersion (string),
virtualizationType (string) = 
['OPENSTACK', 'KUBERNETES'],
virtualizationVersion (string),
imageUrl (string),                            // For container VNFs this should be the Docker image name TODO: ref
imagePullSecretName (string, optional),       // New field added for container VNFS. Contains the name of the key used by the virtualization platform to pull the container images from a private registry.
encapsulationTypes (Array[string], optional),
imageProperties (object, optional),
configProperties (object, optional),
minCpus (integer, optional),
memoryInMb (integer, optional),
diskSizeInGb (integer, optional),
additionalNicForInspection (boolean, optional),
}
```


### OSC Services

#### Appliance and Appliance Software Version Services
Two new services are being added to enable the creation of an Appliances and Appliance Software Versions: `AddApplianceService` which expects the `ApplianceDto` as input, validating and persisting it; and `AddApplianceSoftwareVersionService` which expects the `ApplianceSoftwareVersionDto` as inputt, validating and persisting it.  
The business logic and validation implemented by these services should mirror the existing service `ImportApplianceSoftwareVersionService`, also, to avoid code duplication, `ImportApplianceSoftwareVersionService` must be refactored to make use of the new services instead of making direct domain calls to persist those entities.  

### OSC SDKs

#### VNF Security Manager SDK
Not applicable.

#### SDN Controller SDK
Not applicable.

### OSC Entities  
#### Appliance Software Version  
The `ApplianceSoftwareVersion` domain entity will have a new optional field `imagePullSecretName` .

```java
@Table(name = "APPLIANCE_SOFTWARE_VERSION", ...)
public class ApplianceSoftwareVersion extends BaseEntity {
	// ... 
	@Column(name = "image_pull_secret_name")
    private String imagePullSecretName;
	// ....
}
```  

	

> **Note:** All the tables and relationships indicated on the previous entities will also be updated on the files `org/osc/core/broker/util/db/upgrade/ReleaseUpgradeManager.java,Schema.java`.  

### OSC UI
Out of scope.

### OSC Synchronization Tasks
**TBD**

## Tests
**TBD on next revision**

Describe here any new test requirement for this feature. This can include: virtualization platform, test infrastructure, stubs, etc. 
> Note: Any feature should be demonstrable and testable independently of a particular vendor component or service. 

## References
### [Kubernetes Home](https://kubernetes.io)  
### [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)  
### [Private Docker Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
