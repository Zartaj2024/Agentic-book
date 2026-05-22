// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to scan your code
// without running it. This improves development experience and helps prevent bugs.

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI Book',
  tagline: 'An Interactive Textbook for Robotics and AI',
  favicon: 'img/favicon.svg',

  // Set the production url of your site here
  url: 'http://localhost:3000/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages: https://<USERNAME>.github.io/<REPO>/
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Zartaj2024', // Usually your GitHub org/user name.
  projectName: 'Agentic-book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Zartaj2024/Agentic-book/edit/main/docs-site/',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Book',
        logo: {
          alt: 'Physical AI Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            label: 'GitHub',
            position: 'right',
            href: 'https://github.com/Zartaj2024/Agentic-book',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Content',
            items: [
              {
                label: 'Textbook',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
             
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
             
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Zartaj2024/Agentic-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),

  plugins: [
    [
      'docusaurus-lunr-search',
      {
        languages: ['en'],
        maxSearchResults: 10,
        lunr: {
          b: 0.75,
          k1: 1.2,
          titleBoost: 10,
          contentBoost: 1,
          tagsBoost: 100,
          parentCategoriesBoost: 20,
        },
      },
    ],
  ],

};

// Pass environment variables to the frontend
const backendConfig = {
  API_URL: process.env.DOCUSAURUS_BACKEND_API_URL || '',
};

// Extend themeConfig with backend configuration
const originalThemeConfig = config.themeConfig;
config.themeConfig = {
  ...originalThemeConfig,
  backendConfig: backendConfig,
};

// Add custom fields to pass to the site
config.customFields = {
  BACKEND_API_URL: process.env.DOCUSAURUS_BACKEND_API_URL || '',
};

// Add a script to the head to configure the backend URL
config.headTags = [
  {
    tagName: 'script',
    attributes: {
      type: 'text/javascript',
    },
    innerHTML: `
      window.chatbotConfig = {
        API_URL: "${process.env.DOCUSAURUS_BACKEND_API_URL || ''}"
      };
    `,
  }
];

module.exports = config;