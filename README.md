# InvoiceCompass

InvoiceCompass is a **100% free**, modern, user-friendly web application for generating professional invoices. The application guides users through a simple step-by-step process to create and download customized PDF invoices with no hidden fees or limitations.

## Features

- **100% Free**: Create unlimited invoices with no hidden fees
- Clean, intuitive user interface with step-by-step form
- Professional PDF invoice generation with customizable details
- Real-time invoice preview as you type
- Dynamic invoice item management (add, remove items easily)
- Automatic tax calculation and totaling
- Responsive design that works on desktop and mobile devices
- No account or registration required

## Installation

1. Clone the repository
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Navigate to the "Create Invoice" page
2. Fill in your company information
3. Add client details and invoice information
4. Add invoice items with descriptions, quantities, and prices
5. Review your invoice and generate a PDF
6. Download the PDF invoice

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: ReportLab
- **Styling**: Bootstrap 5
- **Icons**: Font Awesome
- **Date Picker**: Flatpickr

## Project Structure

```
invoice-generator/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css      # Custom CSS styles
│   ├── js/
│   │   └── main.js         # JavaScript functionality
│   └── images/             # Image assets
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── index.html          # Homepage
│   └── invoice.html        # Invoice creation page
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who helped shape this project
