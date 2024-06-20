from aws_cdk import (
    Stack,
    Duration,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    aws_lambda as lambda_,
    aws_cloudwatch as cloudwatch,
    CfnOutput,
)
from constructs import Construct
from serverless_app.shared.constants import (
    ProductTableName,
    ProductTablePrimaryKeyName,
    ProductTableSecondaryKeyName,
    LambdaEnvKeys,
)
from aws_solutions_constructs.aws_lambda_dynamodb import LambdaToDynamoDB


class ServerlessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        product_backend = LambdaToDynamoDB(
            self,
            "ProductBackend",
            lambda_function_props={
                "runtime": lambda_.Runtime.PYTHON_3_9,
                "code": lambda_.Code.from_asset("lambda_functions/products"),
                "handler": "get_products.handler",
            },
            dynamo_table_props={
                "partition_key": dynamodb.Attribute(
                    name=ProductTablePrimaryKeyName,
                    type=dynamodb.AttributeType.STRING,
                ),
                "sort_key": dynamodb.Attribute(
                    name=ProductTableSecondaryKeyName,
                    type=dynamodb.AttributeType.STRING,
                ),
                "table_name": ProductTableName,
                "removal_policy": RemovalPolicy.DESTROY,
            },
            table_environment_variable_name=LambdaEnvKeys.PRODUCT_TABLE_NAME,
            table_permissions="Read",
        )

        product_table = product_backend.dynamo_table
        # product_table.add_global_secondary_index(
        #     index_name="product_id",
        #     partition_key=dynamodb.Attribute(
        #         name=ProductTableSecondaryKeyName,
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        # )
        # product_table.add_global_secondary_index(
        #     index_name="product_name",
        #     partition_key=dynamodb.Attribute(
        #         name=ProductTablePrimaryKeyName,
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        #     sort_key=dynamodb.Attribute(
        #         name=ProductTableSecondaryKeyName,
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        # )

        get_product_lambda = product_backend.lambda_function

        # product_table.grant_read_data(get_product_lambda)

        get_product_lambda_url = get_product_lambda.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            cors=lambda_.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[lambda_.HttpMethod.GET],
                allowed_headers=["*"],
            ),
        )

        get_product_lambda.metric_errors(
            label="Get Product Function Error",
            period=Duration.minutes(1),
            statistic=cloudwatch.Stats.SUM,
        ).create_alarm(
            self,
            "GetProductLambdaErrors",
            threshold=1,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=cloudwatch.TreatMissingData.IGNORE,
            alarm_name="GetProductLambdaErrors",
        )

        CfnOutput(
            self,
            "ProductApiUrl",
            value=get_product_lambda_url.url,
            export_name="ProductApiUrl",
        )
