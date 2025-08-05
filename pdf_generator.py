from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from datetime import datetime
import io
from typing import Dict, List

class ITResourcesPDFGenerator:
    def __init__(self):
        self.pagesize = A4
        self.margin = 20 * mm
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            alignment=1,  # Center
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            alignment=1
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica'
        )
    
    def generate_pdf(self, user_data: Dict, output_path: str = None) -> bytes:
        """Generate PDF report from user data"""
        if output_path:
            doc = SimpleDocTemplate(output_path, pagesize=self.pagesize,
                                  rightMargin=self.margin, leftMargin=self.margin,
                                  topMargin=self.margin, bottomMargin=self.margin)
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=self.pagesize,
                                  rightMargin=self.margin, leftMargin=self.margin,
                                  topMargin=self.margin, bottomMargin=self.margin)
        
        # Build the document content
        story = []
        
        # Header
        story.extend(self._build_header())
        story.append(Spacer(1, 12))
        
        # Basic info section
        story.extend(self._build_basic_info(user_data))
        story.append(Spacer(1, 12))
        
        # Worker data section
        story.extend(self._build_worker_data(user_data['user']))
        story.append(Spacer(1, 12))
        
        # IT Resources section
        story.extend(self._build_it_resources(user_data['assets']))
        story.append(Spacer(1, 12))
        
        # Terms and conditions
        story.extend(self._build_terms_conditions())
        
        # Build PDF
        doc.build(story)
        
        if output_path:
            return None
        else:
            buffer.seek(0)
            return buffer.getvalue()
    
    def _build_header(self) -> List:
        """Build the header section"""
        elements = []
        
        # Create header table
        header_data = [
            ['', 'ACTA DE CONTROL DE RECURSOS INFORMÁTICOS', 'PEA-F-AF-TI-002-04']
        ]
        
        header_table = Table(header_data, colWidths=[80*mm, 130*mm, 50*mm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, 0), colors.lightgrey),
        ]))
        
        elements.append(header_table)
        return elements
    
    def _build_basic_info(self, user_data: Dict) -> List:
        """Build basic info section (Código Acta, Empresa, Fecha, Tipo Movimiento)"""
        elements = []
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        act_code = f"{datetime.now().strftime('%Y%m%d')}{user_data['user'].get('id', '001')}"
        
        basic_info_data = [
            ['Código Acta', act_code, 'Fecha', current_date],
            ['Empresa', user_data['user'].get('company', {}).get('name', ''), 'Tipo Movimiento', 'Asignación Directa']
        ]
        
        basic_table = Table(basic_info_data, colWidths=[40*mm, 60*mm, 40*mm, 60*mm])
        basic_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, 1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (0, 1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, 1), colors.lightgrey),
        ]))
        
        elements.append(basic_table)
        return elements
    
    def _build_worker_data(self, user: Dict) -> List:
        """Build worker data section"""
        elements = []
        
        # Section header
        header_data = [['DATOS DEL TRABAJADOR']]
        header_table = Table(header_data, colWidths=[200*mm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        
        # Worker data
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        employee_num = user.get('employee_num', '')
        location = user.get('location', {}).get('name', '') if user.get('location') else ''
        department = user.get('department', {}).get('name', '') if user.get('department') else ''
        job_title = user.get('job_title', '')
        
        worker_data = [
            ['Nombres', full_name, 'DNI', employee_num],
            ['Gerencia', department, 'Área', location],
            ['Centro Costo', '', 'Cargo', job_title]
        ]
        
        worker_table = Table(worker_data, colWidths=[50*mm, 50*mm, 50*mm, 50*mm])
        worker_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ]))
        
        elements.append(worker_table)
        return elements
    
    def _build_it_resources(self, assets: List[Dict]) -> List:
        """Build IT resources section"""
        elements = []
        
        # Section header
        header_data = [['RECURSOS INFORMÁTICOS']]
        header_table = Table(header_data, colWidths=[200*mm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        
        # Basic asset info (first asset if available)
        if assets:
            first_asset = assets[0]
            model_name = first_asset.get('model', {}).get('name', '') if first_asset.get('model') else ''
            asset_tag = first_asset.get('asset_tag', '')
            serial = first_asset.get('serial', '')
            location_name = first_asset.get('location', {}).get('name', '') if first_asset.get('location') else ''
        else:
            model_name = asset_tag = serial = location_name = ''
        
        basic_asset_data = [
            ['Tipo', '', 'Línea', '', 'Marca', ''],
            ['Modelo/Nombre', model_name, 'N° Serie/Licencia', serial, 'Cód Inventario', asset_tag],
            ['Nomb. Dominio', 'HF', 'Sede', location_name, 'Ubi. Técnica', '']
        ]
        
        basic_asset_table = Table(basic_asset_data, colWidths=[33*mm, 33*mm, 33*mm, 33*mm, 33*mm, 33*mm])
        basic_asset_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
            ('BACKGROUND', (4, 0), (4, -1), colors.lightgrey),
        ]))
        
        elements.append(basic_asset_table)
        
        # Characteristics table
        char_header_data = [['Características']]
        char_header_table = Table(char_header_data, colWidths=[200*mm])
        char_header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(char_header_table)
        
        # Characteristics content
        characteristics = [
            ['Nro', 'Característica', 'Descripción'],
            ['1', 'Fecha de Fabricación', ''],
            ['2', 'Disco Duro', ''],
            ['3', 'Guía de Ingreso', ''],
            ['4', 'MAC', ''],
            ['5', 'Memoria', ''],
            ['6', 'Procesador', ''],
            ['7', 'Propietario', ''],
            ['8', 'Serie Cargador', ''],
            ['9', 'Sistema Operativo', ''],
            ['10', 'Tarjeta de Video', ''],
            ['11', 'Tipo de Adquisición', '']
        ]
        
        # Fill characteristics from asset data if available
        if assets:
            asset = assets[0]
            custom_fields = asset.get('custom_fields', {})
            
            # Try to map common fields
            for i, (num, field, desc) in enumerate(characteristics[1:], 1):
                if field == 'MAC' and asset.get('_snipeit_mac_address_1'):
                    characteristics[i][2] = asset.get('_snipeit_mac_address_1', '')
                elif field == 'Sistema Operativo' and asset.get('model', {}).get('manufacturer', {}).get('name'):
                    characteristics[i][2] = asset.get('model', {}).get('manufacturer', {}).get('name', '')
        
        char_table = Table(characteristics, colWidths=[20*mm, 60*mm, 120*mm])
        char_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        
        elements.append(char_table)
        return elements
    
    def _build_terms_conditions(self) -> List:
        """Build terms and conditions section"""
        elements = []
        
        # Section header
        header_data = [['TÉRMINOS Y CONDICIONES GENERALES']]
        header_table = Table(header_data, colWidths=[200*mm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(header_table)
        
        # Terms text
        terms_text = """El usuario se compromete a dar uso adecuado al equipamiento tecnológico que proporciona Hornfrit, el cual será empleado de manera exclusiva para el pago y al beneficio de las funciones. Este equipo tecnológico está prohibida su utilización laboral, el uso de aplicación laboral, el uso de dispositivos de privacidad de los mensajes, correos o información en general que se encuentre almacenada en el equipamiento tecnológico. En ese sentido, el trabajador deberá respetar las normas de control y recursos sobre la adecuada utilización..."""
        
        terms_paragraph = Paragraph(terms_text, self.normal_style)
        
        terms_data = [[terms_paragraph]]
        terms_table = Table(terms_data, colWidths=[200*mm])
        terms_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'JUSTIFY'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(terms_table)
        return elements