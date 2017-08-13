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
For the first release of this feature all the `key` values of the labels in a given security group member will always be the same, i.e.: security=webserver, security=backend, etc.

## Design Changes
The discovery flow adopted for this work will follow the same model already adopted by OSC for OpenStack with RabittMQ:
1. The user creates a security group providing the needed primitives defined by the virtualization environment. In this case those primitives are a set of labels.
2. OSC will watch for notifications related to any entities, in this case pods, labeled with any of the values on the security group.
3. When a meaningful notification is received OSC will trigger a synchronization job for the whole security group.
4. The synchronization job will retrieve the entities associated with the security group from Kubernetes and update its database and other services (security manager and SDN controller) accordingly.  


### REST API  

#### Security Group
The security group resource `/api/server/v1/virtualizationConnectors/{vcId}/securityGroups/{sgId}` is being slightly modified: the **projectid** and **projectName** now are optional, these fields are not applicable to Kubernetes.  For OpenStack, the enforcement of these fields will be done in the OSC business logic instead.  

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
}
```

#### Security Group Member
The security group member resource `/api/server/v1/virtualizationConnectors/{vcId}/securityGroups/{sgId}/members` will new include a new field: **label**. This field is applicable only to Kubernetes and the following will be enforced at the business logic:
a) It must always be present when updating the security group members;  
b) All labels must be strings in the format "key=value".  

> Note: Other than validating the format "key=value" for a fail early approach for Kubernetes this key+value template is completely transparant to OSC, OSC invokes the K8s API providing a string.  

```java
SecurityGroupMemberItemDto {
id (integer, optional),
parentId (integer, optional),
name (string),
region (string),
openstackId (string),
type (string),
protectExternal (boolean, optional),
parentOpenStackId (string, optional),
label (string, optional)
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
These services must also implement adding a security group member of type `SecurityGroupMemberType.Label`. As is today, these services will trigger the conformance tasks for the security group. Thoses tasks will be responsible for discovering the pods associated with the label members and persisting those entities accordingly.  

### OSC SDKs

#### VNF Security Manager SDK
Not applicable.

#### SDN Controller SDK
Details on this is **TBD** but we will at least need to add APIs to return a network element given the **pod name, namespace and name of the hosting node**.  The returned network element should contain the unique port id for both OVN SFC and Nuage. For OVN SFC it should also return the name of the logical switch.  

### OSC & Kubernetes
This section describes how OSC will use the Kubernetes API service endpoint to retrieve and perform live discovery of the protected workloads, highlighting the chosen SDK, connectivity inputs and required APIs.   

#### OSC Kubernetes Wrapper Package
The direct communication between the OSC core modules and the Kubernetes API service will be contained within the new package `org.osc.core.broker.rest.client.k8s` . The purpose of this package is to make it easier for other osc core components to use the K8s APIs as well as prevent leaks of SDK specific details. The class diagram below depicts the classes and functionalities exported by this package.
![](./images/k8s-wrapper-class-diagram.png)  
*Kubernetes Wrapper Package Class Diagram*  


* **KubernetesClient**: Provides a communication channel for the Kubernetes APIs, it is reponsible for initializing the *fabric8* `KubernetesClient`, as part of its constructor and close it, as part of its `close()` method.
* **KubernetesApi**: Represents the base class for the `Kubernetes*Api` classes and contains an instance of the `KubernetesClient`.  
* **KubernetesPodApi**: This class provides all the pod related methods used by other OSC core packages: 
	* `getPodsByLabel`: returns all pods with a matching label, for details [see below](#k8s-targeted-apis). 
	* `getPodsById`: returns the pod with the given uid, namespace and name. 
	* `watchPods`: returns a watcher object that performs event calls when pod matching the provided selector is changed. To create this watcher the caller must provide as `KubernetesSelector` of type `KubernetesSelectorType.Label` with the label string value `KubernetesStringSelectorValue` and a `KubernetesWatchEventHandler` to be invoked when a targeted pod is modified.  
	> All these methods should through a `VmidcException` if an SDK (Fabric8) specific exception is caught.
* **KubernetesEntity**: Base class representing the K8s entities used by OSC.
* **KubernetesPod**: This class provides all the pod information needed by other OSC core packages.
* **KubernetesWatchEventHandler**: This functional interface represents the contract for the method to be invoked when a watched pod changes. The `eventReceived` method will be called with the **KubernetesAction** and the `KubernetesPod`.
* **KubernetesWatcher**: Encapsulates a fabric8 `Watch` object.
* **KubernetesSelector**: Represents the information provided to watch APIs. The selector object also enables the reusability of the type `KubernetesNotificationListener`. The current possible values when creating a selector are **KubernetesSelectorType**.`LABEL` and **KubernetesStringSelectorValue**.  

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

#### Kubernetes Notification Events
OSC will need to maintain connections opened with Kubernetes APIs in order to watch for entity changes. The mechanism for this will be similar to the approach used for RabbitMq with OpenStack but it will also make use of OSGi services to manage the state of the connections and watchers.  
![](./images/k8s-notification-class-diagram.png)  
*Kubernetes Notification Events Class Diagram*  
* **KubernetesClientProvider**: This class provides open `KubernetesClient` objects to other classes and components. This provider must be instantiated by the `Server` class and registered on the OSGi framework. When `start` is invoked it must list all virtualization connectors in the database and initiate a `KubernetesClient` for each one of them. Other classes can resolve this singleton instance through OSGi and look up live clients using the method `getKubernetesClient`. `receiveBroadcast` must react to messages indicating changes on virtualization connectors and create, delete or update and existing client accordingly.  Note that before closing a client a  call to `closeListeners` for all the `KubernetesNotificationRunners` providing the virtualization connector id must be done.  
* **SecurityGroupMemberNotificationRunner**: This class is responsible for managing instances of `KubernetesNotificationListeners`, keeping these instances in sync with the security members in the database. An instance of this class must be initiated by the `Server` class and registered with the OSGi framework. When `start` is invoked it will list all the security group members in the database and create or delete the correspoding `SecurityGroupMemberPodNotificationListener`.  `receiveBroadcast` will listen to events related to security group members and create, update or delete the corresponding listener.  When creating or updating a listener the runner must make use of the method `KubernetesNotificationListener.init` providing the `PodApi` to be used to create the watcher within the listener. `closeListeners` must close all the listeners with a virtualization connector with the id matching the provided id parameter. 
* **SecurityGroupMemberPodNotificationListener**: This listener is responsible for receiving events corresponding to pods related to the given security group member. When `init` is invoked the SGM will be retrieved from the database and set in the selector of the listener, then  a `PodApi` will be created with a client obtained with the `KubernetedClientProvider.getKubernetesClient` and `PodApi.watchPod` will be invoked which will initialize a pod watcher.  When `eventReceived` is called it will react to CREATE or UPDATE events in the pod and it will trigger a sync of the security group using the `conformService`


### OSC Entities  
#### Virtualization Connector  
The `VirtualizationConnector` domain entity field `virtualizationType` can now have a new value: **VirtualizationType.KUBERNETES**.

#### Security Group Member
A new type of security group member is being introduced, **Label**. This member carries a set of **Pods**. 
* **osc-domain** updates:  
Similarly to the existing Network type, the Label entity can be temporarily a member of multiple security groups while concurrent deletion(s) occurr, thus it has a many to one relationship with security group members:  

```java
@Table(name = "SECURITY_GROUP_MEMBER", ...)
public class SecurityGroupMember extends BaseEntity implements Comparable<SecurityGroupMember> {
	// ... 
	@ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "label_fk", foreignKey = @ForeignKey(name = "FK_SGM_LABEL"))
    private Label label;
	
	// ....
}
```  

```java
@Entity
@Table(name = "LABEL")
public class Label extends BaseEntity {
    @Column(name = "value", nullable = false)
    private String value;

    @OneToMany(mappedBy = "label", fetch = FetchType.LAZY)
    private Set<Pod> pods = new HashSet<Pod>();

    @OneToMany(mappedBy = "label", fetch = FetchType.LAZY)
    private Set<SecurityGroupMember> securityGroupMembers = new HashSet<>();
	}
```   

The **Pod** entity carries the relavant information regarding a Kubernetes pod: the name, namespace, uid, host name, a set of ports and a many to many relationship with labels (the same pod can have multiple labels, as long as they do not map to different security groups).   
> Note: Although currently a pod can only have one ip address [support for multiple ip addresses and networks is intended](#k8s-pods-with-multiple-ips-issue).   

```java
@Entity
@Table(name = "POD")
public class Pod extends BaseEntity {
    @Column(name = "name", nullable = false)
    private String name;

	@Column(name = "namespace", nullable = false)
    private String namespace;
	
    @Column(name = "external_id", nullable = false, unique = true)
    private String externalId;

    @Column(name = "host")
    private String host;

    @OneToMany(mappedBy = "pod", fetch = FetchType.LAZY)
    private Set<PodPort> ports = new HashSet<PodPort>();

    @ManyToMany(fetch = FetchType.LAZY, mappedBy = "pod")
    private Set<Label> labels = new HashSet<Label>();
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
The security group(SG) membership will be synchronized by OSC using its tasks and metatasks. This synchronization will continue to be triggered, as today, by: security group creation, update or deletion; and notifications received from Kubernetes relevant for the security group.
The diagram below depicts the tasks and metatasks involved on this change:
![](./images/discovery-tasks.png)  
*Tasks and Metatasks for Synchronizing Security Group Members*
* **SecurityGroupCheckMetaTask**: This metatask will continue mostly as is, but for SGs of Virtualization Connectors of type Kubernetes it will add to the graph `KubernetesSecurityGroupUpdateOrDeleteMetaTask` instead of the existing `SecurityGroupUpdateOrDeleteMetatask`.  
* **KubernetesSecurityGroupUpdateOrDeleteMetaTask:** The main purpose of this task is to trigger the task `KubernetesSecurityGroupLabelCheckMetTask` for each label security group member. Similarly to the existing `SecurityGroupUpdateOrDeleteMetatask` this task will also add the existing task `PortGroupCheckMetaTask` if the SDN controller supports port group.  
* **KubernetesSecurityGroupLabelCheckMetaTask:** This metatask forks the graph in two possible options for a given label security member: update or deletion, adding to the graph either `SecurityGroupMemberLabelUpdateMetaTask` or 
* **SecurityGropuMemberDeleteTask**: This existing task is currently responsible for deleting security members, entities (VM, network, etc) and ports when applicable. It will remain mostly the same but also handling the member type `Label`.  
* **SecurityGroupMemberLabelUpdateMetaTask:** The main purpose of this task is to list the K8s pods using the `KubernetesPodApi` and checking if a new pod needs to be created or an existing one must be deleted.  Observe that pod updates are not expected, any changes on the pod: name, namespace, node, network info should represent a new pod (K8s does not currently support pod migration). Once binding is developed this metatask will also include tasks to synchronize information with the SDN controller.  `
* **LabelPodCreateTask:** This task is responsible for retrieving additional network information from the SDN controller related to the targeted pod and it will persit the pod with that information (i.e. pod port) on the OSC database.  `
* **LabelPodDeleteTask:** This task is responsible for purging pod and pod network information from the OSC db.  `

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
### [Mockito Deep Stubs](https://www.atlassian.com/blog/archives/mockito-makes-mocking-fluid-interfaces-easy)  


