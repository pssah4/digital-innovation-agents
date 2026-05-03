import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

const tutorialsSidebar = [
  {
    text: 'Tutorials',
    items: [
      { text: 'Installation', link: '/tutorials/installation' },
      { text: 'Your first Business Analysis', link: '/tutorials/first-business-analysis' },
      { text: 'A full V-Model run', link: '/tutorials/full-v-model-run' },
    ],
  },
]

const guidesSidebar = [
  {
    text: 'Orientation',
    items: [
      { text: 'Using DIA', link: '/guides/using-digital-innovation-agents' },
    ],
  },
  {
    text: 'Guide',
    items: [
      { text: 'V-Model workflow guide', link: '/guides/dia-guide' },
    ],
  },
  {
    text: 'Brownfield entry',
    items: [
      { text: 'Reverse Engineering', link: '/guides/reverse-engineering' },
    ],
  },
  {
    text: 'Migration',
    items: [
      { text: 'DIA Migration', link: '/guides/dia-migration' },
    ],
  },
  {
    text: 'Design phases (left side of V)',
    items: [
      { text: 'Business Analysis', link: '/guides/business-analysis' },
      { text: 'Requirements Engineering', link: '/guides/requirements-engineering' },
      { text: 'Architecture', link: '/guides/architecture' },
    ],
  },
  {
    text: 'Implementation',
    items: [
      { text: 'Coding', link: '/guides/coding' },
    ],
  },
  {
    text: 'Verification (right side of V)',
    items: [
      { text: 'Testing', link: '/guides/testing' },
      { text: 'Security Audit', link: '/guides/security-audit' },
    ],
  },
  {
    text: 'Foundations',
    items: [
      { text: 'Project Conventions', link: '/guides/project-conventions' },
      { text: 'Consistency Check', link: '/guides/consistency-check' },
      { text: 'Humanizer', link: '/guides/humanizer' },
    ],
  },
]

const referenceSidebar = [
  {
    text: 'Reference',
    items: [
      { text: 'Commands', link: '/reference/commands' },
      { text: 'Artifacts', link: '/reference/artifacts' },
      { text: 'Conventions', link: '/reference/conventions' },
      { text: 'Reachability by stack', link: '/reference/reachability-by-stack' },
      { text: 'Troubleshooting', link: '/reference/troubleshooting' },
    ],
  },
  {
    text: 'Methods (BA and RE toolkit)',
    items: [
      { text: 'Discovery methods', link: '/reference/methods-discovery' },
      { text: 'Ideation methods', link: '/reference/methods-ideation' },
      { text: 'Validation methods', link: '/reference/methods-validation' },
    ],
  },
]

const conceptsSidebar = [
  {
    text: 'Foundations',
    items: [
      { text: 'The V-Model', link: '/concepts/v-model' },
      { text: 'Three-layer documentation model', link: '/concepts/three-layer-documentation' },
      { text: 'Living Documents', link: '/concepts/living-documents' },
      { text: 'Drift defense', link: '/concepts/drift-defense' },
    ],
  },
  {
    text: 'Discipline patterns',
    items: [
      { text: 'Tech-agnostic Requirements', link: '/concepts/tech-agnostic-requirements' },
      { text: 'Handoff Rituals', link: '/concepts/handoff-rituals' },
      { text: 'Verification Gates', link: '/concepts/verification-gates' },
    ],
  },
]

export default withMermaid(
  defineConfig({
    title: 'Digital Innovation Agents',
    description: 'AI-augmented Innovation & Development Workflow. From raw idea to production-ready code through structured, quality-gated phases.',
    base: '/digital-innovation-agents/',
    head: [
      ['meta', { property: 'og:title', content: 'Digital Innovation Agents' }],
      ['meta', { property: 'og:description', content: 'AI-augmented V-Model workflow from business analysis to security audit.' }],
      ['meta', { name: 'keywords', content: 'V-Model, innovation, business analysis, requirements engineering, architecture, ADR, arc42, OWASP, Claude Code, Cursor, Codex' }],
    ],

    appearance: { initialValue: 'light' },
    lastUpdated: true,
    cleanUrls: true,
    lang: 'en',

    themeConfig: {
      siteTitle: 'Digital Innovation Agents',
      nav: [
        { text: 'Tutorials', link: '/tutorials/installation', activeMatch: '/tutorials/' },
        { text: 'Guides', link: '/guides/dia-guide', activeMatch: '/guides/' },
        { text: 'Reference', link: '/reference/commands', activeMatch: '/reference/' },
        { text: 'Concepts', link: '/concepts/v-model', activeMatch: '/concepts/' },
        { text: 'PULSE', link: '/pulse' },
        { text: 'About', link: '/about' },
      ],
      sidebar: {
        '/tutorials/': tutorialsSidebar,
        '/guides/': guidesSidebar,
        '/reference/': referenceSidebar,
        '/concepts/': conceptsSidebar,
      },
      socialLinks: [
        { icon: 'github', link: 'https://github.com/pssah4/digital-innovation-agents' },
      ],
      search: {
        provider: 'local',
      },
      editLink: {
        pattern: 'https://github.com/pssah4/digital-innovation-agents/edit/main/docs/:path',
        text: 'Edit this page on GitHub',
      },
      footer: {
        message: '<a href="https://github.com/pssah4/digital-innovation-agents/blob/main/LICENSE">MIT License</a> | <a href="/digital-innovation-agents/imprint">Imprint</a>',
        copyright: 'Provided as-is, without any warranty or liability.',
      },
    },

    mermaid: {},
  }),
)
