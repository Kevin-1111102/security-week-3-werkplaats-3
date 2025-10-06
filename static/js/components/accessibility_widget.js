import { setCookie, getCookie, isLightOrDark } from '../util/utils.js';

document.addEventListener('DOMContentLoaded', function () {
    const accessibilityForm = document.getElementById('accessibility-form');
    const themeSelect = document.getElementById('theme-select');
    const customColors = document.getElementById('custom-colors');
    const colorInputs = document.querySelectorAll('input[type="color"]');
    const body = document.body;

    // apply theme to the page
    function applyTheme(theme) {
        body.removeAttribute('style');
        body.setAttribute('data-bs-theme', theme);
        
        if (theme === 'custom') {
            applyCustomColors();
        }
    }

    // apply custom colors from cookie to variables and inputs
    function applyCustomColors() {
        const savedColors = getCookie('custom-colors');
        if (savedColors) {
            const colors = JSON.parse(savedColors);
            console.log(colors);
            for (const [key, value] of Object.entries(colors)) {
                body.style.setProperty(`--${key}`, value);
                document.getElementById(`${key}-color`).value = value;

                // determine if user has a light or dark background
                if (key === 'background') {
                    const theme = isLightOrDark(value);
                    body.setAttribute('data-bs-theme', theme);
                }
            }
        }
    }

    // set custom colors to cookie from inputs
    function setCustomColors() {
        const colors = {};
        colorInputs.forEach(input => {
            colors[input.name] = input.value;
        });

        setCookie('custom-colors', JSON.stringify(colors), 31);
    }

    // load previous custom colors from cookie to inputs
    function loadPreviousColors() {
        const savedColors = getCookie('custom-colors');
        if (savedColors) {
            const colors = JSON.parse(savedColors);
            for (const [key, value] of Object.entries(colors)) {
                document.getElementById(`${key}-color`).value = value;
            }
        }
    }

    // handle theme-select change
    function handleThemeSelect() {
        const isCustomTheme = themeSelect.value === 'custom';
        customColors.classList.toggle('d-none', !isCustomTheme);
        if (isCustomTheme)
            loadPreviousColors();
    }

    // handle form submit
    function handleFormSubmit(event) {
        event.preventDefault();
        const theme = themeSelect.value;
        if (theme === 'custom')
            setCustomColors();

        setCookie('theme', theme, 31);
        applyTheme(theme);
    }
    
    function init() {
        const savedTheme = getCookie('theme') || 'light';
        themeSelect.value = savedTheme;
        
        applyTheme(savedTheme);
        handleThemeSelect();

        accessibilityForm.addEventListener('submit', handleFormSubmit);
        themeSelect.addEventListener('change', handleThemeSelect);
    }

    init();
});