// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialize Bootstrap Components (Tooltips & Popovers)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 2. Fixed Event Countdown Timer
    function updateCountdown() {
        const countdownElements = document.querySelectorAll('.countdown');
        countdownElements.forEach(element => {
            const endDateStr = element.getAttribute('data-end');
            if (!endDateStr) return;

            const endDate = new Date(endDateStr).getTime();
            const now = new Date().getTime();
            const distance = endDate - now;
            
            // Fix for invalid dates in database
            if (isNaN(endDate)) {
                element.innerHTML = "<small class='text-muted text-uppercase'>Date TBA</small>";
                return;
            }

            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                // Using PadStart for a cleaner "Digital" look
                element.innerHTML = `
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold">${days.toString().padStart(2, '0')}</div><small class="text-cyan">DAYS</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold">${hours.toString().padStart(2, '0')}</div><small class="text-cyan">HRS</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold">${minutes.toString().padStart(2, '0')}</div><small class="text-cyan">MIN</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold">${seconds.toString().padStart(2, '0')}</div><small class="text-cyan">SEC</small></div>
                `;
            } else {
                element.innerHTML = "<div class='alert alert-cyber mt-3'><i class='bi bi-megaphone-fill me-2'></i>EVENT HAS STARTED!</div>";
            }
        });
    }
    
    if (document.querySelector('.countdown')) {
        setInterval(updateCountdown, 1000);
        updateCountdown();
    }

    // 3. Card Hover Effects
    const cards = document.querySelectorAll('.cyber-card, .cyber-card-orange, .member-card, .event-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(-10px)';
                card.style.transition = 'all 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(0)';
            }
        });
    });

    // 4. Panel Tab Highlighting Logic
    const panelTabs = document.querySelectorAll('.panel-tab');
    panelTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            panelTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 5. Form Validation with Enhanced Cyber Effects
    const forms = document.querySelectorAll('.cyber-form, form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    
                    // Create error feedback if not exists
                    let feedback = input.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback text-danger small mt-1';
                        feedback.textContent = 'This field is required';
                        input.parentNode.appendChild(feedback);
                    }
                    
                    // Red Cyber Glitch Shadow
                    input.style.boxShadow = '0 0 10px #ff0000';
                    setTimeout(() => { input.style.boxShadow = ''; }, 1000);
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>CHECK FIELDS';
                    submitBtn.classList.add('btn-danger');
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.classList.remove('btn-danger');
                    }, 2000);
                }
            }
        });
    });

    // 6. Auto-hide Alerts
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});