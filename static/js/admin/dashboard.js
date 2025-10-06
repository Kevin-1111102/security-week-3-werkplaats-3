import { showToast } from '../util/utils.js';

document.addEventListener('DOMContentLoaded', function () {
    const actions = new Map([
        ['Goedkeuren', 'Goedgekeurd'],
        ['Afkeuren', 'Afgekeurd']
    ]);

    const names = new Map([
        ["users", "Gebruiker"],
        ["organizations", "Organisatie"],
        ["researches", "Onderzoek"],
        ["subscriptions", "Aanmelding"]
    ]);

    function setActiveTab(tabId) {
        localStorage.setItem("activeTab", tabId);
    }

    document.querySelectorAll('.title').forEach(tab => {
        tab.addEventListener('click', function () {
            setActiveTab(this.textContent.trim());
        });
    });

    const activeTab = localStorage.getItem("activeTab");
    if (activeTab) {
        const tabElement = [...document.querySelectorAll('.title')]
            .find(tab => tab.textContent.trim() === activeTab);
        if (tabElement) {
            tabElement.click();
        }
    }

    const tbody = document.querySelector('.table-section');
    tbody.addEventListener('click', function (event) {
        const target = event.target;
        const button = target.closest('.action-btn');
        if (!button) return;

        const action = button.getAttribute('data-action');
        const id = button.getAttribute('data-id');

        const onderzoek_id = button.getAttribute('data-onderzoek_id');
        const gebruiker_id = button.getAttribute('data-gebruiker_id');


        const activeTable = document.querySelector('.title.active')?.textContent.trim();

        if (!activeTable) return;

        if (activeTable === 'Gebruikers') {
            handleUserActions(action, id);
        } else if (activeTable === 'Organisaties') {
            handleOrganizationActions(action, id);
        } else if (activeTable === 'Onderzoeken') {
            handleResearchActions(action, id);
        } else if (activeTable === 'Aanmeldingen') {
            handleSubscriptionActions(action, onderzoek_id, gebruiker_id);
        }
    });

    async function updateStatus(endpoint, id, status, ) {
        try {
            const response = await fetch(`/api/${endpoint}/${id}`, {
                method: "PATCH",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: actions.get(status) || status }),
            });

            if (response.ok) {
                window.dispatchEvent(new Event('table-refresh'));
                showToast('success', `${names.get(endpoint)} is ${actions.get(status) || status}`);
            } else {
                showToast('error', `Fout bij het bijwerken van ${names.get(endpoint)}`);
            }
        } catch (error) {
            console.error(`Fout bij bijwerken van ${names.get(endpoint)}:`, error);
            showToast('error', `Er is een fout opgetreden bij het verwerken van de actie.`);
        }
    }

    async function updateSubscription(endpoint, onderzoek_id, gebruiker_id, status, ) {
        try {
            const response = await fetch(`/api/${endpoint}`, {
                method: "PATCH",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    status: actions.get(status) || status,
                    onderzoek_id: onderzoek_id,
                    gebruiker_id: gebruiker_id
                 }),
            });

            if (response.ok) {
                window.dispatchEvent(new Event('table-refresh'));
                showToast('success', `${names.get(endpoint)} is ${actions.get(status) || status}`);
            } else {
                showToast('error', `Fout bij het bijwerken van ${names.get(endpoint)}`);
            }
        } catch (error) {
            console.error(`Fout bij bijwerken van ${names.get(endpoint)}:`, error);
            showToast('error', `Er is een fout opgetreden bij het verwerken van de actie.`);
        }
    }

    function handleUserActions(action, id) {
        if (action === 'Details') {
            window.location.href = `/admin/user-detail?id=${id}`;
        } else if (actions.has(action)) {
            updateStatus('users', id, action);
        }
    }

    function handleOrganizationActions(action, id) {
        if (action === 'Details') {
            window.location.href = `/admin/organization-detail?id=${id}`;
        } else if (actions.has(action)) {
            updateStatus('organizations', id, action);
        }
    }

    function handleResearchActions(action, id) {
        if (action === 'Details') {
            window.location.href = `/admin/research-detail?id=${id}`;
        } else if (actions.has(action)) {
            updateStatus('researches', id, action);
        }
    }

    function handleSubscriptionActions(action, onderzoek_id, gebruiker_id) {
        if (action === 'Details') {
            window.location.href = `/admin/subscription-detail?onderzoek_id=${onderzoek_id}&gebruiker_id=${gebruiker_id}`;
        } else if (actions.has(action)) {
            updateSubscription('subscriptions', onderzoek_id, gebruiker_id, action);
        }
    }
});