# Development Worklow

## Requirements

 - **Code Access:**  Complete the steps **[Accessing OSC Repositories](repo_access.md)**.

## Create a Branch
Once you have cloned the OSC repositories you must create a new branch. 
> **You should NOT commit or push changes directly on the 'master' branch**.

You may create as many branches as you wish, branches that you intend to push to GitHub should be prefixed by your GitHub user name. Since you cannot commit or push to the 'master' branch you will need at least one branch pushd remotely. 
```sh
git checkout -b [YOUR_GITHUB_USER_NAME]_branch
```


## Committing Your Changes

You can commit and push your changes on your branch as often as you would like. 
The following commands can be used for that:


```sh
# Adding files to your commit.
git add "filename1"
git add "filename2"
# ...
git commit -m "Message"
git push origin [YOUR_GITHUB_USER_NAME]_branch
# Make your code changes
```

Make sure to use meaningfull messages on your commits. Clear messages help describe your pull request for code reviews.

## Keeping Your Branch In Sync

Use the following commands to synchronize your branch with the master branch.
```sh
git fetch origin
git rebase origin/master
```

## Next

- **[Pull Requests](pull_requests.md)**


