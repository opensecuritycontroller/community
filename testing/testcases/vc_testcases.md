# Virtualization Connector (VC) Test Cases

**ID:** VC_1  
**Name:** Add a VC  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add an OpenStack VC (while OpenStack uses HTTP).

**Required Initial State:**  
OSC can ping the OpenStack Controller and OpenStack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connectors**->**Add**.  
4. Type: select OPENSTACK.  
5. Provide VC name e.g. My_VC1, SDN Type: NONE.  
6. Fill OpenStack Keystone IP, Tenant, User, Password fields.  
7. (optional). If Rabbit MQ does not use default settings, click **Show Advanced Settings** and fill in all RabbitMQ fields and click **OK**. 
8. Click **OK**.  

**Expected Result:**  
Virtualization Connector with the name My_VC1 should be added. The Type should be OPENSTACK, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status should be ****PASSED**.

****

**ID:** VC_2  
**Name:** Add a VC OpenStack using HTTPS  
**Priority:** High  
**Type:** Positive  

**Description:**  
User can add an OpenStack VC (while OpenStack uses HTTPS)

**Required Initial State:**  
OSC can ping the OpenStack Controller and OpenStack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connectors**->**Add**.  
4. Type: select OPENSTACK.  
5. Provide VC name e.g. My_VC2, SDN Type: NONE.  
6. Fill OpenStack Keystone IP, Tenant, User, Password fields.  
7. Click the **Show Advanced Settings** button, select Https checkbox and fill in all RabbitMQ fields and click **OK**.
8. Click **OK**.

**Expected Result:**  
A dialog asks you to approve SSL Certificates will appear. Upon completion, the
line with Virtualization Connector with the name My_VC2 should be added. The Type should be OPENSTACK, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status should be **PASSED**.

****

**ID:** VC_3  
**Name:** Delete a VC  
**Priority:** High  
**Type:** Negative  

**Description:**  
User can delete an existing OpenStack VC.  

**Required Initial State:**  
OSC can ping the OpenStack Controller and OpenStack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Virtualization Connectors**->**Virtualization Connector**->**Delete**.  
4. Click **OK**.  

**Expected Result:**  
The VC should be deleted if no Distributed Appliance is referenced, otherwise it pops up Error.  
