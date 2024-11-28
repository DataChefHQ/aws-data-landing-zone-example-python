import aws_cdk as core
import aws_cdk.assertions as assertions

from data_landing_zone_example_python.data_landing_zone_example_python_stack import DataLandingZoneExamplePythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in data_landing_zone_example_python/data_landing_zone_example_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DataLandingZoneExamplePythonStack(app, "data-landing-zone-example-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
