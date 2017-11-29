<html>
	
	<head>	
		
		<link rel="stylesheet" type="text/css" href="./style/style.css" />
		<script src="./siteLib/functions_02.js"></script>
		
		<script>
		</script>
		
	</head>
	
	<body>
		
		<?php
		
			require('config.php');
		
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
						
			$practTestPlatformsInstacnesPerSet = array( 
							1 =>  array(), 
							2 =>  array(), 
							3 =>  array(), 
							4 =>  array(), 
							5 =>  array(), 
							6 =>  array(), 
							7 =>  array(), 
							8 =>  array(), 
							9 =>  array(),
							10 =>  array()

			);
					
			
			ksort ($_POST);
						
			foreach($_POST as $key => $value){
				if (strpos($key, 'chk') !== false) {
					array_push($practTestPlatformsInstacnesPerSet[substr($key,4,strpos($key, '|')-4)],substr($key,strpos($key, '|')+1));
				}
			}
					
			foreach($practTestPlatformsInstacnesPerSet as $platformID => $testIDsArray){
				
				if (sizeof($testIDsArray) > 0) {				
					
					// Create test set
					$data_string = '{
										"user_id"	 : "' . $user_id .'",
										"project_id" : "' . $practiTestProjectID . '",
										"api_token"  : "' . $api_token . '",
										"name"		 : "' . $practTestPlatforms[$platformID] . '"
									}';
					$ch = curl_init();
					curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json", "Authorization: " . $auth_header));
					curl_setopt($ch, CURLOPT_URL, "https://api.practitest.com/api/v1/sets.json" );
					curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
					curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
					curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);  
					$jsonResult = curl_exec($ch);
					$info = curl_getinfo($ch);
					if ($info['http_code'] == 200){
						$objTest = json_decode($jsonResult);
						if (isset($objTest->id)) {
							$testSetID =  $objTest->id;
							echo ("Created test set id ") . $testSetID . "<br>";

							// Add instances
							$data_string = '{
												"user_id"	: "' . $user_id .'",
												"project_id": "' . $practiTestProjectID . '",
												"api_token" : "' . $api_token . '",
												"test_ids"	: [' . implode (",",$testIDsArray) . ']
											}';
							$ch = curl_init();
							curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json", "Authorization: " . $auth_header));
							curl_setopt($ch, CURLOPT_URL, "https://api.practitest.com/api/v1/sets/" . $testSetID . "/add_instances.json" );
							curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
							curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
							curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);  
							$jsonResult = curl_exec($ch);
							$info = curl_getinfo($ch);
							if (strlen (trim ($jsonResult)) == 0  && $info['http_code'] == 200){
								echo ("Successfully added instances<br>" );
							}
							else{
								echo ("Add instances failed. <br><br> Debug information: <br> Request: <br>" . $data_string . "<br><br>Response: " .$jsonResult . "<br><br> Error Code: " . $info['http_code']);
							}
						}
					}
					else{
						echo ("Create session failed failed. <br><br> Debug information: <br> Request fields: <br>" . $data_string . "<br><br>Response: " .$jsonResult . "<br><br> Error Code: " . $info['http_code']);
					} 
				}
			}
			
		?>
	<body>
</html>		