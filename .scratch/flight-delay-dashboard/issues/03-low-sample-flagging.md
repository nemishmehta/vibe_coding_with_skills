# 03: Low-sample visual flagging

**What to build:** In any grouped view, a group backed by a small flight count is visually flagged (e.g. muted styling or an explicit annotation) rather than displayed at the same visual weight as a high-volume group, so the user doesn't mistake a noisy, low-sample rate for a meaningful one. Implemented in the shared chart component so it applies automatically to the Route view once ticket 04 lands.

**Blocked by:** 02 (Destination view)

**Status:** ready-for-agent

- [ ] The chart component used to render grouped rates applies a distinct, visibly different treatment (e.g. muted color/opacity, or an inline annotation) to groups whose backing flight count falls below a reasonable low-sample threshold.
- [ ] The flagging is visible in the Destination view, where some destinations have far fewer flights than others.
- [ ] The flagging does not hide or remove low-sample groups from the ranking — it only changes how they're visually presented.
- [ ] The threshold and treatment are implemented once, in the shared chart component, not duplicated per view.
