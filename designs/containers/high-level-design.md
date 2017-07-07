# OSC Containers Support
This document describes the high level architecture for supporting protection of containerized workloads managed by Kubernetes (K8S). It highlights the main integration points between OSC and the related external services, lists assumptions (each one of them requiring additional validation and investigation) and restrictions, and scopes the work targeted for the next OSC release. 


## High Level Architecture


![](./images/architecture.png)
*OSC and K8S: High Level Architecture*

### Deployment
The deployment of the security VNF should be done on the same virtualization environment managed by the Kubernetes Controller. This should be possible by using one of the available implementations for the [Container Runtime Interface (CRI)](http://blog.kubernetes.io/2016/12/container-runtime-interface-cri-in-kubernetes.html) such as [Kubevirt](https://github.com/kubevirt/kubevirt) or [Virtlet](https://github.com/Mirantis/virtlet) .

> **Restriction:**  The protected workload must reside in the same node as the VM VNF. To workaround this restriction the VNF will be depployed on all existing K8S nodes for the first release. 

> **Assumption:** When deployed in the environment the VM VNF will be automatically registered in the OVN network.  

Once OSC has deployed all the VM instances (one in each node) it should also store their  OVN port ids registered on their respective vswitch, in the image above the port id would be `vnfp1` and `vnfp2`.

### Workload Discovery
The workloads to be protected will be defined in OSC using K8S labels. The user should be able to define a security group on OSC using one or more K8S label and OSC should apply an `OR` to the labels on that list: as long as a pod has at least one of the defined labels in the security group it should be protected.  
> **Assumption:** A notification mechanism exists in K8S that will allow OSC to discover when new pods are created or deleted.  OSC may need to perform additional calls to the OVN NB to retrieve detailed network information such as the name of the switch (i.e.: `k8s-minion1`) and the port identifier of the pod in that switch (i.e.: `clientp1`)

### Traffic Steering
Once the VM VNF instances have been deployed and workloads can be discovered by OSC it should now be able to steer the traffic through the VNF. This will be done through operations performed in the OVN NB database.  
OVN supports SFC operations to perform the traffic steering, additionally there might be other SFC implementations exposed by different virtualization platforms, i.e.: OpenStack. To isolate the implementation details of specific SFC operations, a well defined interface should be created for the SFC APIs, the `OSC SFC SDK`. We would then have an `SFC OVN Plugin` implementing those APIs by communicating with the OVN VN database through `TCP`.

> **Assumption**: Remote communication with the OVN NB database is possible through TCP provided the correct endpoint and necessary credentials. 
> **Restriction**:  The redirection will always be performed with the values `exit-lport` and `bi-directional` for the first release. 

## Releases

### Release 1.0.0
This is the first release for integrating OSC with K8S. The main goal of this release is enhancing OSC to be able to protect containerized workloads, adjusting its current architecture and adding all the necessary new integration pieces.  The following items apply to all features targeted by this release:
1.  All the *Restrictions* mentioned previously apply to this release.
2.  No regression on existing OSC functionalities.
3.  Production readiness is **out of scope**.  While all the features on this release will be part of the OSC codebase and will be repeatable they will not go through QA validation and should be considered as a prototype. 
3.  All the features listed below will be exposed through the OSC APIs when applicable, **UI updates are out of scope**.

### Features

#### Containers - VNF Deployment
**Description:**
As a security administrator, I want to be able to deploy a security VNF VM to perform protection of containerized workloads hosted on a Kubernetes environments.

**Acceptance Criteria:**
* Demonstrate a VM capable of intercepting the traffic between containers can be deployed on a virtualization environment.
* The VM must be added to the same logical switch as the workload containers to be protected.
* The VM can be removed (un-deployed) from the virtualized environment. 
* If the VM is deleted by the user from the virtualized environment it must be recreated as expected.
* The security manager responsible to manage the deployed security appliance is notified  when the VM is deployed or removed.

**Out of Scope:** 
* Newly added K8S nodes will not have a VM VNF automatically deployed. 
* OSC will not implement deletion of the deployed VM VNFs. As a workaround the VNFs can be deleted directly in the virtualization environment.  

#### Containers  - Workload Discovery
**Description:**
As a security administrator, I must be able to define security groups in OSC to determine which workloads to protect on the containerized environment. 

**Acceptance Criteria:**
* Demonstrate a security group can be created in OSC using K8S labels.
* OSC must identify all current pods containing at least of the labels populating the security group with those members.
* OSC must discover the network ids related to the workloads (switch, port)
* OSC must automatically identify creation and deletion of entities on the container environment tagged with at least of of the labels creating or removing that entity from their respective security group.  

**Out of Scope:** 
* Deleted pods will not trigger a notification to OSC. For this release, resyncing the security group can be used as a workaround.   

#### Containers  - Traffic Steering

**Description:**
As a security administrator, I must be able to bind a defined container security group to a deployed VNF VM to protect container workloads and perform traffic redirection to that VNF. 

**Acceptance Criteria:**
* Demonstrate a security group can be bound to a deployed distributed appliance for the VM VNF.
* Demonstrate the SDN plugin responsible for configuring the traffic steering receives from OSC the correct information needed to perform the action when:
    * A new pod gets created on K8S with the parameter defined in the OSC security group.
    * A pod get deleted on K8S with the parameter defined in the OSC security group.