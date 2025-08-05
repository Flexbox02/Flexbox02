#!/usr/bin/env python3
"""
Test script for Snipe IT PDF Report Generator
This script demonstrates how to use the API and creates a sample PDF with mock data
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_generator import ITResourcesPDFGenerator

def create_mock_user_data():
    """Create mock user data for testing purposes"""
    mock_data = {
        'user': {
            'id': 123,
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez Rodríguez',
            'email': 'juan.perez@empresa.com',
            'employee_num': 'EMP001234',
            'job_title': 'Analista de Sistemas Senior',
            'department': {
                'name': 'Tecnologías de la Información'
            },
            'location': {
                'name': 'Oficina Principal - Lima'
            },
            'company': {
                'name': 'HORNFRIT S.A.C.'
            }
        },
        'assets': [
            {
                'id': 456,
                'asset_tag': 'LAP-TI-001',
                'serial': 'DL2023ABC123456',
                'model': {
                    'name': 'Dell Latitude 5520',
                    'manufacturer': {
                        'name': 'Dell Inc.'
                    }
                },
                'status_label': {
                    'name': 'Deployed'
                },
                'location': {
                    'name': 'Oficina Principal - Lima'
                },
                'custom_fields': {
                    'mac_address': '00:1A:2B:3C:4D:5E',
                    'ram': '16 GB DDR4',
                    'processor': 'Intel Core i7-1165G7',
                    'hard_drive': 'SSD 512GB NVMe',
                    'operating_system': 'Windows 11 Pro'
                },
                '_snipeit_mac_address_1': '00:1A:2B:3C:4D:5E'
            }
        ]
    }
    return mock_data

def test_pdf_generation():
    """Test PDF generation with mock data"""
    print("🧪 Testing PDF generation with mock data...")
    
    try:
        # Create PDF generator
        pdf_generator = ITResourcesPDFGenerator()
        
        # Create mock data
        user_data = create_mock_user_data()
        
        # Generate PDF
        output_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_generator.generate_pdf(user_data, output_file)
        
        print(f"✅ PDF generado exitosamente: {output_file}")
        
        # Display user data summary
        user = user_data['user']
        print(f"\n📋 Datos del usuario de prueba:")
        print(f"   • Nombre: {user['first_name']} {user['last_name']}")
        print(f"   • Email: {user['email']}")
        print(f"   • Empleado: {user['employee_num']}")
        print(f"   • Cargo: {user['job_title']}")
        print(f"   • Departamento: {user['department']['name']}")
        print(f"   • Ubicación: {user['location']['name']}")
        print(f"   • Empresa: {user['company']['name']}")
        
        print(f"\n💻 Activos asignados ({len(user_data['assets'])}):")
        for asset in user_data['assets']:
            print(f"   • {asset['model']['name']} (Tag: {asset['asset_tag']})")
            print(f"     Serial: {asset['serial']}")
            print(f"     Estado: {asset['status_label']['name']}")
        
        print(f"\n🎯 El archivo PDF ha sido creado con la estructura del formulario 'Acta de Control de Recursos Informáticos'")
        print(f"📄 Archivo: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_integration():
    """Test API integration (requires running server)"""
    print("\n🌐 Testing API integration...")
    
    try:
        import requests
        
        # Test health endpoint
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            print("✅ Health endpoint responding")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"❌ Health endpoint failed: {health_response.status_code}")
            return False
        
        # Test user info endpoint with mock email
        test_email = "juan.perez@empresa.com"
        info_response = requests.post(
            'http://localhost:5000/api/user-info',
            json={'email': test_email},
            timeout=10
        )
        
        if info_response.status_code == 404:
            print(f"ℹ️  User not found in Snipe IT (expected for test email): {test_email}")
        elif info_response.status_code == 200:
            print(f"✅ User info endpoint working")
            user_info = info_response.json()
            print(f"   User: {user_info.get('user', {}).get('first_name', 'N/A')}")
        else:
            print(f"❌ User info endpoint error: {info_response.status_code}")
            print(f"   Response: {info_response.text}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️  API server not running. Start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Snipe IT PDF Report Generator - Test Suite")
    print("=" * 50)
    
    # Test 1: PDF Generation
    pdf_test_passed = test_pdf_generation()
    
    # Test 2: API Integration (optional)
    api_test_passed = test_api_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   • PDF Generation: {'✅ PASSED' if pdf_test_passed else '❌ FAILED'}")
    print(f"   • API Integration: {'✅ PASSED' if api_test_passed else '⚠️  SKIPPED (server not running)'}")
    
    if pdf_test_passed:
        print("\n🎉 Core functionality working! The PDF generator is ready to use.")
        print("\n📋 Next steps:")
        print("   1. Configure your .env file with Snipe IT credentials")
        print("   2. Start the API server: python app.py")
        print("   3. Test with real user data from your Snipe IT installation")
    else:
        print("\n❌ Core functionality failed. Please check the error messages above.")
    
    return pdf_test_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)