# Issue Tracking

OSC uses GitHub issues to track and triage different types of issues such as defects and discussions. This document explains the issue lifecycle.

## Opening an Issue

Once an issue is found, the first step is to look at current issues to see if it is already being tracked. If the issue is not being tracked, create a new one and fill out the issue template.
   > Note: If the issue template is not a fit for the type of issue you are opening, for example, a question issue, delete the template and provide a detailed description.

Upon filling out the template, select a *single* [issue type](#issue-types) label and as many [issue specifier](#issue-specifiers) labels as needed. Do not add an [issue status](#issue-statuses) as this is done by the triage team.

Do not check any boxes in the *Status* section of the issue template at this time.

## Triage Flow

1. An issue is opened without a [status](#issue-statuses) label.
2. The triage team adds a single *triage* label and a single *priority* label. A single *inactive* label can be added if the issue is deemed inactive.
3. Once the triage team has approved the issue, they will add both the *triage/approved* label and an assignee.
4. Either the triage team or assignee will attempt to reproduce the issue. Once it is successfully reproduced, they will check the *Reproduced* task box.
5. Once the assignee starts working on the issue, they will check the *In Progress* task box.
6. When the assignee is ready with a fix, they will send out a pull request [referencing the issue](https://github.com/blog/1506-closing-issues-via-pull-requests) and check the *Pull Request Out* task box.
7. Once the pull request is merged, the issue will be closed if it was referenced correctly.
8. Notice the last task box, *Validated*, is still unchecked. This box will be checked by the QA team after they have validated that the issue has been resolved.

## Issue Labels

It is important to understand the use and meaning of labels as they help facilitate the triage process.

### Issue Types

Choose only **one** of the following label types:
* defect
* discussion
* improvement
* addition

### Issue Specifiers

Choose any amount of the following specifier labels:

* experience

> Note: More issue specifiers will be added as the need for them occurs.

### Issue Statuses 
These labels are for the triage team only.

Choose **at most one** of each type of status label:

Triage Status
* triage/approved
* triage/declined
* triage/more-info
* triage/re-evaluate  

Assigned Priority
* priority/high
* priority/medium
* priority/low  

Inactive Status (optional)
* inactive/duplicate
* inactive/invalid
* inactive/on-hold
* inactive/wont-fix

Valid combination of labels: triage/more-info, priority/low, inactive/on-hold.

Invalid combination of labels: triage/approved, triage/re-evaluate, inactive/wont-fix