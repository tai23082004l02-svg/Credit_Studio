# Continuing Credit Studio

Before changing this repository, read `docs/PROJECT_HANDOFF.md` and `README.md`.
For video production, also read the current video's README, script and storyboard.

- Communicate with the user in Vietnamese. Current video narration targets US viewers in English.
- Preserve the user's Times New Roman preference throughout the editors, captions and rendered video.
- For icon-and-label cards, center both the artwork and label horizontally within each card; use balanced padding and consistent spacing across the group. The user requested this for future video layouts after reviewing the Taxes card.
- Check character silhouettes against image crops, canvas edges and foreground text/background panels. Keep heads, hands and feet intact unless a crop is intentional; inspect composited frames at entrance, middle and exit. Known review defect: the headline background covers Alex's hair in the “PLAN AROUND WHAT ARRIVES” shot. User flagged it for future attention; it has not yet been corrected in the current export.
- Shared props live in `library/props/catalog.json` and the root “Kho đạo cụ” view. Preserve stable IDs, paths and source sheets; register new prop images with `tools/index-props.py`, then add descriptive names/categories/tags and verify crops. R2 is deferred.
- Keep the root website as the single project-management entry point; preserve existing project IDs and saved-project compatibility.
- Preserve source audio, existing projects and user edits. Do not overwrite original recordings or previous exports without an explicit reason and authorization.
- Browser drafts and attachments live in IndexedDB, not GitHub. Do not assume repository files include the user's latest browser edits; request a project backup when those edits are needed.
- The first video now has a complete 486.75-second review in `review/` (64 shots); `intro/` is the preserved 40.5-second style draft. Distinguish a full review from a user-approved final export.
- Update the handoff after significant changes, recording what is implemented, verified and still pending. Never put credentials or private chat data in it.

Use validation appropriate to the change; commands and deployment instructions are in README.md. Documentation-only changes do not require video rendering or browser tests.
