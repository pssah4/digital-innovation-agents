/**
 * Digital Innovation Agents plugin for OpenCode.ai
 *
 * Injects bootstrap context via system prompt transform.
 * Auto-registers skills directory via config hook (no symlinks needed).
 *
 * Adapted from superpowers plugin:
 * https://github.com/obra/superpowers/blob/main/.opencode/plugins/superpowers.js
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Simple frontmatter extraction (avoid dependency on skills-core for bootstrap)
const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};

  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }

  return { frontmatter, content: body };
};

// Normalize a path: trim whitespace, expand ~, resolve to absolute
const normalizePath = (p, homeDir) => {
  if (!p || typeof p !== 'string') return null;
  let normalized = p.trim();
  if (!normalized) return null;
  if (normalized.startsWith('~/')) {
    normalized = path.join(homeDir, normalized.slice(2));
  } else if (normalized === '~') {
    normalized = homeDir;
  }
  return path.resolve(normalized);
};

export const DigitalInnovationAgentsPlugin = async ({ client, directory }) => {
  const homeDir = os.homedir();
  const pluginRoot = path.resolve(__dirname, '../..');
  const skillsDir = path.resolve(pluginRoot, 'skills');
  const envConfigDir = normalizePath(process.env.OPENCODE_CONFIG_DIR, homeDir);
  const configDir = envConfigDir || path.join(homeDir, '.config/opencode');

  // Export DIA_PLUGIN_ROOT so skills can resolve helper scripts under
  // tools/, hooks/, scripts/. The skills reference these as
  // ${DIA_PLUGIN_ROOT}/tools/... at runtime.
  if (!process.env.DIA_PLUGIN_ROOT) {
    process.env.DIA_PLUGIN_ROOT = pluginRoot;
  }

  // Resolve the project's mode from .dia/config.toml. Walks upwards
  // from the OpenCode session directory looking for the closest
  // config file. Returns 'git-only' as the default when nothing is
  // found, matching the SessionStart hook fallback.
  const readDiaMode = () => {
    let dir = directory ? path.resolve(directory) : process.cwd();
    const root = path.parse(dir).root;
    while (true) {
      const candidate = path.join(dir, '.dia', 'config.toml');
      try {
        if (fs.existsSync(candidate)) {
          const text = fs.readFileSync(candidate, 'utf8');
          const match = text.match(/^[ \t]*mode\s*=\s*"(off|git-only|github-sync)"/m);
          return match ? match[1] : 'git-only';
        }
      } catch {
        // ignore and walk up
      }
      if (dir === root) return 'git-only';
      const parent = path.dirname(dir);
      if (parent === dir) return 'git-only';
      dir = parent;
    }
  };

  const diaMode = readDiaMode();

  // Helper to generate bootstrap content
  const getBootstrapContent = () => {
    const skillPath = path.join(skillsDir, 'dia-bootstrap', 'SKILL.md');
    if (!fs.existsSync(skillPath)) return null;

    const fullContent = fs.readFileSync(skillPath, 'utf8');
    const { content } = extractAndStripFrontmatter(fullContent);

    const toolMapping = `**Tool Mapping for OpenCode:**
When skills reference tools you don't have, substitute OpenCode equivalents:
- \`TodoWrite\` -> \`todowrite\`
- \`Task\` tool with subagents -> Use OpenCode's subagent system (@mention)
- \`Skill\` tool -> OpenCode's native \`skill\` tool
- \`Read\`, \`Write\`, \`Edit\`, \`Bash\` -> Your native tools

Use OpenCode's native \`skill\` tool to list and load skills.`;

    return `<EXTREMELY_IMPORTANT>
You have Digital Innovation Agents skills.

**IMPORTANT: The dia-bootstrap skill content is included below. It is ALREADY LOADED - you are currently following it. Do NOT use the skill tool to load "dia-bootstrap" again - that would be redundant.**

${content}

${toolMapping}
</EXTREMELY_IMPORTANT>`;
  };

  return {
    // Inject skills path into live config so OpenCode discovers the skills
    // without requiring manual symlinks or config file edits. Skipped
    // when the project opts out via mode = "off" so the plugin really
    // disappears for that project.
    config: async (config) => {
      if (diaMode === 'off') return;
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }
    },

    // Inject bootstrap into the first user message of each session.
    // Using a user message instead of a system message avoids:
    //   1. Token bloat from system messages repeated every turn
    //   2. Multiple system messages breaking some models
    // Skipped when the project's mode is "off" so the bootstrap stays
    // silent on opted-out projects, matching the SessionStart hook
    // semantics documented in docs/concepts/three-modes.md.
    'experimental.chat.messages.transform': async (_input, output) => {
      if (diaMode === 'off') return;
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages.length) return;
      const firstUser = output.messages.find(m => m.info.role === 'user');
      if (!firstUser || !firstUser.parts.length) return;
      // Only inject once
      if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('EXTREMELY_IMPORTANT'))) return;
      const ref = firstUser.parts[0];
      firstUser.parts.unshift({ ...ref, type: 'text', text: bootstrap });
    }
  };
};
