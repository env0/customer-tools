# IAM / AWS 

Simple terraform code to create the AWS Assume Role and create the corresponding credential in your env0 Organization.

### Pre-requisites:
* AWS Credentials configured in your local environment
* env0 Credentials configured in your local environment (ENV0_API_KEY / ENV0_API_SECRET) (see doc on [env0 API KEYS](https://docs.env0.com/docs/api-keys))
* Terraform binary installed

### HowTo:

* To create the assume role for env0 to assume: 

```
cd assume-role
terraform init
terraform plan
terraform apply
```
* To create the cost assume role for env0 to assume: 

```
cd cost-assume-role
terraform init
terraform plan
terraform apply
```

### Notes:

* By default, this code will provision Administrator access to the assume-role.
* The cost-assume-role can be deployed in any account that is under the parent billing account.
* After deploying these roles, you will still need to associate the credential to your projects. 
