// Custom JavaScript for Child Vaccination Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeSearch();
    initializeForms();
    initializeTooltips();
    initializeModals();
    initializeAnimations();
    initializeCalendar();
    initializeQuickActions();
    initializeNotifications();
});

// Search functionality
function initializeSearch() {
    const quickSearch = document.getElementById('quickSearch');
    if (quickSearch) {
        let searchTimeout;
        
        quickSearch.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                clearSearchResults();
            }
        });
        
        quickSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = e.target.value.trim();
                if (query) {
                    window.location.href = `/children/?q=${encodeURIComponent(query)}`;
                }
            }
        });
    }
}

function performSearch(query) {
    showLoading();
    
    fetch(`/api/search/?q=${encodeURIComponent(query)}&type=all`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            displaySearchResults(data);
        })
        .catch(error => {
            hideLoading();
            console.error('Search error:', error);
            showNotification('Search failed. Please try again.', 'danger');
        });
}

function displaySearchResults(results) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    let html = '';
    
    if (results.children && results.children.length > 0) {
        html += '<div class="search-section"><h6>Children</h6><div class="list-group">';
        results.children.forEach(child => {
            html += `
                <a href="/children/${child.id}/" class="list-group-item list-group-item-action">
                    <div class="d-flex justify-content-between">
                        <div>
                            <strong>${child.name}</strong>
                            <small class="text-muted d-block">${child.age} years old</small>
                        </div>
                        <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                </a>
            `;
        });
        html += '</div></div>';
    }
    
    if (results.vaccines && results.vaccines.length > 0) {
        html += '<div class="search-section"><h6>Vaccines</h6><div class="list-group">';
        results.vaccines.forEach(vaccine => {
            html += `
                <a href="/vaccines/${vaccine.id}/" class="list-group-item list-group-item-action">
                    <div class="d-flex justify-content-between">
                        <div>
                            <strong>${vaccine.name}</strong>
                            <small class="text-muted d-block">${vaccine.manufacturer}</small>
                        </div>
                        <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                </a>
            `;
        });
        html += '</div></div>';
    }
    
    if (html === '') {
        html = '<div class="text-center py-4"><p class="text-muted">No results found</p></div>';
    }
    
    resultsContainer.innerHTML = html;
    resultsContainer.style.display = 'block';
}

function clearSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
}

// Form enhancements
function initializeForms() {
    // Auto-save functionality
    const forms = document.querySelectorAll('form[data-auto-save]');
    forms.forEach(form => {
        let autoSaveTimeout;
        
        form.addEventListener('input', function() {
            clearTimeout(autoSaveTimeout);
            autoSaveTimeout = setTimeout(() => {
                autoSaveForm(form);
            }, 2000);
        });
    });
    
    // Form validation
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            validateField(field);
        });
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[name*="phone"], input[name*="contact"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', formatPhoneNumber);
    });
    
    // Date picker enhancements
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set max date to today for birth dates
        if (input.name.includes('birth')) {
            input.max = new Date().toISOString().split('T')[0];
        }
        // Set min date to today for future dates
        if (input.name.includes('scheduled') || input.name.includes('administered')) {
            input.min = new Date().toISOString().split('T')[0];
        }
    });
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    } else if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    } else if (field.name.includes('phone') && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    if (!isValid) {
        field.classList.add('is-invalid');
        showFieldError(field, errorMessage);
    } else {
        field.classList.remove('is-invalid');
        hideFieldError(field);
    }
    
    return isValid;
}

function showFieldError(field, message) {
    let errorElement = field.parentNode.querySelector('.invalid-feedback');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        field.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = message;
}

function hideFieldError(field) {
    const errorElement = field.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.remove();
    }
}

