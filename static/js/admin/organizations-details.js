class OrganizationDetails {
    constructor() {
        this.organizationData = null;
        this.organizationId = new URLSearchParams(window.location.search).get('id');
        this.sections = {
            organization: document.querySelector('#organization-info'),
        };
        this.init();
    }

    init() {
        this.fetchOrganizationData();
        document.getElementById('back-btn').addEventListener('click', () => {
            window.history.back();
        });
    }

    async fetchOrganizationData() {
        try {
            const response = await fetch(`/api/organizations/${this.organizationId}`);
            const data = await response.json();

            if (!data.success) {
                this.sections.organization.innerHTML = '<p>Organisatie niet gevonden.</p>';
                return;
            }

            this.organizationData = data.data;
            this.renderOrganizationData(this.organizationData);
        } catch (error) {
            console.error('Error fetching organization data:', error);
            this.sections.organization.innerHTML = '<p>Fout bij laden van organisatie.</p>';
        }
    }

    renderOrganizationData(organization) {
        this.sections.organization.innerHTML = this.createTabContent({
            "Naam": organization.organisatie_naam,
            "Type": organization.organisatie_type,
            "Website": organization.website || 'Geen website opgegeven',
            "Beschrijving": organization.beschrijving || 'Geen beschrijving opgegeven',
            "Contactpersoon": organization.contactpersoon || 'Geen contactpersoon opgegeven',
            "Email": organization.email || 'Geen email opgegeven',
            "Telefoonnummer": organization.telefoonnummer || 'Geen telefoonnummer opgegeven',
            "Status": organization.status
        });
    }

    createTabContent(data) {
        return Object.entries(data)
            .map(([key, value]) => `<p><strong>${key}</strong><br>${value}</p>`)
            .join('');
    }
}

document.addEventListener('DOMContentLoaded', () => new OrganizationDetails());