# OSC Releases

OSC releases are represented across all OSC repositories by a release branch. This document describes the process for committing changes on release branches and updating *master* with those changes.

## Release Branches
OSC release branches are protected and merges can only be made by the organization admin. Commits to these branches are reserved only for hotfixes of high priority bugs identified on that release and approved by triage.

To submit commits for a release branch create a pull request in that branch following the same steps defined in the [pull requests (PRs) flow](pull_requests.md). We will diverge only on the last step: once your PR is approved the organization admin will merge it to the respective release branch.

### Merging a Hotfix to *Master*
Once your hotfix has been committed to a shared/remote release branch you must also bring that fix to the *master* branch. It is  responsibility of the hotfix submitter to update *master* with the fix, for that follow the steps below:

1. Ensure that your local `master` and release branch containing the hotfix are up to date:

```sh
$ git fetch

# Updating master
$ git checkout master
$ git pull
$ git status 
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working tree clean

# Updating the release branch, i.e.: 0.6
$ git checkout 0.6
$ git pull
$ git status 
On branch 0.6
Your branch is up-to-date with 'origin/0.6'.
nothing to commit, working tree clean
```
2. Create branch that will serve as the merge branch from the HEAD of `master`:
```sh
$ git checkout master
$ git checkout -b owner/hotfix_merge
```
2. Cherry-pick your commit from the release branch to your new branch. 
> Note: While cherry-picking supports multiple commits you should NOT cherry-pick multiple commits from a release branch to bring to `master` in a single merge. That is because merges to master always must be squashed, therefore if you cherry-pick multiple commits from a release branch to `master` after the merge those commits will be transfered as a single one and this will make it harder to follow the commits history accross branches.  

> Note: When cherry-picking ensure to use the option `-x`. This will add the original commit number to your new commit in `master`.  

The commands below demonstrate how you can cherry-pick the commit `04b42aa0ee0672f117d754b03ac92e0c459d6f47` from the 0.6 branch. **Tip**: On the GitHub commits history each commit has the button "Copy the full SHA" which you can use to easily copy your targeted commit.
```sh
$ git cherry-pick -x 04b42aa0ee0672f117d754b03ac92e0c459d6f47
# This will bring that commit as a new one on your hotfix_merge branch. 
Observe that the commit message contains the original commit number: 
```
3. Push your new branch to the remote:

```sh
$ git push -f origin owner/hotfix_merge
```
4. At this point, you must create a PR from your branch to `master` on GitHub. If your cherry-pick had any conflicts or required any additional changes follow the [code review process](pull_requests.md#addressing-comments), otherwise you can directly merge your PR.
> Note: As for any other merge to `master` your PR must be **squashed** during the merge.
