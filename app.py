#!/usr/bin/env python3


import aws_cdk as cdk

from serverless_app.serverless_app_stack import ServerlessAppStack
from serverless_app.shared.envs import ACCOUNT, REGION
from serverless_app.shared.constants import STACK_NAME


env = cdk.Environment(
    account=ACCOUNT,
    region=REGION,
)
app = cdk.App()
ServerlessAppStack(
    app,
    STACK_NAME,
    env=env,
)

app.synth()
