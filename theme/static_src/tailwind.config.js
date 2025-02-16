module.exports = {
    content: [
        "../templates/**/*.html",  // Theme app templates
        "../../templates/**/*.html",  // Main templates directory
        "../../**/templates/**/*.html",  // Other Django apps' templates
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/aspect-ratio"),
        require("daisyui"),  // Added DaisyUI plugin
    ],
    daisyui: {
        themes: ["light","dark","cupcake","bumblebee","emerald","corporate","synthwave","retro","cyberpunk","valentine","halloween","garden","forest",
      ],  // Predefined themes
    },
};
