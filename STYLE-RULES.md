# Reel feedback ledger — read FIRST before producing any reel

STRUCTURE: universal rules apply to every style; style-specific taste rules
and treatment history live in styles/<name>.md. Entries below dated per reel.
Styles available: varun-mayya (default), nick-saraev.

## 2026-08-06 — qwen-max v1 → v2 (voice default + brand recognition)

- **"I wanted to use vibe voice"** — v1 shipped with HeyGen TTS per the
  2026-07-29 canonical policy. User re-confirmed VibeVoice as their preference.
  RULE: VibeVoice (voice-sample-ref clone) is the DEFAULT voice for all reels again;
  HeyGen native TTS is the FALLBACK (Space down / quota). This supersedes the
  2026-07-29 "HeyGen TTS default" line. Avatar = audio-driven avatar_iv from
  the VibeVoice track.
- **"Throughout the reel focus on branding elements recognizable by viewers —
  Alibaba original logo, Jack Ma's photo — people know these so they instantly
  relate; showing them ANIMATED in the beginning helps a lot"** — v1 led with
  the Qwen sub-brand (mark + wordmark films), which most viewers don't know.
  RULES (universal):
  - Every reel anchors on the most HOUSEHOLD-RECOGNIZABLE brand assets: the
    parent company's official logo in its brand colors, and, when the story is
    company-scale, the famous founder/CEO's face (properly licensed photo,
    credited). Recognition beats abstraction — a sub-brand mark supports, never
    replaces, the household brand.
  - These anchors appear ANIMATED inside the first 2-3 seconds (draw-on/
    assemble/pan-zoom photo card), and brand touches recur through the reel
    (logo on charts/cards, brand color accents), not just at the hook.

## GOVERNING RULE (2026-07-23, read before EVERY reel — no exceptions)

- EVERY reel is built in exactly ONE of two styles: varun-mayya or nick-saraev,
  strictly per that style pack. Never invent a third look.
- If the user names a style, use it. If the user names NO style, DEFAULT to
  varun-mayya.
- A REFERENCE REEL the user gives supplies the TOPIC (and which of the two
  styles best fits) ONLY. NEVER copy the reference's visual style, layout,
  fonts, or effects — rebuild the topic in our varun or nick pack. The ONLY
  exception is if the user EXPLICITLY says "use these visuals / copy this look".
- VOICE is the ONLY thing that changed with VibeVoice. Visuals, scene grammar,
  sound design, captions, pacing, treatment history — all unchanged, still
  driven entirely by the two style packs and the universal rules here.

## UNIVERSAL PACING RULE (2026-07-31 — BLOCKING, applies to BOTH styles)

User (angry, repeated feedback): "the first frame with face at bottom and a
different block on top shouldn't be there for more than 2 seconds… we can't
afford static screens for more than 2 seconds. Instagram retention is low —
keep showing people something new." google-15 held its hook layout 6.4s.

- NO layout/composition persists longer than ~2s. This includes the hook
  split/BrandHook (face visible by s1, gone or replaced by s2), typecards,
  logo beats, charts, annotatezoom holds, any designed card.
- "It animates internally" is NOT an exemption for held layouts — micro
  -motion (push-ins, springs, count-ups, camera ease) does not count as a
  scene change. Only genuinely moving FOOTAGE/screen-recordings may run
  2.5-4s, and even those target a cut every 2-2.5s when the VO allows.
- Long VO sentences get SPLIT across 2-3 distinct visuals, always.
- ENFORCEMENT: tools/lint_frames.py flags scene 0 if >2.2s and any
  non-footage scene >2.6s ([PACING] flags). A build with PACING flags on the
  hook does not ship.

## UNIVERSAL DENSITY + INTENSITY RULES (2026-07-31 — BLOCKING, both styles)

User: "why are you limiting yourself to limited footage? content is limitless
on the internet… when I say 'brand's whole social campaign' you show one
boring screen — nothing matching the intensity of the words." Plus a
meaningless filler frame (dark mid-scroll page section) shipped unverified.

