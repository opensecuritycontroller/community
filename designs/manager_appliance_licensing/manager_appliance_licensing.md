# OSC Security Manager Licensing
Currently, we hardcode the license auth code (e.g. PAN plugin) and provide it as bootstrap information. This document describes the proposed changes to receive the license auth code from the user.

## Scope of Security Manager License
- **Manager Connector**: All device groups and device members share the same license
- **Distributed Appliance**: All device group share the same license
- **Deployment Specification (DAI)**: All device members share the same license

## API Changes
The OSC REST API **POST** `/api/server/v1/applianceManagerConnectors` will accept additional field “licenseAuthCode”.

`ApplianceManagerConnectorDto`: Update `ApplianceManagerConnectorDto` to add a new variable `licenseAuthCode` to receive the value from API and UI.

`ApplianceManagerConnector`: Update `ApplianceManagerConnector` to add a new variable/mapped column `licenseAuthCode` to persist the license auth code.

`DeleteSvaServerTask`: Add functionality to delete/deactivate the license before deleting the device.

## SDK Changes

`ManagerDeviceApi`: Update `ManagerDeviceApi` to add a new interface method `boolean isLicenseSupported()`.

## Plugin Changes

`PLUGIN_NAMEDeviceApi`: Implement methods `getLicense()` and `deactivateLicense()` to manage the lifecycle of the license, e.g., In `PANDeviceApi` enhance `getLicense()` and implement `deactivateLicense()`.

## UI Changes

Add and enable a text field on Manager Connector window to accept the license auth code from the user for manager supporting licensing. The user entered value on the UI should be hidden.

![](./images/add_manager_connector.jpg) 

For the manager not supporting licensing, the text field and the label will be hidden.

`AddManagerConnectorWindow`: Update `AddManagerConnectorWindow` to add a new text field `License Auth Code`.

## Database Changes

Update `TABLE APPLIANCE_MANAGER_CONNECTOR` in `Schema` to add a new column `license_auth_code`.

The `license_auth_code` should be hidden field in database table.

## License Upload
Assumption: All device groups and device members share the same license.

UI: User will provide the license auth code in text field `License Auth Code`.

API: User will provide license auth code for `licenseAuthCode` field with body.

## Release License
We need to call Security Manager API to delete/deactivate the license after the device is deleted.

## Open Issues/ Questions
1. What is the PAN license policy?
	-	Same license for all device groups and device member? **Yes**
	-	Same license for a single device group?
	-	Same/different license for each of the device member?

2. If the license for each device member (DAI) is different, how do we accept the license for the DS with more than one count? **N/A**

3. How do we release/manage the license? Is there any API we need to call or the manager handles it? **Yes. PAN has apis to manage the license.**

4. Does the license expire? **N/A**
	- If yes, how do we update the bootstrap information?

5. If the vendor does license bundles for a certain group of device members? **N/A**

6. How do we save the license auth code in OSC database? Do we need any encryption mechanism? **License auth code should be hidden in the database**

## References

[PAN Licensing API](https://www.paloaltonetworks.com/documentation/71/virtualization/virtualization/license-the-vm-series-firewall/licensing-ap)
