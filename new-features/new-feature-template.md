# New Feature Proposal Template
Provide a short single paragraph description for the feature. 

## Assignees
Provide the names and GitHub handles of the contributors driving the implementation of this feature.

## Background
Provide any additional background for the feature. I.e.: user scenarios, business value, etc.

## Constraints and Assumptions
Call out any constraint and/or assumption relevant for the development and use of this feature. 

## Design Changes
Provide a high level description of the design highlighting the impacted OSC components, i.e.: REST API, data entities, SDKs, etc. 
> Note: Using a high level design diagram and/or sequence diagrams in this section can be helpful.

### REST API 
Describe in details any changes to the OSC REST APIs. This should include any new, modified or removed API and describing their payloads, headers and response status.
> Note: Using the [swagger specification](#swagger-specification) is highly recommended.

### OSC SDKs

#### VNF Security Manager SDK
Describe the API changes to be made in the VNF security manager SDK. 

#### SDN Controller SDK
Describe the API changes to be made in the SDN Controller SDK. 

### XYZ Integration Point
This section is meant to describe any other new integration point added to OSC.

### OSC Entities 
Describe any changes to the OSC database schema.

### OSC UI
Use UI mock ups to describe any UI change.

### OSC Synchronization Tasks
Describe any changes on the OSC internal synchronization tasks or metatasks. Use a diagram to represent any updated or new task graph.

## Tests
Describe here any new test requirement for this feature. This can include: virtualization platform, test infrastructure, stubs, etc. 
> Note: Any feature should be demonstrable and testable independently of a particular vendor component or service. 

## References
### [Swagger Specification](http://swagger.io/specification/)


