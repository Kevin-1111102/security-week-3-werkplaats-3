import { setFieldValue, showToast } from '../util/utils.js';
class UserProfile {
    constructor(profileContainer) {
        this.profileContainer = profileContainer;
        this.userId = profileContainer.dataset.userId;
        this.sections = {
            personal: document.querySelector('#personal-info'),
            contact: document.querySelector('#contact-info'),
            preferences: document.querySelector('#preferences'),
            guardian: document.querySelector('#guardian-info'),
        };
        this.guardianCheckbox = document.getElementById('has_guardian');
        this.guardianField = document.getElementById('guardian');
        this.form = document.querySelector('#profile-form');
        this.init();
    }

    init() {
        this.fetchUserData();
        this.toggleGuardianField();
        this.guardianCheckbox.addEventListener('change', this.toggleGuardianField.bind(this));
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
    }

    fetchUserData() {
        fetch(`/api/users/${this.userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success && data.data)
                    this.renderUserData(data.data);
                else
                    this.renderErrorData();
            })
            .catch(error => {
                showToast('danger', 'Er is iets misgegaan bij het ophalen van de gegevens');
                console.error('Error fetching data:', error);
                this.renderErrorData();
            });
    }

    renderErrorData() {
        Object.values(this.sections).forEach(section => {
            section.innerHTML = `<p>Er is iets misgegaan bij het ophalen van de gegevens</p>`;
        });
    }

    // fill in the form with the user data
    renderUserData(user) {
        setFieldValue('first-name', user.voornaam);
        setFieldValue('middle-name', user.tussenvoegsel);
        setFieldValue('last-name', user.achternaam);
        setFieldValue('birthdate', user.geboortedatum);
        setFieldValue('gender', user.geslacht, 'radio');
        setFieldValue('disabilities', user.beperkingen, 'select');
        setFieldValue('disability-details', user.bijzonderheden);
        setFieldValue('tools', user.hulpmiddelen);
        setFieldValue('introduction', user.introductie);

        setFieldValue('postalcode', user.postcode);
        setFieldValue('tel', user.telefoonnummer);
        setFieldValue('email', user.email);

        setFieldValue('contact_preference', user.contact_voorkeur, 'radio')
        setFieldValue('research_preference', user.onderzoektype_voorkeur, 'checkbox', 'onderzoektype_voorkeur');
        setFieldValue('availability', user.bijzonderheden_beschikbaarheid);

        if (user.heeft_voogd) {
            this.guardianCheckbox.checked = true;
            setFieldValue('guardian_name', user.naam_voogd);
            setFieldValue('guardian_email', user.email_voogd);
            setFieldValue('guardian_tel', user.telefoonnummer_voogd);
            this.toggleGuardianField();
        }
    }

    // toggle guardian fields from showing based on checkbox
    toggleGuardianField() {
        const show = this.guardianCheckbox.checked;
        this.guardianField.style.display = show ? 'block' : 'none';
        console.log('toggle guardian field', show);

        this.guardianField.querySelectorAll('input').forEach(input => {
            input.required = show;
            input.setAttribute('aria-required', show);
        });
    }

    // handle update form submit
    handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(this.form);
        let obj = Object.fromEntries(formData);
        obj.beperkingen = formData.getAll('beperkingen').map(beperking => parseInt(beperking));
        obj.onderzoektype_voorkeur = formData.getAll('onderzoektype_voorkeur').join(', ');
        
        fetch(`/api/users/${this.userId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(obj)
        })
            .then(response => {
                if (response.ok)
                    return response.json();
            })
            .then(data => {
                if (data.success) {
                    showToast('success', `${data.message}`, 5000);
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 5000);
                }
            })
            .catch(error => {
                showToast('danger', 'Er is iets misgegaan bij het opslaan van de gegevens');
                console.error('Error:', error);
            });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const profileContainer = document.querySelector('.profile-container');
    new UserProfile(profileContainer);
});
