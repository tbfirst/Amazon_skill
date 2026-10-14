# Quality and repair

Review every actual result against the current request and product evidence. A generation status or model self-report is not proof of fidelity.

## Review in priority order

1. **Product identity:** type, flower/leaf shapes, key branches, color, texture, quantities, container, markings, and included items. Assess explicitly permitted arrangement changes separately.
2. **Physical integration:** scale, support/contact, insertion depth, occlusion, load-bearing structure, intersections, light, shadows, and replaced-object remnants.
3. **Composition:** shot distance, horizontal facing and pitch, placement, coverage, completeness, and allowed cropping.
4. **Local quality:** halos, ghosting, broken stems, fused shapes, patches, sharpness discontinuities, exposure, and color drift.
5. **Information and delivery:** image type, factual copy, numbers/units, annotation position, requested count and export settings. Confirm alpha only through actual inspection.

Use relevant checks for the image type. Hidden details, tiny unreadable components, and unproven performance remain unverifiable; do not fill gaps with confident claims.

## Shared repair budget

After the initial generation, automatically repair material defects for at most **three rounds**. The initial generation is not a repair round. Deliver sooner if satisfactory.

A round is one targeted repair attempt on each failed candidate in the current task. Candidate batches share at most three review/repair cycles. Leave passed candidates unchanged; each failed candidate gets at most one repair attempt per round.

All modules and regions share the counter. Restarting from a source, revising prompts, or changing edit methods still counts. A failed repair tool call consumes that attempt. Do not reset the counter by relabeling automatic work as a new task. Do not switch the user's model or add candidates to evade the cap.

Before each round, identify the observable failure and choose an appropriate local edit, reframing, or source-based redo. Update the instruction using result feedback rather than repeating it mechanically.

Report service/tool failures as such, not as visual defects. When results cannot be viewed, stop blind automatic repair and explain that visual review is incomplete. A new user-requested modification is a new task; automatic retries are not.

## Stop and deliver

Show actual results. If defects remain after three repair rounds, stop and state the unresolved issue, which candidates are relatively usable, and what specific evidence or user decision would help.

For example, only when actually observed: “After three repair rounds, the right leaf cluster still differs from the product photo. This is not ready as a final image. A clearer photo of that area or a composition that retains the original subject would help.”

Keep history and selections in Lovart. Review is assistance, not a guarantee that every leaf, pixel, or marketplace check passed.
