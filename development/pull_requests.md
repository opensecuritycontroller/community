# Pull Requests

The code and documentation review process for OSC is driven by GitHub pull requests. This document describes the guidelines and actions related to pull requests (PR)s.

## Requirements
 - **Development Workflow:**  Complete the steps **[Development Workflow](dev_flow.md)**.

## Pull Request Flow
The diagram shown below depicts the detailed steps, along with the git commands involved in a **PR** lifecycle:  
![](./images/pr_flow.jpg)  
*Pull Request Steps and Commands*  

## Squashing Commits
Pull requests should generally have a single commit. You may send pull requests with more than one commit if that accrues to the clarity of the `master` logs. Commits not meant to be present in the git logs of the master branch should be **[squashed](https://ariejan.net/2011/07/05/git-squash-your-latests-commits-into-one/)** prior to sending and merging a PR.  
> **NOTE:** Commits added to a **PR** in response to code review comments **SHOULD NOT** be squashed until the PR is ready to be merged (**Approved**)


## Addressing Comments
Once a pull request is created, other community members can comment on your changes and give an overall review of either **Approved** or **Changes requested**. All comments should be addressed by either a response comment or a code change.  


## Merging Pull Requests
Once a pull request has been flagged as **Approved**, a designated branch administrator can merge it to the master branch.






