Attempted to run ECS with LocalStack, but the community edition does not support this service.

Leaving these notes here in case they are useful for future reference.


# Install localstack in minikube


Install Localstack via helm
```

helm repo add localstack https://localstack.github.io/helm-charts
helm repo update
helm upgrade --install localstack localstack/localstack -f sandbox/values/localstack-values.yaml
```

# Create credentials

Intall `awslocal` command line cli, and then run:
```
awslocal iam create-user --user-name demo-admin
awslocal iam attach-user-policy --user-name demo-admin --policy-arn=arn:aws:iam::aws:policy/AmazonECS_FullAccess

awslocal iam create-access-key --user-name demo-admin
```
This will output something like this:
{
    "AccessKey": {
        "UserName": "demo-admin",
        "AccessKeyId": "XXXXXXXXXXXXXXXXXXXX",
        "Status": "Active",
        "SecretAccessKey": "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
        "CreateDate": "2026-01-15T19:49:51.663900+00:00"
    }
}

Alternatively, one can use the aws cli directly instead awslocal.
Just do this before running commands:
```
alias aws="aws --endpoint-url=http://localhost:4566"
(.venv) lysianebouchard@CRHSJ108084 sandbox % export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1


# Create the aws connection


You can encode your AWS connection as a Kubernetes secret:
```
kubectl create secret generic aws-localstack-connection-secret 
--from-literal=my_db_conn='aws://ACCESS_KEY:SECRET_KEY@localstack:4566/?region_name=us-east-1'
````

There seem to be actually a bug with this connection url ... It's probably a small typo.

Once the secret is created, reference it in your values.yaml as an airflow connection environment variable to inject the connection.

If you have too much trouble making it work, just set the connection manually in the UI through the admin tab.

# Run ecs code

You will need to create the ECS cluster and task definition before running ECS tasks.
Use awslocal or the AWS CLI (with the alias above) to create these resources.
