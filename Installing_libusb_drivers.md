# Procedure to Install libusb drivers to access Raw HID 

<!-- ## Working With Building Cables
The SSS2 Interface App must be run in Python 3.4. The file SSS2-Interface.py should be opened with Python 3.4 to run. If you are developing files for the different cables, please be sure to set the Universal Flag to True (```UNIVERSAL = True```).
Be sure to commit and Sync all new files to Githup after each development. -->

## Installing libusb drivers using Zadig:
1. Install Zadig from ```https://zadig.akeo.ie/```
   
2. The application needs to run with administrative privileges. To be able to install a driver, you should run the application as a **Administrator**.
3. With the application running, you should see your USB device appear in the dropdown list (click on the dropdown to see all devices).
You can also plug your USB device after Zadig is running, as the list is refreshed automatically. If the list doesnt Auto populate you can go to Options -> List all Devices.

4. Select **Teensyduino RawHID (Interface 0)** from the list drop down.
5. Select **libusb-win32** from the driver dopdown menu and Hit **Replace Driver** Button
      [Zadig Image]('Zadig_1.PNG')

