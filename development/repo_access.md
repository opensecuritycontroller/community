# Accessing OSC Repositories

The following information will provide you the instructions to access OSC repositories.

## Requirements

- **Git**: Download and Install [git](https://git-scm.com/download/).  
 > Note: If installing for Windows, **Git Bash** is included in the installation. Shell commands mentioned in this document must be completed using Git Bash.

## Connecting To GitHub

### SSH Configuration

1. Setup your git to connect with GitHub via SSH by following these steps: https://help.github.com/articles/connecting-to-github-with-ssh
2. Once you have added your SSH key and registered it on your GitHub account, you should be able to run the following command successfully:
```sh
ssh -T git@github.com
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access
```

## Getting The Code

The following steps will clone the code in your local git and configure some common hooks. To clone:

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
## Useful Aliases

Update your git aliases in `~/.gitconfig` with [git-aliases](./aliases/git-aliases). While these aliases are optional they can be very useful as they simplify common git operations.  

## Next Steps

- **[Development Worflow](dev_flow.md)**
- **[Configure Eclipse](eclipse.md)**



