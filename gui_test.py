#!/usr/bin/env python3
"""
Script de prueba para la aplicación GUI de Snipe IT
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Probar que todas las importaciones funcionen"""
    print("🧪 Probando importaciones...")
    
    try:
        # Importaciones básicas
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
        print("  ✅ Tkinter importado correctamente")
        
        # Importaciones de red
        import requests
        print("  ✅ Requests importado correctamente")
        
        # Importaciones de PDF
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table
        print("  ✅ ReportLab importado correctamente")
        
        # Importaciones del proyecto
        from gui_config import GUIConfig
        print("  ✅ GUIConfig importado correctamente")
        
        from gui_snipe_client import GUISnipeITClient
        print("  ✅ GUISnipeITClient importado correctamente")
        
        from gui_config_window import ConfigWindow
        print("  ✅ ConfigWindow importado correctamente")
        
        from main_gui import MainGUI
        print("  ✅ MainGUI importado correctamente")
        
        from pdf_generator import ITResourcesPDFGenerator
        print("  ✅ ITResourcesPDFGenerator importado correctamente")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False

def test_config():
    """Probar funcionalidad de configuración"""
    print("🧪 Probando configuración...")
    
    try:
        from gui_config import GUIConfig
        
        # Crear instancia de configuración
        config = GUIConfig()
        print("  ✅ Instancia de configuración creada")
        
        # Probar métodos básicos
        is_configured = config.is_configured()
        print(f"  📋 Configuración existente: {is_configured}")
        
        # Probar guardado (con datos de prueba)
        test_url = "https://demo.snipeitapp.com"
        test_token = "test_token_12345"
        
        save_result = config.save_config(test_url, test_token)
        print(f"  💾 Guardado de prueba: {'✅' if save_result else '❌'}")
        
        # Verificar datos guardados
        saved_url = config.get_snipe_url()
        saved_token = config.get_api_token()
        
        if saved_url == test_url and saved_token == test_token:
            print("  ✅ Datos guardados correctamente")
        else:
            print("  ❌ Error en datos guardados")
            return False
        
        # Limpiar configuración de prueba
        config.clear_config()
        print("  🧹 Configuración de prueba limpiada")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en configuración: {e}")
        return False

def test_pdf_generation():
    """Probar generación de PDF con datos de prueba"""
    print("🧪 Probando generación de PDF...")
    
    try:
        from pdf_generator import ITResourcesPDFGenerator
        
        # Crear datos de prueba
        test_data = {
            'user': {
                'id': 999,
                'first_name': 'Usuario',
                'last_name': 'Prueba',
                'email': 'usuario.prueba@test.com',
                'employee_num': 'TEST001',
                'job_title': 'Analista de Pruebas',
                'department': {'name': 'Departamento de Testing'},
                'location': {'name': 'Oficina de Pruebas'},
                'company': {'name': 'Empresa de Testing S.A.'}
            },
            'assets': [
                {
                    'id': 1,
                    'name': 'Laptop de Prueba',
                    'asset_tag': 'TEST-LAP-001',
                    'serial': 'SN123456789',
                    'model': {'name': 'Dell Latitude Test'},
                    'status_label': {'name': 'Deployed'},
                    'location': {'name': 'Oficina de Pruebas'},
                    'type': 'hardware'
                },
                {
                    'id': 2,
                    'name': 'Mouse de Prueba',
                    'model_number': 'M-TEST-001',
                    'location': {'name': 'Oficina de Pruebas'},
                    'type': 'accessory'
                }
            ]
        }
        
        # Crear generador de PDF
        pdf_gen = ITResourcesPDFGenerator()
        print("  ✅ Generador de PDF creado")
        
        # Generar PDF de prueba
        test_file = "test_report.pdf"
        pdf_gen.generate_pdf(test_data, test_file)
        
        # Verificar que el archivo fue creado
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"  ✅ PDF generado exitosamente ({file_size} bytes)")
            
            # Limpiar archivo de prueba
            os.remove(test_file)
            print("  🧹 Archivo de prueba eliminado")
            return True
        else:
            print("  ❌ Archivo PDF no fue creado")
            return False
            
    except Exception as e:
        print(f"  ❌ Error generando PDF: {e}")
        return False

def test_gui_creation():
    """Probar creación de ventanas GUI"""
    print("🧪 Probando creación de GUI...")
    
    try:
        # Probar ventana de configuración
        from gui_config_window import ConfigWindow
        
        # Crear ventana sin mostrarla
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        config_window = ConfigWindow(parent=root)
        print("  ✅ Ventana de configuración creada")
        
        # Destruir ventana de prueba
        config_window.window.destroy()
        
        # Probar ventana principal
        from main_gui import MainGUI
        
        # Crear aplicación principal sin ejecutar mainloop
        app = MainGUI()
        print("  ✅ Ventana principal creada")
        
        # Destruir ventana de prueba
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error creando GUI: {e}")
        return False

def test_client_creation():
    """Probar creación del cliente Snipe IT"""
    print("🧪 Probando cliente Snipe IT...")
    
    try:
        from gui_config import GUIConfig
        from gui_snipe_client import GUISnipeITClient
        
        # Crear configuración
        config = GUIConfig()
        
        # Crear cliente
        client = GUISnipeITClient(config)
        print("  ✅ Cliente Snipe IT creado")
        
        # Probar que el cliente maneje correctamente la falta de configuración
        result = client.test_connection()
        if not result['success'] and 'configuración' in result['error'].lower():
            print("  ✅ Cliente maneja correctamente la falta de configuración")
        else:
            print("  ⚠️  Respuesta inesperada del cliente sin configuración")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error creando cliente: {e}")
        return False

def run_interactive_test():
    """Ejecutar prueba interactiva con GUI real"""
    print("🧪 Iniciando prueba interactiva...")
    
    try:
        from main_gui import MainGUI
        
        # Crear aplicación
        app = MainGUI()
        
        # Mostrar mensaje informativo
        messagebox.showinfo(
            "Prueba Interactiva",
            "Se abrirá la aplicación principal.\n\n"
            "Puede probar las siguientes funcionalidades:\n"
            "• Configuración de conexión\n"
            "• Búsqueda de usuarios\n"
            "• Generación de PDFs\n\n"
            "Cierre la aplicación cuando termine."
        )
        
        # Ejecutar aplicación
        app.run()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en prueba interactiva: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la aplicación GUI")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Generación PDF", test_pdf_generation),
        ("Creación GUI", test_gui_creation),
        ("Cliente Snipe IT", test_client_creation),
    ]
    
    results = {}
    
    # Ejecutar pruebas automáticas
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"  ❌ Error ejecutando {test_name}: {e}")
            results[test_name] = False
        print()
    
    # Mostrar resumen
    print("=" * 50)
    print("📊 Resumen de Pruebas:")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        
        # Preguntar si ejecutar prueba interactiva
        import tkinter.messagebox as mb
        root = tk.Tk()
        root.withdraw()
        
        if mb.askyesno(
            "Prueba Interactiva",
            "Todas las pruebas automáticas pasaron.\n\n"
            "¿Desea ejecutar la prueba interactiva con la GUI real?"
        ):
            root.destroy()
            run_interactive_test()
        else:
            root.destroy()
    else:
        print("❌ Algunas pruebas fallaron. Revise los errores anteriores.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)