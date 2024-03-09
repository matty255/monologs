/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

const plugin = require('tailwindcss/plugin');

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
              'clear-white': 'rgba(255, 255, 255, 0.75)',
              dark: {
                background: '#121212',
                text: '#E0E0E0',
                border: '#FFC107',
                primary: '#FFC107',
              },
              light: {
                background: '#FFFFFF',
                text: '#212121',
                border: '#FFC107',
                primary: '#FFC107',
              },
              },
              backgroundImage: theme => ({
                'custom-full-image': "url('../../../static/images/banners/background.webp')",
              }),
              fontFamily: {
                'Hippie': ['NanumHippie', 'sans-serif'],
                'Nanum': ['NanumSquare', 'sans-serif'],
                'Happiness': ['HappinessSans', 'sans-serif'],
                'WhiteTail': ['WhiteTail', 'sans-serif'],
              },
            },
          },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        plugin(function({ addUtilities }) {
          const newUtilities = {
            '.a11y': {
              display: 'inline-block',
              position: 'absolute',
              overflow: 'hidden',
              width: '1px',
              height: '1px',
              border: '0',
              clipPath: 'inset(50%)', 
            },
          };
          addUtilities(newUtilities, ['responsive', 'hover']);
        }),
        require("daisyui"),
        require("tailwind-scrollbar-hide"),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
