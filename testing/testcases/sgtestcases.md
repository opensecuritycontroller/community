# Security Group Test Cases

**ID:** SG_1  
**Name:** Add valid SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add a SG which has VC, MC, DA, DS associated

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA, DS added

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Virtualization Connector-Security Group-Add  
4.Provide SG name e.g. My_SG1  
5.Select Openstack Tenant  
6.Select Openstack default RegionOne  
7.Select By Type VM/Network/Subnet  
8.Move the item from left to the right  
9.Leave Protect External unselected or select  
10.Click OK  

**Expected Result:**  
SG with members, services of DA shown and Job Status PASSED

****

**ID:** SG_2  
**Name:** Delete valid SG  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: Delete a SG which has VC, MC, DA, DS associated

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, SG has been added but VC Security Group has not been bound, SG line with Services box empty

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Virtualization Connector-Security Group-Delete  
4.Click OK to delete SG  

**Expected Result:**  
The SG should be deleted.

****

**ID:** SG_3  
**Name:** Sync valid SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: Sync a deployed SG with Openstack

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, and Deployment Specification has been deployed

**Steps:**  
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Virtualization Connector-Security Group-Sync  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED

****

**ID:** SG_4  
**Name:** Bind valid SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: Bind a SG with Openstack DAI

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, and Deployment Specification has been deployed

**Steps:**  
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Virtualization Connector-Security Group-Bind  
4.Enable Openstack DA service with Inspection Policy selected  
5.Click OK  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED

****


**ID:** SG_5  
**Name:** Unbind the valid SG  
**Priority:** High  
**Type:** Negative  

**Description:**  
OSC: Unbind a SG with Openstack DAI

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, and Deployment Specification has been deployed

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Virtualization Connector-Security Group-Bind  
4.Disable Openstack DA service with Inspection   Policy selected
5.Click OK  

**Expected Result:**  
The SG should have Job Status from RUNNING to PASSED

****
