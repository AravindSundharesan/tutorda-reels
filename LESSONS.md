# TutorDA lessons log

Read this before every TutorDA job. Each lesson is a real correction or failure, written as
**failure -> what to do instead**. When the user corrects or rejects anything, add a new dated line here
(and re-zip the kit). Keep entries short, concrete and checkable. Remove a lesson only if the user reverses it.

## Priority order when rules conflict
1. The user's explicit instructions (including every lesson below).
2. TutorDA's brand (colours, fonts, logo, "Tutor-da" pronunciation, white theme).
3. Hard limits: maths correct; text >= 40 px on reels (>= 12 px web, contrast 4.5:1); nothing clipped or overlapping;
   key content inside safe areas; file <= 30 MB for chat delivery; -14 LUFS.
4. What students need: one clear idea, readable on a phone, muted-first.
5. The visual idea for this topic.
6. Defaults from skills (visual-design-direction, taste-critique, math-explainer-craft, ...).
Fewer, prioritised rules beat long lists: check against the hard limits and this log *after* rendering.

## Voice and audio
- 2026-10-15 Voice sounded flat ("no boldness") -> use the energetic chain (hm_omega, speed ~1.22, pitch x1.35, +1.5 st, presence EQ + compression) and upbeat music.
- 2026-10-15 "TutorDA" mispronounced as "Too-dur D A" / "Toora" -> brand line by phonemes `tjˈuːtəɹ dˈɑː` ("Tutor-da", DA as one syllable).
- 2026-10-15 A one-word line ("Wrong!") was muddy -> use a fuller phrase ("That's wrong!") and slow single lines to ~1.17.
- 2026-10-15 Sound effect landed on the brand name and masked it -> never place SFX on the brand word or a key number.
- 2026-10-16 User found the energetic voice had drawbacks -> default is now voice v2 (`tools/make_voice2.py`): hm_omega blended 25% with am_puck, speed 1.15, no WORLD pitch resynthesis (it caused a buzzy edge and the checker lost words like "pizzas", "thick"), light EQ/compression. Old chain kept in make_voice.py. Awaiting the user's ear on v2.
- 2026-10-15 Checker hears Indian "tutor"/"maths" wrongly -> do not "fix" accent by the checker; ask the user to listen.

