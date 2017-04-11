# OSC Partnership SDN Controller Compatibility Test Plan
This document describes the QA Test Plan for testing SDN Controller. Details in the test cases section.

##	Purpose
Open Security Controller (OSC) partners with other Cloud Security vendor products. This test plan is for verifying a third party Software Defined Network (SDN) Controller compatibility with OSC.

## Feature Functionalities to be tested
The tests have been categorized according to the workflow on OSC UI. Test cases should be followed to verify different areas of testing and functionalities.

##	Openstack Environment
We are using Redhat 7.1 OS, Openstack – Kilo.
Test setup includes at least 2 nodes:
-	One controller node and 2 compute nodes, or
-	One Controller + Compute, and an additional Compute node.

##	Requirements and Testbed

### Hardware Requirements
Whatever required in order to install the Software Requirements.
### Software Requirements
OSC, 3rd party or dummy VNF which can capture traffic, Openstack environment (Redhat 7.1 – Kilo or later)
##	Assumptions
-	OSC should be deployed with a Virtualization Connector (VC)  (with SDN configured as NONE), Manager Connector (MC), a third party or dummy VNF which can capture traffic, a Distributed Appliance (DA) (using the Manager Connector, Service Function Definition, and selectively enabled Virtualization Systems), and a Deployment Specification (DS).
-	Openstack setup with at least one Controller, and two Compute nodes.
-	A Third Party SDN Controller which can be added as a plugin into the OSC.

> NOTES: The tests marked P1 are higher priority tests.
Some tests may be more OSC related than SDN, but they are relevant for the workflow to test 3rd party SDN Controller Compatibility with OSC.

##	Test Cases

### 1.1 PLUGINS
### 1.6.1	From OSC, select Manage  Plugins. Verify you can upload a third party SDN Controller Plugin into OSC. Verify that the uploaded plugin is displayed under the ‘Plugins’ table.
### 1.6.2	Verify you can upload different versions of the same plugin. All different uploaded versions should be displayed under the Plugins table.
### 1.6.3	Verify you can Download SDN Controller Plugin SDK using the button ‘Download SDN Controller Plugin SDK’. You should see ‘OscSdnController-sources.jar’ file downloaded at a location on your PC.
### 1.6.4	Verify you can ‘Delete’ the plugin by clicking on the ‘Delete’ button (which is in the Plugins Section). When the plugin is deleted, it should disappear and not be displayed in the Plugins table.
### 1.6.5	Upload an SDN Controller Plugin which is already existing. The plugin should be overwritten.

### 1.2 VIRTUALIZATION CONNECTOR
### 1.2.1	Verify that once the plugin is uploaded, when you ‘Add/Edit’ a Virtualization Connector, and select Type ‘Openstack’, the plugin appears as a selectable option under SDN Controller Type.
### 1.2.2	Verify that you can ‘Add/Edit’ a Virtualization Connector with SDN Controller Type selected. The VC should be displayed on the Virtualization Connector page with accurate parameters for Name, Type, Controller IP and Provider IP.
### 1.2.3	Verify you can create an Openstack VC without configuring the SDN Controller – i.e. when choosing the option ‘NONE’. The VC should be displayed on the Virtualization Connector page with accurate parameters for Name, Type, Controller IP and Provider IP.

### 1.3 DEPLOYMENTS
### 1.3.1	Verify that Deployment Spec added from OSC is displayed on Openstack Horizon under Project Instances. (OSC Test needed for the workflow)
### 1.3.2	There is a greyed out ‘Delete’ tab under Virtual Systems. The ‘Delete’ is not generally applicable, other than for ‘Force Delete’. Verify that you can do a ‘Force Delete’ using the ‘Delete’ button – this should delete the Virtual System and should not be displayed on OSC after deletion.  (OSC Test needed for the workflow)

