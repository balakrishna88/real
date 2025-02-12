module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        './static_src/**/*.js',
    ],
    darkMode: 'class', // Enable dark mode via class toggling
    theme: {
        extend: {
            colors: {
                // Light Theme
                light: {
                    primary: '#ffffff',
                    secondary: '#f4f4f4',
                    text: '#333333',
                    accent: '#007bff',
                    btnBg: '#007bff',
                    btnText: '#ffffff',
                },
                // Dark Theme
                dark: {
                    primary: '#121212',
                    secondary: '#1e1e1e',
                    text: '#ffffff',
                    accent: '#bb86fc',
                    btnBg: '#bb86fc',
                    btnText: '#000000',
                },
                // Blue Theme
                blue: {
                    primary: '#e7f3ff',
                    secondary: '#c9e4ff',
                    text: '#0d47a1',
                    accent: '#1e88e5',
                    btnBg: '#1e88e5',
                    btnText: '#ffffff',
                },
            },
        },
    },darkMode: 'class', // Enable dark mode via class toggling
    theme: {
        extend: {
            colors: {
                // Light Theme Colors
                'light-bg': '#f5f5f5',       // Grey background
                'light-divBg': '#fff3cd',   // Light yellow for divs
                'light-text': '#333333',    // Dark text
        
                // Dark Theme Colors
                'dark-bg': '#121212',       // Dark grey background
                'dark-divBg': '#bb86fc',    // Purple for divs
                'dark-text': '#ffffff',     // White text
        
                // Blue Theme Colors
                'blue-bg': '#3b82f6',       // Light blue background
                'blue-divBg': '#00308F',    // Lighter blue for divs
                'blue-text': '#ffffff',     // White text
              },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
};