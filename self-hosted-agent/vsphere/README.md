# Overview

Demo to show how to use env0 self-hosted agents to deploy using Terraform to an on-prem vSphere environment.

## Agents Installation

Follow the [guide here.](https://docs.env0.com/docs/self-hosted-kubernetes-agent)

```bash
helm repo add env0 https://env0.github.io/self-hosted
helm repo update
helm upgrade --install --create-namespace env0-agent env0/env0-agent --namespace env0-agent \
-f tekanaid_values.yaml -f values.tekanaid.yaml \
--post-renderer ./kustomize-agent
```

AWS template for variable references:
```
${ssm:<secret-id>}
```

