# OSC - Plugin Properties
The SDN Controller and Security Manager Plugins have some APIs that provide static information related to the connectors. This information is better represented as properties exposed by the plugins as this will simplify the plugin APIs by making our extension points more clear and less cluttered.  

## Plugin Properties
The plugin properties will be implemented as OSGi service properties, just like the existing property `osc.plugin.name`: 

```java
@Component(property=“osc.plugin.name=Example”)
public class ExampleApplianceManager implements ApplianceManagerApi
{
    // ...
}
```
## API Changes

### Service Properties
The table below lists the APIs being changed and their respective property names and values for the existing plugins:  

**Security Manager** 

| API | Property Name | Notes | NSM | SMC | ISM |
|--------|--------|--------|--------|--------|--------|
| org.osc.sdk.manager.api.ApplianceManagerApi.getName()|  `osc.plugin.name` | Already exists | NSM | SMC | SMP |
| org.osc.sdk.manager.api.ApplianceManagerApi.getVersion() | N/A| Not called by OSC. Could be Deployment-Version from the bar file. It will be removed from the SDK.  | | | |
| org.osc.sdk.manager.api.ApplianceManagerApi.getVendorName() | `osc.plugin.vendor_name` | | MCAFEE| Forcepoint | SAMPLE | 
|  org.osc.sdk.manager.api.ApplianceManagerApi.getServiceName() |  `osc.plugin.manager.nvf_name` | | NG-IPS | NGFW | DPI | 
|  org.osc.sdk.manager.api.ApplianceManagerApi.getNsxServiceName() |  `osc.plugin.manager.external_nvf_name` | |IDS_IPS | FIREWALL | SAMPLE_IPS|
|  org.osc.sdk.manager.api.ApplianceManagerApi.getAuthenticationType() |  `osc.plugin.manager.authentication_type` | Values:  BASIC_AUTH and KEY_AUTH|  BASIC_AUTH| KEY_AUTH| BASIC_AUTH|
|  org.osc.sdk.manager.api.ApplianceManagerApi.getNotificationType() |  `osc.plugin.manager.notification_type` | Values:  TRANSIENT_WEB_SOCKET, CALLBACK_URL or NONE| CALLBACK_URL |  TRANSIENT_WEB_SOCKET |  NONE |
|  org.osc.sdk.manager.api.ApplianceManagerApi.isSecurityGroupSyncSupport() |   `osc.plugin.manager.sync_security_group.enabled` | | false | true | false
|  org.osc.sdk.manager.api.ApplianceManagerApi.isAgentManaged() |  `osc.plugin.manager.device_status.enabled` | | false | false | true |
|  org.osc.sdk.manager.api.ApplianceManagerApi.isPolicyMappingSupported() |  `osc.plugin.manager.policy_mapping.enabled` | | true | true | false |

**SDN Controller**  

| API | Property Name | Notes | NSC |
|--------|--------|--------|--------|
|    org.osc.sdk.controller.api.SdnControllerApi.isOffboxRedirectionSupported()   |  `osc.plugin.sdn.offbox_redirection.enabled`  |  | false |
| org.osc.sdk.controller.api.SdnControllerApi.isServiceFunctionChainingSupported()| `osc.plugin.sdn.service_function_chaining.enabled` | | false |
| org.osc.sdk.controller.api.SdnControllerApi.isFailurePolicySupported()| `osc.plugin.sdn.failure_policy.enabled` | | false |
| org.osc.sdk.controller.api.SdnControllerApi.isUsingProviderCreds()| `osc.plugin.sdn.provider_credentials.required` || true |
| org.osc.sdk.controller.api.SdnControllerApi.isSupportQueryPortInfo()| `osc.plugin.sdn.query_port_info.enabled` || false |
| org.osc.sdk.controller.api.SdnControllerApi.isPortGroupSupported()| `osc.plugin.sdn.port_group.enabled` || false |
|    org.osc.sdk.controller.api.SdnControllerApi.getName()    |   `osc.plugin.name`      | Already exists | NSC |
| org.osc.sdk.controller.api.SdnControllerApi.getVersion() | N/A |Not called by OSC. Could be Deployment-Version from the bar file. It will be removed from the SDK. | N/A

## Database changes
The Virtualization Connector (VC) table will have the following new columns: `offbox_redirection_enabled, service_function_chaining_enabled, failure_policy_enabled, provider_credentials_required, query_port_info_enabled, port_group_enabled`

The Manager Connector (MC) table will have the following new columns: `vendor_name, nvf_name, external_nvf_name, authentication_type, notification_type, sync_security_group_enabled, device_status_enabled, policy_mapping_enabled.`  

During database restore operations if those values dont exist (i.e.: 2.5 to current release) they will be populated with the expected values (see tables above). 

When plugins are uploaded their properties will be populated on the existing database entities, i.e.: if OSC has an MC for NSM with device_status_enabled = false, and the NSM plugin is deleted and uploaded again with device_status_enabled = true, after the plugin upload the MC should be updated with this new value and behave accordingly, in this case provide device member status.  

### Updating Virtualization and Manager Connector Entities
The existing Virtualization Connector and Manager Connector entities will be updated when a plugin of their type is uploaded.  
The existing  `ManagerApiFactory` and `SdnControllerApiFactory` creates trackers that are triggered when new services/plugins are added. At this time these factories will load all their respective connectors through the services  `ListVirtualizationConnectorService` and `ListApplianceManagerConnectorService` and update the connectors of the applicable type using the value of the properties loaded from the services. The updates will happen through the services `UpdateVirtualizationConnectorService` and `UpdateManagerConnectorService`.

## Test Considerations

While this feature does not have much impact on OSC UI and visible functionalities the validation of the plugins management and E2E flows using the various affected plugis is highly important to identify possible regressions. Below are some notes to help planning the test for this work:

* Validate the service manager name on NSX is the same as the one in `osc.plugin.vendor_name` for the respective plugins. 
* Ensure to validate that NSM and SMC are successfully calling OSC when changes happen (i.e.: policy changes)
* Validate that upgrade from 2.5 to current release works. Plugins should be added after the database is restored and the database should contain sufficient data (DAs of different types: VMware, OpenStack, NSM, SMC) and that the connectors (VC, MC) will have the correct values based on the tables above and be fully functional.
* Validate E2E flows using all the plugins mentioned above exerising the relavant settings (usingProviderCreds, isSecurityGroupSyncSupport, etc)
* Validate that removing and adding a plugin with a different value than before will update the respective connector with the new value.  
* Ensure that E2E validations are verified in different systems: NSM, SMC, OSC, OST and VMware VCenter and NSX.










