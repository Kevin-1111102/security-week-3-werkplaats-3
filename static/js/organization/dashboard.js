import { showToast, confirmModal } from '../util/utils.js';
document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('tbody').addEventListener('click', function (event) {
        const target = event.target;
        const button = target.closest('.action-btn');

        if (!button) return;

        const action = button.getAttribute('data-action');
        const id = button.getAttribute('data-id');

        if (action === 'Bewerken') {
            window.location.href = `/organisatie/bewerk/${id}`;
        }

        if (action === 'Verwijderen') {
            confirmModal({
                title: 'Verwijderen onderzoek',
                message: `Weet je zeker dat je dit onderzoek wilt verwijderen?`,
                confirmText: 'Verwijderen',
                confirmClass: 'btn-danger',
                onConfirm: () => { handleDeleteResearch(button, id) }
            })
        }
    });

    function handleDeleteResearch(button, id) {
        fetch(`/api/researches/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                button.closest('tr').remove();
                showToast('success', `${data.message}`, 5000);
            })
            .catch(error => {
                console.error('error:', error);
                showToast('danger', 'Er is iets fout gegaan bij het verwijderen van het onderzoek');
            });
    }
});
