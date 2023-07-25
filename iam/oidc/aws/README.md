# AWS OIDC 

### References:
* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-wif

## 1. Using AWS CLI to Create an OIDC provider (identity provider)

```bash
aws iam create-open-id-connect-provider --url https://login.app.env0.com --thumbprint-list db3017fae2d1d7871eb718c3797c0c9557eb679e --client-id-list https://prod.env0.com
```

## 2. Setting up the AWS assume role with Identity Provider

Manually create an AWS assume role that utilizes the new Web Identity Federation / Identity Provider

[Todo] add TF example
see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp.html


## Retrieving the Thumbprint for yourself

You can follow along with AWS's example, but I find it easier to simply use the browser's certificate browser.  Click on the "security" or "lock" icon next to the URL - and open the certificate for inspection. 

### Summary of AWS's instructions;
1. `openssl s_client -servername login.app.env0.com -showcerts -connect login.app.env0.com:443`
2. Create the crt file by copying the top level CA and saving it into a file. (everthing between BEGIN and END CERTIFICATE, inclusive of the titles)
3. `openssl x509 -in oidc.crt -fingerprint -noout -sha1`

## Restrictions 
* According to [IAM Conditions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html) and [IAM keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-wif) there are only a limited number of claims that can be used in the Trust Policy.
