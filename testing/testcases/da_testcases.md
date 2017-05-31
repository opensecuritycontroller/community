# Distributed Appliances Test Cases

**ID:** DA_1  
**Name:** User can add a DA  
**Priority:** High  
**Type:** Positive  

**Description:**  
Given an existing service function, manager connector and virtualization connector the user can add a distributed appliance on OSC.

**Required Initial State:**  
OSC has VC, MC and SF added.

**Steps:**  
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Add.  
4. Provide a unique DA name e.g. My_DA1.  
5. Select the previously added Manager Connector.  
6. Select the previously added Service Function.  
7. Check Enable for the OpenStack Virtualization System.
8. Select the Manager Domain and Encapsulation Type if applicable.  
9. Click OK.  

**Expected Result:**  
Distributed Appliances with the name My_DA1 should be added. Manager and VNF Model must be shown, Job Status must be PASSED.

****

**ID:** DA_2  
**Name:** User can delete a DA  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing DA.

**Required Initial State:**  
OSC has DA added but VC Security Group has not been bound.  

**Steps:**   
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Delete.  
4. Click OK to delete DA.  

**Expected Result:**  
The DA should be deleted.

****

**ID:** DA_3  
**Name:** User can force delete a SG bound DA.  
**Priority:** High  
**Type:** negative  

**Description:**  
User can force delete a SG bound DA.

**Required Initial State:**  
OSC has the DA added and VC Security Group has been bound with this DA.

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Distributed Appliances->Delete.  
4. Popup confirmation with force selection.  
5. Click OK and reconfirm force selection to delete the DA.  
6. Also go to Openstack to delete the VNF Instance since OSC force delete will not force delete in Openstack.  

**Expected Result:**  
The DA should be deleted.

****