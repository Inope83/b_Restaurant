// Main JavaScript for Hotel Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Date input validation
    var checkInInput = document.querySelector('input[name="check_in_date"]');
    var checkOutInput = document.querySelector('input[name="check_out_date"]');
    
    if (checkInInput && checkOutInput) {
        checkInInput.addEventListener('change', function() {
            var checkInDate = new Date(this.value);
            var minCheckOut = new Date(checkInDate);
            minCheckOut.setDate(minCheckOut.getDate() + 1);
            
            checkOutInput.min = minCheckOut.toISOString().split('T')[0];
            
            if (checkOutInput.value && new Date(checkOutInput.value) <= checkInDate) {
                checkOutInput.value = '';
            }
        });
    }

    // Room availability checker
    var availabilityForm = document.querySelector('#availability-form');
    if (availabilityForm) {
        availabilityForm.addEventListener('submit', function(e) {
            e.preventDefault();
            checkRoomAvailability();
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Search form auto-submit delay
    var searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        var timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                input.closest('form').submit();
            }, 500);
        });
    });
});

// Room availability checker function
function checkRoomAvailability() {
    var roomId = document.querySelector('input[name="room_id"]').value;
    var checkIn = document.querySelector('input[name="check_in_date"]').value;
    var checkOut = document.querySelector('input[name="check_out_date"]').value;
    
    if (!roomId || !checkIn || !checkOut) {
        return;
    }
    
    showLoadingSpinner();
    
    fetch(`/rooms/check-availability/?room_id=${roomId}&check_in=${checkIn}&check_out=${checkOut}`)
        .then(response => response.json())
        .then(data => {
            hideLoadingSpinner();
            
            var resultDiv = document.querySelector('#availability-result');
            if (data.available) {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i> ${data.message}
                    </div>
                `;
                document.querySelector('#book-button').disabled = false;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-x-circle"></i> ${data.message}
                    </div>
                `;
                document.querySelector('#book-button').disabled = true;
            }
        })
        .catch(error => {
            hideLoadingSpinner();
            console.error('Error:', error);
            showAlert('Error checking availability. Please try again.', 'danger');
        });
}

// Loading spinner functions
function showLoadingSpinner() {
    var spinner = document.createElement('div');
    spinner.className = 'spinner-overlay';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    var spinner = document.querySelector('.spinner-overlay');
    if (spinner) {
        spinner.remove();
    }
}

// Alert function
function showAlert(message, type = 'info') {
    var alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    var container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Price calculator for booking form
function calculatePrice() {
    var checkIn = document.querySelector('input[name="check_in_date"]').value;
    var checkOut = document.querySelector('input[name="check_out_date"]').value;
    var pricePerNight = parseFloat(document.querySelector('#price-per-night').dataset.price);
    var discountPercentage = parseFloat(document.querySelector('#discount-percentage').dataset.discount || 0);
    
    if (checkIn && checkOut && pricePerNight) {
        var checkInDate = new Date(checkIn);
        var checkOutDate = new Date(checkOut);
        var nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));
        
        if (nights > 0) {
            var subtotal = nights * pricePerNight;
            var discount = subtotal * (discountPercentage / 100);
            var total = subtotal - discount;
            
            document.querySelector('#nights-count').textContent = nights;
            document.querySelector('#subtotal-amount').textContent = '$' + subtotal.toFixed(2);
            document.querySelector('#discount-amount').textContent = '$' + discount.toFixed(2);
            document.querySelector('#total-amount').textContent = '$' + total.toFixed(2);
            
            document.querySelector('#price-breakdown').style.display = 'block';
        }
    }
}

// Image gallery modal
function openImageModal(imageSrc, caption) {
    var modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${caption || 'Room Image'}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="${imageSrc}" class="img-fluid" alt="${caption || 'Room Image'}">
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    var bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', function() {
        modal.remove();
    });
}

// Confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }).catch(function() {
        showAlert('Failed to copy to clipboard.', 'danger');
    });
}