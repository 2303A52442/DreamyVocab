; ============================================================
;  Personal Vocabulary Tracker  –  Inno Setup Installer
;  Build:  iscc installer.iss   (requires Inno Setup 6+)
; ============================================================

#define AppName      "Personal Vocabulary Tracker"
#define AppVersion   "1.0"
#define AppPublisher "Personal Vocabulary Tracker"
#define AppExeName   "Vocabulary Tracker.exe"
#define AppId        "{{A3F2C1D0-8B4E-4F7A-9E2C-1D0B5A6F8E3C}"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://github.com
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
; Single combined installer exe
OutputDir=installer_out
OutputBaseFilename=VocabTracker-Setup
SetupIconFile=icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
; Require 64-bit Windows
ArchitecturesInstallIn64BitMode=x64compatible
; Don't need admin if installing per-user
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main launcher (PyInstaller exe)
Source: "dist\Vocabulary Tracker.exe"; DestDir: "{app}"; Flags: ignoreversion
; Python backend (PyInstaller exe)
Source: "dist\backend.exe";            DestDir: "{app}"; Flags: ignoreversion
; JavaFX fat JAR
Source: "dist\Tracker.jar";            DestDir: "{app}"; Flags: ignoreversion
; Application icon (used by shortcuts)
Source: "icon.ico";                    DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\{#AppName}";          Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
; Desktop shortcut (optional task)
Name: "{autodesktop}\{#AppName}";    Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Offer to launch immediately after install
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove any leftover files the app might have created in the install folder
Type: filesandordirs; Name: "{app}"

[Code]
function JavaIsInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('java.exe', '-version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

function InitializeSetup(): Boolean;
var
  ErrorCode: Integer;
  Msg: String;
begin
  if not JavaIsInstalled() then
  begin
    Msg := 'Java Runtime Environment (JRE) is required to run {#AppName}.' + Chr(13) + Chr(10) + Chr(13) + Chr(10);
    Msg := Msg + 'Java was not found on this system.' + Chr(13) + Chr(10);
    Msg := Msg + 'Click OK to open the Java download page, then re-run this installer.';
    if MsgBox(Msg, mbError, MB_OKCANCEL) = IDOK then
      ShellExec('open', 'https://www.java.com/en/download/', '', '', SW_SHOW, ewNoWait, ErrorCode);
    Result := False;
  end
  else
    Result := True;
end;
