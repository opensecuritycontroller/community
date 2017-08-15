# Using SLF4J Logging Facade
Currently, as of [osc-core / 02b8024](https://github.com/opensecuritycontroller/osc-core/commit/02b80247faa29b069d2b6082f2e866a2f71b0f20),
OSC uses the log4j logging framework directly. The goal is to add flexibility by having all the code reference 
the **slf4j** facade only. Another logging framework may be plugged in by the user.

## Background

The SLF4j facade provides a common API, inluding logging levels: **error**, **warn**, **info**, **debug** and (since 1.4.0) **trace**. It detects the presence of one of several logging frameworks and uses it. 

We want to use be able to use it throughout the project because:
- We shall then be able to easily replace the logging framework behind the facade.
- The implementation log4j, version 1.2, currently used, is obsolete.
- A specific requirement is that plugin implementations be able to use our slf4j log configuration without any dependence on any of our packages. 

## Design Changes
- All the java code to only import **org.slf4j** packages. All the **.bnd** files -- likewise. 
- The only project dependent on some concrete slf4j implementation framework is **osc-server**.
  - The dependencies added to pom.xml: **slf4j-api** plus some implementation dependency. (**slf4j-log4j12**, **logback**, etc.)
  - The **LogUtil.initLogging()** function is modified to initialize the logging framework and register with the context.
  - **bnd.bnd**: Provide-Capability: osgi.service;objectClass=org.slf4j.ILoggerFactory
  - Other bundles (**osc-ui** or plugins) have to implement their own *@Component*s to obtain the *ILoggerFactory* implementation from the OSGi framework and deliver it to the non-OSGi classes.
  
![](./images/diag_logging.png)

## Logging framework options

Several logging frameworks have been considered to use with slf4j. 
- **logback** -- [More robust](https://logback.qos.ch/reasonsToSwitch.html) than log4j2. Considered the best option so far.
  - Groovy or XML configuration.
  - Log rotation and compression.
  - Well tested.
  
- **log4j2** version 2 -- very common and is currently used by most of the project directly. Considered second best.
  - XML, YAML or JSON configuration.

- **log4j** -- Not actively maintained, though it significantly [outperforms](http://blog.takipi.com/the-logging-olympics-a-race-between-todays-top-5-logging-frameworks/) its successor, according to some benchmarks.

- **jacarta.commons.logging (jcl)** -- according to the [slf4j](https://www.slf4j.org/manual.html) documentation, buggy and not entirely reliable.

- **java.util.logging (jul)** -- level naming not compatible with the others. Also, it is [rather unpopular](http://blog.takipi.com/is-standard-java-logging-dead-log4j-vs-log4j2-vs-logback-vs-java-util-logging/).

- **slf4j-simple** -- according to the [slf4j](https://www.slf4j.org/manual.html) this one is suitable for smaller projects. Only one "appender," fewer features.


![](./images/concrete-bindings.png)

### REST API 
N/A.

### OSC SDKs
Make sure there are no explicit references to log4j, etc.

#### VNF Security Manager SDK
Make sure there are no explicit references to log4j, etc.

#### SDN Controller SDK
Make sure there are no explicit references to log4j, etc.

### OSC Entities 
N/A.

### OSC UI
N/A.

### OSC Synchronization Tasks
N/A.

## Tests
POC build of the osc-core project.

## References
[SLF4j](https://www.slf4j.org/manual.html)

[Logback](https://logback.qos.ch/index.html)

[Java Logging Dead](http://blog.takipi.com/is-standard-java-logging-dead-log4j-vs-log4j2-vs-logback-vs-java-util-logging/)

[Logging Olympics](http://blog.takipi.com/the-logging-olympics-a-race-between-todays-top-5-logging-frameworks/)

[Chainsaw](https://logging.apache.org/chainsaw/)
