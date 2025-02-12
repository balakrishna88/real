// static/js/theme-toggle.js

const toggleButton = document.getElementById('theme-toggle');
const themes = ['light', 'dark', 'blue']; // List of available themes
let currentThemeIndex = 0;

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme); // Save the selected theme
}

toggleButton.addEventListener('click', () => {
  currentThemeIndex = (currentThemeIndex + 1) % themes.length; // Cycle through themes
  applyTheme(themes[currentThemeIndex]);
});

// Load saved theme on page load
const savedTheme = localStorage.getItem('theme') || 'light'; // Default to 'light'
applyTheme(savedTheme);