## 🎨 EXPORT / GRADIENT / RENDER RULES

* **CSS gradients allowed on backgrounds only.** `background: linear-gradient(...)` / `radial-gradient(...)`, glow blobs, bars, buttons are fine.
* **Gradient text forbidden — CSS or SVG.** No `background-clip:text`/`text-fill-color:transparent`, no `<text fill="url(#grad)">`. Text is solid colours only (`#FF9500`, `#fff`, theme accents).
* **html2canvas compatible:** `html2canvas({ scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#080808', logging: false })`. Chrome-hiding uses `visibility:'hidden'` (NOT `display:'none'`). Always hide `[data-chrome], #download-panel, .posts-shell, .swb, .section-label, .section-divider, .gcard-wrap`. Always save/restore `track.style.transform`/`transition` in a `try/finally`, and `waitForSlideAssets(slide)` + double `requestAnimationFrame` before capture. `captureSlide()` must use the exact pattern from the project-constitution.md.

### Export bugs — do not re-introduce
1. Swipe arrow / chrome bleeding into the download → `visibility:'hidden'` + finally-restore.
2. Slide position lost after capture → save/restore transform+transition in try/finally.
3. Fonts/images not ready → `waitForSlideAssets` + double `requestAnimationFrame`.

**Verify by exporting, not by reading markup.** Review HTML is not the deliverable; the output is. Drive the file's own capture function via headless Playwright (see `.ai-workflow/tools/README.md`) and look at the result.
