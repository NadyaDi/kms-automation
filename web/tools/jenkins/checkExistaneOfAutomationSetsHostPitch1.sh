#!/bin/bash
testSets=$(curl --silent -H "Content-Type: application/json" "https://api.practitest.com/api/v2/projects/8783/sets.json?filter-id=479917&api_token=deee12e1d8746561e1815d0430814c82c9dbb57d&developer_email=oleg.sigalov@kaltura.com")
if [[ $testSets == *"display-id"* ]]; then
  exit 0
else
  exit 1
fi