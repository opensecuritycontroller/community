# Tasks and MetaTasks Coding Guidelines

## Introduction

OSC tasks and metatasks classes are used for the core orchestration functions and for other long running asynchronous operations within OSC. This document outlines the code conventions and guidelines that must be followed when authoring tasks and metatasks.  

## Conventions  

In addition to the conventions listed below ensure to use the [Java Programming Language Code Conventions](http://www.oracle.com/technetwork/java/codeconvtoc-136057.html).  

### Location

All tasks and metatasks classes must be in a package named with the prefix **org.osc.core.broker.service.tasks.***.
> Note:  Only common classes across many tasks or metatasks should be placed directly in **org.osc.core.broker.service.tasks**, most classes should be under a more specific package.  

**DO:**

```java
org.osc.core.broker.service.tasks.securitymanager.CreateSecurityManagerDeviceMemberTask 
```

**DON'T:**
 
```java
org.osc.core.broker.service.securitymanager.CreateSecurityManagerDeviceMemberTask
```
```java
org.osc.core.broker.service.tasks.CreateSecurityManagerDeviceMemberTask
```

### Naming

#### Package Names
As previously mentioned all tasks and metatasks packages must be prefixed with **org.osc.core.broker.service.tasks***. In addition to that they must follow the scheme: `org.osc.core.broker.service.tasks.[OPT:VIRTUALIZATION_PLATFORM].[OPT:INTEGRATION_POINT].[ENTITY_NAME]`.  
* `VIRTUALIZATION_PLATFORM`: The possible values for this *optional* part are `ost` and `k8s`. This part indicates that the task or metatask in the package is specific to OpenStack (`ost`) or Kubernetes (`k8s`).  Only tasks and metatasks agnostic to the virtualization platform should not have this part.  
*  `INTEGRATION_POINT`: The possible values for this *optional* part are `manager` and `sdn`. This part indicates that the task or metatask in the package is specific to security managers (`manager`) or SDN controllers (`sdn`).  Only tasks and metatasks agnostic to an specific integration point should not have this part.  
* `ENTITY_NAME`: This part is the most granular in the package name and it is NOT optional. It should be the name of an entity known to the OSC design, for instance an entity defined in the REST API, plugin SDKs, database, etc. Some well-known entity names are: `securitygroup`, `virtualizationconnector`, `usercredentials`, `networksettings`, `deploymentspec`, `inspectionhook`, `portgroup`, `virtualsytem`, `distributedappliance`, `device`, `devicemember`, etc.   
> **Note:** You should always be able to relate a task or metatask to a single well known entity. A task or metatask that relates to multiple entities is an indication that it should be refactored.  
> **Noted:** Do **NOT** use abbreviated entity names like `dai`, `da`, `vs`, etc. 


**DO:**

```java
org.osc.core.broker.service.tasks.manager.device.MyTask  // Tasks or MetaTasks specific to security manager devices and agnostic to virtualization platform
```
```java
org.osc.core.broker.service.tasks.k8s.securitygroup.MyTask  // Tasks or MetaTasks specific to security group and k8s
```
```java
org.osc.core.broker.service.tasks.distributedappliance.MyTask  // Tasks or MetaTasks specific to distributed appliance, agnostic to virtualization platform and integration point
```
```java
org.osc.core.broker.service.tasks.ost.sdn.securitygroup.MyTask  // Tasks or MetaTasks specific to SDN controller, OpenStack and security group
```

**DON'T:**
```java
org.osc.core.broker.service.tasks.manager.MyTask // Mandatory entity name part missing.
```  
```java
org.osc.core.broker.service.tasks.domain.SomeDomainTask // Domain is an entity specific to security manager this package is likely missing "securitymanager".
```
```java
org.osc.core.broker.service.tasks.distributedappliances.MyTask // Do NOT use PLURAL in the entity name part.
```
```java
org.osc.core.broker.service.tasks.manager.device.member.MyTask // There should be only one part for the entity, this should be "devicemember" instead.
```
```java
org.osc.core.broker.service.tasks.k8s.pod.create.MyTask // The package name should ALWAYS end with the entity name, do NOT create more granular packages like "*.create".
```
```java
org.osc.core.broker.service.tasks.conform.securitygroup.MyTask // "conform" is not a part name.
```

####  Class Names  

Tasks and MetaTasks class names must follow the pattern `[ACTION][OPT:VIRTUALIZATION_PLATFORM][OPT:INTEGRATION_POINT][ENTITY_NAME][OPT: ENTITY_ACTION_DETAILS][TASK_METATATASK]`.  
* `ACTION`:  This is the action performed by the task or metatask with respect to the `ENTITY` part. Common actions are CRUD calls to integration points, checking the state of some entity, conforming some entity with multiple integration points and virtualization platform, etc. Expected names are: `Create`, `Upsert`, `Update`, `Delete`, `Conform`, `Check`, `CreateOrUpdate`, `DeleteOrUpdate`, etc.   
>  **Note:** For consistency DO NOT use other semantically equivalent names like `Register` (equivalent to `Create` or `Upsert`) or `Remove` (equivalent to `Delete`) .  Stick to the terms mentioned above. If you come across a new action and are sure that nothing similar already exists in the code you may create a new action name.  
>  **Note:** Observe there is a difference between the action `Upsert` and `CreateOrUpdate`. The former indicates the task will invoke some API that creates or updates and entity (if it already exists) on the database or integration point. The latter should be used only for metatasks and it indicates that the metatask will conditionally add a `Create` or `Update` task to the execution graph.  
* `VIRTUALIZATION_PLATFORM`: The possible values for this *optional* part are `Ost` or `K8s`. This part indicates that the task or metatask is specific to a given virtualization platform. Only tasks and metatasks that are platform agnostic should not have this part.  
* `INTEGRATION_POINT`: The possible values for this *optional* part are `Manager` or `Sdn`.  This part should be used only to disambiguate where the action is being performed. For instance the task `UpdateSecurityGroupTask` indicates it updates a security group in the OSC database, if instead it primarily updates it in the security manager it should be `UpdateManagerSecurityGroupTask`.  
* `ENTITY_NAME`: This part is NOT optional. It should be the name of an entity known to the OSC design, for instance an entity defined in the REST API, plugin SDKs, database, etc. Some well-known entity names are: `SecurityGroup`, `VirtualizationConnector`, `UserCredentials`, `NetworkSettings`, `DeploymentSpec`, `InspectionHook`, `PortGroup`, `VirtualSytem`, `DistributedAppliance`, `Device`, `DeviceMember`, etc.   
> **Note:** Do **NOT** use abbreviated entity names such as `DAI`, `VS`, `DS`, etc.  
* `ENTITY_ACTION_DETAILS`: This *optional* part can be used to provide more details about what is being done with/to the entity. A common use for this is when a task is updating an specific property of the entity and you would like to highlight that in the name, for 
`DeleteDistributedApplianceInstanceInspectionPortTask` .  
* `TASK_METATASK`: The values for this part are `Task` or `MetaTask`.  


**DO:**

```java
CreateK8sDeploymenTask 
```
```java
ConformSecurityGroupMetaTask
```
```java
CheckK8sDeploymentStateTask
```
```java
DeleteDistributedApplianceInstanceInspectionPortTask  // Deletes the inspection port info from the DAI
```
```java
ConformOstDeploymentSpecMetaTask
```
```java
CreateSecurityManagerDeviceTask
```

**DON'T:**
```java
CreateK8sDeploymensTask  // DO NOT use plural
```
```java
ConformSecurityGroupTask // The Conform action is likely misused here, this should likely be a metatask since conforming involves multiple operations and a task should be only responsible for a single operation.  
```
```java
DeploymentStateCheckTask // The Action part should ALWAYS come first.
```
```java
UpdateOrCreateSecurityGroupMetaTask  // Should be CreateOrUpdate for consistency.
```
```java
CreateDAITask  // Do NOT use acronyms here, this should be CreateDistributedApplianceInstanceTask instead
```
```java
DeleteOrUpdateSecurityGroupTask  // This should likely be a MetaTask instead since it has a conditional actions.  
```

### Design

#### Tasks
Task classes should almost **NEVER** perform multiple state changing actions. State change actions are typically create, update or delete entities in the OSC database or integration points.  The only exception for this rule is to update an OSC database entity with a result of another action, for instance updating security manager device ID in the OSC database after the task creates a device in the security manager. Other than this exception if your task is performing more than one action it should be refactored into a MetaTask that adds to the graph the tasks needed for each action.  
> **Note:** A good example of this design principal is the existing task `CreateK8sDeploymentTask` . This task creates a deployment in Kubernetes and updates the OSC deployment spec external ID in the database. Observe this task does not perform any other state changing action.   

#### MetaTasks
MetaTasks should **NEVER** perform any state changing action. The purpose of metatasks is to combine tasks in an execution graph based on the current state of the system.  To do that it may perform multiple read operations on the OSC database and/or integration points and output a single graph with the task(s) to be executed.  This design principal/restriction allows for a simpler standardized unit test approach for all the metatasks. Meta task unit tests will NEVER check if a metatask has perform a change in the system, they just check the expected execution graph.   

> **Note:** A good example of this design principal is the existing task `ConformK8sDeploymentSpecMetaTask` . This task does NOT perform any changing action on the database or integration points (like updates, deletes, creates). It simply adds other tasks to the graph. Observe its the unit tests, `ConformK8sDeploymentSpecMetaTaskTest`, simply validate the expected graph and do not check whether something in the system has changed.  
> **Note:** While you may be able to create a metatask that adds many different task types in the graph try to keep the number of task dependencies for a given metatask limited. As with any class design metatask are better off small which means a good metatask should attempt to stick with no more than 4 different task types.  Bigger metatasks are hard to unit test and maintain. If your metatask is growing beyond 4 different task types it is an indication it should be refactored into multiple metatasks.   
