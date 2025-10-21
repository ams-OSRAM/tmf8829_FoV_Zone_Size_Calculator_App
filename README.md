# Application to calculate field of view for TMF8829
TMF8829 Python utility to calculate FoV (field of view) and projected zone sizes 
<img width="987" height="532" alt="image" src="https://github.com/user-attachments/assets/548a3679-7557-4643-9fd4-691e298c8650" />

## Run program
Executable in 
[TMF8829_FoV_Zone_Size_Calculator.exe](https://github.com/ams-OSRAM/tmf8829_FoV_Zone_Size_Calculator_App/releases/download/1v0/TMF8829_FoV_Zone_Size_Calculator.exe) 
respectively [latest release](https://github.com/ams-OSRAM/tmf8829_FoV_Zone_Size_Calculator_App/releases/latest) or run the Python program TMF8829_FoV_Zone_Size_Calculator.pyw

## Create exe program
To create the executable use
```shell
pyinstaller --onefile --exclude-module pkg_resources TMF8829_FoV_Zone_Size_Calculator.pyw
```
