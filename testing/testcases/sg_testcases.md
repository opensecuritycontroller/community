# Security Group Test Cases

**ID:** SG_1  
**Name:** User can add a SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
Given an existing service function, manager connector and virtualization connector, distributed appliance, user can add a secirity group for hosts or networks.  

**Required Initial State:**  
OSC has VC, MC, DA, DS added.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Add.  
4. Provide an unique SG name e.g. My_SG1.  
5. Select Openstack Tenant.  
6. Select Openstack default RegionOne.  
7. Select By Type VM or Network or Subnet.  
8. Move the item from left to the right.  
9. Leave Protect External unselected or select.  
10. Click OK.  

**Expected Result:**  
SG with members, services of DA should be shown and Job Status should be PASSED.  

****

**ID:** SG_2  
**Name:** User can delete a SG  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing SG which has VC, MC, DA, DS associated.  

**Required Initial State:**  
OSC has VC, MC, DA added, SG has been added but VC Security Group has not been bound, SG line with Services box empty.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Delete.  
4. Click OK to delete SG.  

**Expected Result:**  
The SG should be deleted.  

****

**ID:** SG_3  
**Name:** User can sync a SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can sync an existing SG.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**  
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Sync.  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED.  

****

**ID:** SG_4  
**Name:** User can bind a SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can bind a SG with Openstack DAI

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**  
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Bind.  
4. Enable Openstack DA service with Inspection Policy selected.  
5. Click OK.  

**Expected Result:**  
The SG should be bound to the DA in Services column and Job Status should be PASSED.  

****


**ID:** SG_5  
**Name:** User can unbind the SG  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can nbind an existing SG with DA.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Bind.  
4. Disable Openstack DA service.  
5. Click OK.  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED.  

****