## Visuals
- 2026-10-15 User removed confetti / colour-paper bursts -> no confetti in any reel.
- 2026-10-15 Camera punch-in pushed the title into the header -> punch amplitude <= 0.045, focus near frame centre, check header clearance in contact sheets.
- 2026-10-15 Stacked fractions overlapped between rows -> \dfrac at 56 px with rows >= 150 px apart.
- 2026-10-15 Long title ran to the frame edge -> headlines <= ~76 px when long; keep >= 85 px side margins.
- 2026-10-15 Yellow text unreadable on white -> yellow only as fills; amber (#D97706 / #B45309) for yellow-coloured text.
- 2026-10-15 Freeze check flagged ~1 s holds -> keep something meaningful moving every 2-4 s (word highlights split per spoken part, a hand-drawn circle on the item being discussed).
- 2026-10-17 User approved a clean background -> new reels use plain white (very slightly cool), no floating symbols, purple tints, grid lines or glow blobs (reel6 overrides V.background). Older reels unchanged until asked.
- 2026-10-17 Critique: the proof (the actual maths) was small with an empty top half -> make the proof the hero: mark the variable on the object (x arrow), magnify the tiny thing the voice names (dx inset), glide the result to the optical centre, show the calculus step the syllabus expects ([pi x^2] from 0 to r), not only the geometric shortcut.
- 2026-10-17 Each number appeared 3-4 times (formula, counter, bar, sticker) -> show each number once on screen; let the caption carry the spoken copy.
- 2026-10-17 Thin Computer Modern looked faint next to Poppins Bold -> use texb() (alpha dilated) for on-screen maths.
- 2026-10-17 Caption lines ended with one orphan word -> balance two-line captions (KaraokeW in reel6).
- OPEN (older reels only): Birthday Paradox still has the purple tint, rainbow avatars and floating symbols.

- 2026-10-16 Grey rectangle behind the yellow answer box -> blurred glows need >= 90 px margin and a transparent *yellow* (not black) base layer.
- 2026-10-16 End-card rings cut through the logo and text -> glow behind the logo instead of line rings.
- 2026-10-16 A lone big integral sign read as a black spike -> show maths symbols with context (e.g. an integral with limits and dx), never bare.

- 2026-10-17 Captions (y~1670) and right-edge numbers sat under Instagram's caption/username overlay and button column -> key content inside x 85-960, y 220-1520; captions at y 1410; website line at 1560. `./make.sh <reel> build` now runs `runner.py check` first and lists anything outside; `./make.sh <reel> safe t1 t2` shades the zones on stills.
- 2026-10-17 Real-life scene showed one pizza alone for 3 s -> things being compared arrive together; numbers come in with the voice.
- 2026-10-17 Small diagram + empty frame while the voice explains it -> slow camera push-in on the diagram (keeps creeping, so no freeze), pull back before it needs the width.

- 2026-10-17 User wants "authentic, best quality, high standards" -> new reels are built in Manim (engine/manim_pizza.py as template): LaTeX maths, vector shapes, Braces, honest geometry. The PIL engine stays for older reels.
- 2026-10-17 Manim pitfalls hit: a dt-driven clock drifted vs the scene (use self.renderer.time); arranging per-word Text broke baselines (use whole-line Text + t2c variants); hidden captions still cost render time (show one live caption, swap on word change); Manim's own encode is CRF 23 (patched to 14); a bounded loop for random toppings (an unbounded one hung the render).
- 2026-10-17 Cues ran late when earlier animations overran -> `until()` prints LATE; fix by shortening or merging animations, never by shifting the voice.
- 2026-10-17 Reviewer: proof small with empty space -> bigger slicing pizza, dashed ghost of the pizza above the triangle that fills with πr² at the answer (shows triangle area = circle area).
- 2026-10-17 Python round(100.5) = 100 (banker's rounding) put "≈ 100" on screen for 32π -> animate to the exact value and round half up.

- 2026-10-17 Image generation works through a custom Hugging Face connector (address https://huggingface.co/mcp?login&gradio=mcp-tools/Qwen-Image-Fast,evalstate/flux1_schnell,not-lain/background-removal); the built-in HF connector has image tools switched off (gradio=none). Use only Apache-2.0 models for TutorDA (Qwen-Image, FLUX.1-schnell); not FLUX.1-dev/Krea-dev/Kontext-dev. Illustrations for objects and scenes; maths stays vector. Record each image in assets/sfx/CREDITS.txt (model, prompt, seed).
- 2026-10-17 Generated images on white: cut out locally (flood-fill the low-saturation background + shadow from the edges) when the hosted background remover can't fetch the temporary link; sample the illustration's colours so vector parts match.

## Content and claims
- 2026-10-16 Said "12%" when the true value was 12.5% -> say the exact value used on screen; rounding must not change a claim.
- 2026-10-15 Nearly claimed "most people guess 5%" -> never state an unsourced statistic; compute every number in Python before it goes on screen.
- 2026-10-15 Reels ran 33-39 s -> say the length on delivery; trim narration before speeding the voice past ~1.27.

## Delivery and continuity
- 2026-10-17 Word times are now stored relative to each clip (clip_start), so changing START or gaps no longer desyncs animations; START=0.15 avoids a near-silent opening.
- 2026-10-17 Critique found 88 words in 29 s (3 words/s) -> keep scripts near 80 words for 30 s; cut words rather than speed the voice.
- 2026-10-17 Builds took ~4.5 min (half of it a second two-pass encode) -> engine/runner.py: one encode to upload size (SSIM 0.991 / PSNR 47 dB vs the old master), draft and one-scene modes. Full build ~70 s on 2 cores. Iterate with stills -> draft -> one scene -> final.
- 2026-10-17 The old high-bitrate encode kept film grain, which hid near-still moments from the freeze check; the new encode drops grain, so QA now flags real still moments. Fix those with motion, don't raise the bitrate.
- 2026-10-16 User asked for speed -> skip a fresh setup when models already exist in the session; preview, build once, review, fix, build once more.
- 2026-10-16 setup.sh interrupted mid-download left a model without tokens.txt -> setup now checks for tokens.txt, not just the folder.
- 2026-10-15 102 MB master could not be sent -> two-pass encode at ~5.2-5.5 Mbps (tools/encode_upload.sh).
- 2026-10-15 Skills were proposed but not saved -> after proposing, tell the user to click Save on the card.
- 2026-10-15 Work lived only in the session -> keep everything in the TutorDA Reel Kit and send the updated zip after changes.

## Voice (2026-10-20)
- Kokoro voices (all of them) were rejected as robotic. Current voice: ElevenLabs "Niki" (eleven_v3, stability 0.5) via the Runway connector, ~1 credit per 50 characters.
- Brand pronunciation: "TutorDA" = TOO-ter-dah, one word -> write it as "Tutor-dah" in the TTS text (tested; "Tooter-dah" and "Tutor D-A" were wrong). "DA" alone (the meaning line) is spelled out: "D. A. stands for Dynamic Assessment". Website: "tutor-dah dot org". JEE: "J-E-E".
- Runway audio can't be downloaded from the workspace or the browser pane; the user saves the MP3 to Downloads and it is staged from there.
