from aws_data_landing_zone import Scripts
from data_landing_zone_example_python import config_minimum

Scripts.deploy_select(props=config_minimum.config, id="security--*")
