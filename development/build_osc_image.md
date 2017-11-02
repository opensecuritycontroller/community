# Building OSC Images
This document describes how to setup a local build environment to build OSC images. Using OSC build process three types of images can be generated, i.e.: VMDK, QCOW2 and RAW image formats.

## Prerequisites
OSC image is built on Ubuntu Linux Operating system. Java related application in OSC can be compiled using Maven in windows using CYGWIN tool.  Following tools and packages are required and mandatory for OSC image builds.

1. Any Linux OS distribution
2. Java 8
3. Apache Maven 3.3
4. Apache Ant 1.9.X
5. [Access to OSC source code](./repo_access.md)

## Assumptions
This document assumes that user is performing following installation steps on Ubuntu 14.04.04 LTS Linux OS. And examples in this section are with reference to Ubuntu Desktop Linux OS.

## Installation Steps
### 1 : Install Java
Install Java on your system also make sure to installed JDK and JRE both. For example to install Java Development Kit on a local Ubuntu Linux OS. [Visit install Java 8 on Ubuntu](https://tecadmin.net/install-oracle-java-8-ubuntu-via-ppa/).  
Verify Java version and make sure the version is *1.8.xxx*.  
![](./images/java-version.png)
### 2 : Install Apache Maven  
After verifying java version on your system. Download Apache Maven from its official website or use following command to download Apache Maven 3.3.9.  
`$ cd /usr/local`  
`$ wget http://www-eu.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz`  
Now extract downloaded archive using following command.

`$ sudo tar xzf apache-maven-3.3.9-bin.tar.gz`  
`$ sudo ln -s apache-maven-3.3.9 apache-maven`  
### 3 : Install Apache Ant
Make sure you have a Java environment installed before installing  Ant.  
Following command is an example to download Ant on Ubuntu14.04:
```sh
$ sudo apt-get update
$ sudo apt-get install ant
```
Refer to your Linux OS guide on how to download Ant.

### 4 : Setup Environment Variables
#### Maven and Java Path Setup
As you have downloaded pre compiled Apache Maven files on your system, you must set the environments variables by creating new file `apache-maven.sh`.

`$ sudo vi /etc/profile.d/apache-maven.sh`  
And add following content.  
```sh
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export M2_HOME=/usr/local/apache-maven
export MAVEN_HOME=/usr/local/apache-maven
export PATH=${M2_HOME}/bin:${PATH}
```

`$ source /etc/profile.d/apache-maven.sh`

Verify the Maven version and required version should be **3.3**.xxx  
![](./images/mvn-version.png)

#### Maven Proxy Setup
If connecting through a proxy create or modify `~/.m2/settings.xml` providing the proxy settings. 


### 5 :  Create CentOS Schroot Environment
OSC build process requires CentOS chroot environment to generate a VMDK, QCOW2 or a RAW image. This CentOS schroot environment allows the user to run a command or a login shell in a chroot environment.  
The following command `create-centos `should be executed only after all the pre-requisites installations are completed and only once on the build Linux machine.

To create a CentOS schroot environment run following commands:  
`$ cd /local-working-directory/osc-core/osc-server-bom/bin`  
`$ ./create-centos`

### 6 : Build Commands
This section explains all the build command formats required to generate different type of images like VMDK, QCOW2 and RAW images. OSC virtual appliance will be packaged and distributed in OVF format.

Go to osc-core directory  
`$ cd /home/local-working-directory/osc-core/`  

#### Image Formats
##### Generate VMDK Image
`$ ant ovf`  
##### Generate QCOW2 Image
`$ ant ovf -Dimage-format=qcow2-only`
##### Generate both VMDK and QCOW2 Images
`$ ant ovf -Dimage-format=qcow2-vmdk`  
##### Generate RAW Image
`$ ant ovf -Dimage-format=raw-only`

#### Image Location
All images will be copied in following build location

`$ cd /home/local-working-directory/osc-core/BuildXX-XXXXXX`

## Troubleshooting Compilation Errors

### Network Issues
For any ***"network unreachable :"*** issues check the following on build machine:

1. Proxy setting, if the system is behind a proxy.
2. General network issues like ipaddress, mask, gateway and default route.

### Maven Errors
For Maven build related issues, see the [Building and Running OSC](./build_run_osc.md) documentation.  

### Bind tool compilation error
If the command `create-centos` is run prior to all pre-requisites installation following error might occur.  
```  
org.apache.tools.ant.launch.Launcher 
[ERROR] Failed to execute goal biz.aQute.bnd:bnd-export-maven-plugin:3.3.0:export (default) on project osc-export: Default handler for Launcher-Plugin not found i                        n biz.aQute.launcher -> [Help 1] 

```  
Work around for this compile error is execute following command  
```
mkdir -p $HOME/.bnd/default-ws/cnf/cache/3.3.0/bnd-cache/biz.aQute.launcher
wget -O $HOME/.bnd/default-ws/cnf/cache/3.3.0/bnd-cache/biz.aQute.launcher/biz.aQute.launcher-3.3.0.jar  http://central.maven.org/maven2/biz/aQute/bnd/biz.aQute.launcher/3.3.0/biz.aQute.launcher-3.3.0.jar
```

##Limitations
For now OSC build environment requires Ubuntu Linux Operating System.