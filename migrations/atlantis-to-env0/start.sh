#!/usr/bin/bash
URL="https://{YOUR_HOSTNAME}.ngrok.io"
SECRET="{YOUR_RANDOM_STRING}"
TOKEN="{YOUR_TOKEN}"
USERNAME="{the username of your GitHub, GitLab or Bitbucket user}"
REPO_ALLOWLIST="$YOUR_GIT_HOST/$YOUR_USERNAME/$YOUR_REPO" #GitLab example: REPO_ALLOWLIST="gitlab.com/public-projects3/infrastructure-software-public/env0-atlantis"
# Any environment variables required for auth
export GOOGLE_APPLICATION_CREDENTIALS="path-to-json-file"

atlantis server \
--atlantis-url="$URL" \
--gitlab-user="$USERNAME" \
--gitlab-token="$TOKEN" \
--gitlab-webhook-secret="$SECRET" \
--repo-allowlist="$REPO_ALLOWLIST"