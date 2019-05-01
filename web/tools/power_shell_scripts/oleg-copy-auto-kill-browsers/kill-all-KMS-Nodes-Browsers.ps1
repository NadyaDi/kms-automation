$computers = Get-Content "Servers.txt"
$Username = 'kaltura.gen@kaltura.com'
$Password = '#H5dCG$pBdqc'
$pass = ConvertTo-SecureString -AsPlainText $Password -Force
$Cred = New-Object System.Management.Automation.PSCredential -ArgumentList $Username,$pass
Invoke-Command -ComputerName $computers -credential $Cred -ErrorAction Stop -ScriptBlock {Invoke-Expression -Command:"cmd.exe /c 'c:\Users\kaltura.gen\Desktop\KillAll.bat'"}