# customer-tools

This repository is to provide our customers a set of tools to help them get started with env0.
It includes things such as scripts and terraform code for migrating and configuring your env0 organization.

Pull Requests are welcome! 

The folder structure is still relatively fluid.  For now, we'll use the following structure:

```
├── iam
│   └── aws                   # aws assume roles 
├── migrations
│   └── tfc-to-env0-migration # script to help migrate from TFC to env0
├── modules
│   └── env0
└── self-hosted-agent

```