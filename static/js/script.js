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

    // 2. Modal Layout Fix - Prevents background text shift when viewing profiles
    document.addEventListener('show.bs.modal', function () {
        document.body.style.paddingRight = '0px';
    });

    document.addEventListener('hidden.bs.modal', function () {
        document.body.style.paddingRight = '0px';
    });

    // 3. Integrated BARS Precision Timer System
    function updateBARSCountdowns() {
        // A. Handle Card Mini-Timers (.countdown-mini)
        document.querySelectorAll('.countdown-mini').forEach(el => {
            const endDateStr = el.getAttribute('data-end');
            if (!endDateStr) return;

            const endDate = new Date(endDateStr).getTime();
            const now = new Date().getTime();
            const dist = endDate - now;
            
            if (isNaN(endDate)) {
                el.innerHTML = "DATA TBA";
                return;
            }
            
            if (dist > 0) {
                const h = Math.floor((dist % 86400000) / 3600000);
                const m = Math.floor((dist % 3600000) / 60000);
                const s = Math.floor((dist % 60000) / 1000);
                el.innerHTML = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            } else {
                el.innerHTML = "00:00:00";
            }
        });

        // B. Handle Major Operation Timers (.countdown)
        document.querySelectorAll('.countdown').forEach(element => {
            const endDateStr = element.getAttribute('data-end');
            if (!endDateStr) return;

            const endDate = new Date(endDateStr).getTime();
            const now = new Date().getTime();
            const distance = endDate - now;
            
            if (isNaN(endDate)) {
                element.innerHTML = "<small class='text-muted text-uppercase'>Date TBA</small>";
                return;
            }

            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                element.innerHTML = `
                    <div class="d-inline-block mx-2">
                        <div class="fs-2 fw-bold text-white">${days.toString().padStart(2, '0')}</div>
                        <small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Days</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-2 fw-bold text-white">${hours.toString().padStart(2, '0')}</div>
                        <small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Hrs</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-2 fw-bold text-white">${minutes.toString().padStart(2, '0')}</div>
                        <small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Min</small>
                    </div>
                    <div class="d-inline-block mx-2">
                        <div class="fs-2 fw-bold text-white">${seconds.toString().padStart(2, '0')}</div>
                        <small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Sec</small>
                    </div>
                `;
            } else {
                element.innerHTML = "<div class='alert alert-cyber mt-3 mb-0 py-2'><i class='bi bi-broadcast-pin me-2'></i>MISSION IN PROGRESS</div>";
            }
        });
    }

    // Initialize Timers
    if (document.querySelector('.countdown') || document.querySelector('.countdown-mini')) {
        setInterval(updateBARSCountdowns, 1000);
        updateBARSCountdowns();
    }

    // 4. Enhanced Card Hover & Role Glow Effects
    const cards = document.querySelectorAll('.cyber-card, .cyber-card-orange, .member-card, .event-card, .role-btn');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('selected')) {
                // Intense glow effect for Advisor Roles & Responsibilities
                card.style.transform = 'translateY(-10px) scale(1.02)';
                card.style.transition = 'all 0.3s ease';
                
                // Dynamic border glow logic
                if (card.style.borderColor.includes('orange') || card.classList.contains('cyber-card-orange')) {
                    card.style.boxShadow = '0 0 30px rgba(255, 107, 0, 0.4)';
                } else {
                    card.style.boxShadow = '0 0 30px rgba(0, 243, 255, 0.4)';
                }
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = 'none';
            }
        });
    });

    // 5. Panel Tab Highlighting Logic
    const panelTabs = document.querySelectorAll('.panel-tab');
    panelTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            panelTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // 6. Form Validation with Enhanced Cyber Feedback
    const forms = document.querySelectorAll('.cyber-form, form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    
                    let feedback = input.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback text-danger small mt-1';
                        feedback.textContent = 'This field is required';
                        input.parentNode.appendChild(feedback);
                    }
                    
                    input.style.boxShadow = '0 0 10px #ff0000';
                    setTimeout(() => { input.style.boxShadow = ''; }, 1000);
                } else {
                    input.classList.remove('is-invalid');
                    let feedback = input.nextElementSibling;
                    if (feedback && feedback.classList.contains('invalid-feedback')) {
                        feedback.remove();
                    }
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

    // 7. Password Visibility Toggle
    const togglePasswordBtn = document.getElementById('togglePassword');
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const passwordInput = document.getElementById('id_password');
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    }

    // 8. Auto-hide Alerts
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            if (alert.parentElement) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});