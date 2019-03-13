# This file contains the list of servers you want to copy files/folders to
$computers = Get-Content "Servers.txt"

# This is the file/folder(s) you want to copy to the servers in the $computer variable
$files = Get-Content "Files.txt"

# The destination location you want the file/folder(s) to be copied to
$destination = "c$\selenium"

foreach ($computer in $computers){
	foreach ($file in $files){
		if ((Test-Path -Path \\$computer\$destination)){
			Copy-Item $file -Destination \\$computer\$destination -Verbose
		} 
	}
}
