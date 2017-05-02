# Deployment Specifications Test Cases

**ID:** DS_1  
**Name:** User can deploy a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
Given an existing service function, manager connector and virtualization connector, distrubuted appliance, the user can add a deployment specifications on OSC.

**Required Initial State:**  
OSC has VC, MC, SF, DA added.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Deployments->Deployment Specifications->Add.  
4. Provide a unique DS name e.g. My_DS1.  
5. Select Openstack Tenant.  
6. Select Openstack default RegionOne.  
7. Select Criterion By Host e.g. and enable it.  
8. Select Management, Inspection Networks.  
9. Select floatingIP pool of Openstack e.f. ext-net.   
10. Keep default Deployment Count 1 and Shared selected.  
11. Click OK.  

**Expected Result:**
It takes a while and Deployment Specifications with the name My_DS1 should be added. Job Status should be PASSED. In Openstack, see Instance IPS installed.  

****

**ID:** DS_2  
**Name:** User can delete a DS  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing DS with Openstack.  

**Required Initial State:**  
OSC has VC, MC, DA added, DS has been added but VC Security Group has not been bound.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Deployments->Deployment Specifications->Delete.  
4. Click OK to delete DS.  

**Expected Result:**  
The DS should be deleted.

****

**ID:** DS_3  
**Name:** User can sync a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can sync a deployed DS with Openstack.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Deployments->Deployment Specifications->Sync.  

**Expected Result:**  
The DS should have Job Status from RUNNING to PASSED.  

****