### 1.4 SECURITY GROUP, BIND SECURITY GROUP AND TRAFFIC POLICY MAPPINGS
### 1.4.1	Verify that you cannot ‘Add’ a Security Group if the SDN Controller is not configured (OSC Test needed for the workflow)
### 1.4.2	From Setup  Virtualization Connectors, under Security Group section, verify you can ‘Add’ a Security Group, once the SDN Controller is configured. Once added, the Security Group should be displayed under ‘Security Group’ on the Virtualization Connectors page with accurate parameters for – Name, Tenant, Members, Services, Deleted and Last Job Status. The Job status should show PASSED for a successfully created Security Group.
### 1.4.3	Verify you can ‘Add’ a SG with Type VM e.g., Victim as Security Group Member (SGM). The VM should be displayed under Selected Items on the right side table. The Security Group should accurately display – Name, Tenant, Members, Services, Deleted and Last Job status. The Last Job status should be PASSED when the Security Group is successfully added.
### 1.4.4	Bind the Security Group to an Openstack DA. Services column on OSC should be accurately updated with the binded DA. A Sync Job should be triggered which should be PASSED. You should see tasks indicating Creation of Security Group interfaces, and corresponding inspection hooks. Corresponding Traffic Policy Mappings should be created on OSC. Verify Traffic Policy Mapping parameters are accurately displayed on OSC UI – Name, Inspection policy, Tag, User-defined, Security Group, Failure Policy, and Deleted fields are appropriately populated. User-defined should be ‘false’.
### 1.4.5	Unbind the Security Group from the DA.  A Sync Job should be triggered which should be PASSED. You should see tasks indicating Deletion of Security Group interfaces, and removal of corresponding inspection hooks The Corresponding Traffic Policy Mapping should be deleted from the Traffic Policy Mappings page.
### 1.4.6	Bind the Security Group with 2 DAs. The Services column of the Security Group should be appropriately updated. Verify Sync Job is updated and PASSED. <<< This is under the assumption that the SDN supports chaining and you can bind multiple services (or DAs) with the same Security Group >>> P1
### 1.4.7	Verify you can create a SG with a Network as Security Group Member (SGM). The network should be displayed under Selected Items on the right side table. The Security Group should accurately display – Name, Tenant, Members, Services, Deleted and Last Job status. The Last Job status should be PASSED when the Security Group is successfully added.
### 1.4.8	Bind the Security Group to an Openstack DA. Sync Job should be triggered which should be PASSED. You should see tasks indicating Creation of Security Group interfaces, and corresponding inspection hooks. Corresponding Traffic Policy Mappings should be created on OSC. Verify Traffic Policy Mapping parameters are accurately displayed on OSC UI – Name, Inspection policy, Tag, User-defined, Security Group, Failure Policy, and Deleted fields are appropriately populated. User-defined should be ‘false’.
### 1.4.9	Unbind the Security Group from the DA.  A Sync Job should be triggered which should be PASSED. You should see tasks indicating Deletion of Security Group interfaces, and removal of corresponding inspection hooks The Corresponding Traffic Policy Mapping should be deleted from the Traffic Policy Mappings page.
### 1.4.10	Bind the Security Group with 2 DAs. The Services column of the Security Group should be appropriately updated. Verify Sync Job is updated and PASSED. <<< This is under the assumption that the SDN supports chaining and you can bind multiple services (or DAs) with the same Security Group >>> P1
### 1.4.11	Verify you can create a SG with a Subnet of a network as Security Group Member (SGM), Protect External Disabled. The subnet should be displayed under Selected Items on the right side table. The Security Group should accurately display – Name, Tenant, Members, Services, Deleted and Last Job status. The Last Job status should be PASSED when the Security Group is successfully added.
### 1.4.12	Bind the Security Group to an Openstack DA. Sync Job should be triggered which should be PASSED. You should see tasks indicating Creation of Security Group interfaces, and corresponding inspection hooks. Corresponding Traffic Policy Mappings should be created on OSC. Verify Traffic Policy Mapping parameters are accurately displayed on OSC UI – Name, Inspection policy, Tag, User-defined, Security Group, Failure Policy, and Deleted fields are appropriately populated. User-defined should be ‘false’.
### 1.4.13	Unbind the Security Group from the DA.  A Sync Job should be triggered which should be PASSED. You should see tasks indicating Deletion of Security Group interfaces, and removal of corresponding inspection hooks. The Corresponding Traffic Policy Mapping should be deleted from the Traffic Policy Mappings page.
### 1.4.14	Bind the Security Group with 2 DAs. The Services column of the Security Group should be appropriately updated. Verify Sync Job is updated and PASSED. <<< This is under the assumption that the SDN supports chaining and you can bind multiple services (or DAs) with the same Security Group >>> P1
### 1.4.15	Verify ordering with 2 different DAs, binded to the same Security Group which has a VM as Security Group Member. (Basically by attacking this VM and checking which VNF got the packet first – this might be dependent on feature of dummy VNF). Change the order and verify appropriate functionality. <<< We are assuming here that from the dummy VNF that logs the packets it will be easy to see what came first to the VNF >>> P1
### 1.4.16	Verify you can create a SG with a Subnet of a network as Security Group Member (SGM), Protect External Enabled. The subnet should be displayed under Selected Items on the right side table. The Security Group should accurately display – Name, Tenant, Members, Services, Deleted and Last Job status. The Last Job status should be PASSED when the Security Group is successfully added.
### 1.4.17	Bind the Security Group to an Openstack DA. Sync Job should be triggered which should be PASSED. You should see tasks indicating Creation of Security Group interfaces, and corresponding inspection hooks. Subnet ports should be deleted and router ports should be added. Corresponding Traffic Policy Mappings should be created on OSC. Verify Traffic Policy Mapping parameters are accurately displayed on OSC UI – Name, Inspection policy, Tag, User-defined, Security Group, Failure Policy, and Deleted fields are appropriately populated. User-defined should be ‘false’.
### 1.4.18	Unbind the Security Group from the DA.  A Sync Job should be triggered which should be PASSED. You should see tasks indicating Deletion of Security Group interfaces, and removal of corresponding inspection hooks. The Corresponding Traffic Policy Mapping should be deleted from the Traffic Policy Mappings page.
### 1.4.19	Bind the Security Group with 2 DAs. The Services column of the Security Group should be appropriately updated. Verify Sync Job is updated and PASSED. <<< This is under the assumption that the SDN supports chaining and you can bind multiple services (or DAs) with the same Security Group >>> P1
### 1.4.20	Verify ordering with 2 different DAs, binded to the same Security Group which has a VM as Security Group Member (SGM). (Need more info on how this works and how can we test this). Change the order and verify appropriate functionality. <<< Again we are assuming here that from the dummy device that logs the packets it will be easy to see what came first to the VNF >>> P1
### 1.4.21	Verify ordering with 2 different DAs, binded to the same Security Group which has a Network as Security Group Member. (Need more info on how this works and how can we test this). Change the order and verify appropriate functionality. <<< Again we are assuming here that from the dummy device that logs the packets it will be easy to see what came first to the VNF >>> P1
### 1.4.22	Verify ordering with 2 different DAs, binded to the same Security Group which has a network subnet as Security Group Member, with Protect External Disabled. (Need more info on how this works and how can we test this). Change the order and verify appropriate functionality. <<< Again if we are assuming that from the dummy device that logs the packets it will be easy to see what came first to the VNF >>> P1
### 1.4.23	Verify ordering with 2 different DAs, binded to the same Security Group which has a network subnet as Security Group Member, with Protect External Enabled. (Need more info on how this works and how can we test this). Change the order and verify appropriate functionality. <<< Again if we are assuming that from the dummy device that logs the packets it will be easy to see what came first to the VNF >>> P1
### 1.4.24	Change default Inspection policy from the Bind page, and it should be reflected under ‘Inspection Policy’ on Policy Mappings page. The ‘tag’ will not change.
### 1.4.25	Verify default Chaining Failure Policy is FAIL_OPEN by default.
### 1.4.26	If SDN supports it, verify Chaining Failure Policy – FAIL_OPEN. Disconnect the VNF from Openstack by shutdown or power off. Verify that the Victim is still getting the packets. P1
### 1.4.27	If SDN supports it, verify Chaining Failure Policy – FAIL_CLOSE. Disconnect the VNF from Openstack by shutdown or power off. Verify that the Victim is not getting the packets anymore. P1
### 1.4.28	If SDN supports it, verify Chaining – On the same compute nodes have a VNF and Load Balancer (LB). Verify that traffic hops through VNF and Load Balancer. Details TBD.  P1
### 1.4.29	Verify packets redirection and chaining order through tcpdump  (this should be used if we don’t have a dummy VNF that can log the packets and can add its own tag to the packets) P1

