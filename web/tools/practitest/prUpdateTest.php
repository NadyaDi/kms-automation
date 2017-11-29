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
		
			// Initializations	
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
			$updateReuiredTestIDS = array();
		
			// Setting tests details to update			
			$platforms = "";
			ksort ($_POST);
			
			// find tests that are with upgrade required equals to true
			foreach(array_reverse($_POST) as $key => $value){
				if(strpos($value, "true" ) !== false ){ 
					$tID = substr ($key,16);
					$updateReuiredTestIDS[$tID] = "";
					// found all pltforms that need to be updated in the post array
					foreach ($practTestPlatforms as $platformID => $platformName){
						if (array_key_exists ("chk_" . $platformID . "|" . $tID,$_POST)){
							//echo "found " . "chk_" . $platformID . "|" . $tID . "<br>";
							if (strlen($updateReuiredTestIDS[$tID]) >0 ){
								$updateReuiredTestIDS[$tID] = $updateReuiredTestIDS[$tID] . ";"; 
							}
							$updateReuiredTestIDS[$tID] = $updateReuiredTestIDS[$tID] . $platformName;
						}
					}
					// update practitest
					$data_string = '{
										"user_id": "' . $user_id .'",
										"___f_14205": {"value":"' . $updateReuiredTestIDS[$tID] . '"},
										"project_id":"' . $practiTestProjectID . '",
										"api_token" :"' . $api_token . '"
									}';
					$ch = curl_init();
					curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: application/json", "Authorization: " . $auth_header));
					curl_setopt($ch, CURLOPT_URL, "https://api.practitest.com/api/v1/tests/" . $tID   . ".json");
					curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
					curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");                                                                     
					curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);  
					$jsonResult = curl_exec($ch);
					$info = curl_getinfo($ch);
					if (strlen (trim ($jsonResult)) == 0  && $info['http_code'] == 200){
						echo ("Update successfull for test : " . $tID);
					}
					else{
						echo ("Update " . $tID . " failed. <br><br> Debug information: <br> Reuest: <br>" . $data_string . "<br><br>Response: " .$jsonResult . "<br><br> Error Code: " . $info['http_code']);
					}
				}
			}

		?>
	<body>
</html>		