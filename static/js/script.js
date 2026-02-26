// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. Bootstrap Component Initialization ---
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // --- 2. Modal Layout Fix ---
    // Prevents background jumping by neutralizing scrollbar padding shift
    const fixModalPadding = () => { document.body.style.paddingRight = '0px'; };
    document.addEventListener('show.bs.modal', fixModalPadding);
    document.addEventListener('hidden.bs.modal', fixModalPadding);

    // --- 3. Integrated BARS Precision Timer System ---
    function updateBARSCountdowns() {
        const now = new Date().getTime();

        // A. Card Mini-Timers (.countdown-mini)
        document.querySelectorAll('.countdown-mini').forEach(el => {
            const endDateStr = el.getAttribute('data-end');
            if (!endDateStr) return;

            const endDate = new Date(endDateStr).getTime();
            const dist = endDate - now;
            
            if (isNaN(endDate)) { el.innerHTML = "DATA TBA"; return; }
            
            if (dist > 0) {
                const h = Math.floor((dist % 86400000) / 3600000).toString().padStart(2, '0');
                const m = Math.floor((dist % 3600000) / 60000).toString().padStart(2, '0');
                const s = Math.floor((dist % 60000) / 1000).toString().padStart(2, '0');
                el.innerHTML = `${h}:${m}:${s}`;
            } else {
                el.innerHTML = "00:00:00";
            }
        });

        // B. Major Operation Timers (.countdown)
        document.querySelectorAll('.countdown').forEach(element => {
            const endDateStr = element.getAttribute('data-end');
            if (!endDateStr) return;

            const endDate = new Date(endDateStr).getTime();
            const distance = endDate - now;
            
            if (isNaN(endDate)) {
                element.innerHTML = "<small class='text-muted text-uppercase'>Date TBA</small>";
                return;
            }

            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24)).toString().padStart(2, '0');
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
                const seconds = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
                
                element.innerHTML = `
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold text-white">${days}</div><small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Days</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold text-white">${hours}</div><small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Hrs</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold text-white">${minutes}</div><small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Min</small></div>
                    <div class="d-inline-block mx-2"><div class="fs-2 fw-bold text-white">${seconds}</div><small class="text-cyan text-uppercase" style="font-size: 0.6rem;">Sec</small></div>
                `;
            } else {
                element.innerHTML = "<div class='alert alert-cyber mt-3 mb-0 py-2'><i class='bi bi-broadcast-pin me-2'></i>MISSION IN PROGRESS</div>";
            }
        });
    }

    if (document.querySelector('.countdown, .countdown-mini')) {
        setInterval(updateBARSCountdowns, 1000);
        updateBARSCountdowns();
    }

    // --- 4. Enhanced Card Hover & Glow Effects ---
    const interactiveElements = document.querySelectorAll('.cyber-card, .cyber-card-orange, .member-card, .event-card, .role-btn');
    interactiveElements.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(-10px) scale(1.02)';
                card.style.transition = 'all 0.3s ease';
                const isOrange = card.classList.contains('cyber-card-orange') || card.style.borderColor.includes('orange');
                card.style.boxShadow = isOrange ? '0 0 30px rgba(255, 107, 0, 0.4)' : '0 0 30px rgba(0, 243, 255, 0.4)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('selected')) {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = 'none';
            }
        });
    });

    // --- 5. Panel Tab Switching Logic ---
    const panelTabs = document.querySelectorAll('.panel-tab');
    panelTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            panelTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // --- 6. Cyber Form Validation ---
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
                        feedback.textContent = 'Field critical. Entry required.';
                        input.parentNode.appendChild(feedback);
                    }
                    input.style.boxShadow = '0 0 10px #ff0000';
                    setTimeout(() => input.style.boxShadow = '', 1000);
                } else {
                    input.classList.remove('is-invalid');
                    if (input.nextElementSibling?.classList.contains('invalid-feedback')) {
                        input.nextElementSibling.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>CHECK DATA FIELDS';
                    submitBtn.classList.add('btn-danger');
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.classList.remove('btn-danger');
                    }, 2000);
                }
            }
        });
    });

    // --- 7. Multi-Target Password Toggle ---
    const togglePasswordBtn = document.getElementById('togglePassword');
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const passwordInput = document.getElementById('id_password') || document.getElementById('id_password1');
            const icon = this.querySelector('i');
            
            if (passwordInput && passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.replace('bi-eye', 'bi-eye-slash');
            } else if (passwordInput) {
                passwordInput.type = 'password';
                icon.classList.replace('bi-eye-slash', 'bi-eye');
            }
        });
    }

    // --- 8. Global Alert Auto-Hide ---
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            if (alert.parentElement && !alert.classList.contains('alert-cyber')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // --- 9. Triumph Submission Backend Uplink ---
    const triumphForm = document.getElementById('triumph-form');
    if (triumphForm) {
        triumphForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const syncBtn = document.getElementById('sync-btn');
            const originalBtnContent = syncBtn.innerHTML;
            
            // 1. Visual Loading State
            syncBtn.innerHTML = '<i class="bi bi-broadcast-pin spin me-2"></i>UPLOADING TO MAINFRAME...';
            syncBtn.style.pointerEvents = 'none';
            syncBtn.classList.remove('btn-danger');

            // 2. Prepare Data
            const formData = new FormData();
            formData.append('name', this.querySelector('input[placeholder*="name"]')?.value || '');
            formData.append('title', this.querySelector('input[placeholder*="Project"]')?.value || '');
            formData.append('category', this.querySelector('select')?.value || '');
            formData.append('description', this.querySelector('textarea')?.value || '');
            
            const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]')?.value;
            if (csrfToken) formData.append('csrfmiddlewaretoken', csrfToken);

            // 3. Execute Uplink
            fetch('/submit-triumph/', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => {
                if (!response.ok) throw new Error('Terminal network error.');
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    syncBtn.innerHTML = '<i class="bi bi-check-all me-2"></i>DATA ENCRYPTED & SENT';
                    syncBtn.classList.replace('btn-cyber-orange', 'btn-success');
                    triumphForm.reset();
                    
                    setTimeout(() => {
                        syncBtn.innerHTML = originalBtnContent;
                        syncBtn.classList.replace('btn-success', 'btn-cyber-orange');
                        syncBtn.style.pointerEvents = 'auto';
                    }, 5000);
                } else {
                    throw new Error(data.message || 'Transmission failed.');
                }
            })
            .catch(error => {
                syncBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>UPLINK FAILED';
                syncBtn.classList.add('btn-danger');
                syncBtn.style.pointerEvents = 'auto';
                console.error('System Error:', error);
                
                // Reset button after 3 seconds so they can try again
                setTimeout(() => {
                    syncBtn.innerHTML = originalBtnContent;
                    syncBtn.classList.remove('btn-danger');
                }, 3000);
            });
        });
    }
});