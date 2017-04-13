# Building and Running OSC

**IMPORTANT** :
Before building or running, navigate to the `org.osc.export` project and open the `server.bndrun` file as shown below.

This is currently required before the first command-line build can succeed, due to a bug in the bnd-export-maven-plugin. We expect this be resolved in due course, but until then this step is required before first command-line build.

![](images/server_bndrun.JPG)

If you skip this, you'll get the following error from the command-line build:

![](images/error_cli.png)

## Command Line
### Building
Once you have checked out the code you can go to the folder osc-core and run:
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

Eclipse -> Run -> Run Configurations -> Maven Build

![](images/clean_install.jpg)

### Running
- First ensure you have a full maven build of osc-core from [the command line](#building).
- Navigate to `org.osc.export` project in Eclipse and open `server.bndrun`
- Click "**Run OSGi**". This will launch the OSC server in Eclipse, as shown below.
- You can now browse to [https://localhost](https://localhost).

![](images/running_osgi.png)