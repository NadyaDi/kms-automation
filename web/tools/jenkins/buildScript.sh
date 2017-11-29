export PYTHONPATH=$WORKSPACE/playerV2/front-automation/lib
export PYTHONIOENCODING=utf-8
export SESSION_RUN_TIME=$(date '+%m-%d-%y_%H-%M-%S')

testSets=$(curl --silent -H "Authorization: custom api_token=b4f9865d8bf732157d4ac3456b8dbd8967e35bfd" -H "Content-Type: application/json" "https://api.practitest.com/api/v1/sets.json?project_id=1596&filter_id=235076" )
rc=$(echo $testSets | jq -r ".data[0].___f_23982.value")
version=$(echo $testSets | jq -r ".data[0].version")
MD_RELEASE=v$version.$rc
MD_SUITE_NAME=$(echo $testSets | jq -r ".data[0].name")
MD_PRACTITEST_SET_ID=$(echo $testSets | jq -r ".data[0].display_id")

mv $WORKSPACE/playerV2/front-automation/ini/testSetAuto.csv $WORKSPACE/playerV2/front-automation/ini/bak/testSetAuto.csv

mkdir $WORKSPACE/playerV2/front-automation/logs/$BUILD_ID

chmod +x $WORKSPACE/playerV2/front-automation/tools/jenkins/checkExistaneOfAutomationSets.sh

cd $WORKSPACE/playerV2/front-automation/tests_setup
python3 -m py.test --tb=line --env=Auto

cd $WORKSPACE/playerV2/front-automation/tests
python3 -m py.test --tb=line --env=Auto

