import { showToast, confirmModal } from '../util/utils.js';

document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.querySelector('.table-section');
    tbody.addEventListener('click', function (event) {
        const target = event.target;
        const button = target.closest('.action-btn');

        if (!button) return;

        const action = button.getAttribute('data-action');
        const id = button.getAttribute('data-id');

        if (action === 'Informatie') {
            window.location.href = `/api/researches/${id}`;
        }

        if (action === 'Aanmelden') {
            target.disabled = true;
            handleJoinResearch(target, id); 
        }

        if (action === 'Afmelden') {
            const title = target?.closest('tr')?.querySelector('td')?.textContent

            confirmModal({
                title: 'Afmelden onderzoek',
                message: `Weet je zeker dat je je wilt afmelden voor <strong>${title||'dit onderzoek'}</strong>?`,
                confirmText: 'Afmelden',
                confirmClass: 'btn-danger',
                onConfirm: () => handleWithdrawFromResearch(target, id)
            });
        }

    });

    // handle user research join
    function handleJoinResearch(target, id) {
        fetch(`/api/subscriptions/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                const row = target.closest('tr');
                if (data.success && row) {
                    window.dispatchEvent(new Event('table-refresh'));
                    showToast('success', `${data.message}`);
                }
            })
            .catch(error => {
                showToast('error', 'Er is iets fout gegaan bij het inschrijven');
                console.error('Fetch error:', error);
            });
    }

    function handleWithdrawFromResearch(target, id) {
        fetch(`/api/subscriptions/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                const row = target.closest('tr');
                if (data.success && row) {
                    window.dispatchEvent(new Event('table-refresh'));
                    showToast('success', `${data.message}`);
                }
            })
            .catch(error => {
                showToast('error', 'Er is iets fout gegaan bij het uitschrijven');
                console.error('Fetch error:', error);
            });
    }

    // handle filter submit
    function filterHandler(filter) {
        filter.preventDefault();
    }

    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', filterHandler);
    });
});