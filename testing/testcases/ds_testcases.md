# Deployment Specifications (DS) Test Cases

**ID:** DS_1  
**Name:** Deploy a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a DS through OSC UI.

**Required Initial State:**  
OSC has Virtualization Connector (VC), Manager Connector (MC), Service Function (SF) and Distributed Appliance (DA) added.
In the Openstack environment, user must have at least one host, and three networks for Management, Inspection and Floating IP Pool.

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Distributed Appliance**->**Deployments**->**Deployment Specifications** for Virtual System->**Add**.  
4. Provide a unique DS name e.g. My-DS1.  
5. Select Openstack Tenant.  
6. Select Openstack Region.  
7. Select Criterion By Host e.g. and enable it.  
8. Select Management, Inspection Networks.  
9. Select FloatingIP pool of Openstack e.g. ext-net.   
10. Keep default Deployment Count 1 and 'Shared' selected.  
11. Click **OK**.  

**Expected Result:**
It takes a while and Deployment Specifications with the name My-DS1 should be added. Job Status should be PASSED. In Openstack, the  appliance instance related to the DS should be deployed.  

****

**ID:** DS_2  
**Name:** Delete a DS  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing DS.

**Required Initial State:**  
OSC has VC, MC, DA and DS added but DA has not been bound to a Security Group.  

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Distributed Appliances**->**Deployments**->**Deployment Specifications** for Virtual System->**Delete**.  
4. Click **OK** to delete DS.  

**Expected Result:**  
The DS should be deleted.

****

**ID:** DS_3  
**Name:** Sync a DS  
**Priority:** Medium  
**Type:** Positive  

**Description:**  
User can sync a deployed DS with Openstack.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Distributed Appliances**->**Deployments**->**Deployment Specifications** for Virtual System->**Sync**.  

**Expected Result:**  
DS Sync job should run and change its status from RUNNING to PASSED.  

****
