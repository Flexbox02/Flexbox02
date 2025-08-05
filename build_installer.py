#!/usr/bin/env python3
"""
Script para construir instalador de la aplicación GUI para Windows
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuración del build
APP_NAME = "SnipeIT_PDF_Generator"
VERSION = "1.0.0"
AUTHOR = "Tu Nombre"
DESCRIPTION = "Generador de Reportes PDF para Snipe IT"

def clean_build_dirs():
    """Limpiar directorios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Limpiando directorio: {dir_name}")
            shutil.rmtree(dir_name)
    
    # Limpiar archivos .spec
    for spec_file in Path('.').glob('*.spec'):
        print(f"🧹 Eliminando archivo spec: {spec_file}")
        spec_file.unlink()

def install_requirements():
    """Instalar dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_gui.txt'
        ], check=True)
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def create_pyinstaller_spec():
    """Crear archivo de especificación de PyInstaller"""
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Datos adicionales
added_files = []

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'reportlab',
        'reportlab.lib',
        'reportlab.platypus',
        'reportlab.pdfgen',
        'PIL',
        'requests',
        'json'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=None,
)
'''
    
    with open(f'{APP_NAME}.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Archivo spec creado: {APP_NAME}.spec")

def create_version_info():
    """Crear archivo de información de versión para Windows"""
    version_info = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{AUTHOR}'),
        StringStruct(u'FileDescription', u'{DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'© 2024 {AUTHOR}'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'{DESCRIPTION}'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ Archivo de versión creado: version_info.txt")

def build_executable():
    """Construir ejecutable con PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    try:
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            f'{APP_NAME}.spec'
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ Ejecutable construido exitosamente")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo ejecutable: {e}")
        sys.exit(1)

def create_installer_files():
    """Crear archivos adicionales para el instalador"""
    dist_dir = Path('dist')
    
    # Crear README para el usuario
    readme_content = f"""# {DESCRIPTION}

## Instalación

1. Extraiga todos los archivos en una carpeta de su elección
2. Ejecute {APP_NAME}.exe
3. Configure la conexión a su servidor Snipe IT

## Configuración inicial

Al ejecutar la aplicación por primera vez:

1. Haga clic en "Configurar"
2. Ingrese la URL de su servidor Snipe IT
3. Ingrese su token de API de Snipe IT
4. Haga clic en "Probar Conexión" para verificar
5. Guarde la configuración

## Uso

1. Ingrese el correo electrónico del usuario
2. Haga clic en "Buscar Usuario"
3. Revise los activos asignados
4. Haga clic en "Generar Reporte PDF" para crear el documento

## Obtener token de API

Para obtener un token de API en Snipe IT:

1. Inicie sesión en su instalación de Snipe IT
2. Vaya a Account Settings → API Keys
3. Cree un nuevo token
4. Copie el token y úselo en la configuración

## Soporte

Para soporte técnico, contacte al administrador del sistema.

Versión: {VERSION}
"""
    
    readme_path = dist_dir / 'README.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README creado")
    
    # Crear script de instalación básico (batch file)
    install_script = f"""@echo off
echo Instalando {DESCRIPTION}...
echo.

REM Crear directorio en Program Files si no existe
if not exist "C:\\Program Files\\{APP_NAME}" (
    mkdir "C:\\Program Files\\{APP_NAME}"
)

REM Copiar archivos
echo Copiando archivos...
copy "{APP_NAME}.exe" "C:\\Program Files\\{APP_NAME}\\"
copy "README.txt" "C:\\Program Files\\{APP_NAME}\\"

REM Crear acceso directo en el escritorio
echo Creando acceso directo...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\{APP_NAME}.lnk'); $Shortcut.TargetPath = 'C:\\Program Files\\{APP_NAME}\\{APP_NAME}.exe'; $Shortcut.Save()"

echo.
echo Instalacion completada!
echo Puede encontrar el programa en el escritorio o en:
echo C:\\Program Files\\{APP_NAME}\\
echo.
pause
"""
    
    install_path = dist_dir / 'install.bat'
    with open(install_path, 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    print("✅ Script de instalación creado")

def create_zip_package():
    """Crear paquete ZIP para distribución"""
    import zipfile
    from datetime import datetime
    
    dist_dir = Path('dist')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f"{APP_NAME}_v{VERSION}_{timestamp}.zip"
    
    print(f"📦 Creando paquete ZIP: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Agregar ejecutable
        exe_path = dist_dir / f'{APP_NAME}.exe'
        if exe_path.exists():
            zipf.write(exe_path, f'{APP_NAME}.exe')
        
        # Agregar archivos adicionales
        for file_name in ['README.txt', 'install.bat']:
            file_path = dist_dir / file_name
            if file_path.exists():
                zipf.write(file_path, file_name)
    
    print(f"✅ Paquete creado: {zip_name}")
    return zip_name

def main():
    """Función principal"""
    print(f"🚀 Construyendo instalador para {APP_NAME} v{VERSION}")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('main_gui.py'):
        print("❌ Error: No se encuentra main_gui.py")
        print("   Ejecute este script desde el directorio del proyecto")
        sys.exit(1)
    
    try:
        # Paso 1: Limpiar
        clean_build_dirs()
        
        # Paso 2: Instalar dependencias
        install_requirements()
        
        # Paso 3: Crear archivos de configuración
        create_version_info()
        create_pyinstaller_spec()
        
        # Paso 4: Construir ejecutable
        build_executable()
        
        # Paso 5: Crear archivos del instalador
        create_installer_files()
        
        # Paso 6: Crear paquete ZIP
        zip_name = create_zip_package()
        
        print("\n" + "=" * 50)
        print("🎉 ¡Construcción completada exitosamente!")
        print(f"📁 Archivos generados:")
        print(f"   • Ejecutable: dist/{APP_NAME}.exe")
        print(f"   • Paquete: {zip_name}")
        print("\n📋 Instrucciones:")
        print("   1. Distribuya el archivo ZIP a los usuarios")
        print("   2. Los usuarios deben extraer y ejecutar install.bat")
        print("   3. O ejecutar directamente el .exe desde la carpeta dist/")
        
    except KeyboardInterrupt:
        print("\n❌ Construcción cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante la construcción: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()