# Deployment Specifications (DS) Test Cases

**ID:** DS_1  
**Name:** Deploy a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a DS on OSC.

**Required Initial State:**  
OSC has Virtualization Connector (VC), Manager Connector (MC), Service Function (SF) and Distrubuted Appliance (DA) added.

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliance->Deployments->Deployment Specifications for Virtual System->Add.  
4. Provide a unique DS name e.g. My-DS1.  
5. Select Openstack Tenant.  
6. Select Openstack default RegionOne.  
7. Select Criterion By Host e.g. and enable it.  
8. Select Management, Inspection Networks.  
9. Select FloatingIP pool of Openstack e.g. ext-net.   
10. Keep default Deployment Count 1 and 'Shared' selected.  
11. Click OK.  

**Expected Result:**
It takes a while and Deployment Specifications with the name My-DS1 should be added. Job Status should be PASSED. In Openstack, see the Instance IPS installed.  

****

**ID:** DS_2  
**Name:** Delete a DS  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing DS with Openstack.  

**Required Initial State:**  
OSC has VC, MC, DA and DS added but DA has not been bound with the Security Group.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Deployments->Deployment Specifications for Virtual System->Delete.  
4. Click OK to delete DS.  

**Expected Result:**  
The DS should be deleted.

****

**ID:** DS_3  
**Name:** Sync a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can sync a deployed DS with Openstack.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Deployments->Deployment Specifications for Virtual System->Sync.  

**Expected Result:**  
The DS should have Job Status from RUNNING to PASSED.  

****