function formatPhoneNumber(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 0) {
        if (value.length <= 3) {
            value = value;
        } else if (value.length <= 6) {
            value = value.slice(0, 3) + '-' + value.slice(3);
        } else {
            value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
        }
    }
    e.target.value = value;
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    const autoSaveData = {};
    
    for (let [key, value] of formData.entries()) {
        autoSaveData[key] = value;
    }
    
    localStorage.setItem('autoSave_' + form.id, JSON.stringify(autoSaveData));
    
    // Show auto-save indicator
    showNotification('Draft saved automatically', 'info');
}

// Tooltips and popovers
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Modal enhancements
function initializeModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            document.body.style.overflow = 'hidden';
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            document.body.style.overflow = '';
        });
    });
}

// Animations
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    const animatedElements = document.querySelectorAll('.card, .stats-card');
    animatedElements.forEach(el => observer.observe(el));
}

// Calendar functionality
function initializeCalendar() {
    const calendarContainer = document.querySelector('.calendar-container');
    if (!calendarContainer) return;
    
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    
    renderCalendar(currentMonth, currentYear);
}

function renderCalendar(month, year) {
    const calendarDays = document.querySelector('.calendar-days');
    if (!calendarDays) return;
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    let html = '';
    
    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        html += '<div class="calendar-day empty"></div>';
    }
    
    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const isToday = new Date().getDate() === day && new Date().getMonth() === month && new Date().getFullYear() === year;
        const hasEvents = checkForEvents(year, month, day);
        
        html += `
            <div class="calendar-day ${isToday ? 'today' : ''} ${hasEvents ? 'has-event' : ''}" 
                 data-date="${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}">
                ${day}
                ${hasEvents ? '<div class="event-indicator"></div>' : ''}
            </div>
        `;
    }
    
    calendarDays.innerHTML = html;
    
    // Add click handlers
    calendarDays.querySelectorAll('.calendar-day:not(.empty)').forEach(day => {
        day.addEventListener('click', function() {
            const date = this.dataset.date;
            showDateEvents(date);
        });
    });
}

function checkForEvents(year, month, day) {
    // This would typically check against your schedule data
    // For demo purposes, return random events
    return Math.random() > 0.7;
}

function showDateEvents(date) {
    // Show events for the selected date
    console.log('Events for date:', date);
    // This would open a modal or show a list of events
}

// Quick actions
function initializeQuickActions() {
    const quickActionButtons = document.querySelectorAll('.quick-action');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            executeQuickAction(action);
        });
    });
}

function executeQuickAction(action) {
    switch(action) {
        case 'add-child':
            window.location.href = '/children/add/';
            break;
        case 'schedule-vaccination':
            window.location.href = '/schedules/add/';
            break;
        case 'add-record':
            window.location.href = '/records/add/';
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Notifications
function initializeNotifications() {
    // Check for notifications every 30 seconds
    setInterval(checkNotifications, 30000);
    
    // Initial check
    checkNotifications();
}

function checkNotifications() {
    fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
            if (data.notifications && data.notifications.length > 0) {
                showNotificationBadge(data.notifications.length);
                data.notifications.forEach(notification => {
                    showNotification(notification.message, notification.type);
                });
            }
        })
        .catch(error => {
            console.error('Notification check failed:', error);
        });
}

function showNotificationBadge(count) {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
}

// Utility functions
function showLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.classList.add('show');
    }
}

function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.classList.remove('show');
    }
}

function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notificationContainer');
    if (!notificationContainer) return;
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Print functionality
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Print</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                ${element.innerHTML}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Export data
function exportData(format, data) {
    switch(format) {
        case 'csv':
            exportToCSV(data);
            break;
        case 'pdf':
            exportToPDF(data);
            break;
        default:
            console.log('Unsupported export format:', format);
    }
}

function exportToCSV(data) {
    // CSV export implementation
    console.log('Exporting to CSV:', data);
}

function exportToPDF(data) {
    // PDF export implementation
    console.log('Exporting to PDF:', data);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const quickSearch = document.getElementById('quickSearch');
        if (quickSearch) {
            quickSearch.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            bootstrap.Modal.getInstance(openModal).hide();
        }
    }
});

// Dark mode toggle (if implemented)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
