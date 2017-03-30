# OSC Security Manager Licensing
Currently, we hardcode the license auth code (e.g. PAN plugin) and provide it as bootstrap information. This document describes the proposed changes to receive the license auth code as a one of the custom property from the user.

## Scope of Security Manager License
- **Manager Connector**: All device groups and device members share the same license
- **Distributed Appliance**: All device group share the same license
- **Deployment Specification (DAI)**: All device members share the same license

## API and OSC Server Changes
The OSC REST API **POST** `/api/server/v1/applianceManagerConnectors` will accept a map of custom properties.

`ApplianceManagerConnectorDto`: The `ApplianceManagerConnectorDto` will have a new map of custom properties to accept value from API and UI.

`ApplianceManagerConnector`: The `ApplianceManagerConnector` will have a new map of custom properties.

## SDK Changes

`ApplianceManagerApi`: The api `List<String> getCustomPropertyNames()` will return the list of property names. If you do not require any custom properties, you need to return null. The custom propery names will be used on UI as label. For license auth code, we expect `License Auth Code` as a label.

`ApplianceManagerConnectorElement`: The api `HashMap<String, String> getCustomProperties()` will return the custom properties.


## Plugin Changes

Plugin authors implementing `ApplianceManagerApi` needs to implement functionality to get the custom properties names.

Plugin authors also need to implement functionality:
- To get the license when creating a device member. If the license is not valid, we expect plugin to return valid error message.
- To delete the license when deleting a device member.

## UI Changes

The `AddManagerConnectorWindow` will have a text field with label `License Auth Code` to accept the license auth code from the user for manager supporting licensing. The user entered value on the UI should be hidden.

![](./images/add_manager_connector.JPG)

For the manager not supporting licensing, the text field and the label will be not be present.

## Database Changes

The `TABLE APPLIANCE_MANAGER_CONNECTOR_ATTR` in `Schema` will hold a map of custom properties.

The license auth code value should be hidden in database table.

## License Upload
Assumption: All device groups and device members share the same license.

UI: The user will provide the license auth code in text field `License Auth Code`.

API: The user will provide a map of custom properties with values in body.

## Release License
Plugin author needs to call Security Manager API to delete/deactivate the license after the device is deleted.

## Enhancement
The api `List<String> getCustomPropertyNames()` can contain the list of objects with different properties, e.g, property name, type, isRequired etc.

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

[PAN Licensing API](https://www.paloaltonetworks.com/documentation/71/virtualization/virtualization/license-the-vm-series-firewall/licensing-api)
