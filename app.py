from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import traceback
from datetime import datetime

from config import Config
from snipe_client import SnipeITClient
from pdf_generator import ITResourcesPDFGenerator

app = Flask(__name__)
CORS(app)

# Initialize components
try:
    Config.validate()
    snipe_client = SnipeITClient()
    pdf_generator = ITResourcesPDFGenerator()
    print("✅ Application initialized successfully")
except Exception as e:
    print(f"❌ Error initializing application: {e}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Snipe IT PDF Report Generator'
    })

@app.route('/api/user-report', methods=['POST'])
def generate_user_report():
    """
    Generate PDF report for a user based on their email
    
    Request body:
    {
        "email": "user@example.com"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not isinstance(email, str) or '@' not in email:
            return jsonify({'error': 'Valid email is required'}), 400
        
        print(f"📧 Generating report for user: {email}")
        
        # Fetch user data from Snipe IT
        try:
            user_data = snipe_client.get_user_complete_data(email)
            print(f"✅ User data retrieved for {email}")
        except Exception as e:
            print(f"❌ Error fetching user data: {e}")
            if "not found" in str(e).lower():
                return jsonify({'error': f'User with email {email} not found in Snipe IT'}), 404
            else:
                return jsonify({'error': f'Error fetching user data: {str(e)}'}), 500
        
        # Generate PDF
        try:
            pdf_bytes = pdf_generator.generate_pdf(user_data)
            print(f"✅ PDF generated for {email}")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            traceback.print_exc()
            return jsonify({'error': f'Error generating PDF: {str(e)}'}), 500
        
        # Create response
        pdf_buffer = io.BytesIO(pdf_bytes)
        
        # Generate filename
        user_name = f"{user_data['user'].get('first_name', '')}_{user_data['user'].get('last_name', '')}".strip('_')
        if not user_name:
            user_name = email.split('@')[0]
        
        filename = f"IT_Resources_Report_{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/user-info', methods=['POST'])
def get_user_info():
    """
    Get user information without generating PDF (for testing/debugging)
    
    Request body:
    {
        "email": "user@example.com"
    }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        print(f"📧 Getting info for user: {email}")
        
        # Fetch user data from Snipe IT
        try:
            user_data = snipe_client.get_user_complete_data(email)
            print(f"✅ User data retrieved for {email}")
            
            # Sanitize sensitive information for response
            sanitized_data = {
                'user': {
                    'id': user_data['user'].get('id'),
                    'first_name': user_data['user'].get('first_name'),
                    'last_name': user_data['user'].get('last_name'),
                    'email': user_data['user'].get('email'),
                    'employee_num': user_data['user'].get('employee_num'),
                    'job_title': user_data['user'].get('job_title'),
                    'department': user_data['user'].get('department', {}).get('name') if user_data['user'].get('department') else None,
                    'location': user_data['user'].get('location', {}).get('name') if user_data['user'].get('location') else None,
                    'company': user_data['user'].get('company', {}).get('name') if user_data['user'].get('company') else None,
                },
                'assets_count': len(user_data['assets']),
                'assets': [
                    {
                        'id': asset.get('id'),
                        'asset_tag': asset.get('asset_tag'),
                        'serial': asset.get('serial'),
                        'model': asset.get('model', {}).get('name') if asset.get('model') else None,
                        'status': asset.get('status_label', {}).get('name') if asset.get('status_label') else None,
                    }
                    for asset in user_data['assets']
                ]
            }
            
            return jsonify(sanitized_data)
            
        except Exception as e:
            print(f"❌ Error fetching user data: {e}")
            if "not found" in str(e).lower():
                return jsonify({'error': f'User with email {email} not found in Snipe IT'}), 404
            else:
                return jsonify({'error': f'Error fetching user data: {str(e)}'}), 500
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        print("🚀 Starting Snipe IT PDF Report Generator API...")
        print(f"📍 Snipe IT URL: {Config.SNIPE_IT_URL}")
        print(f"🔧 Debug mode: {Config.FLASK_DEBUG}")
        print(f"🔌 Port: {Config.FLASK_PORT}")
        print("\n📋 Available endpoints:")
        print(f"  • GET  /health - Health check")
        print(f"  • POST /api/user-report - Generate PDF report")
        print(f"  • POST /api/user-info - Get user information (debug)")
        print("\n💡 Example usage:")
        print(f"  curl -X POST http://localhost:{Config.FLASK_PORT}/api/user-report \\")
        print(f"       -H 'Content-Type: application/json' \\")
        print(f"       -d '{{\"email\": \"user@example.com\"}}' \\")
        print(f"       --output report.pdf")
        
        app.run(
            host='0.0.0.0',
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        raise