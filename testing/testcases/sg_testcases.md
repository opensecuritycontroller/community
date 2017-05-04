# Security Group (SG) Test Cases

**ID:** SG_1  
**Name:** Add a SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a secirity group for hosts or networks in Openstack.  

**Required Initial State:**  
OSC has Virtualization Connector (VC), Manager Connector (MC), Service Function (SF) and Distrubuted Appliance (DA) added and Deployment Specification (DS) deployed.

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
**Name:** Delete a SG  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing SG which has VC, MC, DA, DS associated.  

**Required Initial State:**  
OSC has VC, MC, DA added, SG has been added but SG has not been bound to the DA, SG line has Services column empty.  

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
**Name:** Bind a SG  
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
4. Select Enabled column.  
5. Click OK.  

**Expected Result:**  
The SG should be bound to the DA in Services column and Job Status should be PASSED.  

****


**ID:** SG_5  
**Name:** Unbind the SG  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can unbind an existing SG with DA.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed and SG bound to the DA.

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Virtualization Connector->Security Group->Bind.  
4. De-select Enabled column.  
5. Click OK.  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED.  

****
