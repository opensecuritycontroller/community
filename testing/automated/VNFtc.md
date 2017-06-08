# OSC Partnership VNF Compatibility Test Plan
This document describes the QA Test Plan for testing VNF. Details in the test cases section.

## Purpose
Open Security Controller (OSC version 0.6) partners with other vendor Cloud Security Virtualized Network Function (VNF) products. NFV (Network Function Virtualization) Infrastructure (NFVI) between vendors’ products needs to be tested. We tested two environments, Openstack (here tested with Redhat 7.1 Kilo) and VMware NSX (6.2) with vCenter (5.5). Other versions will be tested e.g. Openstack Liberty, Mitaka; vCenter 6.0 and so on.

###	Abbreviations
* **OSC** – Open Security Controller
* **VC** – Virtualization Connectors in OSC
* **MC** – Manager Connectors in OSC
* **DA**- Distributed Appliance in OSC
* **DAI**- Distributed Appliance Instance in Openstack or Vmware VM

## Requirements

### OpenStack Environment
We are using Redhat 7.1 OS, Openstack – Kilo and Mitaka
Test setup includes at least 3 nodes:
-	One controller node and one compute node, and one network node

### Hardware Requirements
Whatever required in order to install the Software Requirements

### Software Requirements
Minimum for VMware: ESXi 5.5 or higher, vCenter 5.5 or higher NSX version 6.1 or higher.
Minimum for Openstack: Kilo or newer.
Also need to use OSC, security VNF and VNF Manager.

## Testbeds

### Test Topology
* End to end applications and data traffic redirects to Security VNF through SDN.
* Have Openstack environment or VMware environment.
* For Openstack the Network topology should have: Inspection Net, Management Net, Public Net and their subnets.
* For Openstack environment you suppose to have one controller, one compute node or more, and one network node.
* Also SDN Controller installed for traffic redirection.
* VNF manager is installed.
* Also have Victim, and Attacker VMs for end to end test.
* Having a VNF image which can be imported to OSC.

## Test Case Identification

All these test cases should pass, OSC has Status Jobs *PASSED*, for the Security VNF to work with OSC.
> Some tests may be more OSC related than VNF, but they are relevant for the workflow to test 3rd party VNF product Compatibility with OSC. Releasing version 0.6 OSC has implemented agentless for partners need, end to end in this way may be up to the VNF Manager to identify VM in protection or not.


### 1.1 VNF OpenStack Test Cases
From OSC Manage => Plugins => Manager Plugins uploads VNF Manager plugin and see it’s in the UI.

