#!/bin/bash

#--------------------------------------------------------------------------------------------------------------------------
# Usage: ./count-changes.sh <s3bucketname>
#
# count-changes.sh counts the amount of version change in an s3 bucket
# 
# Pre-Requisites: 
# - aws v2 CLI access
# - s3:ListBucketVersions
# - macos (date function specific for macos)
#--------------------------------------------------------------------------------------------------------------------------

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

### Error Handling

set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions

trap 'error ${LINENO} ${?}' ERR

# --- 
info "Counting State Changes..."

if [[ -z $1 ]]; then
  warn "need bucket name"
  exit 1
else
  BUCKET_NAME=$1
fi

info "Looking at changes for \"$BUCKET_NAME\""

VERSION_STATUS=$(aws s3api get-bucket-versioning --bucket $BUCKET_NAME | jq -r '.Status')

info "Versioning is: $VERSION_STATUS"

if [[ $VERSION_STATUS != "Enabled" ]]; then
  warn "Skipping Bucket: \"$BUCKET_NAME\" does not have versioning enabled, this bucket cannot be counted."
fi

JQ_OUT=($(aws s3api list-object-versions --bucket env0-acme-tfstate --no-paginate | jq -r '.Versions | length, sort_by(.LastModified)[0].LastModified'))

NUM_CHANGES=${JQ_OUT[0]}
FIRST_CHANGE=${JQ_OUT[1]}

info "Number of changes since $FIRST_CHANGE: $NUM_CHANGES"

ARCH=$(uname)
info "You're using $ARCH"

if [[ $ARCH == "Darwin" ]]; then
  START=$(date -j -f "%Y-%m-%dT%T" $FIRST_CHANGE +%s)
  END=$(date +%s)
  DIFF=$(($END-$START)) 
  DIFF_MONTHS=$(printf %.1f "$(($DIFF / 60/60/24/(365/12)))")
  info "$NUM_CHANGES changes over $DIFF seconds or $(( $DIFF / 60/60/24 )) days or $DIFF_MONTHS months"
else
  warn "this script is currently adapted for MacOS"
  info "manually calculate the change rate from $FIRST_CHANGE to \"Last state change\""
  info "and the number of changes in between: $NUM_CHANGES"
  info "CHANGE_RATE (per month) = NUM_CHANGES / Time diff in months"
fi