# This file contains the list of servers you want to copy files/folders to
$computers = Get-Content "Servers.txt"

# This is the file/folder(s) you want to copy to the servers in the $computer variable
$source = "KillAll.bat"

# The destination location you want the file/folder(s) to be copied to
$destination = "c$\Users\kaltura.gen\Desktop"

foreach ($computer in $computers) 
{
if ((Test-Path -Path \\$computer\$destination))
{
Copy-Item $source -Destination \\$computer\$destination -Verbose
} 
}
