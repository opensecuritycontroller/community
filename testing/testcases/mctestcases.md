# Manager Connector Test Cases

**ID**:MC_1  
**Name**:Add valid MC  
**Priority**:High  
**Type**:Positive  

**Description**: 
OSC: add a VNF (McAfee NSM/SMC e.g.) MC

**Required Initial State**: 
OSC installed and up, OSC can ping the VNF Manager (NSM/SMC e.g.)

**Steps**:  
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Manager Connectors-Add  
4.Type: select NSM e.g.  
5.Provide MC name e.g. My_MC1  
6.Fill up NSM login credential fields  
7.Click OK  

**Expected Result**: 
Line with Manager Connector with the name My_MC1 should be added. IP shown as input at step 6., Job Status PASSED.

****

**ID**:MC_2  
**Name**:Delete valid MC  
**Priority**:High  
**Type**:Negtive  

**Description**: 
OSC: delete an Openstack MC

**Required Initial State**: 
OSC installed and up, MC to VNF Manager (NSM/SMC e.g.) has been created

**Steps**:  
1.Launch OSC GUI: https://OSC-ip-address  
2.Login OSC  
3.OSC-Setup-Manager Connectors-Delete  
4.Click OK for default settings  

**Expected Result**: 
The MC should be deleted.

****
