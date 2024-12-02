from aws_data_landing_zone import (
    Defaults,
    DlzAccountType,
    Region,
    DataLandingZoneProps,
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
)
