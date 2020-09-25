# A Graphical User Interface for the Smart Sensor Simulator 2
A Python tkinter GUI for the SSS2 that sends and recieves serial commands to the SSS2 over USB.

## For Developers:
if using the latest version we need to have a way to access kernel drivers to read RAW HID. In order to do that we need to install libusb drivers. Please refer to the [Procedure](Installing_libusb_drivers.md)

## Working With Building Cables
The SSS2 Interface App must be run in Python 3.4. The file SSS2-Interface.py should be opened with Python 3.4 to run. If you are developing files for the different cables, please be sure to set the Universal Flag to True (```UNIVERSAL = True```).
Be sure to commit and Sync all new files to Githup after each development.

## Installing the correct files
1. Install Python 3.4 ```https://www.python.org/downloads/release/python-343/```
   1. Open a command prompt by typing `cmd` in the Windows start menu.
   2. Upgrade pip: ```py -3.4 -m pip install --upgrade pip```
   3. Install PySerial: ```py -3.4 -m pip install pyserial```
   4. Install cxFreeze: ```py -3.4 -m pip install cx_freeze```
2. Install the Teensy USB drivers from https://www.pjrc.com/teensy/serial_install.exe
3. Download Github Desktop from https://desktop.github.com/
4. Clone this repository in Github Desktop to work on it.

## Building a Windows Executable
1. Be sure all updated SSS2 files are in the SSS2-GUI directory. This is the default setting when the UNIVERSAL is True.
2. Save all the files are with the latest verison and hash values. 
3. Change directories to ```~/Documents/GitHub/SSS2-GUI/``` or wherever the repository is installed.
3. Change the Universal Flag to False (```UNIVERSAL = False```) for a production release.
4. Package the Python sources into an executable using ```py -3.4 -m createFreeze.py build```
6. Be sure all graphics files are copied into the newly created dist and build directories. This is only needed if new graphics were installed or this is the first build on your computer. 
7. Use Inno windows installer to create a single executable file. http://www.jrsoftware.org/isdl.php#qsp
   1. Open the `windows installer for cx_freeze for SSS2.iss` file.
   1. Change the version number.
   2. Compile it.
   3. Find the executable in Documents/SSS2
   4. Rename the executable with the version number.
   5. Send the executable to a zip file.
   6. Drag all the .SSS2 files from SSS2-GUI into SSS2settings.zip and replace all files inside.
   7. Upload the exe file, and both zip files to the web.
     1. Use WinSCP or equivalent to log into mallory.synercontechnologies.com
     2. Navigate to `/var/www/synercontechnologies.com/files` and drop the files there.
	 3. Open Wordpress https://synercontechnologies.com/wp-admin
	 4. edit the Smart Sensor Simulator 2 page and update the links to the latest version.
7. Log into the website and update the release information with the latest version. 
   1. Write up a list of product improvements since the last release.
   2. Explain what new SSS2 files are available. 
   3. Run the file against https://www.virustotal.com
   4. Print the result to a PDF and upload it to the SSS2 Interface Release Notes page in Wordpress.
8. Add a version number in Github.
8. Set the Universal Flag to True (```UNIVERSAL = True```) to continue work.
9. Commit and Sync to Github
