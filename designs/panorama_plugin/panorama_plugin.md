# Panorama Security Plugin
This is a security appliance plugin for the Panorama Security Management Appliance, which orchestrates PaloAlto virtual firewalls deployed by OSC. The plugin shall conform to the [security manager api](https://github.com/opensecuritycontroller/security-mgr-api) specification. We propose to have:
- In Panorama, we define two classes of tags: one to associate Panorama Address Objects with an OSC security group, and another -- with a security policy.
- OSC policies are defined by shared tags in Panorama.
- The security group tags are managed by OSC (through the Panorama API) and the policy tags are simply shared tags on Panorama. They are managed manually.

## Assignees
Dmitry Gerenrot ([dmitryintel](https://github.com/dmitryintel)).

## Constraints and Assumptions
The Panorama version is at least 7.1. The firewalls are running PAN-VM-KVM-7.1.4.

## Design Changes

We propose the following workflow for creating a security group from OSC.

- Begin by creating a distributed appliance on OSC with PAN-VM-KVM-7.1.4 as the service function. OSC then creates a Device Group under Panorama via the Panorama API. (For example, **DistributedAppGroup**).
- Each policy rule on Panorama can reference dynamic address groups (DAGs) under the **DistributedAppGroup**. The DAGs are constructed manually by Panorama administrators, using shared tags for their match criteria.
	
![](./images/AddressGroups.PNG)

- There should be no more manual steps on the Panorama side.
- In the OSC, create a security group. Suppose the security group Id, _which assigned by OSC_ is **54321**.
- Binding the security group causes OSC to create the address objects with the OSC custom tag **OSC_SecurityGroup_54321** _and_ the policy tags (which are shared tags on Panorama).
- The OSC will use the [Panorama API](https://www.paloaltonetworks.com/documentation/71/pan-os/xml-api) to do that.

![](./images/Address.PNG)

Panorama administrators should:
- understand this workflow
- recognize the DAGs and tags created by OSC
- generally speaking, not edit any of them

The naming conventions/prefixes are up for discussion.

### REST API 
No changes anticipated.

### OSC SDKs
No changes anticipated. However, an implementation detail should be noted.

Under `org.osc.sdk.manager.api`:
- `ManagerSecurityGroupApi`
	- `create/update/deleteSecurityGroup` calls will result in creation/update or deletion of Panorama address objects with the appropriate tag.
	- `getSecurityGroupList` and `getSecurityGroupById` will list the OSC-managed security group tags.
- `ManagerSecurityGroupInterfaceApi`
	- `create/update/deleteSecurityGroupInterface` calls will result in adding or changing the policy tags under each address object. (The argument to these calls is a `SecurityGroupInterfaceElement` which carries policy information.
- `ManagerPolicyApi` will list shared tags.

### SDN Controller SDK
No changes anticipated.

## Tests
TBD

## References
### [Panorama XML API](https://www.paloaltonetworks.com/documentation/71/pan-os/xml-api)
### [OSC Security Manager API](https://github.com/opensecuritycontroller/security-mgr-api)


