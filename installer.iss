#define MyAppName "MiniNotes"
#define MyAppVersion "1.5.0"
#define MyAppPublisher "shimi amos"
#define MyAppExeName "MiniNotes.exe"

[Setup]
AppId={{B8D1F70D-3E4D-4C8A-9F4A-7C3A2D8E1F50}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\MiniNotes
DefaultGroupName=MiniNotes
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=MiniNotes-Setup
SetupIconFile=mininotes.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "he"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\MiniNotes"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\MiniNotes"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"
