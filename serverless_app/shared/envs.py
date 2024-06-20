import os
from serverless_app.shared.constants import LambdaEnvKeys

ACCOUNT = os.getenv("CDK_DEFAULT_ACCOUNT")
# REGION = os.getenv("CDK_DEFAULT_REGION")
REGION = "ap-northeast-3"

PRODUCT_TABLE_NAME = os.environ.get(LambdaEnvKeys.PRODUCT_TABLE_NAME)
