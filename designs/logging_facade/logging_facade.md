# Using SLF4J Logging Facade
Currently, as of [osc-core / 02b8024](https://github.com/opensecuritycontroller/osc-core/commit/02b80247faa29b069d2b6082f2e866a2f71b0f20),
OSC uses the log4j logging framework directly. The goal is to add flexibility by having all thecode reference 
the **slf4j** facade only. Another logging framework may be plugged in by the user.

## Background

The SLF4j facade provides a common API, inluding logging levels: *error*, *warn*, *info* and *debug*. It detects the presence of one of several logging frameworks.

![](./images/concrete-bindings.png)

## Design Changes
All the java code to only import **org.slf4j** packages. All the **.bnd** files likewise. 

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
POC build of the osc-core.

## References
[SLF4j](https://www.slf4j.org/manual.html)
[Logback](https://logback.qos.ch/index.html)