- ASSET DENSITY: every tool/claim gets MULTIPLE visuals — the scout gathers
  3-5 usable shots per subject (official videos are long: mine several
  segments, punch-in crops of 4K sources count as extra shots; credited
  creator demos allowed). One-clip-per-tool beats are BANNED. Long beats
  (>2.5s) become 2-3 rapid sub-shots.
- INTENSITY MATCHING: the visual must match the SCALE of the words. Plural/
  totalizing words ("whole campaign", "everything", "15 tools", "unlimited")
  demand plural visuals: walls/grids of creatives, rapid montages, stacked
  results — never a single static screen. Say-big show-big.
- ONE CLIP PER BEAT: a source clip may carry only ONE footage beat in a reel.
  Reusing the same shot at a different `from` offset still reads as "same
  footage again and again" (india-claude v1: 6 clips across 11 beats). Cut a
  DISTINCT shot for every slot — a 3-5 min aerial/demo source holds 15-20
  separable locations; mine them. ENFORCED: lint_frames.py [CLIP REUSE] flag,
  blocking.
- EVERY scene's source range is frame-verified AT ITS EXACT in/out points
  before it enters the beat sheet. "It's from the right page" is not
  verification — the pomelli-scroll filler fail. No unverified filler, ever.

Every entry: date, reel, the raw feedback, root cause, distilled rule.
Rules here override SKILL.md. Never repeat a mistake recorded here.

## 2026-07-29 — grok-voice v1 → v2 (hook composition)

- **"Black text overlapping the dark background in the first 3 seconds; the
  first-3s visuals aren't pleasing"** — hook split put dark serif headline
  over the number-provisioning clip's dark/orange gradient regions.
  RULE (hardens the existing legibility rule): the HOOK headline never sits
  on footage at all — hook display type goes on a CLEAN light/cream field.
  Legibility check at the landing frame is BLOCKING for the hook beat.
- **"The subject brand (xAI) must be LARGE — it's the center of attraction."**
  User supplied Nick's hook frame as the target composition: giant brand/
  product name on cream, the tool's real screen in a floating window under
  it, one italic serif line, face in a rounded bottom card.
  ENGINE: new `brandhook` scene (BrandHook.tsx, theme-aware) = title (huge
  serif brand name) + subtitle caps + framed media window (video) + italic
  serif line + rounded facecam card. USE THIS as the default varun/nick hook
  for product-launch reels; chips auto-hidden (hideCaptions default in beat).
- Liked: SFX selection and overall visuals — keep the current sound recipe.
- Process: avatar + VO reuse across visual revisions (no regeneration needed
  when only scene composition changes).
- **v5 → v6: "captions are boring and not large enough — I want Nick's
  caption style"** — measured teardown of Nick's caption system across the 12
  reference reels (2026-07-30): BIG free-floating text (~66-86px at 1080w),
  NO pill by default, deep soft drop shadow carries legibility; TWO VOICES
  mixed inside one phrase — connective words italic, the KEY word lands
  HEAVIER + BIGGER; words accumulate as spoken (per-word reveal, not
  chip-swap); keyword gets an accent color; pill only as fallback over busy
  footage. ENGINE (permanent): captionStyle "nick-display" in CaptionChips —
  per-word reveal times in beats captions[].words, emphasis list drives the
  heavy+accent keyword, per-scene `captionTheme: dark` flips white→ink over
  cream fields (accent shifts to amber #E8A200 on light bg so it never
  blends), phrases hold through VO pauses (+0.9s cap). SF Pro Italic plays
  the italic voice per the SF-Pro-only rule. DEFAULT for all reels;
  chip modes remain as legacy fallback.
- **v3 → v4: "use SF Pro only, all type"** — the brand font is SF Pro
  (Display), every variation (weight/italic) at the director's discretion.
  ENGINE (permanent): theme `serif` tokens for BOTH styles now point to the
  SF Pro stack; HeadlineBuild/KineticType hardcoded Fraunces removed; display
  weights bumped (800 headlines) since SF Pro reads lighter than a serif.
  RULE: no Fraunces/Georgia/serif families in any reel — SF Pro
  everywhere (chips were already SF Pro).
