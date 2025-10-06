const tabs = document.querySelectorAll('.tab');
const sections = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        activateTab(tab);
    });

    tab.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
            activateTab(tab);
        }
    });
});

function activateTab(tab) {
    tabs.forEach(tab => {
        tab.classList.remove('active');
        tab.attributes['aria-selected'].value = 'false';
    });

    sections.forEach(section => {
        section.classList.remove('active');
    });

    const index = [...tabs].indexOf(tab);
    sections[index].classList.add('active');
    tab.classList.add('active');
    tab.attributes['aria-selected'].value = 'true';
}