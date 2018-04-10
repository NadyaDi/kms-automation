export KMS_WEB=$WORKSPACE/web/
export PYTHONPATH=$WORKSPACE/web/lib/
export PYTHONIOENCODING=utf-8
export SESSION_RUN_TIME=$(date '+%m-%d-%y_%H-%M-%S')

testSets=$(curl --silent -H "Content-Type: application/json" "https://api.practitest.com/api/v2/projects/1328/sets.json?filter-id=259788&api_token=deee12e1d8746561e1815d0430814c82c9dbb57d&developer_email=oleg.sigalov@kaltura.com")
AutomationEnv=$(echo $testSets | jq -r ".data[0].attributes[\"custom-fields\"][\"---f-30772\"]")
version=$(echo $testSets | jq -r ".data[0].attributes.version")
MD_RELEASE=v$version
AUTO_ENV=$AutomationEnv
MD_SUITE_NAME=$(echo $testSets | jq -r ".data[0].attributes.name")
MD_PRACTITEST_SET_ID=$(echo $testSets | jq -r ".data[0].attributes[\"display-id\"]")

if [ -f $WORKSPACE/web/ini/testSetAuto.csv ]; then
   mv $WORKSPACE/web/ini/testSetAuto.csv $WORKSPACE/web/ini/bak/testSetAuto.csv 
fi

mkdir $WORKSPACE/logs/$BUILD_ID

chmod +x $WORKSPACE/web/tools/jenkins/checkExistaneOfAutomationSets.sh

cd $WORKSPACE/web/tests_setup
python3 -m pytest --tb=line --env=Auto

cd $WORKSPACE/web/tests
python3 -m pytest --tb=line --env=Auto

echo $MD_PRACTITEST_SET_ID
