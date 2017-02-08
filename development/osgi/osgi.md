# OSC And OSGi  

The Open Security Controller (OSC) application is built using OSGi technology. This allows plugins to be dynamically added to and removed from the OSC application.  This document describes the OSGi principles and some of the basic concepts.

## Introduction

The [OSGi Alliance](www.osgi.org) is an Open Standards organization which defines the specification for the core OSGi framework, and specifications for a variety of useful tools and technologies that can be deployed on top of the OSGi framework. The boundaries between these standards can be easily identified; the OSGi Framework is defined by the OSGi Core Specification, and the additional specifications form separate chapters within the OSGi Compendium and Enterprise specifications.  
As the core part of OSGi technology, the OSGi framework provides a platform for installing, running and managing modular applications. This makes it easy to provide extensions, or to reuse existing functions.

## OSGi Modules
Modules in OSGi are called “bundles”. An OSGi bundle is a Java ARchive (JAR) file with additional metadata in its manifest file. This additional information defines a number of important things: 
* An identifier for the bundle
* A version for the bundle
* A list of versioned API packages provided by the bundle
* A list of API package dependencies required by the bundle

This information ensures that OSGi bundles are self-describing - namely that an OSGi bundle can be introspected to see what it is, what it provides, and what it requires to run.

**AN EXAMPLE OSGI MANIFEST**

```
Manifest-Version: 1.0
Bundle-ManifestVersion: 2
Bundle-SymbolicName: org.osc.example
Bundle-Version: 1.2.3
Export-Package: org.osc.example.api;version="1.0.0"
Import-Package: javax.websocket;version="[2.0,2.1)"
```

An important feature of OSGi’s modularity is that packages contained inside an OSGi bundle are isolated from one another, meaning that multiple copies of a package can exist at runtime, potentially with different versions. Packages which are contained in a bundle but not exported cannot be seen or loaded by other OSGi bundles, providing a strong encapsulation of internal implementation detail.  
Dependencies in OSGi bundles are expressed as imports for Java packages. A package import can only be satisfied by a suitably versioned package export, and the OSGi framework will prevent any code being loaded from a bundle that does not have all of its package imports satisfied. A bundle which has all of its package imports satisfied is said to be **RESOLVED** by the framework. This creates wires which link an OSGi bundle to the other bundles that provide API packages to it.  
The OSGi manifest headers are a vital part of any OSGi bundle, and it is recommended that tools are used to generate and validate them. Authoring a correct OSGi manifest by hand is difficult and error prone as identifying the complete list of API packages used in a bundle is non-trivial.  

## OSGi Services
The modularity provided by the OSGi framework is only one part of the OSGi core specification, another vital part is the OSGi service layer, provided by the OSGi Framework’s Service Registry. OSGi Services provide a dynamic mechanism by which OSGi bundles can share implementation objects even though they are not able to see each other’s implementation packages.  
For example in Java SE applications must use Class.forName, or the ServiceLoader API, to find an implementation of an API. This mechanism uses reflection to find the internal implementation type for the API, and therefore requires that it have a no-argument constructor. The constraints on this type preventing refactoring, and the use of numerous frameworks, in the implementation. These Java SE mechanisms also do not guarantee that the dependencies of the implementation are available, leading to difficulties at startup.  
OSGi services eliminate these issues by placing the responsibility for providing an API implementation on the implementation bundle. Once an implementation bundle has been started, and any of its dynamic runtime dependencies have become available, then it can register its implementation object instance with the service registry. The consuming bundle can then obtain the implementation instance from the service registry, looking it up using the API type.  
An important feature of OSGi services is that they are dynamic, they can be registered and unregistered at runtime. This means that service consumers cannot simply look up a service and expect to find it, they must also be prepared to wait for the service that they need, and to shut down if the service that they are using is unregistered. It is possible to use the OSGi API to do this, however the code to do so can be complex. It is usually preferable to use an injection container, such as Declarative Services, to manage this lifecycle.  

### Consuming OSGi Services
Declarative Services makes it easy to provide an OSGi service, but it also provides an easy to use injection container for consuming other OSGi services.  
The `@Reference` annotation can be applied to a field, or to a setter method, to mark an injection site. The type of the service is inferred from the type of the field, or the type of the object received by the setter method.  
By default Declarative Services references are `mandatory` and `static`. Mandatory means that the component will not be registered as a service or activated until a matching service is available for the reference. Static means that there is no re-injection if the backing service changes, instead the component is destroyed and recreated.  
More complex injection strategies are available, and described in detail in numerous examples. For most plugins, however, a mandatory static reference will provide the simplest and most effective model for using objects from the service registry.  

### Detailed Component Lifecycle
The Declarative Services Component lifecycle is relatively simple. When a component is first detected by the Service Component Runtime (the name for a running Declarative Services implementation) then the component enters the “unsatisfied” state. The component remains in this state until all of its mandatory dependencies are available. Once the component's mandatory dependencies are all available (which may be immediately) then the component moves into the “satisfied” state.  

