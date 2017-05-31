# Virtualization Connector (VC) Test Cases

**ID:** VC_1  
**Name:** Add a VC  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add an Openstack VC (while open stack uses http).

**Required Initial State:**  
OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Virtualization Connectors**->**Add**.  
4. Type: select OPENSTACK.  
5. Provide VC name e.g. My_VC1, SDN Type: NONE.  
6. Fill up Openstack Keystone IP, Tenant, User, Password fields.  
7. If needed (If Rabbit MQ does not use default settings) click the ‘**Show Advanced Settings**’ button and put the parameters for Rabbit MQ (https, IP, user name, password, port) and click **OK** in the ‘Show Advanced Settings’ dialog.  
8. Click **OK**.  

**Expected Result:**  
Virtualization Connector with the name My_VC1 should be added. The Type should be Openstack, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status should be PASSED.

****

**ID:** VC_2  
**Name:** Add a VC Openstack using https  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add an Openstack VC (while Openstack uses https)

**Required Initial State:**  
OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Virtualization Connectors**->**Add**.  
4. Type: select OPENSTACK.  
5. Provide VC name e.g. My_VC2, SDN Type: NONE.  
6. Fill up Openstack Keystone IP, Tenant, User, Password fields.  
7. Click the ‘**Show Advanced Settings**’ button, select Https box and put the parameters for Rabbit MQ (IP, user name, password, port) and click **OK** in the ‘Advanced Settings’ dialog.  
8. Click **OK**.  

**Expected Result:**  
A dialog asks you to approve SSL Certificates will appear. Upon completion, the
line with Virtualization Connector with the name My_VC2 should be added. The Type should be Openstack, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status should be PASSED.

****

**ID:** VC_3  
**Name:** Delete a VC  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing Openstack VC.  

**Required Initial State:**  
OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click OSC->**Setup**->**Virtualization Connectors**->**Virtualization Connector**->**Delete**.  
4. Click **OK**.  

**Expected Result:**  
The VC should be deleted if no Distributed Appliance is referenced, otherwise it pops up Error.  
