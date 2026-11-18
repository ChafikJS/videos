---
name: aistudio2api
description: Generate images (Nano Banana), narration audio (Gemini TTS) and video clips through a running AIStudio2API instance, a proxy that exposes Google AI Studio as an OpenAI-compatible API. Use when asked to generate stills, voice-over or clips for scenes via AI Studio, Gemini, Nano Banana or "aistudio2api", or to check which models that instance offers.
---

# AIStudio2API client

[Mag1cFall/AIStudio2API](https://github.com/Mag1cFall/AIStudio2API) is a Go
server the user runs themselves with their own Google account. This skill only
talks to an instance that is already running; it does not install the server
and never handles Google credentials or cookies.

## Before anything else

```bash
python3 .claude/skills/aistudio2api/scripts/gen.py models
```

- `AISTUDIO2API_BASE_URL` (default `http://127.0.0.1:2048`) and
  `AISTUDIO2API_KEY` (the instance's `PROXY_API_KEY`) configure the client.
  Never write the key into a file in the repository.
- If the instance is unreachable, stop and tell the user. Do not fall back to
  placeholder images or silent audio. In a cloud session `127.0.0.1` is the
  container, not the user's computer: the instance must be reachable at a
  public HTTPS URL whose host the environment's network policy allows.
- Model names change with the upstream catalog. If a default model is rejected,
  pick the closest one from the `models` output and pass it with `--model`.

## Commands

```bash
# still image; --size is the final pixel size
python3 .claude/skills/aistudio2api/scripts/gen.py image "<prompt>" -o out/scene-01.png --size 3840x2160

# narration to WAV; --instructions sets the speaking style
python3 .claude/skills/aistudio2api/scripts/gen.py tts --file take.txt -o out/story-1.wav --voice <voice> --instructions "calm, low, unhurried"

# video clip (creates a task, polls, downloads)
python3 .claude/skills/aistudio2api/scripts/gen.py video "<prompt>" -o out/scene-01.mp4
```

Other endpoints the server exposes, if a task needs them: `/v1/chat/completions`,
`/v1/responses`, `/v1/messages` (Anthropic), `/v1beta/...` (Gemini native),
`/v1/images/edits` (image-to-image, same fields as generations). Voices are
listed in the live model catalog under `capability_options.voices`.

## Using it for this repository

- Image and video prompts for all 65 scenes are in `02-shot-list.md`; use them
  verbatim, since the character and location anchors are already written into
  each one. Master format is 16:9, 3840x2160.
- Generate one reference image per character first and get the user's approval
  before batch-generating scenes.
- Narration: one take per story from `01-narration-script.md`, deep calm male
  voice, about 150 wpm. `[PAUSE]` markers are direction, not text to speak.
- Free AI Studio accounts have a daily request count per model. Generate a few
  scenes, check them, then continue; do not fire all 65 at once.
- Write outputs under `out/` and do not commit generated media unless asked.

## Caveat to pass on once

The proxy drives the AI Studio website outside Google's official API, so using
it may break Google's terms and can get the account restricted. For work that
must not be at risk, the official Gemini API with an API key is the supported
route.
