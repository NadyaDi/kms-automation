#!/bin/bash
export PYTHONPATH=/home/ubuntu/build/workspace/autotest/playerV2/lib/
testSets=$(curl --silent -H "Authorization: custom api_token=b4f9865d8bf732157d4ac3456b8dbd8967e35bfd" -H "Content-Type: application/json" "https://api.practitest.com/api/v1/sets.json?project_id=1596&filter_id=235076" )
if [[ $testSets == *"system_id"* ]]; then
  exit 0
else
  exit 1
fi

