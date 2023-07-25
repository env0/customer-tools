# self-hosted-agent / aws 

This directory contains examples of how to consume the modules defined in https://github.com/env0/k8s-modules
The best way so far to deploy is to separate out the deloyment of each resource, as this will problems with the k8s provider.


### Deployment Order
```
├── vpc
├── eks           
├── efs
├── csi-driver
└── env0-agent
```

### Notes:
* Some shortcuts were taken to make the modules work together: namely, VPC name == "var-<cluster name>"; if you are deploying your cluster in an existing VPC, please be mindful of this.
* The Subnet CIDR blocks are not optimized
* us-east-1 has an issue with AZ: us-east-1e which means you cannot use the branch - dynamicazs - that its currently point to. 