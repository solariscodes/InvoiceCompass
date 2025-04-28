from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, make_response
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from datetime import datetime, timedelta
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invoice')
def invoice():
    return render_template('invoice.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Resources page removed
# @app.route('/resources')
# def resources():
#     return render_template('resources.html')

# All resource pages removed
# @app.route('/invoicing-guide')
# def invoicing_guide():
#     return render_template('invoicing-guide.html')
# 
# @app.route('/invoice-templates')
# def invoice_templates():
#     return render_template('invoice-templates.html')
# 
# @app.route('/tax-calculator')
# def tax_calculator():
#     return render_template('tax-calculator.html')
# 
# @app.route('/international-invoicing')
# def international_invoicing():
#     return render_template('international-invoicing.html')
# 
# @app.route('/faq')
# def faq():
#     return render_template('faq.html')

# Admin routes
@app.route('/admin')
def admin():
    # Check for admin access using environment variable
    admin_key = request.args.get('key')
    
    # Direct admin key - replace this with your actual password
    # This is a fallback if environment variables aren't working
    ADMIN_PASSWORD = "invoicecompass"
    
    # Try to get from environment variable first
    admin_password = os.environ.get('ADMIN_KEY', ADMIN_PASSWORD)
    
    print(f"Debug - Admin key provided: {admin_key}")
    print(f"Debug - Admin password expected: {admin_password}")
    
    if admin_key != admin_password:
        print(f"Debug - Authentication failed: keys don't match")
        return redirect(url_for('index'))
    
    print(f"Debug - Authentication successful")
    
    # HTTP traffic statistics
    total_requests = 12482
    unique_visitors = 4856
    today_requests = 342
    avg_response_time = 0.125  # in seconds
    
    # Mock HTTP request logs
    recent_requests = [
        {
            'id': 'REQ-001',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip': '192.168.1.101',
            'method': 'GET',
            'path': '/',
            'status': '200',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110'
        },
        {
            'id': 'REQ-002',
            'timestamp': (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'),
            'ip': '192.168.1.102',
            'method': 'POST',
            'path': '/generate-pdf',
            'status': '200',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15'
        },
        {
            'id': 'REQ-003',
            'timestamp': (datetime.now() - timedelta(minutes=12)).strftime('%Y-%m-%d %H:%M:%S'),
            'ip': '192.168.1.103',
            'method': 'GET',
            'path': '/invoice',
            'status': '200',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1) AppleWebKit/605.1.15 Mobile/15E148'
        },
        {
            'id': 'REQ-004',
            'timestamp': (datetime.now() - timedelta(minutes=18)).strftime('%Y-%m-%d %H:%M:%S'),
            'ip': '192.168.1.104',
            'method': 'GET',
            'path': '/terms',
            'status': '200',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/91.0'
        },
        {
            'id': 'REQ-005',
            'timestamp': (datetime.now() - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S'),
            'ip': '192.168.1.105',
            'method': 'GET',
            'path': '/privacy',
            'status': '200',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/94.0.4606.81'
        }
    ]
    
    # HTTP access logs
    logs = [
        f"<strong>[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]</strong> 127.0.0.1 - - [GET /admin HTTP/1.1] 200 - Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        f"<strong>[{(datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.102 - - [POST /generate-pdf HTTP/1.1] 200 - Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        f"<strong>[{(datetime.now() - timedelta(minutes=12)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.103 - - [GET /invoice HTTP/1.1] 200 - Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1)",
        f"<strong>[{(datetime.now() - timedelta(minutes=18)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.104 - - [GET /terms HTTP/1.1] 200 - Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        f"<strong>[{(datetime.now() - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.105 - - [GET /privacy HTTP/1.1] 200 - Mozilla/5.0 (X11; Linux x86_64)",
        f"<strong>[{(datetime.now() - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.106 - - [GET / HTTP/1.1] 200 - Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        f"<strong>[{(datetime.now() - timedelta(minutes=42)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.107 - - [GET /favicon.ico HTTP/1.1] 200 - Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        f"<strong>[{(datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.108 - - [GET /static/css/styles.css HTTP/1.1] 200 - Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        f"<strong>[{(datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.109 - - [GET /static/js/main.js HTTP/1.1] 200 - Mozilla/5.0 (X11; Linux x86_64)",
        f"<strong>[{(datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.110 - - [GET /static/images/favicon.svg HTTP/1.1] 200 - Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1)"
    ]
    
    # Add some 404 errors
    logs.append(f"<strong>[{(datetime.now() - timedelta(hours=1, minutes=15)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.111 - - [GET /nonexistent-page HTTP/1.1] 404 - Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    logs.append(f"<strong>[{(datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}]</strong> 192.168.1.112 - - [GET /wp-admin HTTP/1.1] 404 - Mozilla/5.0 (compatible; Googlebot/2.1)")
    
    return render_template('admin.html', 
                           total_requests=total_requests,
                           unique_visitors=unique_visitors,
                           today_requests=today_requests,
                           avg_response_time=avg_response_time,
                           recent_requests=recent_requests,
                           logs=logs)

@app.route('/download_access_logs')
def download_access_logs():
    # Check for admin access using environment variable
    admin_key = request.args.get('key')
    
    # Direct admin key - same as in admin route
    ADMIN_PASSWORD = "invoicecompass"
    
    # Try to get from environment variable first
    admin_password = os.environ.get('ADMIN_KEY', ADMIN_PASSWORD)
    
    print(f"Debug - Download logs - Admin key provided: {admin_key}")
    print(f"Debug - Download logs - Admin password expected: {admin_password}")
    
    if admin_key != admin_password:
        print(f"Debug - Download logs - Authentication failed: keys don't match")
        return redirect(url_for('index'))
    
    print(f"Debug - Download logs - Authentication successful")
    
    # Create a simple log file in Apache Common Log Format
    log_content = f"""# InvoiceCompass HTTP Access Logs
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Format: IP - - [timestamp] "METHOD /path HTTP/1.1" status size "referer" "user-agent"

"""
    
    # Add mock log entries
    for i in range(1, 101):
        log_date = datetime.now() - timedelta(minutes=i*15)
        ip = f"192.168.1.{100+i}"
        methods = ['GET', 'POST', 'GET', 'GET', 'GET']  # More GETs than POSTs
        method = methods[i % len(methods)]
        paths = ['/', '/invoice', '/terms', '/privacy', '/static/css/styles.css', '/static/js/main.js', '/static/images/favicon.svg']
        path = paths[i % len(paths)]
        status = '200'
        size = '1024'
        referer = '-'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/96.0.4664.110'
        
        # Add some 404 errors
        if i % 20 == 0:
            path = '/nonexistent-page'
            status = '404'
            size = '512'
        
        log_content += f"{ip} - - [{log_date.strftime('%d/%b/%Y:%H:%M:%S +0000')}] \"{method} {path} HTTP/1.1\" {status} {size} \"{referer}\" \"{user_agent}\"\n"
    
    # Create a response with the log file
    response = make_response(log_content)
    response.headers["Content-Disposition"] = "attachment; filename=access_logs.txt"
    response.headers["Content-Type"] = "text/plain"
    
    return response

@app.route('/view_request/<request_id>')
def view_request(request_id):
    # This would normally fetch the request details from logs
    # For now, we'll just redirect to the home page
    return redirect(url_for('index'))

@app.route('/sitemap.xml')
def sitemap():
    return send_file('static/sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Get form data
    data = request.json
    
    # Create a PDF in memory
    buffer = io.BytesIO()
    
    # Set up the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Create a list to hold the flowables
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0066ff'),
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#555555')
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333')
    )
    
    # Add company logo if available (placeholder for now)
    # logo_path = os.path.join(app.static_folder, 'img', 'logo.png')
    # if os.path.exists(logo_path):
    #     logo = Image(logo_path, width=2*inch, height=0.75*inch)
    #     elements.append(logo)
    
    # Add invoice title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Create a table for company and client information
    company_data = [
        # Header row
        [Paragraph("<b>FROM</b>", subheading_style), "", Paragraph("<b>TO</b>", subheading_style), ""],
        # Company and client details
        [Paragraph(data['company']['name'] or "Your Company", normal_style), "", 
         Paragraph(data['client']['name'] or "Client Name", normal_style), ""],
        [Paragraph(data['company']['email'] or "company@example.com", normal_style), "", 
         Paragraph(data['client']['email'] or "client@example.com", normal_style), ""],
        [Paragraph(data['company']['phone'] or "(123) 456-7890", normal_style), "", 
         Paragraph(data['client']['phone'] or "(123) 456-7890", normal_style), ""],
        [Paragraph(data['company']['address'] or "123 Company St, City, Country", normal_style), "", 
         Paragraph(data['client']['address'] or "456 Client Ave, City, Country", normal_style), ""]
    ]
    
    # Create a table for invoice details
    invoice_data = [
        # Header row
        [Paragraph("<b>INVOICE DETAILS</b>", subheading_style), ""],
        # Invoice details
        [Paragraph("Invoice Number:", normal_style), 
         Paragraph(data['invoice']['number'] or f"INV-{datetime.now().strftime('%Y%m%d')}", normal_style)],
        [Paragraph("Invoice Date:", normal_style), 
         Paragraph(data['invoice']['date'] or datetime.now().strftime('%Y-%m-%d'), normal_style)],
        [Paragraph("Due Date:", normal_style), 
         Paragraph(data['invoice']['dueDate'] or datetime.now().strftime('%Y-%m-%d'), normal_style)]
    ]
    
    # Create a 2-column table with company/client info and invoice details
    top_table_data = [
        # First row contains both tables
        [
            # First column: Company and client info table
            Table(company_data, colWidths=[1.5*inch, 0.1*inch, 1.5*inch, 0.1*inch]),
            # Second column: Invoice details table
            Table(invoice_data, colWidths=[1.5*inch, 1.5*inch])
        ]
    ]
    
    top_table = Table(top_table_data, colWidths=[4*inch, 3*inch])
    top_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(top_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Add items table
    elements.append(Paragraph("ITEMS", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Create items table header
    items_data = [
        # Header row
        [Paragraph("<b>Description</b>", normal_style),
         Paragraph("<b>Quantity</b>", normal_style),
         Paragraph("<b>Unit Price</b>", normal_style),
         Paragraph("<b>Amount</b>", normal_style)]
    ]
    
    # Add item rows
    for item in data['items']:
        if item['description']:
            items_data.append([
                Paragraph(item['description'], normal_style),
                Paragraph(str(item['quantity']), normal_style),
                Paragraph(f"${item['price']:.2f}", normal_style),
                Paragraph(f"${item['amount']:.2f}", normal_style)
            ])
    
    # Create the items table
    items_table = Table(items_data, colWidths=[4*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
    ]))
    
    elements.append(items_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Calculate totals
    subtotal = data['totals']['subtotal']
    tax_rate = data['invoice']['taxRate']
    tax_amount = data['totals']['taxAmount']
    total = data['totals']['total']
    
    # Create summary table
    summary_data = [
        ["", Paragraph("<b>Subtotal:</b>", normal_style), Paragraph(f"${subtotal:.2f}", normal_style)],
        ["", Paragraph(f"<b>Tax ({tax_rate}%):</b>", normal_style), Paragraph(f"${tax_amount:.2f}", normal_style)],
        ["", Paragraph("<b>Total:</b>", normal_style), Paragraph(f"<b>${total:.2f}</b>", normal_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch, 1*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('LINEABOVE', (1, -1), (2, -1), 1, colors.HexColor('#dddddd')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Add notes and payment terms if provided
    if data['invoice']['notes']:
        elements.append(Paragraph("NOTES", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(data['invoice']['notes'], normal_style))
        elements.append(Spacer(1, 0.3*inch))
    
    if data['invoice']['paymentTerms']:
        elements.append(Paragraph("PAYMENT TERMS", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(data['invoice']['paymentTerms'], normal_style))
        elements.append(Spacer(1, 0.3*inch))
    
    # Add footer
    footer_text = f"Invoice generated by InvoiceCompass.com on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=1  # Center alignment
    )))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value from the buffer
    pdf_value = buffer.getvalue()
    buffer.close()
    
    # Create a unique filename for the PDF
    unique_id = str(uuid.uuid4())[:8]
    clean_invoice_number = ''.join(c if c.isalnum() else '_' for c in data['invoice']['number'])
    filename = f"invoice_{clean_invoice_number}_{unique_id}.pdf"
    
    # Create the pdfs directory if it doesn't exist
    pdf_dir = os.path.join(app.static_folder, 'pdfs')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Save the PDF to a file
    pdf_path = os.path.join(pdf_dir, filename)
    with open(pdf_path, 'wb') as f:
        f.write(pdf_value)
    
    # Return the PDF file path
    return jsonify({
        'success': True,
        'filename': filename,
        'pdfUrl': f"/static/pdfs/{filename}"
    })

@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    pdf_path = os.path.join(app.static_folder, 'pdfs', filename)
    if os.path.exists(pdf_path):
        # Force the browser to download the file instead of opening it
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    else:
        return jsonify({'error': 'File not found'}), 404

# Create the pdfs directory if it doesn't exist
pdfs_dir = os.path.join(app.static_folder, 'pdfs')
os.makedirs(pdfs_dir, exist_ok=True)

if __name__ == '__main__':
    # Use environment variable for port with a default of 5000
    port = int(os.environ.get('PORT', 5000))
    # In development, debug=True. In production, debug=False
    debug = os.environ.get('FLASK_ENV', 'production') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
