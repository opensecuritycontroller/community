# Panorama Security Plugin
This is a security appliance plugin for the Panorama Security Management Appliance, which orchestrates PaloAlto virtual firewalls deployed by OSC. The plugin shall conform to the [security manager api](https://github.com/opensecuritycontroller/security-mgr-api) specification. We propose to have:
- A Panorama Dynamic address group for each OSC security policy. It will be labeled by a tag and targeted by a _Panorama_ security policy.
- In Panorama, we define two classes of tags: one to associate Panorama Address Objects with a security group, and another -- with a security policy.
- The security group tags are managed by OSC (through the Panorama API) and the policy tags are managed manually on Panorama.

## Assignees
Dmitry Gerenrot ([dmitryintel](https://github.com/dmitryintel)).

## Constraints and Assumptions
The Panorama version is at least 7.1. The firewalls are running PAN-VM-KVM-7.1.4.

## Design Changes

We propose the following workflow for creating a security group from OSC.

- Begin by creating a distributed appliance on OSC with PAN-VM-KVM-7.1.4 as the service function. OSC then creates a Device Group under panorama via the Panorama API. (For example, **DistributedAppGroup**).
- Proceed by defining the security policies on panorama as follows:
	- For each policy to be managed by the **Panorama Security Plugin**, there will be a dynamic address group (DAG) under the **DistributedAppGroup** and a _shared_ tag, e.g., **OSC_Policy_1**. Panorama administrators _create these manually_.
	- It is also possible to use any other shared tag that has been used to label a Panorama security policy.
	- Under the panorama **Policies** tab, create a security policy to target the DAG as usual.
	
![](./images/AddressGroups.PNG)

- There should be no more manual steps on the panorama side.
- In the OSC, create a security group. (Suppose the security group Id, _which assigned by OSC_ is **54321**). For each address in a security group, the OSC will create an address object under the **DistributedAppGroup**.
- OSC also creates a Panorama tag of the form **OSC_SecurityGroup_54321**.
- There will be one such tag per security group. All the address objects will be labeled by it.
- Binding happens when OSC creates the address objects in Panorama and labels them with security group and security policy tags. 
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
	- `create/update/deleteSecurityGroup` calls will result in creation/update or deletion of Panorama address objects with the appropriate label.
	- `getSecurityGroupList` and `getSecurityGroupById` will list the OSC-managed security group tags.
- `ManagerSecurityGroupInterfaceApi`
	- `create/update/deleteSecurityGroupInterface` calls will result in adding or changing the policy tags under each address object. (The argument to these calls is a `SecurityGroupInterfaceElement` which carries policy information.
- `ManagerPolicyApi` will list the shared tags.

### SDN Controller SDK
No changes anticipated.

## Tests
TBD

## References
### [Panorama XML API](https://www.paloaltonetworks.com/documentation/71/pan-os/xml-api)
### [OSC Security Manager API](https://github.com/opensecuritycontroller/security-mgr-api)


