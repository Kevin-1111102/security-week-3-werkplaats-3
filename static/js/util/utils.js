
// set the value of a form field
function setFieldValue(id, value='', type='text', name='') {
    const element = document.getElementById(id);
    if (element) {
        switch (type) {
            case 'radio':
                element.querySelectorAll('input[type="radio"]').forEach(el => {
                    el.checked = el.value === value;
                })
                break;
            case 'select':
                element.querySelectorAll('option').forEach(option => {
                    option.selected = value.includes(option.text);
                });
                break;
            case 'checkbox':
                value.split(', ').forEach(option => {
                    const input = document.querySelector(`input[name="${name}"][value="${option}"]`);
                    if (input) input.checked = true;
                });
                break;
            default:
                element.value = value;
        }
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value, days=31) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = '; expires=' + date.toUTCString();
    document.cookie = name + '=' + value + '; path=/' + expires;
}

// show a toast notification
function showToast(type='info', message, delay=10000) {
    const toastContainer = document?.querySelector('.toast-container');
    if (!toastContainer) return;

    const icons = {
        info: 'fa-circle-info',
        danger: 'fa-circle-exclamation',
        success: 'fa-circle-check'
    };

    const toast = `
        <div class="toast toast-${type} py-1 px-1 py-sm-3 px-sm-2 mt-2" role="alert" aria-live="assertive" data-bs-autohide="true" data-bs-delay="${delay}">
            <div class="toast-body d-flex align-items-center gap-2 gap-sm-3">
                <i class="toast-icon fa-solid ${icons[type]} fs-5" aria-hidden="true"></i>
                <p class="toast-text m-0" tabindex="-1">${message}</p>
            </div>
            <div class="progress-bar" style="animation-duration: ${delay}ms;"></div>
        </div>
    `;
    toastContainer.insertAdjacentHTML('beforeend', toast);

    const toastElement = toastContainer.lastElementChild;
    const bsToast = new bootstrap.Toast(toastElement);
    bsToast.show();
}

function confirmModal({ title, message, confirmText='Bevestigen', confirmClass='btn-primary', link=null, onConfirm=()=>{}, backdrop='true', keyboard=true, focus=true }) {
    const confirmContainer = document?.querySelector('.confirm-container');
    if (!confirmContainer) return;

    confirmContainer.innerHTML = `
        <div class="modal fade" id="confirmDialog" tabindex="-1" 
            data-bs-backdrop="${backdrop}" 
            data-bs-keyboard="${keyboard}" 
            data-bs-focus="${focus}">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content p-3 p-sm-4">
                    <div class="modal-header py-1 border-0">
                        <h2 class="modal-title fw-bold fs-4">${title}</h2>
                        ${keyboard ? '<button type="button" class="btn-close fs-6" data-bs-dismiss="modal" aria-label="Close"></button>' : ''}
                    </div>
                    <div class="modal-body py-2">
                        <p>${message}</p>
                        <div class="d-flex gap-2 pt-2">
                            ${link 
                                ? `<a href="${link}" class="btn btn-sm ${confirmClass} fw-bold">${confirmText}</a>`
                                : `<button id="cancelBtn" class="btn btn-sm btn-outline fw-bold">Annuleren</button>
                                <button id="confirmBtn" class="btn btn-sm ${confirmClass} fw-bold">${confirmText}</button>`
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    const modalElement = confirmContainer.querySelector('.modal');
    const modal = new bootstrap.Modal(modalElement);

    if (!link) {
        confirmContainer.querySelector('#cancelBtn').addEventListener('click', () => {
            modal.hide();
        });

        confirmContainer.querySelector('#confirmBtn').addEventListener('click', () => {
            onConfirm();
            modal.hide();
        });
    }

    modal.show();
}

// determine if a color is light or dark CREDITS (Andreas Wik August 7, 2018) https://awik.io/determine-color-bright-dark-using-javascript/
function isLightOrDark(color) {
    let r, g, b, hsp;
    
    color = +("0x" + color.slice(1).replace( 
    color.length < 5 && /./g, '$&$&'));

    r = color >> 16;
    g = color >> 8 & 255;
    b = color & 255;
    
    hsp = Math.sqrt(
        0.299 * (r * r) +
        0.587 * (g * g) +
        0.114 * (b * b)
    );

    if (hsp>127.5) 
        return 'light';
    return 'dark';
}

export { setFieldValue, setCookie, getCookie, showToast, confirmModal, isLightOrDark };