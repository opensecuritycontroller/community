# Manager Connector (MC) Test Cases

**ID**: MC_1  
**Name**: Add a MC  
**Priority**: High  
**Type**: Positive  

**Description**: 
User can add a VNF (McAfee NSM e.g.) MC.

**Required Initial State**: 
OSC can ping the VNF Manager (NSM e.g.).

**Steps**:  
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Manager Connectors->Add.  
4. Type: select NSM e.g.  
5. Provide a unique MC name e.g. My_MC1.  
6. Fill up NSM login credential fields.  
7. Click OK.  

**Expected Result**: 
Manager Connector with the name My_MC1 should be added. IP should be shown as input at step 6., Job Status should be PASSED.

****

**ID**: MC_2 
**Name**: Delete a MC  
**Priority**: High  
**Type**: Negative  

**Description**: 
User can delete an existing MC.

**Required Initial State**: 
MC to VNF Manager (NSM e.g.) has been added.

**Steps**:  
1. Launch OSC web application: https://OSC-ip-address.  
2. Login to OSC.  
3. Click OSC->Setup->Manager Connectors->Delete.  
4. Click OK.  

**Expected Result**: 
The MC should be deleted.

****
