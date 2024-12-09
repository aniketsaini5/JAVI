; -- javi_setup_file.iss --

[Setup]
AppName=JAVI
AppVersion=1.0
DefaultDirName={pf}\JAVI
DefaultGroupName=JAVI
OutputBaseFilename=JAVIInstaller
SetupIconFile=javi.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\CodeGPT.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}\dist"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "CodeGPT.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "CodeGPT.spec"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\JAVI"; Filename: "{app}\CodeGPT.exe"
Name: "{group}\Uninstall JAVI"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\CodeGPT.exe"; Description: "{cm:LaunchProgram,JAVI}"; Flags: nowait postinstall skipifsilent
