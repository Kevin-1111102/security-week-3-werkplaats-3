import {showToast} from '../util/utils.js'

(() => {
    const form = document.querySelector('.needs-validation');
    const message_401 = "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.";
    const custom_message_401 = "Ongeldige inloggegevens";

    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            displayLoginErrorMessage();
        } else {
            submitForm(event);
        }

        form.classList.add('was-validated');
    }, false);

    async function submitForm(event) {
        event.preventDefault();

        const email = document.querySelector('#floatingInput').value;
        const password = document.querySelector('#floatingPassword').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password}),
            });

            const data = await response.json();

            if (data.success) {
                clearErrorMessages();
                form.classList.remove('was-validated');
                showToast('success', `${data.message}`, 1000);

                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1000);
            } else if (data.message !== message_401 && data.message !== custom_message_401){
                displayAuthMessage(data.message || 'Er ging iets mis tijdens het valideren van uw inlogpoging, probeer opnieuw.');
                form.classList.remove('was-validated');
            } else {
                displayLoginErrorMessage();
            }
        } catch (error) {
            console.error('Error:', error);
            displayAuthMessage('Er ging iets mis tijdens het valideren van uw inlogpoging, probeer opnieuw.');
        }
    }

    function displayAuthMessage(message) {
        clearErrorMessages();

        const errorSummary = document.createElement('div');
        errorSummary.className = 'error-message alert alert-danger mt-3';
        errorSummary.setAttribute('role', 'alert');
        errorSummary.setAttribute('tabindex', '-1');
        errorSummary.textContent = message;

        const targetDiv = document.querySelector('.w-100.max-w-sm-md');
        targetDiv.insertAdjacentElement('afterbegin', errorSummary);

        announceMessage(message);
        errorSummary.focus();
    }

    function displayLoginErrorMessage() {
        clearErrorMessages();
        
        const email = document.querySelector('#floatingInput');
        const password = document.querySelector('#floatingPassword');

        email.setAttribute('aria-invalid', 'true');
        password.setAttribute('aria-invalid', 'true');

        email.value = '';
        password.value = '';

        const errorSummary = document.createElement('div');
        errorSummary.className = 'error-message alert alert-danger mt-3';
        errorSummary.setAttribute('role', 'alert');
        errorSummary.setAttribute('tabindex', '-1');

        errorSummary.innerHTML = `
            <p class="mb-0 px-2">Er zijn 2 fouten gevonden:</p>
            <ul class="mb-0 px-2 list-unstyled">
                <li><a href="#floatingInput">E-mailadres</a></li>
                <li><a href="#floatingPassword">Wachtwoord</a></li>
            </ul>
        `;

        const targetDiv = document.querySelector('.w-100.max-w-sm-md');
        targetDiv.insertAdjacentElement('afterbegin', errorSummary);

        errorSummary.querySelectorAll('.error-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const field = document.querySelector(link.getAttribute('href'));
                field.focus();
            });
        });

        announceMessage('De ingevoerde inloggegevens zijn onjuist. Controleer je e-mailadres en wachtwoord en probeer het opnieuw.');
        errorSummary.focus();
    }

    function clearErrorMessages() {
        document.querySelectorAll('.error-message').forEach(error => error.remove());

        document.querySelectorAll('[aria-invalid="true"]').forEach(input => input.removeAttribute('aria-invalid'));
    }

    function announceMessage(message) {
        const errorInfo = document.querySelector('#errorInfo');
        errorInfo.textContent = '';
        setTimeout(() => {
            errorInfo.textContent = message;
        }, 100);
    }
})();