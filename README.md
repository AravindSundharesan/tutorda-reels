# TutorDA Reel Kit

Code-made vertical maths reels for TutorDA (www.tutorda.org): 1080x1920, 30 fps, AI voice, word-timed captions,
motion graphics, -14 LUFS audio. Everything runs locally (Python + ffmpeg). No paid APIs.

**Read `LESSONS.md` first.** It holds every correction the user has made, as rules, plus the priority order for conflicting advice. Add a line whenever the user corrects something.

## Setup (once)
```
./setup.sh          # installs Python packages, downloads voice/speech models (~500 MB on disk) into models/
```
Needs Python 3.10+, ffmpeg and internet access to pypi.org and github.com.

## Render the finished reels
```
./make.sh pizza build       # Integral calculus: area of a circle with pizza rings (clean white, voice v2, current standard)
./make.sh bday build        # Birthday Paradox v2 (white theme)
./make.sh xx-white build    # d/dx(x^x) + the 37% rule, white theme
./make.sh xx-dark build     # same, dark theme
```
Each build writes `out/<reel>.mp4` (upload size, <= 30 MB) and prints a QA report.

## Manim edition (current standard look)
`./setup.sh manim` once (Manim 0.19 + LaTeX + dvisvgm + Pango), then:
- `./make.sh pizza-m draft`  ~45 s, 540x960 @ 15 fps, prints any animation cue that runs late
- `./make.sh pizza-m build`  ~95 s, 1080x1920 @ 30 fps + audio + frame-based safe-area check + QA
`engine/manim_pizza.py` is the template: real LaTeX maths, vector shapes, Braces, Write/Indicate/Flash, the honest ring-unroll,
word-timed captions (Manim maps characters to glyphs, so highlights land on whole words). Audio, cue times and word times
come from `engine/reel6.py`, so both editions share one voice track. `tools/safe_frames.py` checks any rendered video.

## Illustrations (AI image generation)
Through the custom Hugging Face connector in Claude (see LESSONS.md): Qwen-Image or FLUX.1-schnell (Apache-2.0) on a white
background, cut out to `assets/img/*.png`, used in Manim with `ImageMobject`. Credits in `assets/sfx/CREDITS.txt`.

## Fast iteration (use this loop)
| Step | Command | Time (2 cores) | Use it for |
|---|---|---|---|
| Stills | `./make.sh pizza preview 3 10 15` | ~2 s | layout, text, overlaps |
| Draft video | `./make.sh pizza draft` | ~25 s | timing, motion, voice sync (540x960, 15 fps) |
| One scene | `./make.sh pizza build 12 19` | ~17 s | final-quality check of a fixed stretch |
| Safe-area stills | `./make.sh pizza safe 3 10 27` | ~3 s | Instagram overlay zones shaded red |
| Final + QA | `./make.sh pizza build` | ~70 s | the file you post (runs the safe-area check first) |
Times drop roughly with core count (all cores used by default; `WORKERS=4 ./make.sh ...` to limit).
Older reels (bday-v1, xx-white, xx-dark) still use the slower master + two-pass path.

## Make a new topic (the workflow)
1. **Script**: copy `topics/birthday_paradox/clips.json` to `topics/<new>/clips.json`. One row per sentence:
   `["beat", "spoken text", "caption text"]`. Same beat letter = same scene. Write maths as it is spoken
   ("d y by d x", "three sixty-five by three sixty-five"). Keep the last row as the TutorDA brand line (phonemes).
   Compute every number in Python first; never state unsourced statistics.
2. **Voice**: `python3 tools/make_voice2.py topics/<new> --speed 1.15` (default: clean energetic Indian male, hm_omega + 25% am_puck).
   Old energetic chain: `python3 tools/make_voice.py topics/<new> hm_omega 1.22`.
   Other voices: `af_heart` (US female), `am_michael` (US male); add `1.0 0` at the end for a plain delivery.
   Re-do single lines slower: `--only 3,5` with speed 1.17.
3. **Check the voice**: `python3 tools/check_voice.py topics/<new>`; reword lines that are misheard.
   (The checker mishears Indian "tutor"/"maths"; judge those by ear.)
4. **Word timing**: `python3 tools/align_words.py topics/<new>` -> `word_times.json` (karaoke + animation cues).
5. **Scenes**: copy `engine/reel5.py` + `engine/reel5b.py` to new files, change the TOPIC path and the scene `build()`
   (layout helpers, counters, rough circles, networks, bars, glow pulses, answer box, end card are all reusable).
   Fire key animations from word times (see `wt()` in reel5b.py). Add the new reel to `make.sh`.
6. **Preview, build, QA**: `./make.sh <reel> preview ...`, then `./make.sh <reel> build`.
   Read the QA report, open the contact sheet in `chk/`, and fix anything flagged before posting.

## House rules (learned with the user)
- White theme is current; dark theme available. Energetic voice. Brand name said "Tutor-da".
- No confetti. One spring/bounce moment per reel (the answer). Hook visible on frame 0. End card <= ~2 s.
- Text >= 40 px. Key content inside the platform-safe box x 85-960, y 220-1520 (Instagram's top bar, caption/username area and like/comment column); captions at y 1410.
- Music well under the voice, dipped before the big reveal; few, deliberate CC0 sound effects.

## Files
- `engine/manim_pizza.py` Manim edition of the integral reel. `tools/manim_build.sh` render + audio + encode for Manim reels.
- `engine/runner.py` fast builder: scene built once and shared by all workers, one encode straight to upload size, cached audio, draft and partial modes.
- `engine/reel2.py` core: timeline from voice clips, elements, springs/easing, audio mixer (music, SFX, ducking).
- `engine/reel3.py` x^x reel, dark PRO edit. `engine/reel4.py` x^x reel, white theme + shared effects library.
- `engine/reel6.py` Integral / pizza reel (rings unroll into a triangle; best template for new topics).
- `engine/reel5.py` Birthday Paradox scenes. `engine/reel5b.py` v2 upgrades (word timing, frame-0 hook, single spring, CC0 SFX).
- `tools/` voice, voice check, word alignment, QA, upload encode. `topics/` scripts, voice clips, word times.
- `assets/fonts` Poppins (SIL OFL, see OFL.txt). `assets/sfx` CC0 sounds (see CREDITS.txt).

## Licences
Kit code: written for TutorDA. Poppins: SIL Open Font License 1.1. Sound effects: CC0 1.0 (Kenney, OpenGameArt,
kmilo93sd/agent-video-editor), no attribution required. Kokoro model: Apache-2.0. sherpa-onnx: Apache-2.0.
Craft rules adapted from MIT/Apache-licensed open-source video skills (see the skills in your Claude account).