### 1.1.2	From OSC Manage => Plugins => Manager Plugins, verify you can delete the plugin in UI.
### 1.1.3	From OSC Setup => Virtualization Connectors Add a VC, type OPENSTACK, verify that VC was added to OSC UI with accurate parameters.
### 1.1.4	From OSC Setup => Manager Connectors Add a Security VNF Manager with host IP login credentials & Job Status passed.
### 1.1.5	From OSC Setup => Manager Connectors Edit a Security VNF Manager with host IP login credentials & Job Status passed.
### 1.1.6	From OSC Setup => Manager Connectors Sync a Security VNF Manager with host IP login credentials & Job Status passed.  After a sync new information from VNF Manager should be passed to the appliances and new information about VNFs should be passed to the VNF Manager.
### 1.1.7	From OSC Setup => Manager Connectors Delete a Security VNF Manager with host IP login credentials & Job Status passed.
•	If not in use the manager connector will be deleted
•	If there are VNF instances or there are distributed appliances the delete will fail, need to delete other connection first
### 1.1.8	From OSC Setup => Service Function Catalog Auto Import a Security VNF Model/Image, show up in OSC Service Function Catalog pane as passed.
### 1.1.9	From OSC Setup => Distributed Appliance Add a SECURITY VNF image DA, show up in OSC DA pane with Last Job Status passed.
### 1.1.10	From OSC Setup => Distributed Appliance Edit a SECURITY VNF image DA, see update in OSC DA pane with Last Job Status passed.
### 1.1.11	From OSC Setup => Distributed Appliance Sync a SECURITY VNF image DA, see update in OSC DA pane with Last Job Status passed.
For last three test cases – at the end of having DA of security VNF – you might (depend on manger implementation) need to have in the manager to show this Virtual Security System (VSS, e.g. IPS’ VNF Manager)
### 1.1.12	From OSC Setup => Distributed Appliance Delete a SECURITY VNF image DA, see DA deleted in OSC DA pane as passed.
•	If not DAI in use – delete pass
•	If DAI but not used for inspection – delete pass
•	If DAI used for inspection – delete fail
### 1.1.13	From OSC Setup => Add (In Deployments Spec) the DA to the Openstack Compute, Openstack Project Instances see this DAI (DA Instance) - Last Job Status should show passed.  And the instance should be launched in Openstack.
### 1.1.14	From OSC Setup => Distributed Appliance Edit (In Deployments Spec) the DA to the Openstack Compute, Openstack Project Instances sees this DAI (DA Instance) updated - Last Job Status should show passed.  The VNF should be updated in Openstack.
### 1.1.15	From OSC Setup => Distributed Appliance Sync (In Deployments Spec) the DA to the Openstack Compute, Openstack Project Instances sees this DAI (DA Instance) updated.  Last Job Status should show passed.  The VNF should be updated if it wasn’t previously in Openstack.
### 1.1.16	From Openstack UI, terminate the VNF Instance – it should be automatically redeployed by OSC and job launching it and the VNF instance will show up in Openstack UI.
### 1.1.17	From OSC Setup => Distributed Appliance Delete (In Deployments Spec) the DA to the Openstack Compute, Last Job Status should show passed.  If used the VNF won’t be removed from Openstack.  If the VNF doesn’t currently protect any port, the VNF should be automatically deleted from Openstack.
### 1.1.18	From OSC Setup => Virtualization Connectors Add a Security Group with VM type and selected Items to have this Victim VM, show up in OSC Virtualization Connectors’ Security Group pane as passed.
### 1.1.19	From OSC Setup => Virtualization Connectors Edit a Security Group with VM type and selected Items to have this Victim VM, show up in OSC Virtualization Connectors’ Security Group pane as passed.
### 1.1.20	From OSC Setup => Virtualization Connectors Sync a Security Group with VM type and selected Items to have this Victim VM as passed.
### 1.1.21	From OSC Setup => Virtualization Connectors Delete a Security Group with VM type and selected Items to have this Victim VM as passed.
### 1.1.22	From OSC Setup => Virtualization Connectors Security Group Bind a DA with specific Policy to this Security Group, next test case end to end will happen as passed.
### 1.1.23	From Attacker, launch an Attack on the Victim VM that supposed to be treated by the VNF that used in the DA, bound to the security group of the Victim VM – the attack should be treated according to the policy that it bound.
### 1.1.24	From OSC Setup => Virtualization Connectors Security Group, Unbind Policy from this Security Group and it has a result the Victim should not be protected anymore.

### 1.2	VNF Vmware Vcenter NSX Test Cases
All tests are the same as Openstack except:
•	Security grouping and binding policies done from NSX and not from OSC.

### 1.2.1	From OSC Setup => Virtualization Connectors Add a VC with type VMWARE, verify that the VC was appears in OSC as expected.
### 1.2.2	From OSC Setup => Service Function Catalog Auto Import a Security VNF Model/Image, show up in OSC Service Function Catalog pane as passed.
### 1.2.3	From OSC Setup => Distributed Appliance Add a SECURITY VNF image DA. Last Job Status in OSC should show passed.  Related Service Definition should be added to NSX. It should also be reflected in the VNF Manager UI.
### 1.2.4	From OSC Setup => Distributed Appliance Edit a SECURITY VNF image DA. Last Job Status in OSC should show passed.  Related Service Definition should be updated on NSX. It should also be reflected in the VNF Manager UI.
### 1.2.5	From OSC Setup => Distributed Appliance Sync a SECURITY VNF image DA. Last Job Status in OSC should show passed.  Related Service Definition should be updated on NSX. It should also be reflected in the VNF Manager UI.
### 1.2.6	From OSC Setup => Distributed Appliance Delete a SECURITY VNF image DA,.  If there is NO VNF deployed that protects VMs in Security group for this DA.  This DA should be successfully deleted and the related Service Definition and reflection in VNF Manager should be removed.
NOTE: Following test cases are in vCenter web client to test it works with OSC:
### 1.2.7	From Installation->Service Deployments add this DA (Service Definition) and install. Installation should be successful and ESX agents should be created on related ESXs. VNF manager should show these devices too, OSC after a while will show those appliance instances as Discovered and Inspection Ready.
### 1.2.8	From NSX Service Composer->Security Groups, Add Victim VM to security group.    From NSX Service Composer->Security Policies add a security VNF policy.   Apply the new Policy to the Victim VM Security Group.

From Attacker, launch an Attack on the Victim VM that supposed to be treated by the VNF that used in the DA, bound to the security group of the Victim VM – the attack should be treated according to the policy that it bound.