# Issue Tracking

OSC uses GitHub issues to track defects, discussions, and improvements. This document explains the guidelines and lifecycles.

## Opening an Issue

Once a defect is found or you would like to suggest an improvement or start a discussion, the first step is to look at existing issues to see if it is already being tracked. If the issue is not being tracked, create a new one.
   > Note: The issue template may not be suitable for all types of issues; if you cannot utilize the issue template, provide a detailed description of the issue.

When opening an issue, do not check any boxes in the *Status* section of the issue template at this time.

## Defects

### Triage Flow
> Note: The triage flow below is executed by the OSC Triage Team (@opensecuritycontroller/osc_triage). If you would like to learn more, have any suggestions or would like to participate join our [Slack team](https://securitycontroller.slack.com).

1. The triage team  looks for opened issues without any labels.
2. The triage team adds a single *defect [issue type](#issue-types)* label, a single *triage* label, and a single *priority* label.
    > Note: If the issue does not contain enough information, the triage team will add the *triage/more-info* label and assign it back to the person that opened the issue. Once the assignee adds the correct information, the assignee must mention `@opensecuritycontroller/osc_triage` to notify them that more information has been added. The triage team can then add the *triage/re-evaluate* label.
3. Once the triage team has approved the issue, they will add a *triage/approved* label.
4. The triage team will also assign two owners for issues labeled with *triage/approved/active* and the milestone for the upcoming release.
    > The second owner is being assigned to the issue to perform additional validation after it has been merged (closed by the other owner), triage will indicate the ownership roles in the defect discussion.

#### Triage Queries
* [Open Issues: Without Labels](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aissue+user%3Aopensecuritycontroller+no%3Alabel+is%3Aopen+)
* [Open Issues: Unassigned](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aissue+user%3Aopensecuritycontroller+no%3Aassignee+is%3Aopen+)
* [Open Issues: Triage Re-Evaluate](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aissue+user%3Aopensecuritycontroller+label%3Atriage%2Fre-evaluate+is%3Aopen+)
* [Open Issues: Triage More-Info](https://github.com/opensecuritycontroller/osc-core/issues?q=is%3Aissue+is%3Aopen+label%3Atriage%2Fmore-info)
* [Closed Issues: Date Filter](https://github.com/issues?utf8=%E2%9C%93&q=is%3Aissue+user%3Aopensecuritycontroller+closed%3A%3E2017-07-11+)

### Assignee Flow

1. After an owner is assigned by the triage team, they will attempt to reproduce the issue. Once it is successfully reproduced, they will check the *Reproduced* task box.
   > Note: If the assignee cannot reproduce the issue, mention the triage team, `@opensecuritycontroller/osc_triage`, and include details to apply the appropriate label, for instance, *triage/declined/duplicate*, *triage/declined/invalid*, or *triage/declined/wont-fix*.
2. Once the assignee starts working on the defect, they will check the *In Progress* task box.
3. When the assignee is ready with a fix, they will send out a pull request [referencing the issue](https://github.com/blog/1506-closing-issues-via-pull-requests).
4. Once the pull request is merged, the issue will be closed if it was referenced correctly.
   > Note: The last task box, *Validated*, is still unchecked. This box will be checked when another community member validates the fix on the applicable project branch.

## Discussions and Improvements

Once the issue is submitted, the triage team will add either a *discussion* or *improvement* label and assign the issue to a community member to help facilitate the discussion or improvement.
> Note: When opening an issue in osc-core pertaining to discussions and improvements, be sure to delete the issue template and provide a detailed description.

## Issue Labels

It is important to understand the use and meaning of labels as they help facilitate the triage process.

> Note: More labels will be added as the need for them occurs.

### Issue Types

Choose only **one** of the following label types:

* defect: Represents typical product or documentation bug with information like: expected behavior, actual behavior, repro steps, existing documentation location, etc. The issue template in each repo should be used for this type of issue.
* discussion: Used to initiate a discussion or ask a question.
* improvement: Used to provide an idea for a product, process or documentation improvement.

> Note: The above types are the three base namespaces of each issue type, for example, in osc-core, defect corresponds to defect/product-code, defect/documentation, and defect/unit-test. To see the exact label name, look at the labels in the repository where you would like to open an issue.

### Issue Specifiers

Choose any amount of the following specifier labels:

* experience: Impacts the user experience without major functionality impact.

### Defect Labels
Choose **at most one** of each type of label:

Triage Status
* triage/approved/active: Accepted defects planned to be addressed on the next release. Issues with this label will also have a milestone assigned to them.
* triage/approved/on-hold: Accepted defects without a targeted release.
* triage/declined/duplicate: Duplicate of another existing issue, triage should add a mention to the existing issue.
* triage/declined/by-design: Declined, the reported behavior is by design.
* triage/declined/no-repro: Declined, the issue cannot currently be reproduced.
* triage/declined/wont-fix: Declined as wont fix, triage should provide more details.
* triage/more-info: The issue does not contain sufficient info.
* triage/re-evaluate: The issue has been updated and is ready to be looked again by triage.

Assigned Priority
* priority/critical
* priority/high
* priority/medium
* priority/low

Assigned Severity
* severity/critical
* severity/high
* severity/medium
* severity/low

Test Effectiveness
* te/automation: Any defect found as a resort of automated testing as part of [osc-tests](https://github.com/opensecuritycontroller/osc-tests)
* te/manual: Any defect found as a resort of Intel’s manual testing
* te/other: Any defect found that a customer did NOT report, nor was found through our automation or manual testing efforts
* te/customer-found: Any defect reported by an end user.