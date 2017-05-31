# Virtualization Connector Test Cases

**ID:** VC_1  
**Name:** Add valid VC  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add an Openstack VC (while open stack uses http)

**Required Initial State:**  
OSC installed and up, OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: https://OSC-ip-address
2. Login OSC
3. OSC-Setup-Virtualization Connectors-Add
4. Type: select OPENSTACK
5. Provide VC name e.g. My_VC1, SDN Type: NONE
6. Fill up Openstack Keystone IP, Tenant, User, Password fields
7. If needed (If Rabbit MQ does not use default settings) click the ‘Show Advanced Settings’ button and put the parameters for Rabbit MQ (https, IP, user name, password, port) and click OK in the ‘Advanced Settings’ dialog
8. Click OK for default settings

**Expected Result:**  
Line with Virtualization Connector with the name My_VC1 should be added. The Type should be Openstack, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status PASSED.

****

**ID:** VC_2  
**Name:** Add valid VC Openstack https  
**Priority:** High  
**Type:** Positive  

**Description:**  
OSC: add an Openstack VC (while Openstack uses https)

**Required Initial State:**  
OSC installed and up, OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: https://OSC-ip-address
2. Login OSC
3. OSC-Setup-Virtualization Connectors-Add
4. Type: select OPENSTACK
5. Provide VC name e.g. My_VC2, SDN Type: NONE
6. Fill up Openstack Keystone IP, Tenant, User, Password fields
7. If needed (If Rabbit MQ does not use default settings) click the ‘Show Advanced Settings’ button and put the parameters for Rabbit MQ (https, IP, user name, password, port) and click OK in the ‘Advanced Settings’ dialog
8. Click OK for default settings

**Expected Result:**  
A dialog ask you to approve SSL Certificates will appear.
Upon completion
Line with Virtualization Connector with the name My_VC2 should be added. The Type should be Openstack, Controller IP should be empty and Provider IP should have the keystone ip according to input at step 6., Job Status PASSED.

****

**ID:** VC_3  
**Name:** Delete valid VC  
**Priority:** High  
**Type:** Negtive  

**Description:**  
OSC: delete an Openstack VC

**Required Initial State:**  
OSC installed and up, OSC can ping the Openstack Controller and Openstack Keystone is Up.

**Steps:**  
1. Launch OSC GUI: https://OSC-ip-address
2. Login OSC
3. OSC-Setup-Virtualization Connectors-Virtualization Connector-Delete
4. Click OK

**Expected Result:**  
The VC should be deleted if no Distributed Appliance is referenced otherwisw it pops up Error.
