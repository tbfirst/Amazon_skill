# Lovart execution

Use this module to distinguish native Lovart use from an external agent installation.

## Inside Lovart

Use the generation, editing, canvas, and export tools actually available in the current session. The user selects the image model in Lovart's interface; preserve that selection. Model names and controls may change, so do not hard-code a model/version or infer availability from these instructions.

The standalone LOVART_INSTRUCTIONS.md contains all modules for a native custom skill; no local file access is needed after it is loaded. Select only relevant sections mentally. Saving and selecting a custom skill is separate from pasting a prompt into a normal conversation.

## In an external agent

Inspect the available, authorized Lovart tools or browser session. A text skill does not install a connector, create credentials, or make a Lovart API available. Use documented capabilities actually exposed by the current environment. Do not invent tool names, endpoints, model IDs, or a connection to the user's canvas.

If usable Lovart access exists, execute within the requested scope and retain the user's settings where the interface supports them. An API route may not inherit the web canvas's model or export settings: resolve required settings from confirmed task information rather than pretending the web selection transferred.

If access is unavailable, finish the useful preparation: give the ready-to-paste prompt, identify which reference is used for each role, and list only genuinely missing input. Clearly state that generation has not run. Do not silently substitute another image provider.

## Output settings and evidence

Use explicit current instructions first, then confirmed settings for this task, then observable current controls. Resolve contradictory width/height and aspect ratio before final generation. A ratio alone is not evidence of actual pixel dimensions.

When an exact requested size or format cannot be produced directly, use available export/resizing capabilities if they can meet the request without distorting the product. Otherwise explain the limitation and ask about the specific alternative; do not silently deliver a different specification. A flattened image is not an editable layered PSD.

Use actual export/file inspection to substantiate pixel dimensions, format, or alpha. A prompt saying “transparent PNG” and a rendered checkerboard do not prove transparency. A successful generation status does not establish product fidelity. If the result cannot be viewed, report that visual review is incomplete and avoid blind repair calls.

History and selected versions remain in Lovart. Reference selection is task-dependent; factual checks remain anchored to real product evidence.

## Native custom skill setup

Lovart's documentation describes Thinking Mode, a project conversation, then Skill Book → Create a Skill → My Skills. Later, select the saved skill in a new chat; instructions and examples can be edited. Use the supplied standalone instructions as the workflow material and check what was saved after creation.

Do not claim that Lovart directly imports a GitHub Agent Skills directory or automatically loads this skill merely from its name. Verify such a capability in the current product before promising it. Setup UI steps may change.

Source checked 2026-10-14: [Lovart Agent Skills and Custom Skills](https://www.lovart.ai/docs/how-to-prompt/agent-skills).
