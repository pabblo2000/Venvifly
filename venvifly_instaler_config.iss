; Script de instalación para Venvify usando Inno Setup

[Setup]
; Nombre de la aplicación
AppName=Venvifly
; Versión de la aplicación
AppVersion=1.1.0
; Nombre del archivo de salida del instalador
OutputBaseFilename=VenviflyInstaller
; Ruta predeterminada donde se instalará la aplicación
DefaultDirName={autopf}\Venvifly
; Nombre de la carpeta del menú de inicio
DefaultGroupName=Venvifly
; Icono del instalador
SetupIconFile=D:\GitHub\Venvifly\venvifly_icon.ico
; Archivo de licencia (si tienes uno)
LicenseFile=D:\GitHub\Venvifly\LICENSE.txt
; Texto que se mostrará en la ventana del instalador
AppCopyright=© 2024 Pablo Álvaro Hidalgo
AppPublisher=Pablo Álvaro Hidalgo
AppPublisherURL=https://github.com/pabblo2000
; Mostrar la opción para crear un acceso directo en el escritorio
CreateAppDir=yes
CreateUninstallRegKey=yes
UninstallDisplayIcon={app}\venvifly_icon.ico
; Requerir permisos de administrador para instalar
PrivilegesRequired=admin
; Estilo moderno para el asistente de instalación
WizardStyle=modern

[Files]
; Incluye el archivo ejecutable de la aplicación compilada con PyInstaller
Source: "D:\GitHub\Venvifly\Venvifly.exe"; DestDir: "{app}"; Flags: ignoreversion
; Incluye el archivo de ícono (opcional si solo se necesita en el acceso directo)
Source: "D:\GitHub\Venvifly\venvifly_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Incluye un archivo README o cualquier otro archivo adicional
Source: "D:\GitHub\Venvifly\README.md"; DestDir: "{app}"; Flags: ignoreversion
; Incluye el archivo de la licencia
Source: "D:\GitHub\Venvifly\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Tasks]
; Opción para crear un acceso directo en el escritorio
Name: "desktopicon"; Description: "Crear un acceso directo en el escritorio"; GroupDescription: "Opciones de instalación"

[Icons]
; Crea un acceso directo en el menú de inicio
Name: "{group}\Venvifly"; Filename: "{app}\Venvifly.exe"; IconFilename: "{app}\venvifly_icon.ico"; WorkingDir: "{app}"

; Crea un acceso directo en el escritorio, solo si se selecciona la opción
Name: "{commondesktop}\Venvifly"; Filename: "{app}\Venvifly.exe"; IconFilename: "{app}\venvifly_icon.ico"; Tasks: desktopicon; WorkingDir: "{app}"


[Run]
; Ejecuta la aplicación después de la instalación (opcional)
Filename: "{app}\Venvifly.exe"; Description: "Ejecutar Venvifly"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Borra automáticamente los archivos creados, si aplicable
Type: files; Name: "{app}\venvifly_icon.ico"
Type: files; Name: "{app}\README.md"
Type: files; Name: "{app}\LICENSE.txt"


