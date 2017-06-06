# Distributed Appliance (DA) Test Cases

**ID:** DA_1  
**Name:** Add a DA  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add a DA through OSC UI.

**Required Initial State:**  
OSC has Virtualization Connector (VC), Manager Connector (MC), and Service Function (SF) added.

**Steps:**  
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliance**->**Add**.  
4. Provide a unique DA name e.g. My-DA1. (Start with a letter, 13 chars max, alphanumeric and dash '-' only)
5. Select the previously added Manager Connector.  
6. Select the previously added Service Function.  
7. Check **Enable** for the OpenStack Virtualization System.
8. Select the Manager Domain and Encapsulation Type if applicable.  
9. Click **OK**.  

**Expected Result:**  
Distributed Appliance with the name My-DA1 should be added. Manager and VNF Model must be shown, Job Status must be **PASSED**.

****

**ID:** DA_2  
**Name:** Delete a DA  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can delete an existing DA.

**Required Initial State:**  
OSC has DA added, but the DA isn't bound to any Security Group (SG).  

**Steps:**   
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliance**->**Delete**.  
4. Click **OK** to delete DA.  

**Expected Result:**  
The DA should be deleted.

****

**ID:** DA_3  
**Name:** Force delete a DA which has been bound to SG.  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can force delete a DA which has SG bound.

**Required Initial State:**  
OSC has a DA added and bound to a Security Group (SG).

**Steps:**   
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Distributed Appliance**->**Delete**.  
4. Popup confirmation with force delete selection.  
5. Click **OK** and reconfirm force delete selection to delete the DA.   

**Expected Result:**  
The DA should be deleted.  
**Note**: Also ensure to delete the VNF instance on OpenStack since forcing deleting a DA on OSC will not delete the deployed instance.

****