- **v3 → v4: "too much empty white space around the framed screens — Nick
  fills it with large text"** (user pointed at 3-22s framed cards + 25s
  receipts; praised the chart's title block at 34s as the model).
  RULE: every framed-card scene (floatcard / deviceframe / annotatezoom)
  carries a BIG display headline in the empty field above the card (label +
  headline kinds, y≈0.10, theme dark on cream) — 2-5 punchy words stating the
  beat's claim, NOT verbatim VO (≤1 shared significant word keeps the karaoke
  chips alive; duplicating numbers like "80+ voices · 25 languages" is the
  exception where chips auto-hide). White space is a canvas, never blank.
- **v2 → v3: "text is getting cut in the browser windows (multiple screens)"**
  — DeviceFrame's browser media area was hardcoded 940x1050 (portrait);
  16:9 clips under objectFit:cover lost ~half their width ("ue_refund",
  "Thank y"). ENGINE FIX (permanent): media area now follows the source
  aspect — VIDEO sources default to a 16:9 window (full frame, zero crop),
  page screenshots keep the tall reading pane; `mediaAspect` prop overrides.
  RULE: a framed clip must show its FULL source frame — if a device window
  and its media have different aspects, the WINDOW adapts, never the media.

## 2026-07-22 — indiaai-gpu v1 → v2

- **"My face is not in the center"** — root cause: HeyGen 9:16 auto-crop.
  HISTORICAL RULE (superseded by the 2026-07-29 connector policy below):
  generate avatar 16:9 + crop ourselves with measured face-x.
- **"Varun's first 2 seconds include the face"** — RULE: hook is always a
  split screen (footage top / facecam bottom) or full facecam. Face visible
  by second 2, always.
- **"Captions bigger + styled"** — RULE: 56px+, extra-bold, solid black pill.
- **"Key pointers highlighted"** — RULE: numbers/prices/brands in yellow
  #FFD84D at 1.22em inside chips (emphasis list in beat sheet).
- **"Static screens feel dead"** — RULE: every scene moves (punch-in on cut,
  receipts open zoomed near the highlight and settle, alternating zoomDir).
- **Liked**: minister/launch-event footage, official b-roll. Keep sourcing
  real event footage for government/company stories.

## 2026-07-22 — indiaai-gpu v2 → v3 (Varun-style audio rebuild)

- **"The audio is shit, sound effects are pathetic"** — root cause: whoosh on
  every cut at ~5 LU under voice, no music bed. Demucs analysis of Varun's
  reels: bed always present ~15 LU under voice with energy curve (hook full →
  duck mid → rise at reveal/CTA); SFX sparse (riser into hook, 2-4 impacts at
  act breaks, pops on highlights) and deep/cinematic, not zippy.
  VARUN-PACK RULES (Nick levels are defined in `styles/nick-saraev.md`):
  - Music bed in every reel, volume-automated (0.07-0.16), never flat.
  - Max 6-9 SFX cues per reel; silent ordinary cuts.
  - SFX vols 0.11-0.18; hook-vs-voice energy delta ≤ +4 dB.
  - Master the final file to -14 LUFS (loudnorm), verify with ebur128.
- **"Captions cover the face in the beginning"** — RULE: split-hook scenes set
  captionBottom≈1000 (seam); any facecam scene must keep chips off the face.

## 2026-07-22 — kimi-india (noted, no re-render requested)

- **"The screen you're showing doesn't match what I'm talking about"** — hook
  top showed a macOS Finder recreation while VO said "a frontier AI model goes
  up for free download". Topically adjacent ≠ visually matching.
  RULE: the hook visual must LITERALLY depict the hook line — the product's
  recognizable UI/logo, the announcement itself, or the named subject. A
  generic demo clip fails even if it came from the right ecosystem. Test:
  would a viewer with the sound off name the subject from the hook frame?
