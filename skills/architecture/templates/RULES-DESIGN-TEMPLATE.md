<!--
Instructions for the agent: produce this file as
`_devprocess/rules/design.md` ONLY when the project has UI surface that
needs design discipline. Skip the file for headless projects.

Write the prose in the user's working language. Keep keywords (Color,
Layout, Spacing, etc.) in English.

Hard cap: 100 lines. Component-specific details go into the component's
file or its module README, not here.
-->

# Design rules for {project-name}

> Max 100 lines. Loaded only when UI changes are in scope.

## Design system

- Primary color: {e.g. #000099}
- Accent color: {e.g. #FE8F11}
- Color distribution: {e.g. 60-30-10 rule}
- Typeface: {e.g. system font stack}

## Layout

- {e.g. Responsive breakpoint at 768px}
- {e.g. Max content width: 1200px}
- {e.g. Spacing scale: 4px base unit}

## Component patterns

- {one rule, e.g. "Inputs always carry label plus error state."}
- {one rule, e.g. "Loading: skeleton placeholders, not spinners."}
- {one rule, e.g. "Modals: at most one visible at a time."}

## Accessibility

- {e.g. WCAG 2.1 AA minimum}
- {e.g. Every interactive element reachable by keyboard}
- {e.g. Color contrast >= 4.5:1}

## Animations

- {e.g. Duration 150-300ms, ease-out}
- {e.g. Honor reduced-motion preference}
