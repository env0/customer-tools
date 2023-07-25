#/bin/bash

# Inputs

echo "----------"
echo ">> Setting inputs"

source inputs.txt
echo tfcOrgName = ${tfcOrgName}
echo tfcWorkspaceID = ${tfcWorkspaceID}
echo env0OrgID = ${env0OrgID}
echo env0ProjectID = ${env0ProjectID}

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
	"terraformVersion": "1.2.9",
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