### 1.5 USER-DEFINED TRAFFIC POLICY MAPPINGS
### 1.5.1	Verify you can ‘Add’ a Traffic Policy Mapping’ by providing appropriate Name, Policy and Tag. All fields – Name, Inspection policy, Tag, User-Defined, Security Group, Failure Policy and Deleted should be accurately displayed. User-defined should display ‘true’.
### 1.5.2	Verify you can ‘Edit’ the added policy – change Name.  The modified ‘Name’ should be accurately reflected on OSC UI Policy Mappings page.
### 1.5.3	Verify duplicate names are allowed by OSC – (should this be allowed). Add two policy mappings with the same name but different tags. Both policy mappings should be added and displayed on the OSC UI Policy Mappings page.
### 1.5.4	Verify you can ‘Edit’ the added policy – change Policy. The changed ‘Policy’ should be accurately reflected on OSC UI Policy Mappings page.
### 1.5.5	Verify you can ‘Edit’ the added policy – change Tag. The changed ‘Tag’ should be accurately reflected on OSC UI Policy Mappings page.
### 1.5.6	Verify duplicate tags are not allowed by OSC - Add 2 policy mappings with different names and same tag. You should get an error – A Traffic Policy Mapping exists for the specified Virtual System and Tag combination.
### 1.5.7	Verify you can ‘Delete’ the added policy. The deleted policy should disappear from the OSC UI Policy Mappings page.
### 1.5.8	Verify you cannot Edit a Policy Mapping which is not user-defined (Edit is greyed out for a policy which is not user defined).
### 1.5.9	Verify you cannot delete a Policy Mapping which is not user-defined defined (Delete is greyed out for a policy which is not user defined).
### 1.5.10	Verify redirection with expected tag either through tcpdump or dummy VNF to see tag is in the packet
### 1.5.11	Change the Inspection Policy. Verify that changed policy is accurately displayed on the OSC UI Policy Mappings page.
### 1.5.12	Verify that you cannot change the tag for a policy that is not user-defined. Change the Inspection Policy from ‘Default Client and Server’ to ‘Default Client’. The changed policy should be reflected on the OSC UI but tag will not change.

