#!/usr/bin/env python3
"""Client for a running AIStudio2API instance (OpenAI-compatible endpoints).

  gen.py models
  gen.py image "prompt" -o out.png [--size 3840x2160] [--model ...]
  gen.py tts   "text"   -o out.wav [--voice Kore] [--model ...]
  gen.py tts   --file narration.txt -o out.wav
  gen.py video "prompt" -o out.mp4 [--model ...]

Environment:
  AISTUDIO2API_BASE_URL  default http://127.0.0.1:2048
  AISTUDIO2API_KEY       the instance's PROXY_API_KEY (optional if it has none)
"""
import argparse
import base64
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("AISTUDIO2API_BASE_URL", "http://127.0.0.1:2048").rstrip("/")
KEY = os.environ.get("AISTUDIO2API_KEY", "")


def call(path, body=None, timeout=600):
    headers = {"Content-Type": "application/json"}
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} from {path}: {e.read().decode(errors='replace')[:800]}")
    except urllib.error.URLError as e:
        raise SystemExit(
            f"cannot reach AIStudio2API at {BASE} ({e.reason}). "
            "Is the service started, and is AISTUDIO2API_BASE_URL right?"
        )


def save(path, blob):
    out = pathlib.Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(blob)
    print(f"wrote {out} ({len(blob)} bytes)")


def cmd_models(a):
    raw, _ = call("/v1/models", timeout=60)
    for m in json.loads(raw).get("data", []):
        print(m.get("id"))


def cmd_image(a):
    body = {"model": a.model, "prompt": a.prompt, "n": 1, "output_format": a.format}
    if a.size:
        body["size"] = a.size
    if a.quality:
        body["quality"] = a.quality
    raw, _ = call("/v1/images/generations", body)
    item = json.loads(raw)["data"][0]
    if item.get("b64_json"):
        blob = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        url = item["url"]
        if url.startswith("data:"):
            blob = base64.b64decode(url.split(",", 1)[1])
        else:
            blob, _ = call(url[len(BASE):], timeout=120) if url.startswith(BASE) else (
                urllib.request.urlopen(url, timeout=120).read(), "")
    else:
        raise SystemExit(f"no image in response: {str(item)[:300]}")
    save(a.output, blob)


def cmd_tts(a):
    text = pathlib.Path(a.file).read_text(encoding="utf-8") if a.file else a.text
    if not text:
        raise SystemExit("give the text as an argument or with --file")
    body = {"model": a.model, "input": text, "voice": a.voice, "response_format": "wav"}
    if a.instructions:
        body["instructions"] = a.instructions
    blob, _ = call("/v1/audio/speech", body)
    save(a.output, blob)


def cmd_video(a):
    raw, _ = call("/v1/videos", {"model": a.model, "prompt": a.prompt})
    job = json.loads(raw)
    vid = job["id"]
    print(f"task {vid} created")
    deadline = time.time() + a.timeout
    while True:
        status = job.get("status")
        if status in ("completed", "succeeded"):
            break
        if status in ("failed", "cancelled", "canceled", "error"):
            raise SystemExit(f"video task {status}: {json.dumps(job)[:600]}")
        if time.time() > deadline:
            raise SystemExit(f"timed out; resume later with GET /v1/videos/{vid}")
        time.sleep(10)
        job = json.loads(call(f"/v1/videos/{vid}", timeout=60)[0])
        print(f"  status: {job.get('status')}", file=sys.stderr)
    blob, _ = call(f"/v1/videos/{vid}/content")
    save(a.output, blob)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("models").set_defaults(fn=cmd_models)

    s = sub.add_parser("image")
    s.add_argument("prompt")
    s.add_argument("-o", "--output", required=True)
    s.add_argument("--model", default="gemini-3.1-flash-image")
    s.add_argument("--size", help="WIDTHxHEIGHT, e.g. 3840x2160")
    s.add_argument("--quality", choices=["low", "medium", "high"], help="1K / 2K / 4K when --size is omitted")
    s.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    s.set_defaults(fn=cmd_image)

    s = sub.add_parser("tts")
    s.add_argument("text", nargs="?")
    s.add_argument("--file")
    s.add_argument("-o", "--output", required=True)
    s.add_argument("--model", default="gemini-3.8-flash-tts")
    s.add_argument("--voice", default="Kore")
    s.add_argument("--instructions", help="speaking style, e.g. 'calm, low, unhurried'")
    s.set_defaults(fn=cmd_tts)

    s = sub.add_parser("video")
    s.add_argument("prompt")
    s.add_argument("-o", "--output", required=True)
    s.add_argument("--model", default="gemini-omni-1.1-flash")
    s.add_argument("--timeout", type=int, default=1200)
    s.set_defaults(fn=cmd_video)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
