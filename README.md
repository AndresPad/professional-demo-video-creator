# Professional Demo Video Creator

A reusable GitHub Copilot skill for creating polished, narrated product-demo
videos from live websites and applications.

It covers:

- script and visual-beat planning
- neural voice-over and readable captions
- Playwright-driven screen recording
- SmartArt-style interstitial slides
- dashboards, nested scroll containers, and iframe interactions
- phrase-level synchronization of narration, highlights, and cursor movement
- MP4 assembly and frame-by-frame verification
- companion PowerPoint decks and Word talk tracks

## Install

Copy this repository into your user Copilot skills directory:

```powershell
git clone https://github.com/neerajjhaveri/professional-demo-video-creator.git `
  "$HOME\.copilot\skills\professional-demo-video-creator"
```

If that destination already exists, pull the latest version instead:

```powershell
Set-Location "$HOME\.copilot\skills\professional-demo-video-creator"
git pull
```

The required skill definition is [`SKILL.md`](SKILL.md).

## Cue audit

The included cue checker estimates when a phrase occurs within a measured
narration clip and validates that visual cues are present and ordered:

```powershell
python scripts\check_cues.py reference\cue-example.json
```

Example output:

```text
n26   5.07s  mean Attack Success Rate
n26   8.13s  how many evaluations have run
n26  10.12s  whether those evaluations
```

These estimates are starting points. Final synchronization should always be
verified against extracted video frames and the audible narration.

## Trigger examples

- "Create a professional demo video from this website."
- "Record a narrated product walkthrough."
- "Make the dashboard visuals match the voice-over."
- "Create a PowerPoint of all static video slides."
- "Fix the captions, cursor, and highlight synchronization."