### 1.6 END-TO-END
### 1.6.1	Create a Security Group with ‘Victim’ VM as Security Group Member. Have another VM ‘Attacker’ and attack the ‘Victim’ VM from the ‘Attacker’. Verify that when the SG is binded, the Victim is protected and the attack is prevented (the binded policy is enforced) P1
### 1.6.2	Create a Security Group with ‘Network as Security Group Member. Verify that all network VMS and ports are protected. P1
### 1.6.3	Create a Security Group with ‘Subnet of a Network as Security Group Member. Verify that all subnet VMs and ports are protected. P1
### 1.6.4	Create a Security Group with ‘Subnet of a Network as Security Group Member and Protect External Disabled. Verify that all subnet VMs and ports are protected.
### 1.6.5	Create a Security Group with ‘Subnet of a Network as Security Group Member and Protect External Enabled. Verify that all Router ports are protected.

### 1.7 OFF-BOXING REDIRECTION
### 1.7.1 Have two Compute nodes – C1 and C2. C1 should have the Victim VM in the Security Group. Have a VNF on C2. When you bind the Security Group to a DA/service, you should be able to send traffic to this VNF. This does require an assumption that off-boxing is supported by SDN. P1

### 1.8 SIX-TUPLE
### 1.8.1	If supported by SDN, verify from the OSC API that 6-tuple is supported. The attacker’s information should be revealed with Source IP, Destination IP, Source Port, Destination Port, Protocol and timestamp. P1

### 1.9 NEGATIVE TESTS
### 1.9.1	Verify that you cannot ‘Upload’ an Invalid file for SDN Controller Plugins. E.g., try uploading an IPS file. You should get an error.
### 1.9.2	Verify that you cannot ‘Upload’ an Invalid file for SDN Controller Plugins. E.g., try uploading Server Upgrade Bundle. Get an error.

###	Abbreviations
OSC – Open Security Controller
SDN – Software Defined Network
VNF – Virtualized Network Function
VC – Virtualization Connector
MC – Manager Connector
DA – Distributed Appliance
DAI – Distributed Appliance Instance
DS – Deployment Specification
SG – Security Group
SGM – Security Group Member
VM – Virtual Machine
