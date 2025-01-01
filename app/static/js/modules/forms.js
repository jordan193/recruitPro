// Gestion des formulaires
export function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                highlightInvalidFields(form);
            }
            form.classList.add('was-validated');
        });
        
        form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('input', () => validateField(input));
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    field.classList.toggle('is-valid', isValid);
    field.classList.toggle('is-invalid', !isValid);
}

function highlightInvalidFields(form) {
    form.querySelectorAll(':invalid').forEach(field => {
        field.classList.add('animate__animated', 'animate__shakeX');
        field.addEventListener('animationend', () => {
            field.classList.remove('animate__animated', 'animate__shakeX');
        });
    });
}

function toggleUserTypeFields() {
    const userType = document.getElementById('user_type').value;
    const recruiterFields = document.getElementById('recruiter-fields');
    const candidateFields = document.getElementById('candidate-fields');
    
    if (userType === 'recruiter') {
        recruiterFields.classList.remove('d-none');
        candidateFields.classList.add('d-none');
    } else {
        recruiterFields.classList.add('d-none');
        candidateFields.classList.remove('d-none');
    }
}

