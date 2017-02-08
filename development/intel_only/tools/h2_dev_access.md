# Access to H2 Database in Developer environment

# Introduction

Follow the steps to connect to database in the developer environment.

- Build the tools/KeyStoreAccess
- Get password by executing the **java –jar** command
- Use a SQLWorkbench to connect to the database using the password in the previous step

# Steps to connect to the database in a local environment

## Get DB connection password in development environment

C:\git\osc\community\development\intel\_only\tools\KeyStoreAccess&gt; **mvn install**

## Get DB connection password in development environment

C:\git\osc\osc-core\osc-export&gt; **java -jar C:\git\osc\community\development\intel\_only\tools\KeyStoreAccess\target\KeyStoreAccess-1.0.jar mainKeyStore.p12**

Initializing keystore...

Initializing keystore...

Opening keystore file....

Loading keystore from file....

Getting password with alias DB\_PASSWORD in keystore ...

DB PASSWORD:

NH[wC2YL)LP04AEG) POu64T&lt;gO5&quot;U)I

Stored in db\_password.txt

## Connect to DB with SQL Client

Connect from **SQLExplorer** to DB with password as above:

Driver: **H2 Database Engine(org.h2.Driver)**

URL: **jdbc:h2:file:c:/git/osc/osc-core/org.osc.export/vmiDCDB;AUTO\_SERVER=TRUE**

Username: **admin**

Password: **NH[wC2YL)LP04AEG) POu64T&lt;gO5&quot;U)I**