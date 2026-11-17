#!/usr/bin/env python3
"""Builds 01-narration-script.md and 02-shot-list.md from source/scenes.txt.

Edit the narration or any shot in source/scenes.txt, then run:  python3 build.py
Timestamps are recalculated from word count at the narration pace below.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
WPM = 150  # calm, deliberate horror read
TITLE = "5 Disturbing Stories From Night Shift Workers"

STYLE = ("photorealistic cinematic horror film still, 35mm anamorphic lens, low-key lighting, "
         "deep natural shadows, muted desaturated color grade, subtle film grain, realistic human "
         "proportions, 16:9 aspect ratio, 4K, no text, no captions, no watermark")
CCTV_STYLE = ("realistic security camera footage still, wide-angle lens with slight barrel distortion, "
              "low resolution, compression artifacts, washed-out color, slight interlacing, "
              "16:9 aspect ratio, no text, no watermark")
VSTYLE = ("Photorealistic, cinematic horror, 24 fps, 16:9, slow deliberate camera movement, "
          "low-key lighting, subtle film grain, no dialogue, no on-screen text.")
CCTV_VSTYLE = ("Realistic low-resolution security camera footage, fixed high-angle camera, "
               "compression artifacts, 16:9, no on-screen text.")

ANCHORS = {
    "DANNY": "Danny, a 26-year-old white American man with a lean build, short messy brown hair, light stubble "
             "and tired eyes, wearing a faded red polo work shirt with a name tag and jeans",
    "FIGURE": "a lean man in a plain gray hooded sweatshirt with the hood down and short brown hair, seen only "
              "from behind, face never visible",
    "STATION": "Lone Mesa Fuel, a small weathered 1990s gas station and convenience store with four pumps under a "
               "buzzing fluorescent canopy beside an empty two-lane desert highway in West Texas",
    "RENEE": "Renee, a 38-year-old Black American nurse with her hair in a low bun, wearing navy blue scrubs and "
             "an ID badge, tired but composed",
    "HOSP": "St. Brennan Memorial, an aging 1970s small-town Pennsylvania hospital with beige walls, worn "
            "linoleum floors and half its ceiling lights switched off",
    "MANNY": "Manny, a 44-year-old stocky Latino American man with a graying goatee, wearing a black security "
             "uniform jacket with a shoulder radio microphone and carrying a flashlight",
    "WH": "a massive modern distribution warehouse complex outside Chicago",
    "TESS": "Tess, a 34-year-old white American woman with shoulder-length auburn hair, wearing a dark green "
            "cardigan over a white blouse",
    "HOTEL": "the Desert Crown Hotel, a faded three-story 1950s roadside hotel in the Nevada desert",
    "ELI": "Eli, a 29-year-old Asian American man with short black hair under a dark beanie, wearing a navy work "
           "jacket with a reflective stripe",
    "VAN": "a plain white high-roof cargo delivery van",
}
STORIES = {1: "The Gas Station", 2: "The Hospital", 3: "The Security Guard",
           4: "The Hotel", 5: "The Delivery Driver"}
FIELDS = [("V", "Visual"), ("A", "Camera angle"), ("M", "Camera movement"), ("L", "Lighting"),
          ("T", "Atmosphere"), ("X", "Sound effects")]


def fill(text):
    return re.sub(r"\{(\w+)\}", lambda m: ANCHORS[m.group(1)], text)


def parse():
    scenes, cur = [], None
    for line in (ROOT / "source/scenes.txt").read_text().splitlines():
        if line.startswith("## "):
            story, section = [p.strip() for p in line[3:].split("|")]
            cur = {"story": int(story), "section": section, "N": [], "P": 1.0}
            scenes.append(cur)
        elif cur is not None and re.match(r"^[A-Z]: ", line):
            key, val = line[0], line[3:].strip()
            if key == "N":
                cur["N"].append(val)
            elif key == "P":
                cur["P"] = float(val)
            else:
                cur[key] = val
    t = 0.0
    for i, s in enumerate(scenes, 1):
        s["num"] = i
        s["words"] = sum(len(p.split()) for p in s["N"])
        s["dur"] = round(s["words"] / WPM * 60 + s["P"])
        s["start"], t = t, t + s["dur"]
        s["end"] = t
    return scenes


def ts(sec):
    return f"{int(sec) // 60:02d}:{int(sec) % 60:02d}"


def build_script(scenes, total_words, total):
    out = [f"# {TITLE}", "", "## Complete Narration Script", "",
           f"**{total_words:,} spoken words · about {ts(total)} at {WPM} wpm including pauses.**  ",
           "`[PAUSE]` marks a beat of music and ambience only. Lines in quotation marks are read slightly "
           "quieter and flatter than the surrounding narration; do not perform them as character voices.", ""]
    last = None
    for s in scenes:
        head = (f"Story {s['story']}: {STORIES[s['story']]}" if s["story"] else s["section"])
        if head != last and s["N"]:
            out += ["---", "", f"### {head}  `[{ts(s['start'])}]`", ""]
            last = head
        for p in s["N"]:
            out += [p, ""]
        if s["N"] and s["P"] >= 2:
            out += [f"`[PAUSE {s['P']:g}s]`", ""]
    (ROOT / "01-narration-script.md").write_text("\n".join(out))


def build_shots(scenes, total):
    out = [f"# {TITLE}", "", "## Cinematic Shot List", "",
           f"{len(scenes)} scenes · total runtime about {ts(total)} · 24 fps · 16:9.", "",
           "**How to use it**", "",
           "- Every image and video prompt is self-contained: character, location and style descriptions are "
           "already written in, so paste them as they are. Generate the image first, then use it as the start "
           "frame for the video prompt (image-to-video) to keep characters and sets consistent.",
           "- Most video generators produce 5-10 second clips. For a longer scene, generate two to four clips from "
           "the same start frame (vary only the camera movement) and add inserts of the objects named under "
           "*Visual*. Aim for a cut every 6-10 seconds.",
           "- AI generators render text badly. Add all on-screen text in the edit: CCTV timestamps, room numbers, "
           "scanner and computer screens, the plaque engraving, the title card.",
           "- Timestamps assume the narration pace in the script. After recording the voice-over, slide each "
           "scene to the real audio.", ""]
    last = None
    for s in scenes:
        head = (f"Story {s['story']}: {STORIES[s['story']]}" if s["story"] else s["section"])
        if head != last:
            out += ["---", "", f"## {head}", ""]
            last = head
        cctv = s["I"].startswith("CCTV:")
        img = fill(s["I"][5:].strip() if cctv else s["I"])
        img = img[0].upper() + img[1:] + ", " + (CCTV_STYLE if cctv else STYLE)
        vid = fill(s["D"]) + " " + (CCTV_VSTYLE if cctv else VSTYLE)
        story = f"{s['story']} ({STORIES[s['story']]})" if s["story"] else f"- ({s['section']})"
        out += [f"### Scene {s['num']}", "",
                f"- **Story:** {story}",
                f"- **Timestamp:** {ts(s['start'])} - {ts(s['end'])}",
                f"- **Duration:** {s['dur']}s",
                "- **Narration:** " + (" ".join(s["N"]) if s["N"] else "*(none: music and sound only)*")]
        out += [f"- **{label}:** {s[k]}" for k, label in FIELDS]
        out += [f"- **AI image prompt:** `{img}`", f"- **AI video prompt:** `{vid}`", ""]
    (ROOT / "02-shot-list.md").write_text("\n".join(out))


if __name__ == "__main__":
    scenes = parse()
    total_words = sum(s["words"] for s in scenes)
    total = scenes[-1]["end"]
    build_script(scenes, total_words, total)
    build_shots(scenes, total)
    print(f"scenes={len(scenes)} words={total_words} runtime={ts(total)}")
    for n, name in [(0, "Intro/transitions/outro")] + list(STORIES.items()):
        ss = [s for s in scenes if s["story"] == n]
        print(f"  {name}: {sum(s['words'] for s in ss)} words, {ts(sum(s['dur'] for s in ss))}, {len(ss)} scenes")
