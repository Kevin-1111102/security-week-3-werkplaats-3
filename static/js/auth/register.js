import { confirmModal } from '../util/utils.js';

(() => {
        'use strict';

        const form = document.getElementById('register-form');
        form.addEventListener('submit', event => {
            if (event.key === 'Enter' && event.target.type !== 'submit') {
                event.preventDefault();
                return;
            }

            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                let valid = true;
                const currentInputs = form.querySelectorAll('input');

                currentInputs.forEach(input => {
                    if (!input.checkValidity()) {
                        valid = false;
                        input.classList.add('is-invalid');
                        input.classList.remove('is-valid');
                    } else {
                        input.classList.remove('is-invalid');
                        input.classList.add('is-valid');
                    }
                });
        
                if (!valid) {
                    const firstInvalid = form.querySelector('.is-invalid');
                    if (firstInvalid) firstInvalid.focus();
                }
                
            } else {
                submitForm(event);
            }

            form.classList.add('was-validated');
        }, false);

        async function submitForm(event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);

            // Check if Terms of Service is accepted
            if (!formData.get('voorwaarden_akkoord'))
                return;

            // Extract data from the form
            const data = {
                email: formData.get('email'),
                wachtwoord: formData.get('wachtwoord'),
                voornaam: formData.get('voornaam'),
                tussenvoegsel: formData.get('tussenvoegsel') || null,
                achternaam: formData.get('achternaam'),
                geboortedatum: formData.get('geboortedatum'),
                geslacht: formData.get('geslacht'),
                postcode: formData.get('postcode'),
                telefoonnummer: formData.get('telefoonnummer'),
                introductie: formData.get('introductie') || null,
                beperkingen: formData.getAll('beperkingen'),
                hulpmiddelen: formData.get('hulpmiddelen') || null,
                contact_voorkeur: formData.get('contact_voorkeur'),
                onderzoektype_voorkeur: formData.getAll('onderzoektype_voorkeur').join(', '),
                heeft_voogd: formData.has('heeft_voogd') === 'on',
                naam_voogd: formData.get('naam_voogd') || null,
                email_voogd: formData.get('email_voogd') || null,
                telefoonnummer_voogd: formData.get('telefoonnummer_voogd') || null,
                voorwaarden_akkoord: formData.get('voorwaarden_akkoord') === 'on'
            };

            try {
                const response = await fetch('/api/users/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (result.success) {
                    form.classList.remove('was-validated');
                    confirmModal({
                        title: 'Registratie voltooid',
                        message: 'Uw account moet eerst worden goedgekeurd voordat u kunt inloggen. U ontvangt een e-mail zodra de goedkeuring is voltooid.',
                        link: result.redirect,
                        confirmText: 'Ga naar login',
                        backdrop: 'static',
                        keyboard: false
                    });
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        // handle guardian
        const birthdateInput = document.getElementById('birthdate');
        const guardianField = document.getElementById('guardian');
        const guardianCheckbox = document.getElementById('has_guardian');
        const hiddenGuardianInput = document.getElementById('heeft_voogd_hidden');

        function toggleGuardianField(show) {
            guardianField.style.display = show ? 'block' : 'none';

            // input fields in guardianField are required when shown
            const guardianInputs = guardianField.querySelectorAll('input');
            guardianInputs.forEach(input => {
                input.required = show;
                input.setAttribute('aria-required', show);
            });

            hiddenGuardianInput.value = guardianCheckbox.checked ? 'on' : '';
        }

        toggleGuardianField(guardianCheckbox.checked);

        birthdateInput.addEventListener('change', function () {
            const birthdateValue = new Date(birthdateInput.value);
            const age = new Date().getFullYear() - birthdateValue.getFullYear();
            if (age < 18) {
                guardianCheckbox.checked = true;
                guardianCheckbox.disabled = true;
                toggleGuardianField(true);
            } else {
                guardianCheckbox.checked = false;
                guardianCheckbox.disabled = false;
                toggleGuardianField(false);
            }
        });

        guardianCheckbox.addEventListener('change', function () {
            if (guardianCheckbox.disabled) {
                guardianCheckbox.checked = true;
            }
            toggleGuardianField(guardianCheckbox.checked);
        });
    }
)();