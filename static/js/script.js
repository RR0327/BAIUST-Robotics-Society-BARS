// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Event Countdown Timer
    function updateCountdown() {
        const countdownElements = document.querySelectorAll('.countdown');
        
        countdownElements.forEach(element => {
            const endDate = new Date(element.dataset.end).getTime();
            const now = new Date().getTime();
            const distance = endDate - now;
            
            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                element.innerHTML = `
                    <div class="d-inline-block mx-2">
                        <div class="fs-1 fw-bold">${days.toString().padStart(2, '0')}</div>
                        <small class="text-cyan">DAYS</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-1 fw-bold">${hours.toString().padStart(2, '0')}</div>
                        <small class="text-cyan">HOURS</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-1 fw-bold">${minutes.toString().padStart(2, '0')}</div>
                        <small class="text-cyan">MINUTES</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-1 fw-bold">${seconds.toString().padStart(2, '0')}</div>
                        <small class="text-cyan">SECONDS</small>
                    </div>
                `;
            } else {
                element.innerHTML = `
                    <div class="alert alert-cyber mt-3">
                        <i class="bi bi-megaphone-fill me-2"></i>
                        EVENT HAS STARTED!
                    </div>
                `;
            }
        });
    }
    
    // Update countdown every second
    if (document.querySelector('.countdown')) {
        setInterval(updateCountdown, 1000);
        updateCountdown(); // Initial call
    }
    
    // Card hover effects
    const cards = document.querySelectorAll('.cyber-card, .cyber-card-orange, .member-card, .event-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(-10px)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Panel tab highlighting
    const panelTabs = document.querySelectorAll('.panel-tab');
    panelTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            panelTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Form validation with cyber effects
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    
                    // Create error feedback
                    let feedback = input.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback text-danger';
                        feedback.textContent = 'This field is required';
                        input.parentNode.appendChild(feedback);
                    }
                    
                    // Cyber effect
                    input.style.boxShadow = '0 0 10px #ff0000';
                    setTimeout(() => {
                        input.style.boxShadow = '';
                    }, 1000);
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                
                // Cyber alert effect
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Please check fields!';
                    submitBtn.classList.add('btn-danger');
                    
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.classList.remove('btn-danger');
                    }, 2000);
                }
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
});