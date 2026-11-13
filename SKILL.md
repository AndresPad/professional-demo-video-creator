---
name: professional-demo-video-creator
description: 'Create polished narrated product-demo videos from live websites or applications, including script review, neural voice-over, Playwright screen recording, synchronized cursor and spotlights, captions, SmartArt-style interstitial slides, dashboard scrolling and iframe interactions, MP4 assembly, verification, PowerPoint static-slide export, and Word talk tracks. Use when asked to create, revise, troubleshoot, or polish a professional demo video, website walkthrough, leadership presentation video, voice-over screen recording, or when narration and visuals do not match.'
---

# Professional Demo Video Creator

Create leadership-ready product-demo videos in which every spoken claim is
supported by the visual shown at that moment. Prefer a real application
walkthrough over a slide-only video when the user asks to demonstrate a site.

The primary quality rule is:

> The screen, highlight, cursor, caption, and narration must describe the same
> subject at the same time.

## When to use

Use this skill for:

- narrated website or application demonstrations
- professional launch, review, leadership, manager, or CVP videos
- Playwright-driven screen recordings
- neural voice-over and caption generation
- static title, problem, transition, impact, and closing slides
- dashboards that must scroll, drill down, or highlight changing metrics
- voice and visual synchronization fixes
- companion PowerPoint decks and Word talk tracks

Do not use it for ordinary video trimming with no product-demo workflow.

## Required inputs

Gather only what is missing:

1. The application URL or existing recording project.
2. The approved or draft talk track.
3. Audience and purpose.
4. Required voice, pace, branding, captions, and runtime.
5. Actions that must never be performed in the live application.
6. Deliverables: MP4, PPTX, DOCX, script, or some combination.

If a requested metric, cost, duration, benefit, or result is not sourced, ask
for the real value. Never invent business-impact figures.

## Safety and authorization

- Treat a live demo as read-only unless the user explicitly authorizes writes.
- Never submit forms, start scans, delete records, publish content, or trigger
  costly operations merely because the narration says to do so.
- Simulate dangerous actions by hovering, spotlighting, or using existing
  completed data.
- Record every prohibited selector or action in a preflight block.
- Do not bypass authentication, access controls, or network restrictions.
- Get approval before sending script text to an online TTS service.
- Do not expose credentials, tokens, private URLs, or sensitive customer data.

## Deliverable contract

Use a project structure that separates source content from generated output:

```text
video-project/
  script.py                 # stable line IDs, spoken text, caption text
  recorder.py               # browser choreography and recording
  cards.py                  # shared static-card definitions
  voice.py                  # TTS generation
  build_video.py            # assembly and encoding
  build_slides.py           # PPTX export
  build_talk_track.py       # DOCX export
  audio/                    # one clip per line ID
  capture/                  # raw recording
  verify/                   # sampled verification frames
  out/                      # final deliverables
```

Keep stable IDs such as `n01`, `n02`, and `n03`. Each script item should contain:

```python
dict(
    id="n01",
    say="Text optimized for speech, including spaced acronyms.",
    cap="Readable caption text with normal acronyms.",
)
```

Regenerate only audio clips whose `say` text changed.

## Workflow

### 1. Lock the script before production

Create a reviewable talk track before recording when the script is not approved.
For every line, define:

- purpose
- spoken text
- readable caption
- expected visual
- approximate duration
- any exact phrase that should trigger a highlight or transition

Use concise sentences. Explain the problem and why the interface matters before
showing detailed controls. Preserve manager-approved wording unless the user
explicitly asks to change it.

### 2. Build a visual beat sheet

Map every line to one visual beat:

| Beat type | Use |
|---|---|
| Static card | problem, impact, transition, summary |
| Live interaction | typing, selecting, opening, filtering |
| Spotlight | a metric, field, result, or ranked row |
| Scroll or drill-down | evidence below the fold |
| Hold | visual already matches the full sentence |

Do not show the next topic early. Do not retain the previous topic after the
voice has moved on. A loading spinner, blank page, frozen card, or irrelevant
dashboard view is not an acceptable placeholder.

### 3. Design static cards consistently

- Use one restrained accent color across the deck unless branding requires more.
- Use large titles, strong hierarchy, generous but intentional spacing, and
  simple diagrams or SmartArt-like visual structures.
- Prefer flow, comparison, cycle, layers, and metric cards over paragraphs.
- Avoid decorative colors that imply status unless the meaning is intentional.
- Keep static-card definitions in one shared module used by both the video and
  PowerPoint generator.
- Render every card and check its measured height. Fail on overflow instead of
  silently clipping content.

### 4. Generate narration

- Use a natural neural voice appropriate to the requested presentation style.
- Tune pace with short calibration samples before generating the full script.
- Normalize audio format, sample rate, and channel count.
- Measure actual WAV duration; never estimate line duration from word count.
- Keep one clip per stable line ID.
- Use retries for network TTS, but surface persistent failures.

### 5. Record the real application

Use Playwright or the repository's existing browser automation.

- Use a fixed 16:9 viewport, normally 1920x1080.
- Navigate through the same route a user takes. Direct deep links may not boot
  SPA or Blazor applications correctly.
- Wait for real readiness signals: visible controls, populated rows, resolved
  data, or application-specific state.
