from recipes_dlz import (
    DataLandingZoneProps,
    Defaults,
    DlzAccountType,
    DlzControlTowerStandardControls,
    Region,
)

config = DataLandingZoneProps(
    local_profile="",  # TODO: Not required; Will be optional from next release
    regions={
        "global": Region.EU_WEST_1,
        "regional": [Region.US_EAST_1],
    },
    mandatory_tags={
        "owner": ["backend"],
        "project": ["accounting"],
        "environment": ["development", "staging", "production"],
    },
    budgets=Defaults.budgets(100, 20),
    security_hub_notifications=[],
    organization={
        "organization_id": "RootOrganizationID",
        "root": {
            "accounts": {
                "management": {
                    "account_id": "YourRootAccountID",
                },
            },
            # Optional, showing that controls can be changed, added, or removed from the default
            # These controls are applied to all the OUs in the org
            "controls": [
                *Defaults.root_controls(),
                DlzControlTowerStandardControls.SH_SECRETS_MANAGER_3,
            ],
        },
        "ous": {
            "security": {
                "ou_id": "SecurityOrganizationUnitId",
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
                # Small Org, all workloads/projects in the same accounts
                "accounts": [
                    {
                        "name": "development",
                        "account_id": "YourDevelopmentAccountID",
                        "type": DlzAccountType.DEVELOP,
                    },
                ],
            },
            "suspended": {
                "ou_id": "SuspendedOrganizationUnitId",
            },
        },
    },
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
)
