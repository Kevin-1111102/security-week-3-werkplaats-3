document.addEventListener('DOMContentLoaded', async function () {
    const userId = new URLSearchParams(window.location.search).get('id');
    if (!userId) {
        alert("Geen gebruiker ID opgegeven");
        window.location.href = '/dashboard';
        return;
    }

    const user = await fetchUserDetails(userId);
    if (user) {
        document.getElementById('user-info').innerHTML = createUserContent(user);
    } else {
        document.getElementById('user-info').innerHTML = '<p>Er is iets misgegaan bij het ophalen van de gegevens</p>';
    }

    document.getElementById('back-btn').addEventListener('click', () => {
        window.history.back();
    });
});

async function fetchUserDetails(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error("Fout bij ophalen van gegevens");
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error("Error:", error);
        return null;
    }
}

function createUserContent(user) {
    return `
        <p><strong>Naam:</strong><br>${user.voornaam} ${user.tussenvoegsel || ''} ${user.achternaam}</p>
        <p><strong>Email:</strong><br>${user.email}</p>
        <p><strong>Status:</strong><br>${user.status}</p>
        <p><strong>Postcode:</strong><br>${user.postcode || 'N/A'}</p>
        <p><strong>Contact Voorkeur:</strong><br>${user.contact_voorkeur || 'N/A'}</p>
        <p><strong>Beperkingen:</strong><br>${user.beperkingen && user.beperkingen.length > 0 
            ? user.beperkingen.join(', ') 
            : 'Geen beperkingen'}</p>
    `;
}
