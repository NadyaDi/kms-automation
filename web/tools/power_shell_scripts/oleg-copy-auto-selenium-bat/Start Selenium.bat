taskkill /IM "geckodriver.exe" /F
taskkill /IM "chromedriver.exe" /F
taskkill /IM chrome.exe /F
taskkill /IM firefox.exe /F
cd C:\selenium\
start C:\selenium\node_chrome_s3.bat
start C:\selenium\node_firefox_s3.bat
start C:\selenium\Run_AutoIt_Server.bat