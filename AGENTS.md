# Continuing Credit Studio

Before changing this repository, read `docs/PROJECT_HANDOFF.md` and `README.md`.
For video production, also read the current video's README, script and storyboard.

- Communicate with the user in Vietnamese. Current video narration targets US viewers in English.
- Preserve the user's Times New Roman preference throughout the editors, captions and rendered video.
- For icon-and-label cards, center both the artwork and label horizontally within each card; use balanced padding and consistent spacing across the group. The user requested this for future video layouts after reviewing the Taxes card.
- Check character silhouettes against image crops, canvas edges and foreground text/background panels. Keep heads, hands and feet intact unless a crop is intentional; inspect composited frames at entrance, middle and exit. The “PLAN AROUND WHAT ARRIVES” hair occlusion is corrected in salary review v02; the preserved v01 still contains the defect.
- Shared props live in `library/props/catalog.json` and the root “Kho đạo cụ” view. Preserve stable IDs, paths and source sheets; register new prop images with `tools/index-props.py`, then add descriptive names/categories/tags and verify crops. R2 credentials are now provided as direct environment variables and read/write access was verified; 26 media files have been copied and SHA-256 verified on R2; the runtime manifest remains disabled pending manual CORS and real-browser verification. Originals remain on GitHub. See docs/R2_SETUP.md. Never log credentials.
- Keep the root website as the single project-management entry point; preserve existing project IDs and saved-project compatibility.
- Preserve source audio, existing projects and user edits. Do not overwrite original recordings or previous exports without an explicit reason and authorization.
- Browser drafts and attachments live in IndexedDB, not GitHub. Do not assume repository files include the user's latest browser edits; request a project backup when those edits are needed.
- The first video now has a animated 486.75-second review in `review-v03/` (88 shots, 23 animated layers in 11 clips); `review-v02/` is preserved; the original `review/` (64 shots) and MP4 v01 are preserved; `intro/` is the preserved 40.5-second style draft. Distinguish a full review from a user-approved final export.
- Update the handoff after significant changes, recording what is implemented, verified and still pending. Never put credentials or private chat data in it.

Use validation appropriate to the change; commands and deployment instructions are in README.md. Documentation-only changes do not require video rendering or browser tests.

- Content animation uses validated per-layer `animation` keys in `video/engine.js`. Keep interpolation deterministic for seeking/export, and preserve legacy projects with no animation. Currency and account-meter widths must agree; calendar rollover uses step easing. UI controls live in `video/editor.js`. Tests: `video-motion.mjs`, `video-motion-editor.cjs`, `salary-motion-review.cjs`, `salary-motion-upgrade.cjs`.

- Video 003 (`videos/003-car-payment-trap/`, `finance-003`) has a full 98-clip / 522.2-second review in `review/` and MP4 `exports/full-review-v01.mp4`, pending user approval. Its 16 artwork designs, 8 illustrations and 12 isolated assets are preserved. `storyboard/project.json` remains the original silent 96-second browsing board, revision `car-artwork-board-v01`; browser drafts are archived before promotion to `car-payment-review-v01`. Original WAV is `audio/tts_20261022_115123_7124d9.wav`. Audio uses the earlier time transition; trade-in figures are explicitly a separate hypothetical example. Shared library now has 73 items (59 props, 14 Alex poses).

- Video 004 (`videos/004-living-alone/`, `finance-004`): **Why Living Alone Has Become So Expensive**, new documentary photographic collage style, ivory paper/burgundy/Times New Roman; do not force the old drawn Alex style onto it. 16 editable artwork boards, 8 generated illustrations, 2 transparent 4×2 atlases and 16 padded isolated props (`solo4-*`). Shared library now **89 items: 75 props, 14 Alex poses**. `storyboard/project.json` is only a silent **96-second artwork board**, revision `living-artwork-board-v01`; no narration or MP4 yet. Preserve the 1,279-word script, historical 2024 data labels, example budget and no-overwrite rules. Review `storyboard.md` and `sources.md` before editing.
