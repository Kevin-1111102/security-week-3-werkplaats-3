import {showToast, confirmModal} from './util/utils.js'
class ResearchDetails {
    constructor() {
        this.researchData = null;
        this.disabilityData = null;

        this.researchId = window.location.pathname.split('/').pop();
        this.researchTitle = document.querySelector('#research-title');
        this.sections = {
            research: document.querySelector('#research-info'),
            participants: document.querySelector('#participants-info')
        };
        this.init();
    }

    init() {
        this.fetchResearchData();
        this.fetchDisabilityData();

        const editButton = document.querySelector('#edit-button');
        if (!editButton) return;

        editButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleEdit();
        });
    }

    fetchResearchData() {
        fetch(`/api/researches/${this.researchId}`)
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }

                if (data.success && data.data) {
                    this.renderResearchData(data.data);
                    this.researchData = data.data
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.renderErrorData();
            });
    }

    fetchDisabilityData() {
        fetch(`/api/disabilities/`)
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                }

                if (data.success && data.data) {
                    this.disabilityData = data.data
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    renderResearchData(research) {
        let beperkingenText = 'Geen opgegeven';

        if (research.beperkingen && research.beperkingen.length > 0) {
            beperkingenText = research.beperkingen.map(item => item.beperking_naam || 'Onbekend').join(', ');
        }
        
        this.researchTitle.textContent = research.titel;
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

        if (this.sections.participants) {
            if (Array.isArray(research.participants) && research.participants.length > 0) {
                const participantsHtml = this.createTabContent({
                    'Deelnemers': research.participants
                        .map(participant => participant.ervaringsdeskundige)
                        .join(', ')
                });
            
                this.sections.participants.innerHTML = participantsHtml;
            } else {
                this.sections.participants.innerHTML = '<p>Geen deelnemers gevonden.</p>';
            }
        }
    }

    renderErrorData() {
        this.sections.research.innerHTML = '<p>Er is iets misgegaan bij het ophalen van de gegevens</p>';
    }

    renderErrorDataEdit() {
        this.sections.research.innerHTML = `
        <p>Er is iets misgegaan bij het bewerken van de gegevens.</p>
        <button id="go-back-button" class="btn btn-sm btn-primary fw-bold">
        <i class="fa-solid fa-arrow-left"></i>
        Terug naar gegevens
        </button>
        `;
        document.getElementById('edit-button').disabled = true;

        document.getElementById('go-back-button').addEventListener('click', () => {
            this.renderResearchData(this.researchData);
            document.getElementById('edit-button').disabled = false;
        });
    }

    // credits (Alex Wayne - Oct 30, 2021) src: https://stackoverflow.com/a/69782855
    createTabContent(data) {
        return Object.entries(data)
            .map(([key, value]) => `<p><strong>${key}</strong><br>${value}</p>`)
            .join('');
    }

    toggleEdit() {
        if (this.sections.research.querySelector('form')) {
            this.renderResearchData(this.researchData);
        } else {
            this.sections.research.innerHTML = `
        <form id="research-form" class="needs-validation">
            <div class="details p-4">
                <h2 class="mb-3">Onderzoeksgegevens bewerken</h2>
                <fieldset class="w-100">
                    <legend class="visually-hidden">Onderzoeksgegevens</legend>
                    <div class="d-flex flex-column gap-3 w-100">

                        <div class="d-flex flex-wrap gap-2">
                            <div class="flex-grow-1 col-sm-2">
                                <label for="title" class="form-label">Titel <span class="label-star-required">*</span></label>
                                <input id="title" type="text" name="title" class="form-control" value="${this.researchData?.titel || ''}" required>
                            </div>
                            <div class="flex-grow-1 col-sm-2">
                                <label for="status" class="form-label">Status <span class="label-star-required">*</span></label>
                                <select id="status" name="status" class="form-control" required>
                                    <option value="Nieuw" ${this.researchData?.status === 'Nieuw' ? 'selected' : ''}>Nieuw</option>
                                    <option value="Gesloten" ${this.researchData?.status === 'Gesloten' ? 'selected' : ''}>Gesloten</option>
                                </select>
                            </div>
                        </div>

                        <div>
                            <label class="form-label">Beschikbaar <span class="label-star-required">*</span></label>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="available" id="available_yes" value="ja" ${this.researchData?.beschikbaar == true ? 'checked' : ''} required>
                                <label class="form-check-label" for="available_yes">Ja</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="available" id="available_no" value="nee" ${this.researchData?.beschikbaar == false ? 'checked' : ''} required>
                                <label class="form-check-label" for="available_no">Nee</label>
                            </div>
                        </div>

                        <div>
                            <label for="description" class="form-label">Beschrijving</label>
                            <textarea id="description" name="description" class="form-control" rows="2">${this.researchData?.beschrijving || ''}</textarea>
                        </div>

                        <div class="d-flex flex-wrap gap-2">
                            <div class="flex-grow-1 col-sm-2">
                                <label for="start-date" class="form-label">Begindatum <span class="label-star-required">*</span></label>
                                <input id="start-date" type="date" name="start_date" class="form-control" value="${this.researchData?.begindatum || ''}" required>
                            </div>
                            <div class="flex-grow-1 col-sm-2">
                                <label for="end-date" class="form-label">Einddatum <span class="label-star-required">*</span></label>
                                <input id="end-date" type="date" name="end_date" class="form-control" value="${this.researchData?.einddatum || ''}" required>
                            </div>
                        </div>

                        <div>
                            <label class="form-label">Met beloning <span class="label-star-required">*</span></label>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="rewarded" id="rewarded_yes" value="ja" ${this.researchData?.met_beloning == true ? 'checked' : ''} required>
                                <label class="form-check-label" for="rewarded_yes">Ja</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="rewarded" id="rewarded_no" value="nee" ${this.researchData?.met_beloning == false ? 'checked' : ''} required>
                                <label class="form-check-label" for="rewarded_no">Nee</label>
                            </div>
                        </div>

                        <div>
                            <label for="reward" class="form-label">Beloning</label>
                            <input id="reward" type="text" name="reward" class="form-control" value="${this.researchData?.beloning || ''}">
                        </div>
                    </div>   
                <button type="submit" class="btn btn-sm btn-primary fw-bold mt-3" id="submit-button">
                <i class="fa-solid fa-floppy-disk"></i>
                    Opslaan
                </button>
                
            </div>
           
        </form>`;
        }
        document.getElementById('research-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = document.querySelector('#research-form');
            const status = formData.querySelector('select[name="status"]').value;
            if (status === "Gesloten") {
                confirmModal({
                    title: 'Onderzoek sluiten',
                    message: `
                    Weet u zeker dat u dit onderzoek wil sluiten?
                    <br/>
                    <strong>Dit proces is onomkeerbaar</strong>
                    `,
                    confirmText: 'Onderzoek sluiten',
                    confirmClass: 'btn-danger',
                    onConfirm: () => this.saveChanges()
                });
            } else {
                this.saveChanges();
            }
        });
    }


    saveChanges() {
        const formData = new FormData(document.getElementById('research-form'));
        const data = {
            title: formData.get('title'),
            status: formData.get('status'),
            available: formData.get('available') === 'ja' ? 1 : 0,
            description: formData.get('description'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            research_type: formData.get('research_type'),
            location: formData.get('location'),
            with_reward: formData.get('rewarded') === 'ja',
            reward: formData.get('reward'),
            age_min: formData.get('age_min'),
            age_max: formData.get('age_max'),
            disability: formData.get('disability')
        };

        document.getElementById('edit-button').disabled = true;

        fetch(`/api/researches/${this.researchId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('success', `${data.message}`, 5000);
                    this.fetchResearchData();
                } else {
                    console.error('Error saving data:', data.message);
                    showToast('danger', 'Er is iets fout gegaan bij het aanpassen van een onderzoek');
                    this.renderErrorDataEdit();
                }
            })
            .catch(error => {
                console.error('Error saving data:', error);
                this.renderErrorDataEdit();
                showToast('danger', 'Er is iets fout gegaan bij het aanpassen van een onderzoek');
            });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const researchContainer = document.querySelector('.research-container');
    if (researchContainer) {
        new ResearchDetails(researchContainer);
    }
});
