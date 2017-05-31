# Distributed Appliances Test Cases

**ID:** DA_1  
**Name:** Add valid DA  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add a DA which has VC, MC associated

**Required Initial State:**  
OSC installed and up, OSC has VC, MC created

**Steps:**  
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Add  
4.Provide DA name e.g. My_DA1  
5.Select Manager Connector  
6.Select Service Function  
7.Enable Virtulization System Openstack  
8.Select Encap Type Vlan  
9.Click OK  

**Expected Result:**  
Distributed Appliances with the name My_DA1 should be added. Manager and VNF Model shown, Job Status PASSED.

****

**ID:** DA_2  
**Name:** Delete valid DA  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: delete a DA with Openstack

**Required Initial State:**  
OSC installed and up, OSC has VC, MC created, DA has been added but VC Security Group has not been bound  

**Steps:**   
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Delete  
4.Click OK to delete DA  

**Expected Result:**  
The DA should be deleted.

****

**ID:** DA_3  
**Name:** Force Delete valid DA  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: Force delete a deployed DA with Openstack

**Required Initial State:**  
OSC installed and up, OSC has VC, MC created, DA has been added and Deployment Specification has been deployed, VC Security Group has been bound 

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Distributed Appliances-Delete  
4.Popup confirmation with force selection  
5.Click OK and reconfirm force selection to delete DA  

**Expected Result:**  
The DA should be deleted.

****
