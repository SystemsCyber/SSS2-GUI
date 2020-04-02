; -- SSS2 GUI.iss --

[Setup]
AppName=SSS2-Interface
AppVersion=1.0.5
DefaultDirName={pf}\SSS2
DefaultGroupName=SSS2
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:SSS2
OutputBaseFilename=SetupSSS2Interface
UninstallDisplayIcon={app}\SSS2-Interface

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "*.ico"; DestDir: "{app}"
Source: "*.gif"; DestDir: "{app}"
Source: "*.SSS2"; DestDir: "{userdocs}\SSS2"
Source: "serial_install.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\SSS2 Interface App"; Filename: "{app}\SSS2-Interface.exe" ; WorkingDir: "{app}"
Name: "{group}\Uninstall SSS2 App"; Filename: "{uninstallexe}"

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; 
Name: quicklaunchicon; Description: "Create a &Quick Launch icon";

[Run]
Filename: "{app}\serial_install.exe"; Description: "Install Serial Drivers";
Filename: "{app}\SSS2-Interface.exe"; Description: "Launch application"; Flags: postinstall nowait skipifsilent 