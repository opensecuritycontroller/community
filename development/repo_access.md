# Accessing OSC Repositories

## Requirements

- **Git**: Download and Install [git](https://git-scm.com/download/).  
- If installing for Windows **Git Bash** will be included in the installation. All the shell commands mentioned on this document must be done using Git Bash.

## Connecting To GitHub
### Proxy Configuration
In some cases you may need to setup a proxy for your SSH Connection. This can be done with the following steps:

1. Copy the content from [ssh_proxy_config](intel_only/ssh_proxy_config) to the clipboard.
2. Update your SSH config file (creating a new one if needed):
``` sh
vi ~/.ssh/config
# Append the copied content to this file.
```

### SSH Configuration

1. Setup your git to connect with GitHub via SSH following these steps: https://help.github.com/articles/connecting-to-github-with-ssh
2. Once you have added your SSH key and registered it on your GitHub account you should be able to run the following command successfully:
```sh
ssh -T git@github.com
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access
```

## Getting The Code

The following steps will clone the code in your local git and configure some common hooks.

1. Create OSC root folder to store the OSC repositories:

```sh
mkdir /OSC
```

2. Copy the content of [clone_repos.sh](./scripts/clone-repos.sh) on your clipboard.

3. Create a local script file on the OSC root:
```sh
cd /OSC
vi clone-repos.sh
# Paste the content clone_repos.sh inside this file and save
```

4. Clone the repositories:
```sh
./clone-repos.sh
```

## Next

- **[Development Worflow](dev_flow.md)**
- **[Configure Eclipse](eclipse.md)**



