; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=FileExtractor
AppVerName=FileExtractor 1.0.3
AppPublisher=Michael Pilgermann
AppPublisherURL=http://kkfileextractor.sourceforge.net
AppSupportURL=http://kkfileextractor.sourceforge.net
AppUpdatesURL=http://kkfileextractor.sourceforge.net
DefaultDirName={pf}\FileExtractor
DefaultGroupName=FileExtractor
AllowNoIcons=yes
OutputDir=D:\Privat\programming\FileExtractor\sources\dist\DistForInstallation
OutputBaseFilename=FileExtractorSetup-1.0.3
SetupIconFile=D:\Privat\programming\FileExtractor\sources\icons\lupe.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags:

[Files]
Source: "D:\Privat\programming\FileExtractor\sources\dist\FileExtractorWizard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\FileExtractor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\fileextractor_settings.dat"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\gpl.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\fileextractorhelp.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\MSVCR71.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\newicons\*"; DestDir: "{app}\newicons"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\icons\small\*"; DestDir: "{app}\icons\small"; Flags: ignoreversion
Source: "D:\Privat\programming\FileExtractor\sources\dist\dd\*"; DestDir: "{app}\dd"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\FileExtractor"; Filename: "{app}\FileExtractorWizard.exe"
Name: "{group}\FileExtractor (experts)"; Filename: "{app}\FileExtractor.exe"
Name: "{group}\{cm:UninstallProgram,FileExtractor}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\FileExtractor"; Filename: "{app}\FileExtractorWizard.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FileExtractorWizard.exe"; Description: "{cm:LaunchProgram,FileExtractor}"; Flags: nowait postinstall skipifsilent

