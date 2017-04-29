# Deployment Specifications Test Cases

**ID:** DS_1  
**Name:** Deploy valid DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add a DS which has VC, MC, DA associated

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Deployments-Deployment Specifications-Add  
4.Provide DS name e.g. My_DS1  
5.Select Openstack Tenant  
6.Select Openstack default RegionOne  
7.Select Criterion By Host e.g. and enable it  
8.Select Management, Inspection Netwroks of Openstack  
9.Select floatingIP pool of Openstack e.f. ext-net  
10.Keep default Deployment Count 1 and Shared selected  
11.Click OK  

**Expected Result:**
It takes a while and Deployment Specifications with the name My_DS1 should be added. Job Status PASSED. In Openstack, see Instance IPS installed

****

**ID:** DS_2  
**Name:** Delete valid DS  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: delete a DS with Openstack

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, DS has been added but VC Security Group has not been bound

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Deployments-Deployment Specifications-Delete  
4.Click OK to delete DS  

**Expected Result:**  
The DS should be deleted.

****

**ID:** DS_3  
**Name:** Sync valid DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: Sync a deployed DS with Openstack

**Required Initial State:**  
OSC installed and up, OSC has VC, MC, DA added, and Deployment Specification has been deployed

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Deployments-Deployment Specifications-Sync  

**Expected Result:**  
The DS should have Job Status from RUNNING to PASSED

****
