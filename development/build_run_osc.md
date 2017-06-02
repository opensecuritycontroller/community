# Building and Running OSC

## Prerequisites

### Known Maven Compile Error and Fix
Before building or running, navigate to the `org.osc.export` project and open the `server.bndrun` file as shown below.

Due to a bug in the bnd-export-maven-plugin, the following step is required before the first command-line build can succeed. This step is required until an expected resolution occurs.

![](images/server_bndrun.JPG)

The following error from the command-line build displays if this step is skipped:

![](images/error_cli.png)

### Setup wget on Windows
Building OSC from the command line depends on wget. If you are using Windows, download and install wget according to your system configuration and requirements.
Version of wget preferred is shown below:  
![](images/wget-version.png)
#### Proxy Setup for wget
If your local machines is behind a proxy, setup `HTTP_PROXY` and `HTTPS_PROXY` environment variables in Windows operating system.

## Command Line
### Building
Once the code is checked out, you can navigate to the folder osc-core and run:
```sh
$ mvn clean install
```

![](images/cli_build.JPG)

### Running
Run vmidc.sh script to start the server or 'vmidc.sh –console' to launch the server in the foreground.
```sh
$ vmidc.sh –console
```

## Eclipse
### Building

To create a proper maven build, complete the following:

Eclipse -> Run -> Run Configurations -> Maven Build

![](images/clean_install.jpg)

### Running

To launch the OSC server in Eclipse, complete the following:

- Ensure you have a full maven build of osc-core from [the command line](#building).
- Navigate to `org.osc.export` project in Eclipse, and then open `server.bndrun`
- Click **Run OSGi**. This launches the OSC server in Eclipse, as shown below.
- You can now browse to [https://localhost](https://localhost).

![](images/running_osgi.png)
