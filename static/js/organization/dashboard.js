import { showToast } from '../util/utils.js';
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('tbody').addEventListener('click', function (event) {
        const target = event.target;
        const button = target.closest('.action-btn');

        if (!button) return;

        const action = button.getAttribute('data-action');
        const id = button.getAttribute('data-id');

        if (action === "Bewerken") {
            window.location.href = `/organisatie/bewerk/${id}`;
        }

        if (action === "Verwijderen") {
            fetch(`/api/researches/${id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(':(');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Success:", data);
                    button.closest('tr').remove();
                    showToast('success', `${data.message}`, 5000);
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    showToast('danger', 'Er is iets misgegaan bij het verwijderen van het onderzoek');
                });
        }
    });
});
