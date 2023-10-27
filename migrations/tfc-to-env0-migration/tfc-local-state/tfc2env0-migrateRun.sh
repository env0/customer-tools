#/bin/bash

# Inputs

echo "----------"
echo ">> Setting inputs"
echo ""

source inputs.txt
env0OrgPrjID="${env0OrgID}.${env0ProjectID}"

# Switching TFC execution mode to local (requires uncommenting in code)
# NOTE: There is an authentication issue here I just can't work out, but if you run this from postman it executes perfectly.

echo "----------"
echo ">> Switching TFC execution mode to local (requires uncommenting in code)."
echo ""

# curl -X PATCH "https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID}" \
# -H 'Content-Type: application/vnd.api+json' \
# -H "Authorization: Bearer {${tfcBearerToken}}" \
# -d ' {"data": {"attributes": {"execution-mode": "local"}}} '

# Gathering environment variables

echo "----------"
echo ">> Gathering workspace variables."

tfcVariablesData=$( curl -s -X GET -H "Accept: application/json" -H \
"Authorization: Bearer ${tfcBearerToken}" \
https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID}/vars | jq -r '.data[].attributes | "{\"name\": \""+.key+"\", \"value\": \""+(.value)+"\", \"category\": \""+(.category)+"\","')
tfcVariables=$(sed '$ s/.$//' <<< $tfcVariablesData)
env0Variables=$(sed 's/'\""category"\"'/'\""type"\"'/g; s/'\""terraform"\"'/'1}'/g; s/'\""env"\"'/'0}'/g' <<< $tfcVariables)
echo "["$env0Variables"]"
echo ""

# Gathering VCS variables

echo "----------"
echo ">> Gathering VCS variables."

branch=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID} |  jq -r '.data.attributes."vcs-repo".branch' ) 
if [ ${branch} = null ] 
    then branch=main 
fi
echo branch = ${branch}

repository=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID} |  jq -r '.data.attributes."vcs-repo"."repository-http-url"' ) 
echo repository = ${repository}

repositoryTrimmed=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID} |  jq -r '.data.attributes."vcs-repo".identifier' ) 
echo repositoryTrimmed = ${repositoryTrimmed}

terraformVersion=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID} |  jq -r '.data.attributes."terraform-version"' ) 
echo terraformVersion = ${terraformVersion}

workingDirectory=$( curl -s -X GET -H "Accept: application/json" -H "Authorization: Bearer ${tfcBearerToken}" https://app.terraform.io/api/v2/workspaces/${tfcWorkspaceID} |  jq -r '.data.attributes."working-directory"' ) 
echo workingDirectory = ${workingDirectory}

echo githubInstallationID = ${githubInstallationID}

echo ""

# Creating API payload

echo "----------"
echo ">> Creating API payload"
echo ""

generate_post_data()
{
  cat <<EOF
{
	"deployRequest": {
		"ttl": {
			"type": "INFINITE",
			"value": "string"
		},
		"envName": "string",
		"userRequiresApproval": true
	},
	"name": "$tfcWorkspaceID",
	"projectId": "$env0ProjectID",
	"workspaceName": "$tfcWorkspaceID",
	"requiresApproval": true,
	"ttl": {
		"type": "INFINITE"
	},
    "continuousDeployment": true,
    "pullRequestPlanDeployments": true,
    "githubInstallationId": $githubInstallationID,
	"organizationId": "$env0OrgID",
	"repository": "$repository",
	"revision": "$branch",
	"path": "$workingDirectory",
	"type": "terraform",
	"isSingleUse": true,
    "terraformVersion": "1.5.7",
    "configurationChanges":
    [ 
        {"type": 0,"name": "ENV0_SKIP_WORKSPACE","value": "true"},
        $env0Variables
    ]
}
EOF
}

# Pushing API payload

echo "----------"
echo ">> Pushing API payload."
echo ""

curl "https://api.env0.com/environments/without-template" \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer {${env0BearerToken}}" \
-X POST --data "$(generate_post_data)" \
&>/dev/null
