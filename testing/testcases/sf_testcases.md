# Service Function (SF) Test Cases

**ID:** SF_1  
**Name:** Auto Import an SF  
**Priority:** High  
**Type:** Positive  

**Description:** 
User can import and upload a VNF service function image to OSC.  

**Required Initial State:** 
OSC can contact a VNF image server to upload the file.

**Steps:**   
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Service Function**->**Auto Import**.  
4. Browse the VNF image file e.g. a zip file.  
5. Click **OK** to finish image uploading to the OSC server.  

**Expected Result:**  
Service Version sees Software Version number, Virtulization Type Openstack e.g., Image Name.  

****

**ID:** SF_2  
**Name:** Delete an SF  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing SF.  

**Required Initial State:**  
VNF Image has been uploaded and displayed in OSC UI.  

**Steps:**    
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Service Function**->**Software Version**->**Delete**.  
4. Click **OK** to delete SF.  

**Expected Result:**  
The SF should be deleted.  

****
