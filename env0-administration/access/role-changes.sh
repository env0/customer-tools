# Script to loop through all ENV0 projects to move all Admin role teams to Custom-Admin Role
UserAuth=""

## Query projects
curl --request GET \
     --user $UserAuth \
     --url 'https://api.env0.com/projects?organizationId=[ORD-ID]' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' | jq '.[].id' >> env0_projects.txt

## For each project, find teams with admin permissions except orgadmin.
for i in cat env0_projects.txt
do
     teamid=$(curl --request GET --user $UserAuth --url "https://api.env0.com/teams/assignments?projectId=${i}" --header 'accept: application/json' --header 'content-type: application/json' | jq '.[] | select(.projectRole == "Admin")' | jq '. | select(.teamId != "[TEAM-ID]")' | jq -r '.teamId')
     echo $teamid

## For each teamid
for e in echo $teamid
do
DATA=$(cat <<EOF
{"teamId": "${e}","projectId": "${i}","projectRole": "Custom-Admin"}
EOF
)
echo $DATA
curl --request POST \
     --user $UserAuth \
     --url https://api.env0.com/teams/assignments \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data "${DATA}"
done
done
