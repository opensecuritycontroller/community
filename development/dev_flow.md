# Development Worklow

## Accessing the Code

It is recommended that you clone all the OSC repositories under the same folder. I.e.:
```sh
mkdir -p /c/git/osc
cd /c/git/osc
```

The following commands should be invoked for each of the OSC repositories:

```sh
# Replace "REPO_NAME" with the respective repository name, i.e.: osc-core, sdn-controller-api, etc
git clone https://github.com/opensecuritycontroller/REPO_NAME.git
```

The command above will clone the code locally, from within each local repository you should create a new branch to be used for your changes:

```sh
# Replace "username" below with your GitHub user name
git checkout -b username-branch
# Make your code changes
```

## Commiting Your Changes

You can commit your changes as often as you would like to and you can also push it to GitHub on your branch frequently. The following commands can be used for that:


```sh
# Replace "filename" with the file you would like to commit. This can be done for multiple files.
git add "filename"
git add "filename2"
# ...
git commit -m "Message"
git push origin username-branch
# Make your code changes
```

The above commands will bring your changes to your branch on GitHub. To have those changes reviewed and merged in the master branch see [Pull Requests](pull_requests.md).