**LAZY COMPONENTS**
If the component is supposed to be registered as an OSGi service then this will happen immediately when the component becomes satisfied. By default the component will not be activated at this stage, instead an OSGi Service Factory is registered representing the component. The component is only created when it is first retrieved from the service registry. This is known as “lazy activation” and helps to improve startup times, as well as saving resources when components are not in use. When a bundle has finished with a service it can release it - if a Declarative Services Component is released then it becomes eligible for deactivation, moving back from the “active” state to the “satisfied” state. Components which do not offer an OSGi service cannot be lazy, and simply activate immediately when they are satisfied.  
Components can disable lazy activation using the immediate attribute of the `@Component` annotation.
```java
@Component(immediate=true, property=“osc.plugin.name=Example”)
public class ExampleApplianceManager implements ApplianceManagerApi
{
	// ...
}
```

**PROTOTYPE SCOPED COMPONENTS**
Declarative Services Components (and OSGi services in general) are usually singleton instances (i.e. only one instance exists at any given time). The OSGi R6 specification, however added the concept of prototype scoped services. Prototype scoped service instances can be created on demand by clients, and so many may exist simultaneously. This behaviour is required by the OSC SDN plugin API, which has stateful configuration methods built in to the primary API object.  
Declarative Services components can be made prototype scoped using the scope attribute of the `@Component` annotation.

```java
@Component(scope=PROTOTYPE, property=“osc.plugin.name=ExampleSdn”)
public class ExampleSdnController implements SdnControllerApi
{
    // ...
}
```

SDN Controller plugins must be registered as prototype scope services so that the server can obtain and configure an instance for each usage of the plugin. 



## OSGi Repositories
OSGi bundles contain a definitive list of their own dependencies, and cannot be used until those dependencies are satisfied. This completely eliminates the JAR hell associated with Java SE and EE applications, where failures can only be found at runtime, but it can still cause problems at deployment time. When presented with an OSGi bundle, how do we find other bundles suitable for supplying those dependencies?  
In OSGi (as with many other types of software) the place from which you can find and install bundles is called a repository. Repositories can exist in many places, an external repository may be a file server on the internet, or a local repository may be a folder on disk. Crucially the repository must be searchable, which means that it requires an index. 
The index of an OSGi repository may take many forms, but the OSGi standards define a common interchange using XML. This XML defines a series of generic resources, which are typically OSGi bundles. Each resource has a set of Requirements and Capabilities. A repository can be queried using a requirement to find resources with capabilities that can match it. By repeatedly applying this search a complete dependency graph can be built.  
The most common sorts of requirement are for OSGi packages - a requirement in the osgi.wiring.package namespace exists for each package imported by a bundle, and acapability exists for each package exported by a bundle. There are, however, other sorts of requirements and capabilities:  
* The identity of the resource - this capability is provided by all resources, and allows modules to be found in the repository by identity.
* The content of the resource - this capability identifies the type of the resource (e.g. an OSGi bundle) and provides a location from which the bundle can be installed.
* Other types of dependency, such as the requirement for a runtime service, or an OSGi extender.
* The process of using an index to generate a dependency graph is known as resolving. This resolution typically takes into account the capabilities already available in the platform. Once a resolved set has been determined it can be provisioned into the running framework.  

### Gathering Dependencies And Creating a Repository Index
In general an OSC plugin implementation will be delivered as a small number of bundles, possibly even as a single bundle, but the implementation will have dependencies on other libraries and runtime services. It is therefore important to deliver these dependencies alongside the plugin implementation, and to provide an OSGi index so that the installation can be validated by the OSC server before the plugin is deployed. In this example we will use the `bnd-indexer-mavenplugin` to generate the index.  

It is assumed that the plugin binary will be generated in a separate maven project from the plugin bundle(s). This provides maximum flexibility when testing, and ensures that each build project has only one output. In this example we assume that the plugin packaging project has the group id org.osc.example, and the artifact id example-manager-plugin. The packaging type of the project should be pom.  

**THE BND-INDEXER-MAVEN-PLUGIN**

There are two main ways to generate an OSGi index with the bnd-indexer-maven-plugin, both mechanisms involve introspecting the bundle metadata, the main difference is about how the bundles’ download URLs are generated.
A remote index references the bundles in their Maven Repositories using absolute URIs. This means that the user of the index can download and use the index easily, but they will have to download any resources that they want to install from these Maven Repositories. Remote indexes can be very useful for portability, validation, and when only a few bundles from the repository are needed, but they do require that the users have access to the remote locations.  
An alternative to remote indexes are local indexes. Local indexes create an index using a local filesystem directory containing resources, all of the location URIs in the index are relative to this directory. Local indexes therefore must be provided including all of the resources that they index, resulting in a larger up-front artifact. The benefit of a local index, however, is that it can be deployed and used in offline systems. Local indexes are also useful in situations where most, or all, of the resources are likely to be needed at runtime.  
OSC plugins use local indexes contained in the plugin binary. This means that plugins include all of their dependencies and so can be easily deployed from a single uploaded artifact.  

## OSC Plugins And OSGi
The OSC server runs as a set of OSGi bundles in an OSGi framework, and plugins can be added as additional OSGi bundles.  
Plugin instances implement an API defined by the OSC SDK, and provide these implementation objects as OSGi services. Metadata, in the form of OSGi service properties, is used to select a suitable service implementation at runtime for interacting with a particular external resource.  
Finally, to enable plugins to deliver more complex functions, the installable unit for a plugin is a self-contained OSGi repository. This allows for library and runtime dependencies to be provided alongside the core plugin, and installed into the OSC platform as needed.  







