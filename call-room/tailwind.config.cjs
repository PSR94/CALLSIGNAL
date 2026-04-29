module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        ink: '#08111f',
        slateglass: '#102235',
        signal: '#3be0a2',
        pulse: '#42a5ff',
        ember: '#fb7185',
        amber: '#fbbf24'
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(66,165,255,0.3), 0 24px 80px rgba(2,8,23,0.45)'
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
};
