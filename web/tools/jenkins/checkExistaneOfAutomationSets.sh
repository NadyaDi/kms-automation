#!/bin/bash
export PYTHONPATH=/home/local/KALTURA/oleg.sigalov/build/workspace/RunAll/web/lib/
testSets=$(curl --silent -H "Content-Type: application/json" "https://api.practitest.com/api/v2/projects/1328/sets.json?filter-id=259788&api_token=deee12e1d8746561e1815d0430814c82c9dbb57d&developer_email=oleg.sigalov@kaltura.com")
if [[ $testSets == *"display-id"* ]]; then
  exit 0
else
  exit 1
fi
