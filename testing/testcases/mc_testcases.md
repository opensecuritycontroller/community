# Manager Connector (MC) Test Cases

**ID**: MC_1  
**Name**: Add an MC  
**Priority**: High  
**Type**: Positive  

**Description**: 
User can add an MC.

**Required Initial State**: 
The security manager endpoint is reachable by OSC.
Manager Plugin has been uploaded.

**Steps**:  
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Manager Connectors**->**Add**.  
4. Select the Manager **Type** corresponding to the plugin you are using.
5. Provide a unique MC name e.g. My_MC1.  
6. Fill in the Manager login credential fields.  
7. Click **OK**.  

**Expected Result**: 
Manager Connector with the name My_MC1 should be added. IP should be shown as input at step 6, Job Status should be **PASSED**.
If this Manager type supports Policy Syncing - you will be able to see its Policies in UI.

****

**ID**: MC_2   
**Name**: Delete an MC  
**Priority**: High  
**Type**: Positive  

**Description**: 
User can delete an existing MC.

**Required Initial State**: 
MC has been added.

**Steps**:  
1. Launch OSC web application: `https://OSC-ip-address`.  
2. Login to OSC.  
3. Click **Setup**->**Manager Connectors**->**Delete**.  
4. Click **OK**.  

**Expected Result**: 
The MC should be deleted.

****
