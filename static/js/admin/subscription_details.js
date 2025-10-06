class SubscriptionProfile {
    constructor(profileContainer) {
        this.profileContainer = profileContainer;
        this.researchId = profileContainer.dataset.researchId;
        this.userId = profileContainer.dataset.userId;
        this.delay = Math.max(1000, parseInt(profileContainer.dataset.delay));
        this.sections = {
            research: document.querySelector('#research-info'),
            user: document.querySelector('#user-info')
        };
        this.init();
    }

    init() {
        this.fetchResearchData();
        this.fetchUserData();

        setInterval(() => {
            this.fetchResearchData();
            this.fetchUserData();
        }, this.delay);
    }

    fetchResearchData() {
        fetch(`/api/researches/${this.researchId}`)
            .then(response => response.json())
            .then(data => {
                if (data.redirect)
                    window.location.href = data.redirect;

                if (data.success && data.data)
                    this.renderResearchData(data.data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.renderErrorData();
            });
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

    renderResearchData(research) {
        let beperkingenText = 'Geen opgegeven';

        if (research.beperkingen && research.beperkingen.length > 0) {
            beperkingenText = research.beperkingen.map(item => item.beperking_naam || 'Onbekend').join(', ');
        }

        this.sections.research.innerHTML = this.createTabContent({
            "Titel": research.titel,
            "Status": research.status,
            "Beschikbaar": research.beschikbaar ? 'Ja' : 'Nee',
            "Beschrijving": research.beschrijving,
            "Begindatum": research.begindatum,
            "Einddatum": research.einddatum,
            "Onderzoekstype": research.onderzoek_type,
            "Locatie": research.locatie || 'Geen opgegeven',
            "Met Beloning": research.met_beloning ? 'Ja' : 'Nee',
            "Beloning": research.beloning || 'Geen opgegeven',
            "Leeftijd Doelgroep": `${research.leeftijd_doelgroep_van} - ${research.leeftijd_doelgroep_tot} jaar`,
            "Beperkingen": beperkingenText
        });
    }

    renderUserData(user) {
        this.sections.user.innerHTML = this.createTabContent({
            "Naam": `${user.voornaam} ${user.tussenvoegsel || ''} ${user.achternaam}`,
            "Leeftijd": this.calculateAge(user.geboortedatum),
            "Geslacht": user.geslacht,
            "Beperkingen": Array.isArray(user.beperkingen) && user.beperkingen.length > 0
            ? user.beperkingen.join(', ')
            : 'Geen opgegeven',
            "Bijzonderheden Beperkingen": user.bijzonderheden_beperkingen || 'Geen opgegeven',
            "Hulpmiddelen": user.hulpmiddelen || 'Geen opgegeven',
            "Introductie": user.introductie || 'Geen opgegeven'
        });
    }

    createTabContent(data) { 
        return Object.entries(data).map(([key, value]) =>
           `<p><strong>${key}</strong><br>${value}</p>`
        ).join('');
    }

    calculateAge(dateString) {
        const birthDate = new Date(dateString);
        const today = new Date();
        
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age;
      }
}

document.addEventListener('DOMContentLoaded', () => {
    const profileContainer = document.querySelector('.subscription-container');
    new SubscriptionProfile(profileContainer);
});
