# L1-L4 security leveraging OpenStack security groups
OSC will support single page view to manage the OpenStack security groups. User will be able to manage the OpenStack security groups and security group rules from OSC.

## Assignees
Larkins Carvalho - https://github.com/larkinscarvalho

## Background
OSC will provide an interface to configure the OpenStack security groups. To integrate OSC with the OpenStack security groups, OSC needs to be aware of any modification to the security groups on the OpenStack. OSC will trigger synchronization tasks upon receiving relavent notification from the OpenStack to keep security group in sync with the OpenStack security groups.

> Note: The current revision of document provides details about the notifications provided by OpenStack which are necessary for OSC to be synced with the OpenStack secutiy groups.

## Constraints and Assumptions
- No addtional security groups are configured by user or admin directly on OpenStack.
- Admin should use the following policies to restrict the user from creating, updating or deleting the security groups on the OpenStack.

	OpenStack provides neutron policy configurations to manage permissions.

    ```
        # Neutron policy.json

        "create_security_group": "rule:admin_or_owner",
        "update_security_group": "rule:admin_or_owner",
        "delete_security_group": "rule:admin_or_owner",
        "create_security_group_rule": "rule:admin_or_owner",
        "delete_security_group_rule": "rule:admin_or_owner",
    ```

## Design Changes

### REST API
**TBD  on next revision**

### OSC SDKs

#### VNF Security Manager SDK
Not applicable

#### SDN Controller SDK
Not applicable

### Notifications provided by OpenStack

OpenStack provides notifications for create, update and delete of security group. However, for security group rule, no update operation is avaiable. With each operation, OpenStack provides the start and the end event notification. OSC receives the notification on RabbitMQ queue and processes the relavent synchronization tasks.

**Security Group notifications**

- **Create**: security_group.create.start and security_group.create.end

- **Update**: security_group.update.start and security_group.update.end

- **Delete**: security_group.delete.start and security_group.delete.end

**Security Group Rule notifications**

- **Create**: security_group_rule.create.start and security_group_rule.create.end

- **Delete**: security_group_rule.delete.start and security_group_rule.delete.end

### OSC Entities
**TBD  on next revision**

### OSC UI
**TBD  on next revision**

### OSC Synchronization Tasks
**TBD  on next revision**

## Tests
**TBD  on next revision**

## References
Not applicable

