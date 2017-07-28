# L1-L4 security leveraging OpenStack security groups
This document describes the notifications available for OpenStack security groups

## Assignees
Intel's OSC core team

## Background
OSC will support single page view to manage OpenStack security groups. User will be able to manage the OpenStack security groups and security group rules from OSC.

## Constraints and Assumptions
No addtional security groups are configured by user or admin directly on OpenStack.

## Notifications provided by OpenStack

OpenStack provides notifications for create, update and delete of security group. However, for security group rule, no update operation is avaiable. With each operation, OpenStack provides the start and the end event notification. OSC receives the notification on RabbitMQ queue and processes the relavent synchronization tasks.

**Security Group notifications**

- **Create**: security_group.create.start and security_group.create.end

- **Update**: security_group.update.start and security_group.update.end

- **Delete**: security_group.delete.start and security_group.delete.end

**Security Group Rule notifications**

- **Create**: security_group_rule.create.start and security_group_rule.create.end

- **Delete**: security_group_rule.delete.start and security_group_rule.delete.end

## User Permissions

User with admin privileges is expected to perform create/update/delete security group and create/delete security group rule operations.

OpenStack provides neutron policy configurations to manage permissions.

```
	# Neutron policy.json

    "create_security_group": "rule:admin_or_owner",
    "update_security_group": "rule:admin_or_owner",
    "delete_security_group": "rule:admin_or_owner",
    "create_security_group_rule": "rule:admin_or_owner",
    "delete_security_group_rule": "rule:admin_or_owner",
```

### REST API
**TBD  on next revision**

### OSC SDKs

#### VNF Security Manager SDK
Not applicable

#### SDN Controller SDK
Not applicable

### XYZ Integration Point
Not applicable

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

