(async () => {
    try {
        const navbarContainer = document.querySelector('#navbar');
        if (!navbarContainer) return;
        
        const response = await fetch('/components/navbar');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
  
        const data = await response.json();
        navbarContainer.innerHTML = '';
        
        const navItems = data.map(item => {
            const navItem = document.createElement('li');
            navItem.className = 'nav-item';
            let navLink;

            if (item[0] !== 'Logout') {
                navLink = document.createElement('a');
                navLink.href = item[1];
            } else {
                navLink = document.createElement('button');
                navLink.id = 'logout';
            }

            navLink.textContent = item[0];
            navLink.className = 'nav-link mx-3';
            navItem.appendChild(navLink);
            return navItem;
        });

        navbarContainer.append(...navItems);

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            if (link.href === window.location.href) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            }
        });

        const logout = document.querySelector('#logout');
        if (logout) {
            logout.addEventListener('click', (event) => {
                event.preventDefault();
                logoutRequest();
            });
        }

        async function logoutRequest() {
            try {
                const response = await fetch('/logout');
                const data = await response.json();
                if (data.success) {
                    window.location.href = data.redirect;
                }
            } catch (error) {
                console.error('Er ging iets mis tijdens het verwerken van uw verzoek: ', error);
            }
        }
        
    } catch (error) {
        console.error('Er ging iets mis bij het ophalen van de navigatie-elementen: ', error);
    }
})();