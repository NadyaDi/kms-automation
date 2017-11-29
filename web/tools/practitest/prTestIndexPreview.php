<html>
	
	<head>	
		
		<link rel="stylesheet" type="text/css" href="./style/style.css" />
		<script src="./siteLib/functions_02.js"></script>
		
		<script>
			
			function target_popup(form) {
				
				var win = window.open('', 'popUpdateTest', 'width=400,height=400,resizeable,scrollbars');
				win.focus();
				
			}
			
			function calculateSlots(txt){
			
				var table = document.getElementById('testCasesTable');
				var slotPlatform = txt.id.substr( txt.id.indexOf("_")+1 );
		
				table.rows[table.rows.length - 2].cells[slotPlatform].innerText = "Platform execution time: " + toHHMMSS(parseInt(txt.value)*parseInt(txt.getAttribute("data-SingleSlotRunTime")));
			
			}
			
			function changeTestStatus(chk){
				
				var table = document.getElementById('testCasesTable');
				var slot = document.getElementById('slot_' + parseInt(chk.id.substr( chk.id.indexOf("_")+1 )));
				
				testExecTime =  toSeconds(table.rows[1+ parseInt(chk.id.substr(0, chk.id.indexOf("^")))].cells[11].innerText);
				platformExecTime = parseInt(slot.getAttribute("data-SingleSlotRunTime"));
				
				if (chk.checked){
					slot.setAttribute("data-SingleSlotRunTime",platformExecTime + testExecTime );
					table.rows[table.rows.length - 2].cells[parseInt(chk.id.substr( chk.id.indexOf("_")+1 ))].innerText = "Platform execution time: " + toHHMMSS(parseInt(slot.value)*(platformExecTime + testExecTime));
				}
				else{
					slot.setAttribute("data-SingleSlotRunTime",platformExecTime - testExecTime );
					table.rows[table.rows.length - 2].cells[parseInt(chk.id.substr( chk.id.indexOf("_")+1 ))].innerText = "Platform execution time: " + toHHMMSS(parseInt(slot.value)*(platformExecTime - testExecTime));
				}	
				
				if (chk.checked == false && chk.getAttribute("data-orgchekedstate") == "true" || chk.checked == true && chk.getAttribute("data-orgchekedstate") == "false" ){
					document.getElementById('lbl_' + chk.id).innerHTML = '<font color = "FFF633" >Update required</font>';
					indexPIPE = chk.id.indexOf("|")
					indexUS   = chk.id.indexOf("_")
					tID  = chk.id.substring(indexPIPE + 1, indexUS);
					document.getElementById('requires_update_' + tID).value = true;
				}				
				else{
					document.getElementById('lbl_' + chk.id).innerHTML = "";
					indexPIPE = chk.id.indexOf("|")
					indexUS   = chk.id.indexOf("_")
					tID  = chk.id.substring(indexPIPE + 1, indexUS);
					document.getElementById('requires_update_' + tID).value = false;
				}
					
			}
			
		</script>
		
	</head>
	
	<body>
		
		<?php
		
			require('config.php');
			
			// Initializations				
			$COLUMN_TEST_NAME  = "Test name";
			$COLUMN_PC         = "PC";
			$COLUMN_MAC        = "MAC";
			$COLUMN_IOS_iPad   = "iPad";
			$COLUMN_IOS_IPHONE = "iPhone";
			$COLUMN_AND_NAT_WITH_CONTROLS    = "Android - Native browser with controls";
			$COLUMN_AND_NAT_WITHOUT_CONTROLS = "Android - Native browser without controls";
			$COLUMN_AND_CHROME = "Android - Chrome";
			$COLUMN_WIN_PHONE  = "Windows Phone";
			$COLUMN_IOS_APP	   = "iOS App";
			$COLUMN_AND_APP	   = "And APP";
			$COLUMN_EXEC_TIME  = "Execution time (HH:MIN:SS)";
			$COLUMN_COMMENT    = "Comment";
		
			$testsTableColumnsIndex = array( 
				0 =>  $COLUMN_TEST_NAME, 
				1 =>  $COLUMN_PC, 
				2 =>  $COLUMN_MAC, 
				3 =>  $COLUMN_IOS_iPad, 
				4 =>  $COLUMN_IOS_IPHONE, 
				5 =>  $COLUMN_AND_NAT_WITH_CONTROLS, 
				6 =>  $COLUMN_AND_NAT_WITHOUT_CONTROLS,
				7 =>  $COLUMN_AND_CHROME, 
				8 =>  $COLUMN_WIN_PHONE,
				9 =>  $COLUMN_IOS_APP,
				10 => $COLUMN_AND_APP,
				11 => $COLUMN_EXEC_TIME,
				12 => $COLUMN_COMMENT   								 
			);
			
			$practTestPlatforms = array( 
				1 =>  "PC", 
				2 =>  "MAC", 
				3 =>  "iPad", 
				4 =>  "iPhone", 
				5 =>  "Android - Native with controls", 
				6 =>  "Android - Native without controls", 
				7 =>  "Android - Chrome", 
				8 =>  "WinPhone",
				9 =>  "iOS - App",
				10 =>  "Android - App"
			);			
			
			$practTestTestComments = array( 
				0 =>  "", 
				1 =>  "", 
				2 =>  "", 
				3 =>  "", 
				4 =>  "", 
				5 =>  "", 
				6 =>  "",
				7 =>  "",
				8 =>  "",
				9 =>  "",
				10 =>  ""

			);
			
			$platformExecTime = array(    1 => 0, 
										  2 => 0, 
										  3 => 0, 
										  4 => 0, 
										  5 => 0, 
										  6 => 0, 
										  7 => 0,
										  8 => 0,
										  9 => 0,
										  10 => 0

								);
			$platformTestCount = array(    1 => 0, 
										  2 => 0, 
										  3 => 0, 
										  4 => 0, 
										  5 => 0, 
										  6 => 0, 
										  7 => 0,
										  8 => 0,
										  9 => 0,
										  10 => 0

								);

			
			$practTestFilterArr = array( 
				"57047" => "Access Control", 
				"57060" => "Additional ui vars parameters", 
				"57072" => "Basics",
				"57058" => "Channel Playlist",
				"57071" => "Delivery Types", 
				"57069" => "Embed Code Types",
				"57068" => "Features",
				"57066" => "Lecture capture",
				"70024" => "Lecture Capture: Dual screen",
				"57065" => "Live Streaming",
				"57046" => "Monetization: Doubleclick",
				"57077" => "Monetization: FreeWheel", 
				"57076" => "Monetization: Others", 
				"57075" => "Monetization: Vast",
				"57074" => "Monetization: Vast events",
				"57059" => "Multiple Playlist: Basics",
				"57064" => "Multiple Playlist: Monetization",
				"57073" => "New API",
				"57061" => "Player plugins configuration",
				"57063" => "Playlist: Basics",    
				"57062" => "Playlist: Monetization",
				"57067" => "Share & Embed"
			);
			
			$suiteDuration  = array();			
			$suiteTestCount = array();
			$errors 		= array();
									
			echo "<button type='submit' form='frmUpdateTest' formaction='prUpdateTest.php' value='Submit'>Update test platforms</button>&nbsp&nbsp&nbsp";
			echo "<button type='submit' form='frmUpdateTest' formaction='prCreateTestSet.php' value='Submit'>Create test sets</button>";
			// Create tests table header
			echo "<form target='popUpdateTest' onsubmit='target_popup(this)' name='frmUpdateTest' method='post' id='frmUpdateTest'></form>";
			echo "<form target='popUpdateTest' onsubmit='target_popup(this)' name='frmUpdateTest' method='post' id='frmUpdateTest'></form>";
			echo "<table class='tg' id='testCasesTable'> <thead><tr align='center'>";
			foreach ($testsTableColumnsIndex as $name => $column) {
					echo "<td class='tg-title'>".$column."</td>";					
			}	
			echo "</tr>";			
			
			$testNum = 0;
			$filterCount = 0;
			foreach ($practTestFilterArr as $filterID => $filter){
				
				// Get test lists from practiTest
				$ch = curl_init();
				curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json", "Authorization: " . $auth_header));
				curl_setopt($ch, CURLOPT_URL, "https://api.practitest.com/api/v1/tests.json?project_id=" . $practiTestProjectID . "&filter_id=" . $filterID . "&api_token=" . $api_token);
				curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
				$jsonResult = curl_exec($ch);
				
				// echo ($jsonResult);
				$objTests = json_decode($jsonResult);
				
				
				if (isset($objTests->data)) {
					foreach ($objTests->data as $test){
		
							// Add test to table
							$testSystemID = $test->system_id;
							$testID 	  = $test->display_id;	
							$testName 	  = $test->name;
							$testPlatform = $test->___f_10734->value;
							$testExecTime = $test->___f_13997->value;
							$testLink     = $test->___f_14115->value;
							$uTestSlots   = $test->___f_14205->value;
							$testSuite    = $filter;
							
							// Basic validation that test data is correct
							if (trim ($testLink) == "")
								$errors[] = "Test: " . $test->display_id . " doesn't have a link";							
							if (trim($testExecTime) == "" or trim($testExecTime) < 30)
								$errors[] = "Test: " . $test->display_id . " doesn't have a execution time or execution time too short";
								
							$practTestTestComments[0] = $test->___f_14107->value;
							$practTestTestComments[1] = $test->___f_14108->value;
							$practTestTestComments[2] = $test->___f_14109->value;
							$practTestTestComments[3] = $test->___f_14110->value;
							$practTestTestComments[4] = $test->___f_14111->value;
							$practTestTestComments[5] = $test->___f_14112->value;
							$practTestTestComments[6] = $test->___f_14113->value;
							$practTestTestComments[7] = $test->___f_14114->value;
							$practTestTestComments[8] = $test->___f_14116->value;
							
							if (array_key_exists($testSuite,$suiteDuration)){
								$suiteDuration[$testSuite]  += $testExecTime;
								$suiteTestCount[$testSuite] += 1;
							}
							else{
								$suiteDuration[$testSuite]  = $testExecTime;
								$suiteTestCount[$testSuite] = 1;
							}	
							$platArray = json_decode($testPlatform);
							$uTestSlotsArray = json_decode($uTestSlots);	
							foreach ($uTestSlotsArray as $slot){
								if (!in_array($slot,$platArray) and (trim ($slot)!=""))
									$errors[] = "Test: " . $testID . " has slots that are unsupported: " . $slot;
							}	
																							
							// Add test name coulum	
							if ($filterCount%2==0)
								echo "<tr name='" . $testSuite .  "' bgcolor='99c1ff'>";
							else	
								echo "<tr name='" . $testSuite .  "' bgcolor='ffcccc'>";
							echo "<td class='tg-text'>";					
							// echo "<form action='prUpdateTest.php' target='popUpdateTest' onsubmit='target_popup(this)' name='frmUpdateTest_" . $testID . " 'method='get' id='frmUpdateTest_" . $testID . "'></form>";
							// echo "<input type='hidden' name='test_id' value='" . $testID . "' form='frmUpdateTest'>";		
							echo "<input type='hidden' id='requires_update_" . $testID . "' name='requires_update_" . $testID . "' value='false' form='frmUpdateTest'>";												
							echo $testSuite . " (" . strval ($filterCount + 1) . "/" . sizeof($practTestFilterArr) . ") - (ID:" . $testID . ") <a href='" . $testLink . "'> " . $testName  . "</a> <a href='https://prod.practitest.com/p/" . $practiTestProjectID . "/tests/" . $testSystemID . "/edit'>  (Edit) </a> </font></center></td>";
		
							// Add platform column
							for ($columnI = 1; $columnI <= count($practTestPlatforms) ; $columnI ++){
								echo "<td class='tg-text'><center>";
								if ( strpos($testPlatform , $practTestPlatforms[$columnI]) !== false ) {
									echo "<font color='green'> Yes</font><br>";
									if ( strpos($uTestSlots , $practTestPlatforms[$columnI]) !== false ){ 
										echo "<input type='checkbox' id='" . $testNum . "^" . $testSuite . "|" . $testID . "_" . $columnI ."' checked  onchange = 'changeTestStatus(this)' form='frmUpdateTest' data-orgChekedState='true' name='chk_". $columnI . "|" . $testID . "'>" . "<label id='lbl_" . $testNum . "^" . $testSuite . "|" . $testID . "_" . $columnI . "'> </label>";
										$platformExecTime[$columnI] += $testExecTime;
										$platformTestCount[$columnI] += 1;
									}
									else
										echo "<input type='checkbox' id='" . $testNum . "^" . $testSuite . "|" . $testID . "_" . $columnI ."' onchange = 'changeTestStatus(this)' form='frmUpdateTest' data-orgChekedState='false' name='chk_". $columnI . "|" . $testID . "'>" . "<label id='lbl_" . $testNum . "^" . $testSuite . "|" . $testID . "_" . $columnI . "'> </label>";
									echo "<br><font color='red'>" . $practTestTestComments[$columnI] . "</font>";
								}
								else {
									echo "<font color='red'> No</font><br>";
								}
								echo "</center></td>";
							}
							
							// Add execution time column
							echo "<td class='tg-text'><center><font color='Blue'>" . gmdate("H:i:s", intval($testExecTime)) ."</font></center></td>";
							
							// Add Generic comment colums 
							echo "<td class='tg-text'><font color='blue'>" .$practTestTestComments[0] . " </font></td>";
							
							echo "</tr>";
						
							$testNum += 1;
			
					}
					$filterCount += 1;
				}
				else{
					$errors[] = "Failed get tests for filter id " .  $filterID . " error : " . $jsonResult;
				}
			}
			
			// Add summary row
			echo "<tr>";
			echo "<td class='tg-text'>Total test cases: " . $testNum . "<br>";
			echo "Total test suites: " . $filterCount . "</td>";
			for ($columnI = 1; $columnI <= count ($practTestPlatforms) ; $columnI ++){
				echo "<td class='tg-text'><b> Platform execution time:</b> " . gmdate("H:i:s", $platformExecTime[$columnI])	 . " <br> <b>Active tests </b>" . strval($platformTestCount[$columnI]) . ". </td>";
			}
			echo "<td class='tg-text'></td><td class='tg-text'></td>";
			echo "</tr>";
			
			// Add slots count row
			echo "<tr>"; 
			echo "<td class='tg-text'># Slots</td>";
			for ($columnI = 1; $columnI <= count ($practTestPlatforms) ; $columnI ++){
				echo "<td class='tg-text'> <textarea rows='2' cols='2' id='slot_" . $columnI ."' data-SingleSlotRunTime='" . $platformExecTime[$columnI] . "' onblur='calculateSlots(this)' >1</textarea> </td>";
			}
			echo "<td class='tg-text'></td><td class='tg-text'></td>";
			echo "</tr>";
			echo "</table>";		
			
			echo "<br><br>";
						
			// Add suiite statistics table
			echo "<table class='tg' id='suitesStats'>";
			echo "<tr align='center'> 
				   <td class='tg-title'> Suite name </td> 
				   <td class='tg-title'> Count </td>
				   <td class='tg-title'> Execution time </td> 
				 </tr>";
			foreach ($suiteDuration as $x => $y){
				echo "<tr>";
				echo "<td class='tg-text'>" . $x . "</td> 
				      <td class='tg-text'>" . $suiteTestCount[$x]  . "</td>
					  <td class='tg-text'>"  . gmdate("H:i:s", $y) .  "</td>";
				echo "</tr>";
			}
			echo "</table>";
			
			// Add errors
			echo "<br><br>";
			echo "<textarea rows='20' cols='60'>";
			foreach ($errors as $error){
				echo $error . "\r\n";
			}
			echo "</textarea>";
			
		?>
	<body>
</html>		