- Do not wait for text in the top document when the content lives in an iframe.
- Resolve the actual scroll container. `window.scrollBy` may be a silent no-op
  when the application scrolls a nested `<main>` or child frame.
- Reinstall overlays after SPA navigation when the document is replaced.

### 6. Handle dashboards and iframes

Inspect frames when visible content cannot be found in the top document.

For frame content:

1. Locate the application frame by stable URL or content.
2. Perform scroll, text search, and bounding-box lookup inside that frame.
3. Convert the target rectangle to top-level coordinates by adding the iframe
   element's bounding box.
4. Prefer a currently visible text match. If none is visible, scroll the best
   match into view and retry.
5. Verify row count and scroll position in logs.

Never assume a visible dashboard belongs to the top document.

### 7. Synchronize by spoken phrase

Do not fire all highlights at the start of a narration clip.

For each highlighted item, identify the exact phrase that names it:

```python
cue("n26", "mean Attack Success Rate")
cue("n26", "how many evaluations have run")
cue("n26", "whether those evaluations")
```

Trigger the visual near that phrase. The bundled
`scripts/check_cues.py` estimates phrase positions and flags missing or
out-of-order cues.

A character-position estimate is acceptable for initial placement:

```python
seconds = phrase_index / len(spoken_text) * audio_duration - lead_seconds
```

Then verify with extracted frames and the audible track. Adjust manually when
TTS cadence, punctuation, or pauses make the estimate inaccurate.

The cursor must follow the highlighted item, but cursor alignment alone is not
proof of synchronization. The highlighted subject must match the words being
spoken.

### 8. Make choreography deadline-driven

Browser calls take real time. A loop that sleeps `duration / steps` after every
JavaScript or frame call will overrun because it ignores call latency.

Pace animation against a monotonic deadline:

```python
end = time.monotonic() + seconds
for i in range(steps):
    await perform_step()
    due = end - seconds * (steps - i - 1) / steps
    if due > time.monotonic():
        await asyncio.sleep(due - time.monotonic())
```

At the end of each beat, absorb only the remaining narration time:

```python
remaining = audio_duration - (time.time() - beat_start)
if remaining > 0:
    await asyncio.sleep(remaining)
```

Do not append fixed waits after a beat without accounting for elapsed time.

### 9. Hide genuine loads without hiding relevant narration

Start slow navigation behind the preceding static card when possible.
Poll the real readiness signal and reveal the application as soon as it is
ready.

If load compression is necessary:

- never compress video under active narration
- remap audio and video using the same boundary
- use `>=` at the post-load boundary so a beat starting exactly there is remapped
- log silence gaps after final remapping
- inspect the transition frame by frame

Prefer eliminating a bogus timeout over speed-ramping it. A top-document wait
for text inside an iframe can create a fake 25-second load even when the frame
is ready in five seconds.

### 10. Captions

- Use one caption location, normally a single line at the bottom.
- Never show duplicate top and bottom captions.
- Generate captions from the readable `cap` text, not speech-optimized text.
- Normalize curly quotes, dashes, non-breaking spaces, and unexpected
  non-ASCII characters when the delivery format requires ASCII.
- Spell-check captions independently of the approved narration.

### 11. Assemble and encode

- Trim setup time before the first beat.
- Mix narration on the remapped timeline.
- Normalize loudness and prevent clipping.
- Use H.264 with `yuv420p` and AAC for broad compatibility.
- Preserve 16:9 and a stable frame rate.
- Use `-shortest` only after confirming the narration and video tails are correct.

### 12. Verify the actual requirement

Do not declare success after the encoder exits.

Verification must include:

1. Extract frames immediately before, during, and after every transition.
2. Inspect every spotlight at the phrase where it should appear.
3. Check that the cursor is on the highlighted item.
4. Confirm dashboard scroll position changes.
5. Confirm there are no blank frames or loading spinners.
6. Calculate narration gaps after timeline remapping.
7. Check the first and final frames.
8. Confirm captions are unique, readable, and free of mojibake.
9. Confirm prohibited live actions were not executed.
10. Verify runtime and output file size.

Use short isolated geometry or synchronization tests instead of repeatedly
recording the full video while debugging one overlay.

## Companion outputs

When requested:

- Build a PPTX from the exact shared static-card definitions used in the video.
- Put the corresponding narration into slide speaker notes.
- Build a DOCX talk track from the same script source and measured audio
  durations.
- Update displayed runtime after the final MP4 is assembled.
- Never maintain separate hand-copied versions that can drift.

## Revision handling

Translate feedback into a measurable change:

- "voice is too fast/slow" -> calibrate rate and compare total narration time
- "slides look dull" -> add a meaningful visual structure, not decoration
- "visual and voice do not match" -> identify the exact spoken phrase and cue
  the matching visual to it
- "dashboard is static" -> identify the real frame and scroll container
- "blank screen" -> preload behind a relevant card and wait on real readiness
- "remove unnecessary dashboard footage" -> end each beat on its last spoken word
- "captions appear twice" -> enforce a single caption surface globally

Never fix a phrase-level mismatch by merely moving the cursor.

## Final handoff

State:

- final filename and runtime
- what materially changed
- where the MP4, PPTX, DOCX, and script are located
- any safety simulation used instead of a live action
- any unresolved limitation

Keep prior user-owned files unless the user explicitly asks to remove them.

