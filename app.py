#!/usr/bin/env python3
import aws_cdk as cdk
from aws_data_landing_zone import (
    DataLandingZone,
)
from data_landing_zone_example_python.config_minimum import config

app = cdk.App()

DataLandingZone(app, config)


app.synth()
