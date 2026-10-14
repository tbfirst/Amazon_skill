# Plant Product Image Skills

A growing collection of Agent Skills for plant merchandise imagery. The first release contains one Lovart-focused skill, with English execution rules and a [Chinese guide](README.zh-CN.md).

**Status:** v1.0.0 local Git repository, 2026-10-14, ready for its initial commit and user-managed push. No GitHub repository has been published. No open-source license has been selected or granted by this package.

## Available skill

| Skill | Use |
| --- | --- |
| [lovart-plant-product-images](skills/lovart-plant-product-images/SKILL.md) | Turn everyday requests and product references into faithful Lovart plant imagery: preparation, integration, scenes, composition, refinement, lighting, individual information images, and review |

Supports real and artificial plants, wreaths, bouquets, potted plants, and flower boxes. Full Amazon listing image campaigns are planned, not implemented.

Each skill lives in its own directory. Supporting modules are resources within that skill, not separately installed skills. Installed metadata helps a compatible agent select the relevant skill; actual discovery and activation depend on the host. Cloning this collection alone does not register it with every agent.

## Install into an agent

Use a host that supports the [Agent Skills format](https://agentskills.io/specification). Install the whole skill directory, including references. Installation provides workflow instructions; generating in Lovart still requires a usable, authorized Lovart integration or browser session.

With Node.js/npm and the third-party [skills CLI](https://github.com/vercel-labs/skills), run these commands from the collection root. They preview or install locally; installation prompts select the target agent:

```sh
npx skills add . --list
npx skills add . --skill lovart-plant-product-images
```

After this collection has a real GitHub URL, replace OWNER/REPOSITORY below with it. These are publication templates, not an existing repository:

```sh
npx skills add OWNER/REPOSITORY --list
npx skills add OWNER/REPOSITORY --skill lovart-plant-product-images
npx skills add OWNER/REPOSITORY --skill '*'
```

The last command selects every skill currently present; it does not automatically install future additions. Retain interactive target selection. Alternatively, copy each complete skill folder into the host's documented skill directory and reload/rescan as that host requires. No custom collection router or fabricated connector manifest is necessary.

This package includes optional agents/openai.yaml UI metadata with implicit selection enabled. Host support varies; the portable entrypoint remains SKILL.md. No installer or authenticated Lovart session was executed during packaging.

## Use in Lovart itself

The [standalone instructions](skills/lovart-plant-product-images/LOVART_INSTRUCTIONS.md) include all functional modules without local file dependencies.

Lovart documents Thinking Mode and a project conversation, followed by Skill Book → Create a Skill → My Skills. Use the standalone text as workflow material in that conversation, save the custom skill, and check/edit its saved instructions. Then select it in a new chat and supply your images and request. The full procedure and an example starter message are in the [Chinese guide](README.zh-CN.md). Direct GitHub/SKILL.md import into Lovart is not established by the documentation. [Lovart documentation](https://www.lovart.ai/docs/how-to-prompt/agent-skills)

Example request:

> Use the plant product image skill. Place my bouquet in a realistic European balcony scene. Only the bouquet is sold. Keep its flowers and colors unchanged. One 2048 × 2048 PNG.

The requested dimensions are an example, not a default. The user controls Lovart's selected model. English rules still accept Chinese and other natural-language requests; reply in the user's language.

## Maintain and verify

Edit SKILL.md and references, then regenerate the standalone delivery file with Python 3.10+ (standard library only):

```sh
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py --check
```

[Behavioral cases](skills/lovart-plant-product-images/evaluation/CASES.md) cover product facts, reference roles, execution boundaries, and repair behavior. [Validation status](docs/VALIDATION.md) separates structural checks from unperformed Lovart image tests. [Design and roadmap](docs/DESIGN.zh-CN.md) records accepted requirements and future image-set work.

Add future skills under skills/<skill-name>/ with distinct descriptions only when implemented. Do not turn roadmap ideas into discoverable empty skills.

## Publication status

The collection is versioned in a local Git repository; the user will configure the remote and push. Generated archives in dist/ are kept locally and excluded from Git. Decide the license and repository identity before public distribution. There is intentionally no LICENSE file or license frontmatter field. The absence of a license is not an open-source grant. No Git initialization, commit, history rewrite, account installation, or publication is performed by the bundled build script.
