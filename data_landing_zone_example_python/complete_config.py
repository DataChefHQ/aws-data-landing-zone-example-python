from aws_cdk import aws_ec2 as ec2, aws_iam as iam
from recipes_dlz import (
    DatabaseAction,
    DataLandingZoneProps,
    Defaults,
    DlzAccountType,
    DlzControlTowerStandardControls,
    NetworkAddress,
    Region,
    SecurityHubNotificationSeverity,
    SecurityHubNotificationSWorkflowStatus,
    SlackChannel,
    TableAction,
    TagAction,
)

slack_budget_notifications = SlackChannel(
    slack_channel_configuration_name="budget-alerts",
    slack_workspace_id="YourWorkspaceId:",
    slack_channel_id="YourChannelId",
)

config = DataLandingZoneProps(
    local_profile="ct-sandbox-exported",
    regions={
        "global": Region.EU_WEST_1,
        "regional": [Region.US_EAST_1],
    },
    mandatory_tags={
        "owner": ["backend"],
        "project": ["accounting"],
        "environment": ["development", "staging", "production"],
    },
    default_notification={
        "slack": {
            "slack_channel_configuration_name": "new-channel-default-notifications",
            "slack_workspace_id": "YourWorkspaceId",
            "slack_channel_id": "YourChannelId",
        },
    },
    budgets=[
        *Defaults.budgets(
            100,
            20,
            slack=slack_budget_notifications,
            emails=["you@org.com"],
        ),
        {
            "name": "backend",
            "for_tags": {
                "owner": "backend",
            },
            "amount": 100,
            "subscribers": {
                "slack": slack_budget_notifications,
                "emails": ["you@org.com"],
            },
        },
        {
            "name": "backend-accounting-internal-development",
            "for_tags": {
                "owner": "backend",
                "project": "accounting-internal",
                "environment": "development",
            },
            "amount": 100,
            "subscribers": {
                "slack": slack_budget_notifications,
                "emails": ["you@org.com"],
            },
        },
    ],
    security_hub_notifications=[
        {
            "id": "notify-high",
            "severity": [
                SecurityHubNotificationSeverity.MEDIUM,
                SecurityHubNotificationSeverity.HIGH,
                SecurityHubNotificationSeverity.CRITICAL,
            ],
            "workflow_status": [SecurityHubNotificationSWorkflowStatus.NEW],
            "notification": {
                "slack": {
                    "slack_channel_configuration_name": "security-hub-high",
                    "slack_workspace_id": "YourWordspaceID",
                    "slack_channel_id": "YourChannelID",
                },
            },
        },
        {
            "id": "notify-resolved",
            "workflow_status": [
                SecurityHubNotificationSWorkflowStatus.RESOLVED,
                SecurityHubNotificationSWorkflowStatus.SUPPRESSED,
            ],
            "notification": {
                "slack": {
                    "slack_channel_configuration_name": "security-hub-resolved",
                    "slack_workspace_id": "YourWordspaceID",
                    "slack_channel_id": "YourChannelID",
                },
            },
        },
    ],
    organization={
        "organization_id": "OrganizationID",
        "root": {
            "accounts": {
                "management": {
                    "account_id": "YourRootAccountID",
                },
            },
            "controls": [
                *Defaults.root_controls(),
                DlzControlTowerStandardControls.SH_SECRETS_MANAGER_3,
            ],
        },
        "ous": {
            "security": {
                "ou_id": "RootOrganizationID",
                "accounts": {
                    "log": {
                        "account_id": "YourLogsAccountID",
                    },
                    "audit": {
                        "account_id": "YourAuditAccountID",
                    },
                },
            },
            "workloads": {
                "ou_id": "WorkloadOrganizationUnitId",
                "accounts": [
                    {
                        "name": "development",
                        "account_id": "YourDevelopmentAccountID",
                        "type": DlzAccountType.DEVELOP,
                        "vpcs": [
                            Defaults.vpc_class_b3_private_3_public(0, Region.US_EAST_1),
                            Defaults.vpc_class_b3_private_3_public(1, Region.EU_WEST_1),
                        ],
                    },
                    {
                        "name": "production",
                        "account_id": "YourProductionAccountID",
                        "type": DlzAccountType.PRODUCTION,
                        "vpcs": [
                            Defaults.vpc_class_b3_private_3_public(2, Region.US_EAST_1),
                            Defaults.vpc_class_b3_private_3_public(3, Region.EU_WEST_1),
                        ],
                        "lake_formation": [
                            {
                                "region": Region.EU_WEST_1,
                                "admins": [
                                    "arn:aws:iam::YourProductionAccountID:role/aws-reserved/sso.amazonaws.com/eu-west-1/AWSReservedSSO_AdministratorAccess_edcdcd01206c378d"
                                ],
                                "hybrid_mode": True,
                                "tags": [
                                    {
                                        "tag_key": "common",
                                        "tag_values": ["true", "false"],
                                    },
                                    {"tag_key": "team:Data", "tag_values": ["true"]},
                                    {"tag_key": "team:DevOps", "tag_values": ["true"]},
                                    {
                                        "tag_key": "shared",
                                        "tag_values": ["true", "false"],
                                        "share": {
                                            "with_external_account": [
                                                {
                                                    "principals": [
                                                        "YourDevelopmentAccountID"
                                                    ],
                                                    "tag_actions": [
                                                        TagAction.DESCRIBE,
                                                        TagAction.ASSOCIATE,
                                                    ],
                                                    "tag_actions_with_grant": [
                                                        TagAction.DESCRIBE,
                                                        TagAction.ASSOCIATE,
                                                    ],
                                                    "specific_values": ["true"],
                                                }
                                            ]
                                        },
                                    },
                                ],
                                "permissions": [
                                    {
                                        "principals": [
                                            "arn:aws:iam::YourProductionAccountID:role/TeamData",
                                            "arn:aws:iam::YourProductionAccountID:role/TeamDevOps",
                                        ],
                                        "tags": [
                                            {
                                                "tag_key": "common",
                                                "tag_values": ["true"],
                                            }
                                        ],
                                        "database_actions": [DatabaseAction.DESCRIBE],
                                        "table_actions": [
                                            TableAction.DESCRIBE,
                                            TableAction.SELECT,
                                        ],
                                    },
                                    {
                                        "principals": [
                                            "arn:aws:iam::YourProductionAccountID:role/TeamData"
                                        ],
                                        "tags": [
                                            {
                                                "tag_key": "team:Data",
                                                "tag_values": ["true"],
                                            }
                                        ],
                                        "database_actions": [DatabaseAction.DESCRIBE],
                                        "table_actions": [
                                            TableAction.DESCRIBE,
                                            TableAction.SELECT,
                                        ],
                                    },
                                    {
                                        "principals": [
                                            "arn:aws:iam::YourProductionAccountID:role/TeamDevOps"
                                        ],
                                        "tags": [
                                            {
                                                "tag_key": "team:DevOps",
                                                "tag_values": ["true"],
                                            }
                                        ],
                                        "database_actions": [
                                            DatabaseAction.DESCRIBE,
                                            DatabaseAction.CREATE_TABLE,
                                            DatabaseAction.ALTER,
                                            DatabaseAction.DROP,
                                        ],
                                        "table_actions": [
                                            TableAction.DESCRIBE,
                                            TableAction.SELECT,
                                            TableAction.ALTER,
                                            TableAction.DELETE,
                                            TableAction.INSERT,
                                            TableAction.DROP,
                                        ],
                                        "database_actions_with_grant": [
                                            DatabaseAction.DESCRIBE,
                                            DatabaseAction.CREATE_TABLE,
                                            DatabaseAction.ALTER,
                                            DatabaseAction.DROP,
                                        ],
                                        "table_actions_with_grant": [
                                            TableAction.DESCRIBE,
                                            TableAction.SELECT,
                                            TableAction.ALTER,
                                            TableAction.DELETE,
                                            TableAction.INSERT,
                                            TableAction.DROP,
                                        ],
                                    },
                                    {
                                        "principals": ["YourDevelopmentAccountID"],
                                        "tags": [
                                            {
                                                "tag_key": "shared",
                                                "tag_values": ["true"],
                                            }
                                        ],
                                        "database_actions": [DatabaseAction.DESCRIBE],
                                        "table_actions": [
                                            TableAction.DESCRIBE,
                                            TableAction.SELECT,
                                        ],
                                    },
                                ],
                            }
                        ],
                    },
                ],
            },
            "suspended": {
                "ou_id": "",
            },
        },
    },
    network={
        "connections": {
            "vpc_peering": [
                {
                    "source": NetworkAddress("development"),
                    "destination": NetworkAddress.from_string(
                        "production.us-east-1.default.private"
                    ),
                },
            ],
        },
        "nats": [
            {
                "name": "development-eu-west-1-internet-access",
                "location": NetworkAddress(
                    "development",
                    str(Region.EU_WEST_1),
                    "default",
                    "public",
                    "public-1",
                ),
                "allow_access_from": [
                    NetworkAddress(
                        "development", str(Region.EU_WEST_1), "default", "private"
                    ),
                ],
                "type": {
                    "instance": {
                        "instance_type": ec2.InstanceType.of(
                            ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
                        ),
                    },
                },
            },
        ],
        "bastion_hosts": [
            {
                "name": "default",
                "location": NetworkAddress(
                    "development",
                    str(Region.EU_WEST_1),
                    "default",
                    "private",
                    "private-1",
                ),
                "instance_type": ec2.InstanceType.of(
                    ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
                ),
            }
        ],
    },
    iam_policy_permission_boundary={
        "policy_statement": {
            "effect": iam.Effect.ALLOW,
            "actions": ["*"],
            "resources": ["*"],
        },
    },
    iam_identity_center={
        "arn": "IdentityCenterARN",
        "id": "IdentityCenterID",
        "store_id": "StoreID",
        "users": [
            {
                "user_name": "you@org.com",
                "name": "Name",
                "surname": "LastName",
            },
        ],
        "permission_sets": [
            *Defaults.iam_identity_center_permission_sets(),
        ],
        "access_groups": [
            {
                "name": "admin-access-group",
                "account_names": ["*"],
                "user_names": ["you@org.com"],
                "permission_set_name": "AdministratorAccess",
            },
        ],
    },
    additional_mandatory_tags=[{"name": "Test"}],
    deny_service_list=[*Defaults.deny_service_list(), "ecs:*"],
    deployment_platform={
        "gitHub": {
            "references": [
                {
                    "owner": "DataChefHQ",
                    "repo": "data-landing-zone-example-typescript",
                },
            ],
        },
    },
    print_report=False,
    print_deployment_order=True,
)
