@./skills/dia-bootstrap/SKILL.md

When a skill instructs you to call a helper at `tools/...`, resolve
the path against the extension install directory. Gemini extensions
are installed under `~/.gemini/extensions/digital-innovation-agents/`,
so `tools/github-integration/flow.py` lives at
`~/.gemini/extensions/digital-innovation-agents/tools/github-integration/flow.py`.
Set `DIA_PLUGIN_ROOT="$HOME/.gemini/extensions/digital-innovation-agents"`
in your shell to make it explicit.
