import { showToast, confirmModal } from '../util/utils.js';
class UserProfile {
    constructor(profileContainer) {
        this.profileContainer = profileContainer;
        this.userId = profileContainer.dataset.userId;
        this.delay = Math.max(1000, parseInt(profileContainer.dataset.delay));
        this.deleteBtn = document.getElementById('delete-account-btn');
        this.sections = {
            personal: document.querySelector('#personal-info'),
            contact: document.querySelector('#contact-info'),
            preferences: document.querySelector('#preferences'),
            guardian: document.querySelector('#guardian-info'),
        };
        this.init();
    }

    init() {
        this.fetchUserData();
        this.deleteBtn.addEventListener('click', this.handleDelete.bind(this));

        setInterval(() => {
            this.fetchUserData();
        }, this.delay);
    }

    fetchUserData() {
        fetch(`/api/users/${this.userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.redirect)
                    window.location.href = data.redirect;

                if (data.success && data.data)
                    this.renderUserData(data.data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.renderErrorData();
            });
    }

    renderErrorData() {
        sections.forEach(section => {
            section.innerHTML = '<p>Er is iets misgegaan bij het ophalen van de gegevens</p>';
        });
    }

    renderUserData(user) {
        this.sections.personal.innerHTML = this.createTabContent({
            'Naam': `${user.voornaam} ${user.tussenvoegsel || ''} ${user.achternaam}`,
            'Geboortedatum': user.geboortedatum,
            'Geslacht': user.geslacht,
            'Beperkingen': Array.isArray(user.beperkingen) && user.beperkingen.length > 0
            ? user.beperkingen.join(', ')
            : 'Geen opgegeven',
            'Bijzonderheden Beperkingen': user.bijzonderheden_beperkingen || 'Geen opgegeven',
            'Hulpmiddelen': user.hulpmiddelen || 'Geen opgegeven',
            'Introductie': user.introductie || 'Geen opgegeven'
        });

        this.sections.contact.innerHTML = this.createTabContent({
            'Postcode': user.postcode,
            'Telefoonnummer': user.telefoonnummer,
            'Email': user.email
        });

        this.sections.preferences.innerHTML = this.createTabContent({
            'Contact voorkeur': user.contact_voorkeur,
            'Onderzoektype voorkeur': user.onderzoektype_voorkeur,
            'Beschikbaarheid': user.bijzonderheden_beschikbaarheid
        });

        this.sections.guardian.innerHTML = user.heeft_voogd ? this.createTabContent({
            'Naam Voogd': user.naam_voogd || 'Geen opgegeven',
            'Email Voogd': user.email_voogd || 'Geen opgegeven',
            'Telefoonnummer Voogd': user.telefoonnummer_voogd || 'Geen opgegeven'
        }) : '<p>Geen voogd opgegeven</p>';
    }

    // credits (Alex Wayne - Oct 30, 2021) src: https://stackoverflow.com/a/69782855
    createTabContent(data) { 
        return Object.entries(data).map(([key, value]) =>
           `<p><strong>${key}</strong><br>${value}</p>`
        ).join('');
    }

    handleDelete() {
        confirmModal({
            title: 'Account Verwijderen',
            message: 'Weet je zeker dat je je account wilt verwijderen? Dit kan niet ongedaan worden gemaakt.',
            confirmText: 'Verwijder Account',
            confirmClass: 'btn-danger',
            onConfirm: this.deleteAccount.bind(this)
        });
    }

    deleteAccount() {
        fetch(`/api/users/${this.userId}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('success', 'Je account is succesvol verwijderd');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1000);
                } else {
                    console.error('Error:', data.error);
                    showToast('danger', 'Er is iets misgegaan bij het verwijderen van je account');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('danger', 'Er is iets misgegaan bij het verwijderen van je account');
            });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const profileContainer = document.querySelector('.profile-container');
    new UserProfile(profileContainer);
});
