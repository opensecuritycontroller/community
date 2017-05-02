# Service Function Test Cases

**ID:** SF_1  
**Name:** User can Auto Import a SF  
**Priority:** High 
**Type:** Positive  

**Description:** 
User can upload a VNF service function image e.g. IPS to OSC.  

**Required Initial State:** 
OSC can contact a VNF image server to upload the file, IPS e.g.

**Steps:**   
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Service Function->Auto Import.  
4. Browse the VNF image file e.g. IPS sensorsw_vm100->vss_8310019.zip.  
5. Click OK to finish image uploading to the OSC server.  

**Expected Result:**  
Service Version sees Software Version number, Virtulization Type Openstack e.g., Image Name.  

****

**ID:** SF_2  
**Name:** User can delete a SF  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing SF.  

**Required Initial State:**  
OSC can contact the VNF Image server (IPS/NGFW e.g.).  

**Steps:**    
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Service Function->Software Version->Delete.  
4. Click OK to delete SF.  

**Expected Result:**  
The SF should be deleted.  

****
