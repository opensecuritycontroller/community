# Multi-Policy Mapping Workflow

This document describes the proposed changes for multi-policy mapping workflow.

## Background

Currently, we have two ways to determine which policy gets applied to which workload:

- Provide the VNF security manager with encapsulation tag
- Provide the VNF security manager with list of policies

If the manager is supporting [Policy Mapping](https://github.com/opensecuritycontroller/security-mgr-api/blob/master/src/main/java/org/osc/sdk/manager/Constants.java#L70) and [Security Group](https://github.com/opensecuritycontroller/security-mgr-api/blob/master/src/main/java/org/osc/sdk/manager/Constants.java#L60), we provide the manager with the security group name and members (their IPs and MACs) information to bind the policy.

## Constraints and Assumptions
The appliance security manager will not delete a security group with one or more security group interfaces.

## Design Changes
`SecurityGroup`: Currently, `SecurityGroup` and `SecurityGroupInterface` have many to many entity mapping. The proposed design will change this relationship to a one to many relationship between the SG and the SGIs

### REST API
`SecurityGroupInterfaceDto`:

```
[
  {
    "virtualSystemId": 0,
    "name": "string",
    "policyId": 0,
    "managerSecurityGroupId": "string", // This new property is added to persist the manager security group id
    "failurePolicyType": "FAIL_OPEN",
    "order": 0,
    "policies": [
      {
        "id": 0,
        "parentId": 0,
        "policyName": "string",
        "mgrPolicyId": "string",
        "mgrDomainId": 0,
        "mgrDomainName": "string"
      }
    ],
    "markedForDeletion": false,
    "binded": false
  }
]
```

### OSC SDKs

#### VNF Security Manager SDK

`SecurityGroupInterfaceElement`: Add a new interface

```
public interface SecurityGroupInterfaceElement {

	/**
	 * @return the identifier of the security group interface defined by the manager
	 */
	String getManagerSecurityGroupInterfaceId();

	/**
	 * @return the name of the security group interface defined by OSC
	 */
	String getName();

	/**
	 * Provides the identifier of the security group defined by security managers that support policy mapping and
	 * security groups
	 *
	 * @return the identifier of the security group defined by the manager
	 */
	String getManagerSecurityGroupId();

	/**
	 * Provides the context information of manager policy element
	 *
	 * @return the set of manager policy elements
	 */
	Set<ManagerPolicyElement> getManagerPolicyElements();

	/**
	 * @return the encapsulation tag supported by the manager
	 */
	String getTag();
}
```


`ManagerSecurityGroupInterfaceApi`: Update `ManagerSecurityGroupInterfaceApi` interface

**Current interface methods**

```
public interface ManagerSecurityGroupInterfaceApi {

    String createSecurityGroupInterface(String name, String policyId, String tag) throws Exception;

    void updateSecurityGroupInterface(String id, String name, String policyId, String tag) throws Exception;
}
```

**Proposed changes to the interface methods**

```
public interface ManagerSecurityGroupInterfaceApi {

    String createSecurityGroupInterface(SecurityGroupInterfaceElement sgiElement) throws Exception;

    void updateSecurityGroupInterface(SecurityGroupInterfaceElement sgiElement) throws Exception;
}
```

`ManagerPolicyElement`: Update `ManagerPolicyElement` interface

**Current interface methods**

```
public interface ManagerPolicyElement {
    /**
     * @return the identifier of the policy defined by the security manager
     */
    String getId();

    /**
     * @return the name of the policy defined in the security manager
     */
    String getName();
}
```

**Proposed changes to the interface methods**

```
public interface ManagerPolicyElement {
    /**
     * @return the identifier of the policy defined by the security manager
     */
    String getId();

    /**
     * @return the name of the policy defined in the security manager
     */
    String getName();

    /**
     * @return the identifier of the domain, the policy belongs to in the security manager
     */
    String getDomainId();
}
```

#### SDN Controller SDK
No changes to SDN Controller SDK are required.

### VNF Security Manager Plugins
Updating the plugins implementing these APIs is out of scope for this feature, with the exception of the security-mgr-sample-plugin which will be modified to support multiple policy mapping.

### OSC UI
Multi-policy mapping is out of scope.

### OSC Entities
`SecurityGroupInterface`: Add `managerSecurityGroupId` field of type string

`SecurityGroup`: Delete the `mgrId` field

### OSC Synchronization Tasks
The major tasks affected by the change are `CreateMgrSecurityGroupTask`, `SecurityGroupUpdateOrDeleteMetaTask`, `MgrSecurityGroupCheckMetaTask`, `UpdateMgrSecurityGroupTask`, `ForceDeleteDATask`, `ForceDeleteVirtualSystemTask`, `ForceDeleteSecurityGroupTask`, `DeleteSecurityGroupInterfaceTask`.

## Tests
- In case of manager not supporting security group, the policy binding should be done based on the tag
- If the manager is supporting the security group, the manager security group id should not be null