# kms-automation - Extends the regression functional KMS testing (Python 3.5)

## Installation

* Install latest Chrome/Firefox - English versions
* Install [AutoIt](https://www.autoitscript.com/site/autoit/downloads/)
* Download chromedriver and geckodriver from official sites and put it to C:\Selenium\drivers
* Add C:\Selenium\drivers to PATH
* Download and install [KalturaVirtualDevices](\\Il-fs-01\department\RnD\Back\kaltura virtual devices\)
* Install python 3.5.2
* Install python packages:
  * pytest
  * openpyxl
  * selenium
  * requests
  * pyperclip
  * Pillow
  * pywin32
  * bottle
  
* Install Kaltura python API:
	1. Download Kaltura Python API to any folder
	2. Extract.
	3. Open CMD as administrator
	4. Go to extracted folder path ("cd c:\bla bla\")
	5. Run "python setup.py install"

* Add project's web/lib folder to PYTHONPATH (or mark as a source folder in your IDE)
* Add 'KMS_WEB' global environment variable with a value of web folder full path
* Restart your IDE or command line window

## Configuration

* Edit instance configuration file located at `web/ini/testPartners<env>.csv` where `<env>` is desired environment (defaults to `TestingNewUI`)
* Point to desired environment by editing `LOCAL_SETTINGS_IS_NEW_UI` and `LOCAL_SETTINGS_RUN_ENVIRONMENT` in `web/lib/localSettings.py`

## Usage

* Run tests in the command line (`python -m pytest web/tests`) or configure your IDE to run tests via pytest
