# TutorDA daily reel run (for scheduled sessions)

Each run builds TOMORROW's two reels from `plan/week_*.json`, publishes the MP4s in this repo, and schedules both in
Metricool for 10:00 and 18:00 IST. Aro reviews the night before and can delete a post in Metricool to cancel it.

## House rules (from Aro, non-negotiable)
- Every number and answer is computed in Python before scripting. No statistics without a source. No tutorda.org images.
- Voice: Runway `generate_speech`, model eleven_v3, voice Niki, stability 0.5. Say TutorDA as "Tutor-dah".
- Emergency voice (approved by Aro, only when Runway credits run out or speech generation fails): Kokoro af_sarah shaped
  to Niki with word stress: mark 2–3 key words per line with *asterisks*, then
  `F0=196 RANGE=1.25 FLAT=0.6 EMPH_ST=2.5 EMPH_DB=3 python3 tools/kokoro_niki2.py af_sarah topics/<t>/vo_full.wav "line 1" …`
  (then convert to mp3 and continue with cuts/split/align as usual). Say in the run summary that the Sarah voice was used.
  Pronunciation dictionary (28 Oct) in kokoro_niki2.py: write JEE, NEET, IELTS, PTE, CSIR-NET, PDF, TutorDA and tutorda.org
  as plain words in the line; they are spoken from fixed phonetics (J-E-E, C-S-I-R, "Tutor-dah"). Add new acronyms to LEX
  (or pass LEX_JSON='{"word": "IPA"}'). Check with tools/check_voice.py: TutorDA should come back as "Tutarda" (as Niki's does).
- Short format (from the sin x insights, 20 Oct; use `ShortReel` in engine/manim_math.py, see Cubic and Area): 17–22 s.
  Frame 0 already moving (graph drawing) with the question + A–D options on screen; spoken hook ≤ 2 s; options are NOT read.
  No spoken "comment" line: an on-screen "Comment A, B, C or D" chip appears at ~1.5 s. Header tag "JEE in 20s" (or "CSIR-NET in 20s"), NO numbers (Aro, 20 Oct).
  Answer lands in the last line, then the CTA "Follow TutorDA and comment TRICKS to get the PDF" (spoken "Follow Tutor-dah, and comment tricks to get the P D F", closing chip
  `self.CTA`; never "Follow for more", never a number), then a ~1 s brand flash (`brand_flash`), no long end card.
  Timing env: START=0.05 IN_GAP=0.12 BEAT_GAP=0.18 END_HOLD=0.9; split tempo 1.08, cap 0.16.
- Instagram via Metricool brand 7477800 (tutorda_), type REEL, showReelOnFeed true, isAiGenerated true, autoPublish true.
- Spoken words and captions must match the on-screen notation exactly (screen shows ln → say "L N", caption "ln"; never "log").
- Never post a reel that failed QA; leave the slot empty and say so in the run summary.

## Steps
1. Setup: `./setup.sh manim` (first run in a fresh container; models come from GitHub). Check `ffmpeg`, `manim`.
2. Read `plan/week_*.json`; pick the two entries for tomorrow (IST). Skip any with status "scheduled".
3. For each reel:
   1. Verify the answer in Python. Write `topics/math_<slug>/clips.json`: 7 rows `[beat, "ELEVENLABS", caption]`,
      captions use `|` for the line break; last row is the brand line "… Follow TutorDA for more."
   2. Voice: one `generate_speech` call with the 7 spoken lines separated by blank lines (spoken forms: "mod x",
      "two to the power hundred", "Tutor-dah"). Poll `get_task` for the URL.
      Download: `curl -o topics/math_<slug>/vo_full.mp3 "<url>"`. If the proxy refuses dnznrvs05pmza.cloudfront.net,
      fetch it through the Claude browser pane instead (any https tab: fetch → base64 → 'B64START…B64END';
      the oversized tool result is saved to a file; decode with `python3 tools/b64file.py <file> <out.mp3>`).
      Then `ffmpeg -i vo_full.mp3 -ac 1 -ar 24000 vo_full.wav`.
   3. Cuts: `python3 tools/cuts_asr.py topics/math_<slug> "first two words of line 2;…;line 7"` →
      `python3 tools/split_vo.py topics/math_<slug> "<cuts>" 1.06 0.2` →
      `START=0.2 IN_GAP=0.18 BEAT_GAP=0.25 END_HOLD=1.4 python3 tools/align_words.py topics/math_<slug>`.
   4. Scene: add a `MathReel` subclass to `engine/manim_math.py` (copy the closest existing one), fire animations on
      `wt(clip, word_index, lead)`. Audio module: copy `engine/aud_pow.py` to `engine/aud_<slug>.py`, change TOPIC,
      events name and music (alternate assets/jee/score.mp3 and assets/svc/score.mp3, vary MUSIC_OFFSET).
   5. Draft: `FILM_AUDIO=aud_<slug> tools/manim_build.sh engine/manim_math.py <Scene> aud_<slug> out/<slug>_draft.mp4 draft`
      (run builds one at a time). Contact sheet: `ffmpeg -i out/<slug>_draft.mp4 -vf "fps=1/1.9,scale=270:480,tile=8x2" -frames:v 1 chk/<slug>.png`
      and LOOK at it: no overlaps, nothing in the top 120 px or bottom caption band, labels readable.
   6. Final: same build without `draft` → `media/<file>.mp4`. QA: duration 25–31 s, loudness about −14 LUFS
      (`ffmpeg -i f.mp4 -af ebur128 -f null -`).
4. Publish media: commit `media/<file>.mp4` + the new topic/engine files, push to `main`.
   Public URL: `https://raw.githubusercontent.com/AravindSundharesan/tutorda-reels/main/media/<file>.mp4` (repo created 20 Oct, Claude app installed; Metricool re-hosts the file at scheduling) (check it returns 200 + video/mp4 size).
5. Schedule with Metricool `createScheduledPost` (brand 7477800, timezone Asia/Calcutta): caption (template below),
   firstCommentText, media [raw URL], instagramData {type REEL, showReelOnFeed true, isAiGenerated true, autoPublish true}.
   Confirm with `getScheduledPosts`. Then set the entry's status to "scheduled" in the plan JSON, commit, push.
6. Update the plan doc (Claude Docs "TutorDA reels: 1-week plan (21–27 Oct)", id a78420d5-4035-4624-b71d-33bfd1189386):
   set that reel's Status dropdown to Scheduled (read the doc first; change only that cell).
7. Finish with a short summary: the two reels, their post times, the raw video links, anything that failed.

## Caption template
Hook question + "Comment your answer BEFORE the reveal 👇" · blank line · the common wrong instinct + "The 20-second method:"
· 1️⃣ 2️⃣ 3️⃣ steps · "✅ Answer: …" · one line on where it applies in JEE Main / CSIR-NET · blank line ·
"📌 Save this for revision · Share it with your JEE study partner" / "👉 Follow @tutorda_ for …" /
"👉 Follow @tutorda_ and comment TRICKS to get the PDF: 12 JEE maths tricks on one page" · "🎯 Your first JEE Main mock is free: tutorda.org"
· blank line · EXACTLY 5 hashtags (Instagram's cap since Dec 2025): #JEEMain #JEEMaths + 2 topic tags + #TutorDA
(CSIR-NET reels: #CSIRNET #CSIRNETMaths + 2 topic tags + #TutorDA).
Free sheet (keyword TRICKS): https://cdn.jsdelivr.net/gh/AravindSundharesan/tutorda-reels@main/freebies/TutorDA_12_JEE_Maths_Tricks.pdf (jsDelivr serves it as a real PDF; raw.githubusercontent sends octet-stream, which stalls in the Instagram browser)
First comment: a two-way vote ("Team stay or team switch? 👇").

## Template v2 and audit rules (28 Oct, from the 17–26 Oct Instagram audit; these override older lines above)
- Build every new reel on `ShortReel2` (see `Nines2`): header at y 262, all text inside y 330–1440 and x 96–870
  (Instagram's top bar, bottom caption overlay and right action rail cover the rest). Captions stay in the ink FOOTER
  band (Aro, 28 Oct): band from y 1460, caption text at y 1545 (upper part of the band); chips at y 1250. The hook question sits inside the profile-grid crop (y 240–1680).
- Length 22–25 s (watch time drove reach; the 16–20 s cuts lost it). Seven lines: hook → the common wrong answer
  ("Most people say …") → method → payoff → a second angle or check ("Still not sure? …") → answer → keyword CTA (Follow TutorDA + comment TRICKS).
  Something must move in every beat; no static frame longer than 2 s.
- Early chip: "Pause and guess" (A–D comment prompts got no comments). The only comment ask is the end keyword:
  "Follow TutorDA and comment TRICKS to get the PDF" (Aro, 28 Oct).
- Series label "Daily maths trick" (bio promises "One JEE maths trick a day").
- Mix: JEE first. CSIR-NET at most once a week. Favour "which is bigger / which total / should you switch" puzzles: they get shared.
- Never post promos as reels (213 views, 30% followers). Promos go to stories or a pinned post.
- Post a story with each reel (reel + Yes/No poll) and answer real comments within the first hour (draft with /ig-reply).
- Track weekly: follows per 1,000 viewers (27 Oct baseline 0.3; target 2+), from each reel's Instagram insights.
