#!/usr/bin/env python3
import aws_cdk as cdk
import recipes_dlz as dlz
from data_landing_zone_example_python.minimum_config import config

app = cdk.App()

dlz.DataLandingZone(
    app,
    local_profile=config.local_profile,
    budgets=config.budgets,
    mandatory_tags=config.mandatory_tags,
    organization=dlz.DLzOrganization(
        organization_id=config.organization.organization_id,
        root=dlz.RootOptions(
            accounts=dlz.OrgRootAccounts(
                management=dlz.DLzManagementAccount(
                    account_id=config.organization.root.accounts.management.account_id
                ),
            ),
            controls=config.organization.root.controls,
        ),
        ous=dlz.OrgOus(
            security=dlz.OrgOuSecurity(
                ou_id=config.organization.ous.security.ou_id,
                accounts=dlz.OrgOuSecurityAccounts(
                    log=dlz.DLzManagementAccount(
                        account_id=config.organization.ous.security.accounts.log.account_id
                    ),
                    audit=dlz.DLzManagementAccount(
                        account_id=config.organization.ous.security.accounts.audit.account_id
                    ),
                ),
            ),
            workloads=dlz.OrgOuWorkloads(
                ou_id=config.organization.ous.workloads.ou_id,
                accounts=[
                    dlz.DLzAccount(
                        name=account.name,
                        account_id=account.account_id,
                        type=account.type,
                    )
                    for account in config.organization.ous.workloads.accounts
                ],
            ),
            suspended=dlz.OrgOuSuspended(
                ou_id=config.organization.ous.suspended.ou_id,
            ),
        ),
    ),
    regions=dlz.DlzRegions(
        global_=config.regions.global_,
        regional=config.regions.regional,
    ),
    security_hub_notifications=config.security_hub_notifications,
    additional_mandatory_tags=config.additional_mandatory_tags,
    default_notification=config.default_notification,
    deny_service_list=config.deny_service_list,
    deployment_platform=config.deployment_platform,
    iam_identity_center=config.iam_identity_center,
    iam_policy_permission_boundary=config.iam_policy_permission_boundary,
    network=dlz.Network(
        connections=dlz.NetworkConnection(
            vpc_peering=[
                dlz.NetworkConnectionVpcPeering(
                    source=dlz.NetworkAddress.from_string(peering.source),
                    target=dlz.NetworkAddress.from_string(peering.target),
                )
                for peering in config.network.connections.vpc_peering
            ]
        )
    ),
    print_deployment_order=config.print_deployment_order,
    print_report=config.print_report,
    save_report=config.save_report,
)


app.synth()
