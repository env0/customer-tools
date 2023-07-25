#/bin/bash

# Inputs

echo "----------"
echo ">> Setting inputs"

source inputs.txt
# echo tfcOrgName = ${tfcOrgName}
# echo tfcWorkspaceID = ${tfcWorkspaceID}
# echo tfcBearerToken = ${tfcBearerToken}

# echo env0OrgID = ${env0OrgID}
# echo env0ProjectID = ${env0ProjectID}
env0OrgPrjID="${env0OrgID}.${env0ProjectID}"
# echo env0OrgPrjID = "${env0OrgPrjID}"

# Gathering environment variables

echo "----------"
echo ">> Gathering workspace variables."

tfcVariablesData=$( curl -s -X GET -H "Accept: application/json" -H \
"Authorization: Bearer ${tfcBearerToken}" \
https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID}/vars | jq -r '.data[].attributes | "{\"name\": \""+.key+"\", \"value\": \""+(.value)+"\", \"type\": 1},"')
tfcVariables=$(sed '$ s/.$//' <<< $tfcVariablesData)
# echo $tfcVariables

# Gathering VCS variables

echo "----------"
echo ">> Gathering VCS variables."

branch=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes.branch' ) 
if [ ${branch} = null ] 
    then branch=main 
fi
# echo branch = ${branch}

repository=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes."vcs-repo"."repository-http-url"' ) 
# echo repository = ${repository}

repositoryTrimmed=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes."vcs-repo".identifier' ) 
# echo repositoryTrimmed = ${repositoryTrimmed}

workingDirectory=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes."working-directory"' ) 
# echo workingDirectory = ${workingDirectory}

# Sync with TFC

echo "----------"
echo ">> Syncing with TFC."

terraform init -migrate-state
sleep 30

# Replace TFC Cloud with env0 Cloud

sed -i "" "s/app.terraform.io/backend.api.env0.com/g" provider.tf
sed -i "" "s/${tfcOrgName}/${env0OrgPrjID}/g" provider.tf
sed -i "" "s/${tfcWorkspaceName}/${env0WorkspaceName}/g" provider.tf

# Migrate state to env0

echo "----------"
echo ">> Migrating state to env0.  Please wait 30 seconds."

terraform init -migrate-state -force-copy -ignore-remote-version
sleep 30

# Testing only - revert remote configuration 

# sed -i "" "s/backend.api.env0.com/app.terraform.io/g" provider.tf
# sed -i "" "s/${env0OrgPrjID}/${tfcOrgName}/g" provider.tf
# sed -i "" "s/${env0WorkspaceName}/${tfcWorkspaceName}/g" provider.tf

# Pull env0 environment ID

sleep 5
echo "----------"
echo ">> Pulling template ID."

templateIdAll=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${env0BearerToken}==" https://api.env0.com/blueprints?projectId=${env0ProjectID} | jq -r '.[].id' )
templateId=$(echo $templateIdAll | awk '{print $NF}')
# echo Template ID = ${templateId}

# Manual update instructions

echo "----------"
echo ">> Please follow the below instructions to complete the migrations"
echo ""
echo "Navigate to https://app.env0.com/templates/${templateId}/settings"
echo ""
echo "Navigate to the VCS tab"
echo ""
echo "Select your VCS (e.g. GitHub)"
echo ""
echo "Insert the following values"
echo ""
echo "Repository : ${repositoryTrimmed}"
echo ""
echo "Branch : ${branch}"
echo ""
echo "Terraform Foler : ${workingDirectory}"
echo ""
echo "Navigate to the Variables tab"
echo ""
echo "Insert the following variables"
echo "${tfcVariables}"
echo "Alternatively you can Load variables from code to minimize your workload"
echo ""
echo "Save the configuration"
echo ""
echo "Navigate to the environment and reploy"
echo "Be aware auto-approval is turned on for this migrated environment.  We recommend disabling this on first redeploy."
echo ""
