class ResearchDetails {
    constructor() {
        this.researchData = null;
        this.researchId = new URLSearchParams(window.location.search).get('id');
        this.sections = {
            research: document.querySelector('#research-info'),
        };
        this.init();
    }

    init() {
        this.fetchResearchData();
        document.getElementById('back-btn').addEventListener('click', () => {
            window.history.back();
        });
    }

    async fetchResearchData() {
        try {
            const response = await fetch(`/api/researches/${this.researchId}`);
            const data = await response.json();

            if (!data.success) {
                this.sections.research.innerHTML = '<p>Onderzoek niet gevonden.</p>';
                return;
            }

            this.researchData = data.data;
            this.renderResearchData(this.researchData);

            if (this.researchData.organisatie_id) {
                this.fetchOrganizationData(this.researchData.organisatie_id);
            }
        } catch (error) {
            console.error('Error fetching research data:', error);
            this.sections.research.innerHTML = '<p>Fout bij laden van onderzoek.</p>';
        }
    }

    async fetchOrganizationData(organizationId) {
        try {
            const response = await fetch(`/api/organizations/${organizationId}`);
            const data = await response.json();

            if (data.success) {
                this.renderOrganizationData(data.data);
            }
        } catch (error) {
            console.error('Error fetching organization data:', error);
            this.renderOrganizationData(null);
        }
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

    renderOrganizationData(organization) {
        const organizationContent = this.createTabContent({
            "Ingediend door": organization?.organisatie_naam || "Onbekend",
            "Contact Organisatie": organization?.email || "Niet beschikbaar"
        });

        this.sections.research.innerHTML += organizationContent;
    }

    createTabContent(data) {
        return Object.entries(data)
            .map(([key, value]) => `<p><strong>${key}:</strong><br>${value}</p>`)
            .join('');
    }
}

document.addEventListener('DOMContentLoaded', () => new ResearchDetails());
