#!/bin/bash

#--------------------------------------------------------------------------------------------------------------------------
# Usage: ./count-changes.sh <s3bucketname | tfc_workspace_name>
#
# count-changes.sh counts the amount of version change in an s3 bucket
# 
# Pre-Requisites: 
# if using s3 bucket
# - aws v2 CLI access - if s3 buckets, ensure you're already authenticated to your cloud
# - s3:ListBucketVersions
# if using TFC
# - TF_TOKEN_api_terraform_io - set this env var prior to running the script
# - TFC_ORGANIZATION - set this to your TFC organization name
# - macos (date function specific for macos)
#--------------------------------------------------------------------------------------------------------------------------

# PHASE I - MVP / PoC
# * get version history for an s3 bucket
# * get version history for a TFC workspace
# PHASE II - Expand to multiple buckets/workspaces
# PHASE III - Profit! ($$$)

### VARIABLES
BACKEND_FLAVOR=${BACKEND_FLAVOR:-tfc}       # Which backend type to count (tfc or s3)
WORKSPACE_PREFIX=$1                           # Prefix or actual workspace name

### Error Handling
set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions

trap 'error ${LINENO} ${?}' ERR

### Logging
LOGFILE="count.log"

# ref: https://tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html
function log() {  
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  BROWN='\033[0;33m'
  CYAN='\033[0;36m'
  GRAY='\033[0;37m'
  NC='\033[0m'
  LEVEL=$1
  MSG=$2
  case $LEVEL in
  "INFO") HEADER_COLOR=$GREEN MSG_COLOR=$NC ;;
  "WARN") HEADER_COLOR=$BROWN MSG_COLOR=$NC ;;
  "ERROR") HEADER_COLOR=$RED MSG_COLOR=$NC ;;
  esac
  printf "${HEADER_COLOR}[%-5.5s]${NC} ${MSG_COLOR}%b${NC}" "${LEVEL}" "${MSG}\n"
  printf "[%-5.5s] %b" "${LEVEL}" "${MSG}\n" >> "$LOGFILE"
}

function info() {
  log "INFO" "$1"
}

function warn() {
  log "WARN" "$1"
}

function error() {
  LASTLINE="$1"         # line of error occurrence    
  LASTERR="$2"         # error code    
  log "ERROR" "line ${LASTLINE} with exit code ${LASTERR}"
  exit 1
}

### HELPER FUNCTIONS

function countS3Bucket() {
  info "Looking at changes for \"$1\""

  # S3 Version
  VERSION_STATUS=$(aws s3api get-bucket-versioning --bucket $1 | jq -r '.Status')

  info "Versioning is: $VERSION_STATUS"

  if [[ $VERSION_STATUS != "Enabled" ]]; then
    warn "Skipping Bucket: \"$1\" does not have versioning enabled, this bucket cannot be counted."
  fi

  JQ_OUT=($(aws s3api list-object-versions --bucket $1 --no-paginate | jq -r '.Versions | length, sort_by(.LastModified)[0].LastModified'))

  NUM_CHANGES=${JQ_OUT[0]}
  FIRST_CHANGE=${JQ_OUT[1]}

  info "Number of changes since $FIRST_CHANGE: $NUM_CHANGES"

  calculateChangeVelocity $FIRST_CHANGE $NUM_CHANGES
}


# TFC Version
# input: WORKSPACE_NAME
function countTFC(){

  response=$(curl --silent --location --globoff \
    --header "Authorization: Bearer $TF_TOKEN_api_terraform_io" \
    --header "Content-Type: application/vnd.api+json" \
    "https://app.terraform.io/api/v2/state-versions?filter[workspace][name]=$1&filter[organization][name]=$TFC_ORGANIZATION")

  FIRST_CHANGE=$(echo $response | jq -r '.data | sort_by (.attributes["created-at"])[0] | .attributes["created-at"]')
  NUM_CHANGES=$(echo $response | jq -r '.meta.pagination["total-count"]')
  
  info "Number of changes since $FIRST_CHANGE: $NUM_CHANGES"

  calculateChangeVelocity
}

# Calculate Change Velocity
# INPUTS: $FIRST_CHANGE, $NUM_CHANGES
function calculateChangeVelocity(){
  
  ARCH=$(uname)
  info "You're using $ARCH"

  if [[ $ARCH == "Darwin" ]]; then
    START=$(date -j -f "%Y-%m-%dT%T" $FIRST_CHANGE +%s 2> /dev/null)
    END=$(date +%s)
    DIFF=$(($END-$START)) 
    DIFF_MONTHS=$(printf %.1f "$(($DIFF / 60/60/24/(365/12)))")
    info "$NUM_CHANGES changes over $(( $DIFF / 60/60/24 )) days or $DIFF_MONTHS months"
  else
    warn "this script is currently adapted for MacOS"
    info "manually calculate the change rate from $FIRST_CHANGE to \"Last state change\""
    info "and the number of changes in between: $NUM_CHANGES"
    info "CHANGE_RATE (per month) = NUM_CHANGES / Time diff in months"
  fi
}

                        # The backend prefix to query.

info "Counting State Changes..."

if [[ -z $WORKSPACE_PREFIX ]]; then
  warn "Need bucket prefix or name"
  exit 1
fi

## TODO: List all bucket and count each bucket matching PREFIX
WORKSPACE=$WORKSPACE_PREFIX

case $BACKEND_FLAVOR in 
"tfc")
  if [[ -z $TF_TOKEN_api_terraform_io ]]; then
    warn "Need to set your TFC/TFE credential using: TF_TOKEN_api_terraform_io"
    exit 1
  fi
  if [[ -z $TFC_ORGANIZATION ]]; then
    warn "Need to set your TFC/TFE Organization ID using: `TFC_ORGANIZATION`"
    exit 1
  fi  
  countTFC $WORKSPACE
  ;;
"s3")
  countS3Bucket $WORKSPACE
  ;;
*)
  error "Invalid BACKEND_FLAVOR: $BACKEND_FLAVOR. Valid values: tfc, or s3" ;;
esac





