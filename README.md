# 5 Disturbing Stories From Night Shift Workers

Production package for a faceless, cinematic horror anthology video for YouTube.
All five stories are original fiction, and the narration says so in the first minute.

| File | Contents |
|---|---|
| [`01-narration-script.md`](01-narration-script.md) | Complete word-for-word narration: hook, intro, five stories, transitions, closing |
| [`02-shot-list.md`](02-shot-list.md) | 65 scenes with timestamp, narration, visuals, camera, lighting, sound, and ready-to-paste AI image and video prompts |
| [`source/scenes.txt`](source/scenes.txt) | Single source both files are built from |
| [`build.py`](build.py) | Rebuilds both files and recalculates every timestamp: `python3 build.py` |

To change a line of narration or a shot, edit `source/scenes.txt` and run the build. Do not edit the two generated files by hand.

## Specifications

| | |
|---|---|
| Runtime | About 33 minutes (4,589 spoken words at 150 wpm, plus pauses) |
| Format | 16:9, 3840x2160 master (1920x1080 minimum), 24 fps |
| Language / audience | Natural American English, USA, ages 18-44 |
| Narration | Deep, natural American male voice, calm and unsettling, first person |
| Look | Photorealistic, low-key lighting, muted grade, subtle film grain, slow camera |
| Content | Psychological horror, no gore, nothing shown that the narration does not earn |

## The five stories

| # | Story | Runtime | False explanation | Final revelation |
|---|---|---|---|---|
| 1 | **The Gas Station** (West Texas) | 5:48 | The old DVR replays "ghost frames" of past customers | The figure on the recording from three days ahead is the narrator himself |
| 2 | **The Hospital** (Pennsylvania, 3:17 AM) | 5:42 | The boiler shakes abandoned call-light wiring | The eleven calls she silenced were a patient who had not been moved into the room yet |
| 3 | **The Security Guard** (outside Chicago) | 5:47 | A robotic floor scrubber and trucker radio bleed | Something in the building checks in using the guards' voices, so nobody ever comes looking |
| 4 | **The Hotel** (Nevada) | 6:33 | A housekeeping phone in the linen closet and a prankster | Room 313 was walled up in 1971, and the narrator sends a visitor up to it |
| 5 | **The Delivery Driver** (Colorado) | 5:57 | A late-added stop at a mis-mapped cabin address | The delivery photo shows the missing drivers, and the scanner now asks for "one driver" |

Each ending lands differently on purpose: identity, guilt, replacement, complicity, invitation.

## Voice direction

- Pace around 150 words per minute. Slow down for the last two sentences of every story.
- No "spooky voice." The narrator sounds like someone telling you something true that they would rather not.
- Quoted lines are read quieter and flatter, never acted as characters. Stories 2 and 4 have women narrators; the transitions frame them as accounts being retold, so the same male voice carries all five.
- Respect every `[PAUSE]`. Leave room tone and music under it, never dead silence, except where the shot list calls for silence.
- If you use an AI voice, generate each story as its own take and check the pronunciation of "Calder Wells," "Halloran," "Tolliver," and "Montrose."

## Music and sound

- Use original or properly licensed dark ambient music only, and keep the license documents. Give each story its own bed so the anthology does not blur together:
  1. Gas station: electrical hum, a slowly rising single tone
  2. Hospital: sparse felt piano, the two-tone call chime as a motif
  3. Warehouse: sub-bass pulse, radio static, long metallic reverbs
  4. Hotel: a distant, warped mid-century ballad through walls
  5. Mountain road: wind, low strings, near-silence in the fog
- Each story has a signature sound (monitor buzz, call chime, radio squelch, elevator bell, scanner chirp). The closing scene replays all five in order.
- Mix narration at about -14 LUFS integrated, music 18-22 dB under the voice, and duck the music further on the final line of each story.

## Visual consistency

Character and location descriptions are fixed in `build.py` (`ANCHORS`) and written into every prompt automatically, so each person and place is described identically in every scene. Generate one reference image per character first, reuse it as a character reference where your tool supports that, and use image-to-video from the approved still for each scene.

Security-camera scenes use a separate low-resolution CCTV style. Add timestamps, room numbers, screen contents and the title in the edit, because image generators do not render text reliably.

## Before publishing

- Keep the "work of fiction" line in the narration and repeat it in the video description.
- Follow YouTube's current disclosure rules for realistic AI-generated or altered content when you upload.
- Place names such as Lone Mesa Fuel, St. Brennan Memorial, Calder Wells, the Desert Crown Hotel and Harrow Creek Road are invented for this script.
