#!/bin/bash

# export AWS_ACCESS_KEY_ID=minioadmin
# export AWS_SECRET_ACCESS_KEY=minioadmin
# export AWS_DEFAULT_REGION=us-west2

export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

ENDPOINT=http://localhost:80
BUCKET=test-bucket

aws s3 --endpoint=${ENDPOINT} ls

dd if=/dev/zero of=test-24M.obj  bs=24M  count=1

aws s3 --endpoint=${ENDPOINT} cp test-24M.obj s3://${BUCKET}/t.obj 

rm test-24M.obj

# aws s3api --endpoint=${ENDPOINT} get-object-tagging --bucket ${BUCKET} \
#     --key doc1.rtf



