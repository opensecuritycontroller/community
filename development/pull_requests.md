# Pull Requests

The code and documentation review process for OSC is driven by GitHub pull requests. This document describes the guidelines and actions related to PRs.

## Requirements
 - **Development Workflow:**  Complete the steps **[Development Workflow](dev_flow.md)**.

## Squashing vs. Merging
Pull requests should generally have a single commit. You may send pull requests with more than one commit if that will help keep the history more clear. Commits that are not meant to be present in the git logs of the master branch should be **[squashed](https://ariejan.net/2011/07/05/git-squash-your-latests-commits-into-one/)** prior to sending a PR.


## Addressing Comments
Once a pull requested is created it will go through a code review/discussion. All the comments must be addressed prior to merging either with a response or code change. 
Commits added to address comments should, in most cases, be squashed.


## Merging Pull Requests
Once the PR has been flagged as '**Approved**' the PR owner can merge it to the master branch. 






