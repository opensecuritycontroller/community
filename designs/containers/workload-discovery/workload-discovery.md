# OSC Container Support - Workload Discovery
This document describes the design changes needed for OSC to support microsegmentation of workloads on a Kubernetes(K8s) cluster.  Microsegmentation is implemented on OSC through the creation of [security groups](#osc-security-groups) which identify the workloads to be protected by a VNF as defined by the security policies applied to the group.  
Applying the security policies to the group by deploying the VNF and configuring the traffic redirection (aka, steering) is out of scope for this document and will be covered on complimentary design documents. 

## Assignees
Emanoel Xavier - https://github.com/emanoelxavier

## Background
OSC currently supports protection of workloads hosted on VM based virtualization environments. This work expands the OSC scope to include also container environments orchestrated by [Kubernetes](#kubernetes-home). The adoption of container technologies is becoming more and more widespread due to its benefits such as easy maintainability, reusability, and minimal overhead with K8s being one of the most popular container orchestrators.  
For the first release of the OSC containers support the focus will be mostly on the integration points between OSC, the virtualization environment and the software defined network(SDN) controller services needed to discovering the workloads to be protected, deploying the security VNFs and performing traffic redirection through a demonstrable E2E flow.  

## Constraints and Assumptions
### Kubernetes Version and Configuration
* **Kubernetes Version:** 1.6.7. 
* **Network Layer**:  [OVN](#ovn-kubernetes) with [SFC](#ovs-sfc) enabled or Nuage.
* **Authentication**: For this first release the access to the Kubernetes API is allowed over `http` and **without user authentication**.  This should be acceptable as the intent of this release is for prototype/demonstration only rather than production readiness. For the longer run we want to allow only `https` access with authenticated users, this should be possible with [Fabric8](#fabric8-credential-example), the java SDK being adopted. 

### OVN with SFC for Kubernetes
> This assumption is being called out given that the traffic redirection using OVN SFC is still under investigation.

To create a traffic redirection using OVN SFC additional calls to the OVN northbound database will be needed to retrieve the **switch name** and **port id** of the pod under protection. For that the following values from Kubernetes will suffice: **name of the node hosting the pod, pod namespace, pod name.**

### Nuage SDN for Kubernetes
> This assumption is being called out given that the traffic redirection using Nuage must still be tried out. 

To create a traffic redirection using Nuage for Kubernetes the only required information about the workload pod is its **port id**. OSC will obtain this **port id** from Nuage by making a separate call while providing the following values: **name of the node hosting the pod, pod namespace, pod name.**  


### Design Assumptions
> Note: The assumptions below refer to design changes not yet fully described in this document but necessary to understand some of its current content. In the next revision of this document those details will be added (look for **TBD on the next revision** along this document) and these assumptions removed.  

* **Security Group:**
For the first release of this feature all the `key` values of the labels in a given security group will always be the same, i.e.: security=webserver, security=backend, etc.

* **Pod Security Group Member:**
A new type of security group member is created, **Pod**. A pod can be part of many security groups at the same time.  


## Design Changes
The discovery flow adopted for this work will follow the same model already adopted by OSC for OpenStack with RabittMQ:
1. The user creates a security group providing the needed primitives defined by the virtualization environment. In this case those primitives are a set of labels.
2. OSC will watch for notifications related to any entities, in this case pods, labeled with any of the values on the security group.
3. When a meaningful notification is received OSC will trigger a synchronization job for the whole security group.
4. The synchronization job will retrieve the entities associated with the security group from Kubernetes and update its database and other services (security manager and SDN controller) accordingly.  


### REST API  

#### Security Groups
The security group resource `/api/server/v1/virtualizationConnectors/{vcId}/securityGroups/{sgId}` is being slightly modified with:
1.  **projectid** and **projectName** now are optional:  These fields are not applicable to Kubernetes.  For OpenStack, the enforcement of these fields will be done in the OSC business logic instead.
2.  optional collection of **labels** being added: These fields are applicable only to Kubernetes and the following restrictions will be enforced by the OSC busines logic for Kubernetes security groups:   
a) At least one label must be provided when creating or updating a security group;  
b) All labels must be strings in the format "key=value". 

> Note: The choice of using a string rather a well defined data type for labels with {key; value} is because the key+value format may not be applicable to other virtualization platforms we may support in the future. 

```javascript
SecurityGroupDto {
id (integer, optional),
parentId (integer, optional),
name (string),
projectId (string,optional),                       // changing from REQUIRED to OPTIONAL 
projectName (string, optional),                    // changing from REQUIRED to OPTIONAL 
markForDeletion (boolean, optional, read only),
protectAll (boolean, optional),
servicesDescription (string, optional, read only),
memberDescription (string, optional, read only),
virtualizationConnectorName (string, optional),
lastJobState (string, optional, read only),
lastJobStatus (string, optional, read only),
lastJobId (integer, optional, read only),
labels (Array[string], optional)                  // Adding the collection of labels
}
```

#### Virtualization Connectors
The virtualization connector resource `/api/server/v1/virtualizationConnectors/{vcId}` field `type` can now have a new possible value: `KUBERNETES`. 
```javascript
VirtualizationConnectorDto {
id (integer, optional),
parentId (integer, optional),
name (string),
type (string) = ['OPENSTACK', 'KUBERNETES'],      // Adding VC type for Kubernetes
controllerIP (string, optional),
controllerUser (string, optional) ,
controllerPassword (string, optional),
providerIP (string),
providerUser (string),
providerPassword (string, optional),
softwareVersion (string, optional),
controllerType (ControllerType, optional),
providerAttributes (object, optional),
adminProjectName (string, optional),
adminDomainId (string, optional),
lastJobState (string, optional, read only),
lastJobStatus (string, optional, read only),
lastJobId (integer, optional, read only)
}
```
### OSC Services
The OSC services `AddSecurityGroup` and `UpdateSecurityGroup` should be updated to enforce the security group required fields accordingly. This can be done by a simple change on `SecurityGroupDtoValidator#checkForNullFields`: `projectId` and `projectName` should NOT be null if the VC type is OpenStack, and `labels` should NOT  be null or empty if the VC is Kubernetes.

### OSC SDKs

#### VNF Security Manager SDK
Not applicable.

#### SDN Controller SDK
Details on this is **TBD** but we will at least need to add APIs to return a network element given the **pod name, namespace and name of the hosting node**.  The returned network element should contain the unique port id for both OVN SFC and Nuage. For OVN SFC it should also return the name of the logical switch.  
As is today, these services will trigger the conformance tasks for the security group. Thoses tasks will be responsible for discovering the relevant members (pods) and persisting those entities accordingly.  

### OSC & Kubernetes
This section describes how OSC will use the Kubernetes API service endpoint to retrieve and perform live discovery of the protected workloads, highlighting the chosen SDK, connectivity inputs and required APIs.   

#### OSC Kubernetes Wrapper Package
The direct communication between the OSC core modules and the Kubernetes API service will be contained within the new package `org.osc.core.broker.rest.client.k8s` . The purpose of this package is to make it easier for other osc core components to use the K8s APIs as well as prevent leaks of SDK specific details. The class diagram below depicts the classes and functionalities exported by this package.
![](./images/k8s-wrapper-class-diagram.png)  
*Kubernetes Wrapper Package Class Diagram*  



* **KubernetesApi**: Represents the base class for the `Kubernetes*Api` classes and it is reponsible for initializing the `KubernetesClient`, as part of its constructor and close it, as part of its `close()` method.
* **KubernetesPodApi**: This class provides all the pod related methods to the other OSC core packages: `getPodsByLabels`, this method should enforce that all labels must be in the form "key=value" with all the "key"s having the same value. For details [see below](#k8s-targeted-apis). `getPodsById` should return the pod with the given uid, namespace and name. Both these methods should through a `VmidcException` if an SDK (Fabric8) specific exception is caught.
* **KubernetesPod**: This class provides all the pod information needed by other OSC core packages.

##### Unit Tests
Because the Fabric8 uses a fluent interface design, unit testing this package might require the use of [mockito deep stubs](#mockito-deep-stubs). If this does not work another approach can be adding a new class to this package `KubernetesPodFluentApi` as package private. This class will be used by `KubernetesPodApi` and isolate the fluent code. Unit tests targeting the `KubernetesPodApi` will then be able to mock the `KubernetesPodFluentApi` thus removing the complexity of the fluent interfaces from the unit tests. 

#### Java SDKs for K8s APIs
Two java client libraries are listed in the [Kubernetes Reference Documentation](#k8s-client-libraries): **amdatu-kubernetes** and **Fabric8 Kubernetes Client**. Due to its higher popularity and active community **Fabric8** will be used for this work and the targeted version is `2.5.6`.  
One of the drawbacks identified with Fabric8 is the lack of compliance with OSGi. The workaround for this issue is to *"osgify"* this dependency with an uber bundle. This approach is similar to what we have done for the OpenStack4j dependencies and it has been done and validated: https://github.com/emanoelxavier/osc-core/tree/k8s-example2/osc-uber-kubernetes . 
> Note: The Kubernetes API call examples on this document uses this SDK.


#### Connectivity with Kubernetes
As mentioned in the Constraints section, the connectivity with Kubernetes will be done through `http` and without user credentials (unauthenticated). 
> Note: Currently, the OSC Virtualization Connector does require the user name to be passed in the `providerUser` field though. This field will continue to be required however its value will not be used.  

The inputs needed to connect with the Kubernetes API service will be: the **ip address** of the service endpoint, provided in the Kubernetes virtualization connector; and **port**, harcoded to 8080. 
> Note: Support to other ports can be added in the future by adding a new field in the `providerAttributes` map: `providerPort`.

#### K8s Targeted APIs

**Receiving Notifications from K8s**
OSC will make use of two Kubernetes API features in order to receive live notifications:  

1. [K8s Selection with Labels](#k8s-labels-and-selectors)
This feature allows filtering notification by labels applied to the pods.  In the first iteration of this work we will support filtering pods using an `OR` operator: a pod with at least one of the defined labels in the security group is a targeted pod.  This can be easily and directly implemented by Kubernetes APIs for labels with the same key and this will be the scope of this implementation. Implementing this functionality with labels of different keys is possible but not natively supported by the K8s APIs, requiring additional code on the client side using multiple watchers. 
2. [K8s Watch APIs](#k8s-pod-watch-api)
These APIs allow a client to receive live notification of the filtered objects on Kubernetes. Notifications arrive on an `eventReceived` method through **Fabric8** while the running thread is alive.  This will likely require one instance of the watcher per security group given that inclusive filtering (`OR`) is not supported by K8s APIs or Fabric8.  
Below we can see a code snippet of this API, the `labelsKey` parameter is the common key of all labels in a security group, the `labelValues` parameter is the set of each label in the security group. **Previously mentioned assumption:** a security group contains a collection of labels with the format  `key=value` where all the `keys` are the same.


```java
try (final KubernetesClient client = connection.getConnection()) {
	try (Watch watch = client.pods().withLabelIn(labelsKey, labelValues).watch(new Watcher<Pod>() {
		@Override
        public void eventReceived(Action action, Pod resource) {
        	// ...
        }

		@Override
        public void onClose(KubernetesClientException e) {
        	/// ...
        }
		})) {
			// ....
		} catch (KubernetesClientException | InterruptedException e) {
			/// ...                
		}
} catch (Exception e) {
	// ....            
}
```

The actions that should trigger a resync of the security group are **ADDED**, **DELETED** and **MODIFIED** under certain conditions. MODIFIED should only trigger a resync if a stored value of the pod has changed (uid, nodename, namespace).   

**Retrieving pod Information from K8s**
In addition to receiving notifications OSC will also need to actively make calls to K8s to retrieve information about the pods. At very least OSC will need to list all the pods in a security group and retrieve a pod by its name. These operations will be invoked by OSC synchronization jobs and accessible through the class `org.osc.core.broker.rest.client.k8s.KubernetesPodApi`. Below you can see a code snippet for each one of these operations.


1. **Listing pods in a security group**
The semantics of the `labelsKey` and `labelValues` parameters are the same as the ones described in the notification selector above.  
> Note: this API will return an empty collection in case no pod is found with any of the provided labels.

```java
try (final KubernetesClient client = connection.getConnection()) {
	PodList pods = client.pods().withLabelIn(labelsKey, labelValues).list();
		for(Pod pod : pods.getItems()) {
			// ....
		}

} catch (KubernetesClientException e) {
	// ...
}
```
The values OSC should persist for a pod are: `namespace`, `name`, `uid`, `nodename`

2. **Retrieving a single pod**
In order to receive a single pod the K8s APIs require the **name** and the **namespace** of the pod. Because retrieving a pod by its [unique identifier (uid) is not supported](#k8s-retrieving-pods-by-uid-issue) it is responsibility of the client to ensure that the pod retrieved with a given name has the expected uid. This must be taken into consideration when we design our customer wrapper around Fabric8.

``` java
try (final KubernetesClient client = connection.getConnection()) {
	Pod pod = client.pods().inNamespace(namespace).withName(name).get();
		if (pod == null) {
			// ...
		} else {
			// Ensure this pod has the expected id.
		}

} catch (KubernetesClientException e) {
// ...
}
```

### OSC Entities  
#### Virtualization Connector 
The `VirtualizationConnector` domain entity field `virtualizationType` can now have a new value: **VirtualizationType.KUBERNETES** .

#### Security Group  
The SecurityGroup  entity will contain a set of labels.  The following changes will implement that:

* **osc-domain** updates:
```java
@Table(name = "SECURITY_GROUP", ...) 
public class SecurityGroup extends BaseEntity implementes LastJobContainer {
   
    // The set of labels used to filter the members of the security group
	@ElementCollection(fetch = FetchType.LAZY)
    @Column(name = "labels")
    @CollectionTable(name = "SECURITY_GROUP_LABEL", joinColumns = @JoinColumn(name = "security_group_fk"),
    foreignKey=@ForeignKey(name = "FK_SECURITY_GROUP_LABEL"))
    private Set<String> labels = new HashSet<String>();
	
	// ...
}  
```
* **database** schema updates:
```sql
create table SECURITY_GROUP_LABEL ("
                    + "security_group_fk bigint not null, label varchar(255));
```
```sql
alter table SECURITY_GROUP_LABEL add constraint " +
                 "FK_SECURITY_GROUP_LABEL foreign key (security_group_fk) references SECURITY_GROUP;"
```
These schema changes will also need to be applied during upgrades, for that the `ReleaseUpgradeMgr.java` file also needs to reflect these changes.

#### Security Group  Member
A new type of security group member is being introduced, **Pod** along with its respective port **PodPort**. 
* **osc-domain** updates:  
Similarly to the existing VM type, the Pod entity can be a member of multiple security groups, thus it has a many to one relationship with security group members:  

```java
@Table(name = "SECURITY_GROUP_MEMBER", ...)
public class SecurityGroupMember extends BaseEntity implements Comparable<SecurityGroupMember> {
	// ... 
	@ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "pod_fk", foreignKey = @ForeignKey(name = "FK_SGM_POD"))
    private Pod pod;
	
	// ....
}
```  

The **Pod** entity carries the relavant information regarding a Kubernetes pod: the name, namespace, uid, host name, a set of ports and a one to many relationship with security group members.   
> Note: Although currently a pod can only have one ip address [support for multiple ip addresses and networks is intended](#k8s-pods-with-multiple-ips-issue).   

```java
@Entity
@Table(name = "POD")
public class Pod extends BaseEntity {
    @Column(name = "name", nullable = false)
    private String name;

	@Column(name = "nameespace", nullable = false)
    private String namespace;
	
    @Column(name = "external_id", nullable = false, unique = true)
    private String externalId;

    @Column(name = "host")
    private String host;

    @OneToMany(mappedBy = "pod", fetch = FetchType.LAZY)
    private Set<PodPort> ports = new HashSet<PodPort>();

    @OneToMany(mappedBy = "pod", fetch = FetchType.LAZY)
    private Set<SecurityGroupMember> securityGroupMembers = new HashSet<>();
	}
```   

The **PodPort** represents the information related to the pod port needed to create network traffic steering through the SDN controller APIs:    

```java
   @Entity
   @Table(name = "POD_PORT")
   public class PodPort extends BaseEntity {

    @Column(name = "external_id", nullable = false, unique = true)
    private String externalId;

    @Column(name = "mac_address", nullable = false, unique = true)
    private String macAddress;

    @ElementCollection(fetch = FetchType.LAZY)
    @Column(name = "ip_address")
    @CollectionTable(name = "POD_PORT_IP_ADDRESS", joinColumns = @JoinColumn(name = "pod_port_fk"),
    foreignKey=@ForeignKey(name = "FK_POD_PORT_IP_ADDRESS"))
    private List<String> ipAddresses = new ArrayList<String>();

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "pod_fk", foreignKey = @ForeignKey(name = "FK_PODP_POD"))
    private Pod pod;

    @Column(name = "parent_id", nullable = true, unique = false)
    private String parentId;
```  
	
* **database** schema updates:  
All the tables and relationships indicated on the previous entities will also be updated on the files `org/osc/core/broker/util/db/upgrade/ReleaseUpgradeManager.java,Schema.java`.  

### OSC UI
Out of scope.

### OSC Synchronization Tasks
**TBD on next revision**  
Describe any changes on the OSC internal synchronization tasks or metatasks. Use a diagram to represent any updated or new task graph.

## Tests
**TBD on next revision**

Describe here any new test requirement for this feature. This can include: virtualization platform, test infrastructure, stubs, etc. 
> Note: Any feature should be demonstrable and testable independently of a particular vendor component or service. 

## References
### [Kubernetes Home](https://kubernetes.io/)  
### [K8s Pod Watch API](https://kubernetes.io/docs/api-reference/v1.7/#watch-64)  
### [K8s Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)   
### [K8s Authentication](https://kubernetes.io/docs/admin/authentication/)   
### [Fabric8 Credential Example](https://github.com/fabric8io/kubernetes-client/blob/master/kubernetes-examples/src/main/java/io/fabric8/kubernetes/examples/CredentialsExample.java)   
### [K8s Retrieving Pods by UID Issue](https://github.com/kubernetes/kubernetes/issues/20572)   
### [K8s Pods Migration Support Issue](https://github.com/kubernetes/kubernetes/issues/3949)   
### [K8s Pods with Multiple IPs Issue](https://github.com/kubernetes/kubernetes/issues/27398)    
### [OSC Security Groups](https://github.com/opensecuritycontroller/opensecuritycontroller.org/blob/master/overviewandarchitecture/concepts.md#security-groups) 
### [K8s Client Libraries](https://kubernetes.io/docs/reference/client-libraries/)   
### [OVN Kubernetes](https://github.com/doonhammer/ovn-kubernetes)  
### [OVS SFC](https://github.com/doonhammer/ovs/tree/sfc.v30)  
### [Mockito Deep Stubs] (https://www.atlassian.com/blog/archives/mockito-makes-mocking-fluid-interfaces-easy)  


