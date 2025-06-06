// Main JavaScript file for InvoiceCompass

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

// Helper function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Main document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Update copyright year
    const yearSpan = document.querySelector('#current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Check if we're on the invoice page
    const isInvoicePage = window.location.pathname.includes('/invoice');
    
    // Only run invoice-specific code when on the invoice page
    if (isInvoicePage) {
        initializeInvoicePage();
    }
});

// Function to initialize invoice page functionality
function initializeInvoicePage() {
    console.log("Initializing invoice page...");
    
    // Initialize Flatpickr for date inputs
    if (document.querySelector('#invoice_date')) {
        flatpickr('#invoice_date', {
            dateFormat: 'Y-m-d',
            defaultDate: 'today',
            onChange: function() {
                updatePreview();
            }
        });
    }
    
    if (document.querySelector('#due_date')) {
        flatpickr('#due_date', {
            dateFormat: 'Y-m-d',
            defaultDate: new Date().fp_incr(30), // Default: 30 days from today
            onChange: function() {
                updatePreview();
            }
        });
    }
    
    // Generate invoice number
    const invoiceNumberInput = document.querySelector('#invoice_number');
    if (invoiceNumberInput && !invoiceNumberInput.value) {
        const today = new Date();
        const year = today.getFullYear().toString().substr(-2);
        const month = (today.getMonth() + 1).toString().padStart(2, '0');
        const randomNum = Math.floor(1000 + Math.random() * 9000);
        invoiceNumberInput.value = `INV-${year}${month}-${randomNum}`;
    }
    
    // Item management
    const addItemButton = document.querySelector('#add-item');
    const itemsContainer = document.querySelector('#items-container');
    let itemCount = 0;
    
    if (addItemButton && itemsContainer) {
        // Add initial item if container is empty
        if (itemsContainer.children.length === 0) {
            addItem();
        }
        
        addItemButton.addEventListener('click', function() {
            addItem();
        });
    }
    
    function addItem() {
        const itemRow = document.createElement('div');
        itemRow.className = 'item-row';
        itemRow.dataset.itemId = itemCount;
        
        itemRow.innerHTML = `
            <div>
                <input type="text" class="form-control item-description" placeholder="Item description" required>
            </div>
            <div>
                <input type="number" class="form-control item-quantity" placeholder="Quantity" value="1" min="1" required>
            </div>
            <div>
                <input type="number" class="form-control item-price" placeholder="Price" value="0.00" min="0" step="0.01" required>
            </div>
            <div class="item-amount">$0.00</div>
            <div>
                <button type="button" class="btn-remove-item" data-item-id="${itemCount}">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        itemsContainer.appendChild(itemRow);
        
        // Add event listeners for calculation
        const quantityInput = itemRow.querySelector('.item-quantity');
        const priceInput = itemRow.querySelector('.item-price');
        const amountDiv = itemRow.querySelector('.item-amount');
        
        function calculateItemAmount() {
            const quantity = parseFloat(quantityInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            const amount = quantity * price;
            amountDiv.textContent = `$${amount.toFixed(2)}`;
            calculateTotal();
        }
        
        quantityInput.addEventListener('input', calculateItemAmount);
        priceInput.addEventListener('input', calculateItemAmount);
        
        // Calculate initial amount
        calculateItemAmount();
        
        // Remove item button
        const removeButton = itemRow.querySelector('.btn-remove-item');
        removeButton.addEventListener('click', function() {
            itemRow.remove();
            calculateTotal();
            
            // If all items are removed, add a new empty one
            if (itemsContainer.children.length === 0) {
                addItem();
            }
        });
        
        itemCount++;
    }
    
    // Calculate total
    function calculateTotal() {
        const itemRows = document.querySelectorAll('.item-row');
        let subtotal = 0;
        
        itemRows.forEach(row => {
            const quantity = parseFloat(row.querySelector('.item-quantity').value) || 0;
            const price = parseFloat(row.querySelector('.item-price').value) || 0;
            subtotal += quantity * price;
        });
        
        const taxRateInput = document.querySelector('#tax_rate');
        const taxRate = taxRateInput ? (parseFloat(taxRateInput.value) || 0) : 0;
        const taxAmount = subtotal * (taxRate / 100);
        const total = subtotal + taxAmount;
        
        // Update summary elements
        const subtotalElement = document.querySelector('#subtotal');
        const taxElement = document.querySelector('#tax_amount');
        const totalElement = document.querySelector('#total-amount');
        
        if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        if (taxElement) taxElement.textContent = `$${taxAmount.toFixed(2)}`;
        if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
        
        return { subtotal, taxAmount, total };
    }
    
    // Tax rate change handler
    const taxRateInput = document.querySelector('#tax_rate');
    if (taxRateInput) {
        taxRateInput.addEventListener('input', calculateTotal);
    }
    
    // Generate PDF
    const generatePdfButton = document.querySelector('#generate-pdf');
    if (generatePdfButton) {
        generatePdfButton.addEventListener('click', function() {
            // Collect form data
            const formData = {
                company: {
                    name: document.querySelector('#company_name')?.value || '',
                    email: document.querySelector('#company_email')?.value || '',
                    phone: document.querySelector('#company_phone')?.value || '',
                    address: document.querySelector('#company_address')?.value || ''
                },
                client: {
                    name: document.querySelector('#client_name')?.value || '',
                    email: document.querySelector('#client_email')?.value || '',
                    phone: document.querySelector('#client_phone')?.value || '',
                    address: document.querySelector('#client_address')?.value || ''
                },
                invoice: {
                    number: document.querySelector('#invoice_number')?.value || '',
                    date: document.querySelector('#invoice_date')?.value || '',
                    dueDate: document.querySelector('#due_date')?.value || '',
                    taxRate: parseFloat(document.querySelector('#tax_rate')?.value || 0),
                    notes: document.querySelector('#notes')?.value || '',
                    paymentTerms: document.querySelector('#payment_terms')?.value || ''
                },
                items: []
            };
            
            // Collect items
            const itemRows = document.querySelectorAll('.item-row');
            itemRows.forEach(row => {
                const item = {
                    description: row.querySelector('.item-description')?.value || '',
                    quantity: parseFloat(row.querySelector('.item-quantity')?.value || 0),
                    price: parseFloat(row.querySelector('.item-price')?.value || 0),
                    amount: parseFloat(row.querySelector('.item-quantity')?.value || 0) * parseFloat(row.querySelector('.item-price')?.value || 0)
                };
                
                formData.items.push(item);
            });
            
            // Calculate totals
            const totals = calculateTotal();
            formData.totals = totals;
            
            // Send data to server
            fetch('/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success modal
                    const filenameElement = document.querySelector('#pdf-filename');
                    const downloadLink = document.querySelector('#download-pdf');
                    
                    if (filenameElement) filenameElement.textContent = data.filename;
                    if (downloadLink) {
                        // Set the download attribute to force download
                        downloadLink.href = `/download-pdf/${data.filename}`;
                        
                        // Add click event listener to handle the download
                        downloadLink.addEventListener('click', function(e) {
                            e.preventDefault();
                            window.location.href = `/download-pdf/${data.filename}`;
                        });
                    }
                    
                    const pdfModal = new bootstrap.Modal(document.querySelector('#pdfModal'));
                    pdfModal.show();
                } else {
                    alert('Error generating PDF: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while generating the PDF.');
            });
        });
    }
    
    // Email functionality removed
    
    // End of invoice page functionality
    
    // Currency formatting for inputs
    document.querySelectorAll('.currency-input').forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value) || 0;
            this.value = value.toFixed(2);
        });
    });
    
    // Add live preview functionality
    function updatePreview() {
        const previewContainer = document.querySelector('#invoice-preview');
        if (!previewContainer) return;
        
        // Clear placeholder if exists
        const placeholder = previewContainer.querySelector('.preview-placeholder');
        if (placeholder) {
            placeholder.style.display = 'none';
        }
        
        // Create or update the preview content
        let previewContent = previewContainer.querySelector('.preview-content-inner');
        if (!previewContent) {
            previewContent = document.createElement('div');
            previewContent.className = 'preview-content-inner';
            previewContainer.appendChild(previewContent);
        }
        
        // Populate preview with form data
        const companyName = document.querySelector('#company_name')?.value || 'Your Business';
        const clientName = document.querySelector('#client_name')?.value || 'Client Name';
        const invoiceNumber = document.querySelector('#invoice_number')?.value || 'INV-0000';
        const invoiceDate = document.querySelector('#invoice_date')?.value || 'Today';
        const dueDate = document.querySelector('#due_date')?.value || 'Due Date';
        
        // Get totals
        const totals = calculateTotal();
        
        // Create preview HTML
        previewContent.innerHTML = `
            <div class="preview-header-section">
                <div class="preview-logo">INVOICE</div>
                <div class="preview-invoice-info">
                    <div><strong>Invoice #:</strong> ${invoiceNumber}</div>
                    <div><strong>Date:</strong> ${invoiceDate}</div>
                    <div><strong>Due Date:</strong> ${dueDate}</div>
                </div>
            </div>
            
            <div class="preview-addresses">
                <div class="preview-from">
                    <div class="preview-label">FROM</div>
                    <div class="preview-company">${companyName}</div>
                    <div>${document.querySelector('#company_email')?.value || ''}</div>
                    <div>${document.querySelector('#company_phone')?.value || ''}</div>
                    <div>${document.querySelector('#company_address')?.value || ''}</div>
                </div>
                
                <div class="preview-to">
                    <div class="preview-label">TO</div>
                    <div class="preview-client">${clientName}</div>
                    <div>${document.querySelector('#client_email')?.value || ''}</div>
                    <div>${document.querySelector('#client_phone')?.value || ''}</div>
                    <div>${document.querySelector('#client_address')?.value || ''}</div>
                </div>
            </div>
            
            <div class="preview-items">
                <table class="preview-items-table">
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th>Qty</th>
                            <th>Price</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${getItemsHTML()}
                    </tbody>
                </table>
            </div>
            
            <div class="preview-summary">
                <div class="preview-summary-row">
                    <div>Subtotal</div>
                    <div>$${totals.subtotal.toFixed(2)}</div>
                </div>
                <div class="preview-summary-row">
                    <div>Tax (${document.querySelector('#tax_rate')?.value || '0'}%)</div>
                    <div>$${totals.taxAmount.toFixed(2)}</div>
                </div>
                <div class="preview-summary-row preview-total">
                    <div>Total</div>
                    <div>$${totals.total.toFixed(2)}</div>
                </div>
            </div>
            
            <div class="preview-notes">
                <div class="preview-notes-section">
                    <div class="preview-label">Notes</div>
                    <div>${document.querySelector('#notes')?.value || 'No notes'}</div>
                </div>
                <div class="preview-terms-section">
                    <div class="preview-label">Payment Terms</div>
                    <div>${document.querySelector('#payment_terms')?.value || 'No payment terms'}</div>
                </div>
            </div>
        `;
    }
    
    // Helper function to generate items HTML for preview
    function getItemsHTML() {
        const itemRows = document.querySelectorAll('.item-row');
        if (!itemRows.length) return '<tr><td colspan="4">No items</td></tr>';
        
        let html = '';
        itemRows.forEach(row => {
            const description = row.querySelector('.item-description')?.value || 'Item';
            const quantity = row.querySelector('.item-quantity')?.value || '1';
            const price = parseFloat(row.querySelector('.item-price')?.value || '0').toFixed(2);
            const amount = (parseFloat(quantity) * parseFloat(price)).toFixed(2);
            
            html += `
                <tr>
                    <td>${description}</td>
                    <td>${quantity}</td>
                    <td>$${price}</td>
                    <td>$${amount}</td>
                </tr>
            `;
        });
        
        return html;
    }
    
    // Add event listeners to form fields to update preview
    const formFields = [
        '#company_name', '#company_email', '#company_phone', '#company_address',
        '#client_name', '#client_email', '#client_phone', '#client_address',
        '#invoice_number', '#notes', '#payment_terms', '#tax_rate'
    ];
    
    formFields.forEach(selector => {
        const field = document.querySelector(selector);
        if (field) {
            field.addEventListener('input', updatePreview);
        }
    });
    
    // Add event delegation for item inputs
    const invoiceForm = document.querySelector('#invoiceForm');
    if (invoiceForm) {
        invoiceForm.addEventListener('input', function(e) {
            if (e.target.classList.contains('item-description') || 
                e.target.classList.contains('item-quantity') || 
                e.target.classList.contains('item-price')) {
                updatePreview();
            }
        });
    }
    
    // Initialize preview
    updatePreview();
    
    // Initialize the first calculation
    calculateTotal();
}
