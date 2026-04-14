import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'home-hero-before': () =>
        h('div', { class: 'hero-works-badge' }, [
          h(
            'span',
            null,
            'Claude Code │ Codex │ Gemini │ GitHub Copilot │ OpenCode',
          ),
        ]),
    })
  },
}
