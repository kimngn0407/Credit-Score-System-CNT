/** @type {import('tailwindcss').Config} */
export default {
	darkMode: 'class',
	content: ['index.html', './src/**/*.{ts,tsx}'],
	theme: {
		extend: {
		colors: {
			primary: {
				DEFAULT: '#60a5fa', // xanh dương nhạt
				light: '#93c5fd',
				dark: '#2563eb',
			},
		},
	},
	},
	plugins: [],
};

