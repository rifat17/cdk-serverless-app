from serverless_app.shared.utils import StrEnum


class Environment(StrEnum):
    DEV = "dev"
    PROD = "prod"


class LambdaEnvKeys(StrEnum):
    PRODUCT_TABLE_NAME = "PRODUCT_TABLE_NAME"


STACK_NAME = "CdkServerlessStack"
ProductTableName = "Products"
ProductTablePrimaryKeyName = "PK"
ProductTableSecondaryKeyName = "SK"
