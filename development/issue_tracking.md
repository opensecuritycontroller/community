# Issue Tracking

OSC uses GitHub issues to track defects, discussions, and improvements. This document explains the guidelines and lifecycles.

## Opening an Issue

Once a defect is found or you would like to suggest an improvement or start a discussion, the first step is to look at existing issues to see if it is already being tracked. If the issue is not being tracked, create a new one.
   > Note: The issue template is for defects. If the issue is pertaining to a discussion or an improvement, delete the template and provide a detailed description.

When opening a defect issue, do not check any boxes in the *Status* section of the issue template at this time.

## Defects

### Triage Flow

1. The triage team looks for opened issues without any labels.
2. The triage team adds a single *defect [issue type](#issue-types)* label, a single *triage* label, and a single *priority* label. A single *inactive* label can be added if the issue is deemed inactive.
    > Note: If the issue does not contain enough information, the triage team will add the *triage/more-info* label and assign it back to the person that opened the issue. Once the assignee adds the correct information, the assignee must mention `@opensecuritycontroller/osc_triage` to notify them that more information has been added. The triage team can then add the *triage/re-evaluate* label.
3. Once the triage team has approved the issue, they will add both a *triage/approved* label and assign a developer.
4. Once a defect has been fixed and closed, the triage team will add a new community member as assignee to perform validation on the appropriate branch.

### Assignee Flow

1. After an owner is assigned by the triage team, they will attempt to reproduce the issue. Once it is successfully reproduced, they will check the *Reproduced* task box.
   > Note: If the assignee cannot reproduce the issue, mention the triage team, @opensecuritycontroller/osc_triage, and include details to apply the appropriate label, for instance, *triage/declined/duplicate*, *triage/declined/invalid*, or *triage/declined/wont-fix*.
2. Once the assignee starts working on the defect, they will check the *In Progress* task box.
3. When the assignee is ready with a fix, they will send out a pull request [referencing the issue](https://github.com/blog/1506-closing-issues-via-pull-requests) and check the *Pull Request Out* task box.
4. Once the pull request is merged, the issue will be closed if it was referenced correctly.
   > Note: The last task box, *Validated*, is still unchecked. This box will be checked when another community member validates the fix on the applicable project branch.

## Discussions and Improvements

When opening an issue pertaining to discussions and improvements, be sure to delete the issue template and provide a detailed description. Once the issue is submitted, the triage team will add either a *discussion* or *improvement* label and assign the issue to a  to help facilitate the discussion or improvement.

## Issue Labels

It is important to understand the use and meaning of labels as they help facilitate the triage process.

> Note: More labels will be added as the need for them occurs.

### Issue Types

Choose only **one** of the following label types:
* defect
* discussion
* improvement

### Issue Specifiers

Choose any amount of the following specifier labels:

* experience

### Defect Labels 
Choose **at most one** of each type of label:

Triage Status
* triage/approved/active
* triage/approved/on-hold
* triage/declined/duplicate
* triage/declined/invalid
* triage/declined/wont-fix
* triage/more-info
* triage/re-evaluate  

Assigned Priority
* priority/high
* priority/medium
* priority/low  