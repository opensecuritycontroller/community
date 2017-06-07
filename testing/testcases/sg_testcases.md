# Security Group (SG) Test Cases

**ID:** SG_1  
**Name:** Add an SG of VM type  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a security group for a host or hosts through OSC UI.  

**Required Initial State:**  
OpenStack is configured with host.

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Add**.  
4. Provide a unique SG name e.g. My_SG1.  
5. Select OpenStack Tenant.  
6. Select OpenStack Region.  
7. Select Type VM.  
8. Move the item from left to the right using the **>** button.  
9. Leave **Protect External** unselected.  
10. Click **OK**.  

**Expected Result:**  
SG with members, services of DA should be shown and Job Status should be **PASSED**.  

****


**ID:** SG_2  
**Name:** Add an SG of Network type  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a security group for a network or networks through OSC UI.  

**Required Initial State:**  
OpenStack is configured with networks.

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Add**.  
4. Provide a unique SG name e.g. My_SG1.  
5. Select OpenStack Tenant.  
6. Select OpenStack Region.  
7. Select Type Network.  
8. Move the item from left to the right using the **>** button.  
9. Leave **Protect External** unselected.   
10. Click **OK**.  

**Expected Result:**  
SG with members, services of DA should be shown and Job Status should be **PASSED**.  

****

**ID:** SG_3  
**Name:** Add an SG of Subnet type   
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a security group for a subnet or subnets through OSC UI.  

**Required Initial State:**  
OpenStack is configured with network and subnet.

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Add**.  
4. Provide a unique SG name e.g. My_SG1.  
5. Select OpenStack Tenant.  
6. Select OpenStack Region.  
7. Select Type Subnet.  
8. Move the item from left to the right using the **>** button.  
9. Leave **Protect External** unselected.   
10. Click **OK**.  

**Expected Result:**  
SG with members, services of DA should be shown and Job Status should be **PASSED**.  

****

**ID:** SG_4  
**Name:** Delete an SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can delete an existing SG.  

**Required Initial State:**  
No specific requirement, may even force-delete an SG.  

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Delete**.  
4. Click **OK** to delete SG.  

**Expected Result:**  
The SG should be deleted.  

****

**ID:** SG_5  
**Name:** Sync an SG  
**Priority:** Medium  
**Type:** Positive  

**Description:**  
User can sync an existing SG.  

**Required Initial State:**  
SG has been added.  

**Steps:**  
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Sync**.  

**Expected Result:**  
The SG should have Job Status from **RUNNING** to **PASSED**.  

****

**ID:** SG_6  
**Name:** Bind an SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can bind an SG with OpenStack DA.

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed.  

**Steps:**  
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Bind**.  
4. Select **Enabled** checkbox.  
5. Click **OK**.  

**Expected Result:**  
The SG should be bound to the DA in Services column and Job Status should be **PASSED**.  

****


**ID:** SG_7  
**Name:** Unbind the SG  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can unbind an existing SG with DA.  

**Required Initial State:**  
OSC has VC, MC, DA added, and Deployment Specification has been deployed and SG bound to the DA.

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connector**->**Security Group**->**Bind**.  
4. De-select **Enabled** checkbox.  
5. Click **OK**.  

**Expected Result:**  
The SG should have Job Status from **RUNNING** to **PASSED**.  

****
