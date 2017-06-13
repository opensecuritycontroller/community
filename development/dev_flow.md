# Development Workflow

## Workflow
The image below depicts the OSC development workflow.
![](./images/dev_flow.jpg)

## Cloning The Repositories
See [Accessing OSC Repositories](repo_access.md) to learn how to access, fork, and clone the OSC repositories. 

## Create a Branch
Once you have forked and cloned the OSC repositories, you must create a new branch from one of the local project branches. 
 > Note: Do not create a branch from the main project branches; you should only create a branch from your forked repository project branches.

Ensure your local project branches are up to date:
 > Note: Use the same commands for the release branches if working on a hotfix.

```sh
cd $working_dir/$repo
git fetch upstream
git checkout master
git rebase upstream/master
```

Branch from your local project branches:

```sh
git checkout -b my-feature
```

You may create as many branches as you wish. Since you cannot commit or push to the project branches, you will need at least one branch pushed remotely to your fork. 

## Keeping Your Branch In Sync
Use the following commands to synchronize your branch with the upstream branch:
 > Note: Use the same commands for the release branches if working on a hotfix.

```sh
git fetch upstream
git rebase upstream/master
```

## Committing Your Changes
You can commit and push changes on your own branch as often as you wish by using the following commands: 

```sh
# Adding files to your commit.
git add "filename1"
git add "filename2"
# ...
git commit -m "Message"
# Make your code changes
```

Make certain to use meaningful messages on your commits. Clear messages help describe your pull request for code reviews.

## Pushing to Your Remote Branch
Push commits from your local feature branch to your remote feature branch:
```sh 
git push -f origin my-feature
```
 > Note: If you are updating a branch with an open pull request, see [Pull Request Guidelines](pull_requests.md).

## Creating a Pull Request
Once your changes are pushed to your remote feature branch on GitHub, you can perform the following steps for creating a pull request. See **[Pull Request Guidelines](pull_requests.md)** for more details.

1.	Review your branch on GitHub, and then click **New pull request**.
2.	Ensure the base fork is set to opensecuritycontroller/$repo and the base branch is appropriate for your type of contribution (for hotfixes, use a release branch).
3.	Ensure the head fork is your forked repository and the branch to compare is the branch you would like to merge.
2.	Add a descriptive name and fill out the template.
3.	Add the reviewers.
4.	Click **Create pull request**.
