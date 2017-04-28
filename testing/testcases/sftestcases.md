# Service Function Test Cases

**ID:** SF_1  
**Name:** Auto Import valid SF  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add a VNF service function image e.g. IPS

**Required Initial State:** 
OSC installed and up, OSC can browse a VNF image, IPS e.g.

**Steps:**   
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Service Function-Auto Import  
4.Browse the VNF image file e.g. IPS sensorsw_vm100-vss_8310019.zip  
5.Click OK to finish image upload to OSC server  

**Expected Result:**  
Service Version saw Software Version number, Virtulization Type Openstack e.g., Image Name

****

**ID:** SF_2  
**Name:** Delete valid SF  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: delete an Openstack SF

**Required Initial State:**  
OSC installed and up, OSC can ping the VNF Manager (NSM/SSF e.g.)

**Steps:**    
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Service FUnction-Software Version-Delete  
4.If DA is referenced, OSC pops-up error to block   deleting SF  
5.If no DA referenced, click OK to delete SF  

**Expected Result:**  
The SF should be deleted

****
