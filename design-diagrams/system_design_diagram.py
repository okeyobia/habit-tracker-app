from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.management import Cloudwatch
from diagrams.programming.language import Python
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.ci import GithubActions
from diagrams.custom import Custom

# You may need to download a React logo PNG and place it in the project directory as 'react.png'

with Diagram("Habit Tracker System Design", show=False, filename="system_design", outformat="png"):
    user = Users("User")
    react = Custom("React (S3/CloudFront)", "./react.png")
    with Cluster("AWS Cloud"):
        cloudfront = CloudFront("CloudFront")
        s3 = S3("S3")
        backend = Python("FastAPI")
        ecs = ECS("ECS")
        rds = RDS("PostgreSQL (RDS)")
        cognito = Cognito("Cognito/JWT Auth")
        cloudwatch = Cloudwatch("CloudWatch")
        codepipeline = Codepipeline("CI/CD")
        github = GithubActions("GitHub Actions")

    user >> react >> cloudfront >> s3
    cloudfront >> backend
    backend >> ecs
    backend >> rds
    backend >> cognito
    backend >> s3
    backend >> cloudwatch
    codepipeline >> github
    codepipeline >> ecs
