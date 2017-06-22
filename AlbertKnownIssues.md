**Issue:**
After upload plugins, UI does not do screen refresh to see the result.  
**Work around:**  
Manually do a refresh from the browser F5.  
****

**Issue:**
Adding MC validation for wrong Ip or wrong user name-password needs dialogue before error message. Right now it pops up red error: **no route to the host**.  
**Expected Result:**  
A white dialogue with reported error, possible reasons, question if the user is sure to continue.  
**Work around:**  
Make sure entries are accurate or double check on errors.
****

**Issue:**
VNF SMC Security Group **Bind/unBind** got failed with Null Exception, a plugin issue filed in github.  
****

**Issue:**
OSC api-doc web page saw dummy red **ERROR {...}.**: Can't read swagger.json.  
****

**Issue:**
User can install Manager plugins from SDN plugin pane, and it shows up in Manager plugins State: INSTALL_WAIT.  
**Work around:**  
Make sure upload SDN plugins in **SDN Plugins** pane and upload Manager plugins in **Manager Plugins** pane.  
****

**Issue:**
Uploading an invalid plugin (e.g. a missing properties plugin) did not display an appropriate error message.  
**Work around:**  
Do not upload an invalid plugin file.  
****
