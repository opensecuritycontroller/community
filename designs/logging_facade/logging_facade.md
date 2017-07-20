# Using SLF4J Logging Facade
Currently, as of [osc-core / 02b8024](https://github.com/opensecuritycontroller/osc-core/commit/02b80247faa29b069d2b6082f2e866a2f71b0f20),
OSC uses the log4j logging framework directly. The goal is to add flexibility by having all the code reference 
the **slf4j** facade only. Another logging framework may be plugged in by the user.

## Background

The SLF4j facade provides a common API, inluding logging levels: **error**, **warn**, **info**, **debug** and (since 1.4.0) **trace**. It detects the presence of one of several logging frameworks and uses it. 

## Design Changes
All the java code to only import **org.slf4j** packages. All the **.bnd** files -- likewise. 

## Logging framework options

Several logging frameworks have been considered to use with slf4j.
	- **log4j** version 2 -- very common and is currently used by most of the project directly.
	- **logback** -- [faster and more robust](https://logback.qos.ch/reasonsToSwitch.html) than log4j.
	- **jacarta commons logging (jcl)** -- according to the [slf4j](https://www.slf4j.org/manual.html) documentation, buggy and not entirely reliable.
	- **simple** -- according to the [slf4j](https://www.slf4j.org/manual.html) documentation, buggy and not entirely reliable.

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
POC build of the osc-core.

## References
[SLF4j](https://www.slf4j.org/manual.html)
[Logback](https://logback.qos.ch/index.html)
[Java Logging Dead](http://blog.takipi.com/is-standard-java-logging-dead-log4j-vs-log4j2-vs-logback-vs-java-util-logging/)
