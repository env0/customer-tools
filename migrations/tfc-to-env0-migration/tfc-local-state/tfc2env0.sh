#/bin/bash

# Inputs

echo "----------"
echo ">> Setting inputs"

source inputs.txt
echo tfcOrgName = ${tfcOrgName}
echo tfcWorkspaceID = ${tfcWorkspaceID}
echo tfcBearerToken = ${tfcBearerToken}

echo env0OrgID = ${env0OrgID}
echo env0ProjectID = ${env0ProjectID}
echo env0WorkspaceID = ${env0WorkspaceID}
echo env0BearerToken = ${env0BearerToken}
env0OrgPrjID="${env0OrgID}.${env0ProjectID}"
echo env0OrgPrjID = "${env0OrgPrjID}"

# Gathering VCS variables

echo "----------"
echo ">> Gathering VCS variables."

branch=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes.branch' ) 
if [ ${branch} = null ] 
    then branch=main 
fi
echo branch = ${branch}

# workingDirectory=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes.working-directory' ) 
# echo workingDirectory = ${workingDirectory}

# Gathering environment variables

echo "----------"
echo ">> Gathering environment variables."

tfcVariablesData=$( curl -s -X GET -H "Accept: application/json" -H \
"Authorization: Bearer ${tfcBearerToken}" \
https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID}/vars | jq -r '.data[].attributes | "{\"name\": \""+.key+"\", \"value\": \""+(.value)+"\", \"type\": 1},"')
tfcVariables=$(sed '$ s/.$//' <<< $tfcVariablesData)
echo $tfcVariables

# Sync with TFC

terraform init
sleep 30

# Replace TFC Cloud with env0 Cloud

sed -i "" "s/app.terraform.io/backend.api.env0.com/g" provider.tf
sed -i "" "s/${tfcOrgName}/${env0OrgPrjID}/g" provider.tf
sed -i "" "s/${tfcWorkspaceName}/${env0WorkspaceName}/g" provider.tf

# Migrate state to env0

terraform init -migrate-state -force-copy
sleep 30

