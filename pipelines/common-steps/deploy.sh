#!/bin/bash

set -x
du -hs * | sort -h
sam deploy template.yaml --config-env ${ENVIRONMENT} --no-confirm-changeset --force-upload --no-fail-on-empty-changeset --no-progressbar --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-15d0sq06jl9ju

