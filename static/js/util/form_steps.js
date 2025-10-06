// Form tabs (https://www.w3schools.com/howto/howto_js_form_steps.asp)
let currentTab = 0;

document.addEventListener('DOMContentLoaded', () => {
    showTab(currentTab);
});

function showTab(index) {
    const tabs = document.querySelectorAll('.tab');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const buttonContainer = prevBtn.parentElement;

    const existingSubmit = document.getElementById('submitBtn');
    if (existingSubmit) buttonContainer.removeChild(existingSubmit);

    tabs.forEach((tab, i) => {
        tab.style.display = i === index ? 'block' : 'none';
    });

    prevBtn.style.display = index === 0 ? 'none' : 'inline';
    nextBtn.style.display = index === tabs.length - 1 ? 'none' : 'inline';

    if (index === tabs.length - 1) {
        buttonContainer.innerHTML += `
          <button type="submit" class="btn btn-lg btn-primary w-100" id="submitBtn">
            Registreer
          </button>
        `;
    }

}

window.switchTab = (step) => {
    const tabs = document.querySelectorAll('.tab');
    const currentTabElement = tabs[currentTab];
    const currentInputs = currentTabElement.querySelectorAll('input, select, textarea');

    if (step === 1) {
        let valid = true;

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
            const firstInvalid = currentTabElement.querySelector('.is-invalid');
            if (firstInvalid) firstInvalid.focus();
            return;
        }
    }

    tabs[currentTab].style.display = 'none';
    currentTab += step;

    if (currentTab >= tabs.length) {
        document.getElementById('register-form').submit();
        return;
    }

    showTab(currentTab);
    const firstInput = tabs[currentTab].querySelector('input');
    if (firstInput) {
        firstInput.focus();
    }
};