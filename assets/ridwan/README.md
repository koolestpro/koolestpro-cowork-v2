# Ridwan's Brand Assets

## Required Photos
Drop your processed photos here with these exact filenames:

- `avatar-circle.jpg` — Circular crop with orange→purple gradient border (the processed versions you shared)
  Used in: LK frame header, CTA slide avatar, about-me sections
  Size: 1080×1080px recommended

- `avatar-circle-smile.jpg` — Same circular format, smiling version
  Used in: CTA slides where a warmer tone is needed

- `photo-main.jpg` — Full original photo (standing, black background)
  Used in: Before/After slides, case study slides

- `photo-thinking.jpg` — Thinking pose (hand on chin, smiling)
  Used in: Framework/educational slides

## How to Use in HTML
```html
<!-- LK Frame Avatar (replace the "R" gradient circle) -->
<div class="lk-av" style="background:none;overflow:hidden;">
  <img src="../assets/ridwan/avatar-circle.jpg" 
       style="width:100%;height:100%;object-fit:cover;border-radius:50%;">
</div>

<!-- CTA Slide Avatar (180px circle) -->
<div style="width:180px;height:180px;border-radius:50%;overflow:hidden;margin:0 auto 20px;">
  <img src="../assets/ridwan/avatar-circle.jpg"
       style="width:100%;height:100%;object-fit:cover;object-position:center top;">
</div>
```

## Note on Gradient Border
Your circular photos already have the orange→purple gradient border applied.
Simply drop them here and the HTML will reference them directly.
