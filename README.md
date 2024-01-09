# Wiederholung

## Setup

### Github Secrets

Im Github Repo -> Settings -> Security ->  Secrets & Variables -> Actions -> New Repository Secret

#### Aws config

- Kopiere das secret von dem AWS SSO Login -> Command Line or programmatic access
Name: AWS_CONFIG
Secret: 
[techstarter]
aws_access_key_id=abcdefg
aws_secret_access_key=12345677
aws_session_token=GAAAANZVIELTEXT

#### Terraform S3 state bucket

- Erstelle einen neuen S3 Bucket für den Terraform state
- Aktivere S3 Versioning

Name: TF_BUCKET
Secret: BUCKET_NAME