- **"FREE FRONTIER AI is white and overlapping with the white background"** —
  white caps type sat over a white Finder window.
  RULE: display type must be legibility-checked against its actual backdrop
  in the verification pass (extract the frame AT the type's landing moment).
  Engine now draws a dark radial scrim behind KineticType over footage, but
  still prefer footage moments with dark/quiet regions at the type position.
- **"You used the same black-screen-with-text frame in both reels — find new
  ways to present information in every reel"** — the plain black serif
  typecard appeared in indiaai-gpu (₹67 vs ₹330, ₹/$) AND kimi-india
  (Hindi·Tamil·Kannada, ₹/$).
  RULES:
  - Never reuse a scene treatment the previous reel used for the same kind of
    information, unless the user has explicitly blessed it as a template.
  - Plain black typecard = fallback of last resort, max once per reel.
  - Prefer varied treatments per reel: type over footage (scrim handles
    legibility), brand-matched cards in the subject's design language (Varun
    does Kimi-dark / Apple-white / Nothing dot-matrix), stat/comparison
    layouts, type inside receipts, split text+footage.
  - Log each reel's treatments in the "Treatment history" list below and
    check it before building the next beat sheet.

## 2026-07-28 — emergent v1 → v2 (retention pacing teardown)

- **"Face should be there in the beginning for only 2 seconds, then change the
  screen, and keep changing screens every 2-3 seconds — Instagram retention is
  very low."** — v1 held the split hook (face on screen) for 7.2s and had a
  6.0s facecam take + 4.4s single floatcard mid-reel.
  RULES (varun style, all future reels):
  - Hook split (face visible) lasts ~2s MAX; the rest of the hook line gets its
    own visuals.
  - NO scene longer than ~3s unless it animates internally (specsheet rows,
    receipt highlight sweeps); target average visual change every 2-2.5s.
  - Long VO beats (personal takes, CTAs) get SPLIT across 2-3 distinct visuals
    even when the voice is one continuous thought.
  - Facecam returns mid-reel in 1.5-3s pops, never one long block.
- **"I never asked you to use the kleo reel or anything from it."** — I cloned
  kleo's build script + treatment flow and cited it in the delivery summary.
  RULE: engine components are shared, but each reel's treatment choices must be
  derived fresh from ITS manifest — never presented or reasoned as "like the
  previous reel". Never name other reels in user-facing summaries.

## Treatment history (check before every new reel)

- indiaai-gpu: split hook, cream receipts w/ highlights, BLACK TYPECARD x2,
  full-bleed footage w/ caps + serif overlays, facecam.
- kimi-india: split hook, cream receipts w/ highlights, BLACK TYPECARD x2,
  full-bleed footage w/ serif overlay, facecam.
- ibm-rehiring: split hook (IBM building top / face bottom), full-bleed
  footage w/ caps overlay, CREAM typecards x2 (new — replaced black), facecam
  bridges, cream receipts w/ highlights (Toms + Forbes). No black typecard. ✓
- model-wave: split serif hook (Kimi 3D-world / face), dark editorial receipt
  (digitalapplied) w/ headline + composed clean stat-row crops, Kimi dark brand
  spec-card AS footage, spec overlays over build footage, NEW TimelineCascade
  (dated brand cards on a rail — Qwen 72h triple), statcard price bars (TTS ⅓,
  $9→$7.50), cream Anthropic receipt w/ half-price highlight, dark SpecSheet
  (clay accent, SOTA badge) over ink-blot brand motion, facecam pops, serif CTA
  over Anthropic grid film. No black typecard. VibeVoice (2 surgical VO cuts —
  see rule below).
- → next reel must introduce at least one new treatment and avoid the plain
  black typecard entirely.


## 2026-07-23 — ibm-rehiring (varun style, natural-audio test)

- UNIVERSAL: whisper splits hyphenated words into a token + a "-suffix" token
  ("re-staff"->"re","-staff"; "entry-level"->"entry","-level"). Caption
  builders MUST merge any token starting with "-" into the previous token
  before chunking, else a chip reads a bare fragment ("re"). Merge loop now in
  build_ibm.py — copy it into every new build script.
