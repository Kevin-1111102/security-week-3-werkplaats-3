import {showToast} from "../util/utils.js";

document.getElementById("research-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch("/api/researches/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            console.log("Response status:", response.status);

            if (!response.ok) {
                return response.json().then(err => {
                    console.log("Error Response Body:", err);
                    throw new Error(err.message || `Error ${response.status}`);
                });
            }

            return response.json();
        })
        .then(data => {
            console.log("Success:", data);
            showToast('success', `${data.message}`, 5000);
            setTimeout(() => {
                window.location.href = `/organisatie`;
            }, 2000);
        })
        .catch(error => {
            console.error("Fetch error:", error);
            showToast('danger', 'Er is iets fout gegaan bij het maken van een onderzoek');
        });
});

document.addEventListener('DOMContentLoaded', () => {
    fetch(`/api/disabilities/categories`)
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            }

            if (data.success && data.data) {
                const disabilitySelect = document.getElementById('disability-category');

                data.data.forEach(disability => {
                    const option = document.createElement('option');
                    option.value = disability.beperking_categorie;
                    option.textContent = disability.beperking_categorie;
                    disabilitySelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

