# Pull Request Guidelines

The code and documentation review process for OSC is driven by GitHub pull requests. This document describes the guidelines and actions related to pull requests (PR)s.

## Requirements
* **[Accessing the Code](repo_access.md)**
* **[Development Workflow](dev_flow.md)**

## Squashing Commits
Pull requests should generally have a single commit. You may send pull requests with more than one commit if that accrues to the clarity of the code review process. Keep in mind that multiple commits in a pull request cannot be merged to the project branches. They must be [squashed](https://ariejan.net/2011/07/05/git-squash-your-latests-commits-into-one/) at the time of merging so that a pull request will result in a single commit on the project branch logs.
> Note: Commits added to a PR in response to code review comments **SHOULD NOT** be squashed until the PR is ready to be merged (**Approved**).

```sh
git rebase -i HEAD~[# of commits to squash]
```

## Addressing Comments
Once a pull request is created, other community members can comment on your changes and give an overall review of either **Approved** or **Changes requested**. All comments should be addressed by either a response comment or a code change.  

## Merging Pull Requests
Once a pull request has been flagged as **Approved**, a designated branch administrator can merge it to the targeted project branch.






