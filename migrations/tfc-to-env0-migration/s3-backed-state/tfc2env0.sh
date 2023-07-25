#/bin/bash

# Inputs

echo "----------"
echo ">> Setting inputs"

source inputs.txt
echo tfcOrgName = ${tfcOrgName}
echo tfcWorkspaceID = ${tfcWorkspaceID}
echo env0OrgID = ${env0OrgID}
echo env0ProjectID = ${env0ProjectID}

# Gathering VCS variables

echo "----------"
echo ">> Gathering VCS variables."

workspace=$( curl -s  -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[] | .id' ) 
echo workspace = ${workspace}

envName=$( curl -s  -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes.name' ) 
echo envName = ${envName}

workingDirectory=$( curl -s  -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes."working-directory"' ) 
echo workingDirectory = ${workingDirectory}

terraformFolder=$( curl -s  -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes."vcs-repo".identifier' ) 
echo terraformFolder = ${terraformFolder}

branch=$( curl -s  -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/organizations/${tfcOrgName}/workspaces |  jq -r '.data[].attributes.branch' ) 
if [ ${branch} = null ] 
    then branch=main 
fi
echo branch = ${branch}

# Gathering environment variables

echo "----------"
echo ">> Gathering environment variables."

tfcVariablesData=$( curl -s  -X GET -H "Accept: application/json" -H \
"Authorization: Bearer $tfcBearerToken" \
https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID}/vars | jq -r '.data[].attributes | "{\"name\": \""+.key+"\", \"value\": \""+(.value)+"\", \"type\": 1},"')
tfcVariables=$(sed '$ s/.$//' <<< $tfcVariablesData)
echo $tfcVariables

# Creating API payload

echo "----------"
echo ">> Creating API payload."

generate_post_data()
{
  cat <<EOF
{
	"deployRequest": {
		"ttl": {
			"type": "INFINITE"
		},
		"envName": "$envName",
		"userRequiresApproval": true
	},
	"name": "$envName",
	"projectId": "$env0ProjectID",
	"workspaceName": "$workspace",
	"requiresApproval": true,
	"ttl": {
		"type": "INFINITE"
	},
	"organizationId": "$env0OrgID",
	"repository": "https://github.com/$terraformFolder",
	"revision": "$branch",
	"path": "$workingDirectory",
	"type": "terraform",
	"isSingleUse": true,
	"terraformVersion": "1.2.2",
	"configurationChanges": 
    [${tfcVariables}]
}
EOF
}

# Pushing API payload

echo "----------"
echo ">> Pushing API payload."

curl "https://api.env0.com/environments/without-template" \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer {${env0BearerToken}}" \
-X POST --data "$(generate_post_data)" \
&>/dev/null