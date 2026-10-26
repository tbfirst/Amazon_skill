# Validation status

For the strategy skill added on 2026-10-15, see [strategy design and validation](AMAZON-STRATEGY.zh-CN.md). The following records the original individual-image skill release only.

Date: 2026-10-14. Package: Plant Product Image Skills, v1.0.0.

## Checks performed

| Check | Result |
| --- | --- |
| Bundled skill-creator quick_validate.py | Passed: frontmatter and skill structure |
| Name and description | Folder/name agree; English description within format limit; scope limited to Lovart plant imagery |
| Optional host metadata | YAML parsed; implicit invocation enabled; display text and default invocation match the skill |
| Functional resources | All nine reference files linked: eight functional modules plus Lovart execution |
| Standalone build | Generated successfully from English sources; --check confirms synchronization |
| Builder failure handling | Isolated temporary copy correctly rejected stale output and a missing source module; rebuild restored synchronization |
| Portability | Local Markdown references checked; no old project paths or user-machine paths embedded in distribution sources |
| Collection structure | One discoverable skill; no root-level umbrella SKILL.md or empty future skill folders |
| Git and license | Local Git repository initialized for the v1.0.0 initial commit; generated dist/ archives ignored; no LICENSE or license frontmatter added |
| Behavioral coverage | Maintainer text walkthrough of 20 cases; no independent agent execution or image-quality pass claimed |

The text walkthrough covered source roles, sale scope, permitted rearrangement, MAIN versus scenes, dimensional truth, copy claims, material identity, repair limits, prompt-only requests, missing Lovart access, alpha evidence, contradictory export settings, and out-of-scope routing.

## Not performed

- No account installation, actual installer discovery command, or live automatic skill selection.
- No Lovart custom skill saved or loaded in an account.
- No model generation/edit/export calls, visual comparison, or paid generation.
- No validation of Lovart instruction-length limits, current account UI, selected-model behavior, or export formats.
- No GitHub repository creation/publication and no audit or rewriting of the prior project's Git history.
- No independent subagent forward test in this continuation.

The packaged rules and local checks are complete. Live usability and image quality remain unverified.

## First live trial

Use the actual user's product photos and confirmed facts. Start with one bouquet lifestyle image, a four-reference integration task, an angle correction, and a dimension/detail image with real measurements. Also try a white-background MAIN task to ensure the default European scene does not leak into it.

Check: the saved custom skill retains the supplied rules; Chinese requests route correctly; the selected model is preserved; actual exported settings match; flowers/leaves/container stay faithful; contact/occlusion/shadow agree; viewpoint follows visible intent; labels are accurate; repairs stop at the shared limit.

Record the source assets, request, observable settings, actual outputs, defects, and repair rounds in Lovart's existing history. If the editor cannot hold the complete instructions, assess the observed limit before changing the packaging; do not silently truncate product protections.