- UNIVERSAL: render reels with `--concurrency=2 --timeout=120000`. Default 4x
  hits "delayRender timed out" when a reel reuses the avatar master at many
  offsets + b-roll + 2 audio tracks (single frames render fine → parallel
  load, not content). Also keep public/ lean (move raw .mkv/.webm to
  _sources/, delete diagnostic PNGs) — Remotion copies all of public/.
- **"whenever you highlight text, zoom in on that part too — at 0:24 there's
  a lot of words on screen"** — receipts showed the whole page so highlighted
  phrases got lost. ReceiptScene now does a STEADY per-scene focus: frames the
  union of that scene's highlights big + centered (fit ~88% width / ~55%
  height, Z clamp 1.35-2.2) and HOLDS it the whole scene with a gentle
  push-in (earlier per-highlight keyframes wrongly RELEASED the zoom mid-scene
  — don't do that). Highlight boxes still sweep on at their cue. UNIVERSAL,
  applies to both styles. (Speed later set to 1.2 — see pace-preference entry
  below; this reel's 1.05 is superseded.)
- Audio naturalness: speed 1.05 (was 1.15-1.2) reads far more human; the
  speed-up was the main "sounds AI" tell. Well-known acronyms (IBM/HR/AI) read
  fluid in TTS; only niche ones (PUBG) need phonetic spelling. create_speech
  audio-only endpoint needs a separate 'api' credit pool the Creator plan
  lacks — cheapest pronunciation test is a short 720p avatar clip.

## 2026-07-23 — pace preference (applies to all upcoming reels)

- **"use the same pace we used for the pubg reel for upcoming videos"** — PUBG
  ran at HeyGen speed 1.2. RULE: default all new reels (both styles) to
  speed 1.2, overriding the earlier 1.05 natural-audio experiment. User
  prefers the punchier pace over maximum naturalness.

## POD reel — "the result is shit" (major structural teardown)

- **NEVER open on a document / browser / file bin / black / loading screen.**
  Open on the STRONGEST shot of the finished result (the AI ad hero frame),
  full-bleed 9:16, push-in + impact. v1 opened on the business-plan doc — hard
  fail. RULE: cold-open on the payoff, then rewind to the process.
- **Rebuild tiny source UI as big motion graphics.** Do not expect the viewer to
  read a screen recording. AI category lists → 2x2 CategoryGrid cards with a
  select animation (fade others 20%, centre, scale 125%, cyan outline, ✓).
  Design gallery → numbered (01-05) Carousel that swipes and lands on the winner
  with SELECTED ✓. Prompts → clean full-screen PromptCard with the spoken
  keywords highlighted in cyan pills, + shimmer loader cards.
- **Let the result breathe.** The 7s payoff ad plays clean — no captions, no MG,
  no "better direction" graphic over the product; music raised. Save the
  design-vs-ad comparison + BETTER DIRECTION → BETTER OUTPUT + "WOULD YOU RUN
  THIS AD?" for AFTER the clean watch.
- **Source-F extraction:** the AI ad lived inside the screen recording. The
  clean copy (no player chrome, no facecam PiP) is only in the "reveal" window —
  crop=606:1080:985:0 from ad.webm t≈16.4-24 (=exact 9:16). The player-playback
  copy has controls + PiP baked in; don't use it.
- New reusable components: PromptCard, CategoryGrid, Carousel, Checklist,
  CompareSplit (src/components/). Beat builder: tools/build_pod2.py.
- **Audio caveat:** VibeVoice ZeroGPU reserves a fixed 90s block per call, so a
  short line can't be generated when <90s quota remains (resets ~daily). Reused
  existing vo-A/vo-B; the exact "40 seconds earlier / didn't exist" hook line is
  a pending 2-min swap once quota resets.

## POD reel v3 — "too slow, tighten to 36-38s" (pace revision)

- **Reel length = audio length.** Faster visual cuts alone don't shorten a reel;
  the VO track sets the floor. To speed up WITHOUT re-recording: tools/tighten_vo.py
  rebuilds the VO from word timings — caps every inter-word pause at 0.11s and
  applies a pitch-preserved atempo. Emits matching word-time JSON so captions stay
  synced (no whisper neede/available). 1.20x + pause-cap took 47s -> 39s naturally.
- **Decouple visual pacing from VO anchoring for J-cuts.** v3 uses FIXED per-scene
  durations (not VO-end anchors) so the design reveal can run 5s while the next VO
  sentence starts underneath. Captions track the VO independently.
- New components: DesignReveal (full-screen sequential, numbered, winner held +
  SELECTED ✓), HCompare (horizontal top-design/bottom-ad, cyan matching boxes +
  connecting line, sequential banners), EndQuestion (ad freeze + YES/NO, avatar
  region reserved). Builder: tools/build_pod3.py.
- **Give the payoff room:** most static screens <=1.5s, but reallocate ~5s to the
  design reveal (the winner gets ~2x hold) and keep the 7s ad clean.
- **Continuity note:** the clean full-frame section-F ad wears "JUGAAD EXPERT"
  while the selected design is "JUGAAD ZINDABAD" (the ZINDABAD ad only exists with
  player chrome). User locked both assets, so the compare boxes are thematic, not
  pixel-identical.
- STILL PENDING (same two unlocks): new opening line "This product advertisement
  didn't exist 40 seconds ago" + HeyGen avatar hook/ending. Layouts are built for
  a clean drop-in.

## 2026-07-27 — nightborne v1 → v2 (film-over-black cards)

- **"Instead of black background, play movie scenes behind the text"** — applies
  to SpecSheet, title cards, credits/names screens. RULES:
  - SpecSheet now takes bgSrc/bgFrom: film footage behind a top-dark gradient
    scrim (0.34→0.82). Never ship a solid-black spec screen when footage exists.
  - Real credit text (titles, cast walls, production cards) gets COMPOSITED over
    footage: crop the white-on-black text region from the source, lumakey the
    black away, overlay on a darkened (eq brightness -0.10..-0.22) 9:16 crop of a
    DARK scene. Never retype real people's names — reuse the film's own pixels.
  - ffmpeg gotcha: `blend=screen` on 10-bit VP9 gives magenta chroma; use
    format=yuv420p + lumakey + overlay instead.
  - zsh gotcha: $VAR expansion inside -filter_complex silently emptied → "No
    such filter: ''" AND the old output file survives (looks like the change
    "didn't take"). Inline the full filtergraph in single quotes.
  - Pick TEXT BEDS by darkness: explosions/night scenes carry white credits;
    white lab coats kill them. Keep the bed scene distinct from other beats
    (don't reuse the finale shot). Watch caption-chip vs composited-text
    collisions — set captionBottom to clear the wordmark.

## 2026-07-29 — model-wave (VibeVoice date flub, process rule)

- VibeVoice mispronounced a spoken DATE ("July 17th" → "July 7th" + a garbled
  artifact phrase) — caught only because whisper was cross-checked at 3 model
  sizes on the suspect slice. RULES:
  - After generating VO, whisper-check every NUMBER and DATE in the transcript
    against the script before rendering the avatar-driven master; re-verify
    suspicious slices with whisper small/medium.
  - Fix strategy when the face is OFF-SCREEN at the flub: surgically cut the
    span from BOTH streams of the avatar master (identical trim windows), then
    re-whisper the trimmed master for caption timings. Prefer cutting a
    dispensable spoken phrase over regenerating (dates can live on-screen).
  - Caption FIX maps operate on CHIP text (post-chunking) — multi-word fixes
    must be written per-chip; verify the fix landed in the beats JSON, not
    just the FIX dict.

## 2026-07-29 — kimi-k3 full review ("visuals too basic" — composition teardown)

User compared the kimi-k3 render against Nick Saraev's 12 reference reels
frame-by-frame. The gap was NOT assets — it was compositing rules. Five root
causes, each now a UNIVERSAL rule + engine fix:

- **ONE TEXT SYSTEM AT A TIME.** kimi-k3 showed "a first-person shooter that
  actually plays" in big serif AND "shooter that actually" in the karaoke chip
  simultaneously — same words twice. ENGINE FIX (permanent): Reel.tsx now
  auto-hides CaptionChips during typecard/wordcascade scenes and any scene with
  a kinetic overlay (`hideCaptions` per-scene override exists; explicit `false`
  forces chips back on). RULE: display type and karaoke chips never co-exist;
  headline overlays may run with chips ONLY when their words differ from the
  concurrent VO.
- **Display type never sits on busy content.** Big serif was stamped over game
  footage and over a white card ("run it yourself" white-on-white, eyebrow line
  overlapping the logo card). The references CUT to a dedicated designed card
  (cream/black, one phrase, push-in) instead. RULE: every beat is exactly one
  of (a) face + chips, (b) full-bleed footage + chips only, (c) designed card
  with no chips. Type-over-footage only via KineticType's scrim on a QUIET
  region, verified at the landing frame.
- **Highlights must never obscure data.** The Arena receipt's highlight used a
  white difference-blend box that inverted the Kimi row into a black bar —
  hiding the exact data being highlighted. ENGINE FIX (permanent):
  ReceiptScene dark backdrops now draw a stroked accent box + faint tint
  around the region (cream keeps yellow multiply marker). RULE: highlight goes
  AROUND data (stroke/underline), never over it.
- **Screenshots are never full-bleed raw.** The Arena chart ran full-bleed,
  low-res, cropped mid-letter ("ontend Code Arena"), with a blurred smear
  filling the top half. RULE: capture receipts at deviceScaleFactor 2-3,
  always card-framed (rounded + shadow on styled fill), zoom via transform to
  the region of interest so edges never cut words. Frame edges must not crop
  text mid-word — check in critic pass (lint tool flags it).
- **No per-scene palette drift.** Green game world → navy chart → black cards
  read as unrelated slides. RULE: every scene pulls bg/accent/type from the
  active style pack's tokens only (varun: cream/black + yellow #FFD84D accent,
  Fraunces serif; nick: cream/black + orange, per pack). Screenshot card
  backdrops included.
- **NEW TOOL (mandatory in STEP 6): `tools/lint_frames.py <slug>`** — extracts
  labeled per-scene stills + contact sheets into out/<slug>-lint/ and
  auto-flags dead space >30%, near-duplicate consecutive scenes, edge-cropped
  text, and double-text risks. Run it BEFORE the vision critic pass; review
  its sheets against the checklist it prints.

## 2026-07-28 — kleo/kimi v2 (dark space + walls of text)

- **"Too much dark space, we can't keep it dark"** — ReceiptScene floated a
  small card on flat black. FIX (component-level, permanent): ReceiptScene now
  renders a blurred, enlarged copy of the receipt itself as a full-frame fill
  behind the card (cream: bright blur; black: darkened blur). No scene should
  ever show flat empty backdrop around a small asset.
- **"Wall of text, getting cut, unprofessional"** — blowing up document/app UI
  to full-bleed 9:16 turns it into cropped text walls. RULE: screen-recordings
  of documents/apps are shown as FRAMED 16:9 floatcards (bg gradient) with the
  serif headline above — never full-bleed unless the content is visual (games,
  film, product motion). Crop the window region (excluding any presenter PiP)
  at its native aspect.
- Receipt crops must contain ONLY the artifact: re-check edges for leftover
  app chrome (kimi arena had residual X-sidebar pixels at x<560).

## 2026-07-29 — canonical automated presenter policy

- The connected HeyGen video connector requires an explicit `9:16` aspect for
  portrait reels. This supersedes the older unconditional 16:9 instruction
  above for calls made through that connector. Always inspect a calibration
  frame; if the automatic framing is poor, show the portrait master with
  `contain`/fit or in a split/card treatment instead of cropping out the face.
- Native HeyGen TTS with the configured creator voice is the default because it
  produces the most reliable lip sync. VibeVoice is opt-in only.
- The canonical file is `public/assets/<slug>/avatar-master.mp4`.
- For Nick-style reels, the universal 6–9 SFX cap wins: place tiny clicks/pops
  only on meaningful landings and leave ordinary cuts silent.
- Production order is scout/manifest first, then script and shot plan, then
  presenter generation. Do not generate paid media before the story has
  verified visual coverage.

## 2026-08-04 — astra v1 → v2 (diagram crop, washed statcard, hook dead space)

- **"From :10 to :13 I can see arrows but not the whole diagram — it's
  getting cut"** — the 16:9 manim fanout ran full-bleed in the 9:16 frame,
  cover-crop ate the diagram's sides. RULE (universal): a 16:9 mechanism/
  diagram render NEVER runs full-bleed in a portrait reel — frame it
  (floatcard/deviceframe, full source frame visible) with a display headline
  filling the field above, or regenerate the diagram at 9:16. Wide diagrams
  are composition-critical; footage-style cover-crop only suits photographic
  b-roll where the subject survives a center crop.
- **"Screen at 0:34 — I get the price but the background is pathetic"** —
  StatCard floated a small white card on flat cream; read washed-out/empty.
  RULE (nick style): money/comparison beats use the full-frame `chart`
  treatment (brand-styled, animated bars + count-ups, title block) or a
  statcard placed over a rich field with a display headline — never a lone
  small card on an empty page-colored background.
- **"Screen around :39 doesn't make sense with what I'm speaking"** — an
  abstract chalk-triangle filler carried the "when someone tells you AI only
  remixes… remember" take. RULE: opinion/take/address-the-viewer lines are
  FACECAM beats (or the claim's receipt) — never decorative filler. If no
  face exists yet, use the receipt of the claim being countered, not
  unrelated texture.
- **"OpenAI logo with huge blank space under it — use large captions to
  cover it"** (reference: Nick hook = logo + tool window + big italic serif
  + face card, every band filled) — the v1 logoassemble hook left the lower
  60% empty with small chips. RULE (hardens BrandHook default): hook and any
  logo beat must fill the vertical: mark + window/media + LARGE display
  caption + face card. If a band would sit empty, put big type in it —
  blank space in the first 2s is a hard fail.
- **v2 → v3: "first 2-3 seconds look like a still screen — use OpenAI's
  official logo, animate it, things should be moving, add text animations"**
  — BrandHook's springs all settled by ~0.7s and the window held a static
  screenshot. ENGINE (permanent, BrandHook.tsx): official brand mark (svgl
  paths) draw-on stroke → fill with spin settle + perpetual slow rotation;
  per-letter title stagger; subtitle tracking-in; serif line pops word-by-
  word (numbers auto-accent amber) + underline sweep; window gets continuous
  push-in and, for still images, a slow pan. RULE (universal): in any hook
  scene the motion must NEVER fully settle — stagger entrances across the
  full beat and give every still asset a continuous camera move; brand marks
  are ANIMATED (draw/assemble), never pasted static.
- Process: HeyGen connector appeared mid-session → avatar generated
  audio-driven from the existing VibeVoice track (16:9 1080p, face-x 0.43),
  dropped into brandhook hook + "remember" take + CTA without touching VO or
  captions. HAS_FACE branch in build_astra.py keeps both variants buildable.

## 2026-08-03 — oss-alt v1 → v2 (tool-name montage + tail trim)

- **"When you start saying tool names (Claude Code, Cursor…) just show their
  animated logos or dashboards"** — v1 cut to each tool's alternatives-page
  scroll during the name montage; at 0.4-0.8s per name those read as walls of
  text. RULE: when the VO merely NAMES tools in rapid succession, show the
  brand MARK (logoassemble) or a recognizable dashboard hero — never a
  text-heavy page. Results-page footage belongs to the beats that talk about
  the results themselves. svgl note: gradient (`url(#…)`) fills strip out —
  drop those layers and keep solid+white paths (canva = purple circle + C);
  tint `currentColor` marks with theme ink or cream per bg.
- **"When you finish speaking the reel goes on while the face is still — cut
  that out"** — v1 held the CTA end-card 1.5s past VO end, freezing the
  avatar's last frame behind it. RULE: reel ends ≤0.3-0.4s after the final
  spoken word; land the end-card BEFORE the VO ends (shift dropAt earlier),
  never hold on a frozen face. Avatar master ends ~0.2s after VO — any scene
  time past that is a freeze.
