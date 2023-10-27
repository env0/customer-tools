#/bin/bash

# Enabling env0 remote backend
# NOTE there appears to be an authentication issue here as well

echo "----------"
echo ">> Enabling env0 remote backend."
echo ""

curl "https://api.env0.com/environments/${env0envID}" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H "Authorization: Bearer {${env0BearerToken}}" \
-X PUT --data '{"isRemoteBackend": true}'

# Modifying variables

echo "----------"
echo ">> Modifying variables."
echo ""

# NOTE: I wasn't able to get to this, but it requires stage 10 from the documentation: 
# https://docs.env0.com/docs/state-migration#option-1-migrating-the-workspace-using-env0
