# Deployment Specifications (DS) Test Cases

**ID:** DS_1  
**Name:** Create a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a DS using an OpenStack Host through the OSC UI.

**Required Initial State:**  
OSC has Virtualization Connector (VC), Manager Connector (MC), Service Function (SF) and Distributed Appliance (DA) added.

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliance**->**Deployments**->**Deployment Specifications** for Virtual System->**Add**.  
4. Provide a unique DS name e.g. My-DS1.  
5. Select OpenStack Tenant.  
6. Select OpenStack Region.  
7. Select Criterion By Host and enable it.  
8. Select the Management Network, Inspection Network, and Floating IP Pool.
9. Keep default Deployment Count 1 and 'Shared' selected.  
10. Click **OK**.  

**Expected Result:**
Deployment Specifications with the name My-DS1 should be added. It may take up to 2 mins to see Job Status becomes **PASSED** since in the OpenStack, the appliance instance related to the DS is deployed.  

****

**ID:** DS_2  
**Name:** Delete a DS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can delete an existing DS.

**Required Initial State:**  
OSC has VC, MC, DA and DS added but DA has not been bound to a Security Group.  

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliances**->**Deployments**->**Deployment Specifications** for Virtual System->**Delete**.  
4. Click **OK** to delete DS.  

**Expected Result:**  
The DS should be deleted.

****

**ID:** DS_3  
**Name:** Sync a DS  
**Priority:** Medium  
**Type:** Positive  

**Description:**  
User can sync a deployed DS with OpenStack.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**    
1. Launch OSC web application: ```https://OSC-ip-address```.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliances**->**Deployments**->**Deployment Specifications** for Virtual System->**Sync**.  

**Expected Result:**  
DS Sync job should run and change its status from **RUNNING** to **PASSED**.  

****
