#!/usr/bin/env python3
"""Search the bundled library of code-animation video prompts.

  search.py recipe cocktail            # keyword search (all words must match)
  search.py --category 3d --tech threejs
  search.py --show ror-fly-880547      # print one full prompt
  search.py --stats
"""
import argparse
import collections
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "videos.json"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("words", nargs="*", help="keywords, all must appear in the prompt")
    p.add_argument("--category", choices=["motion", "3d", "explainer", "interactive"])
    p.add_argument("--tech", help="tech tag, e.g. canvas, svg, threejs, shader, gsap, css, audio")
    p.add_argument("--full-only", action="store_true", help="skip entries whose prompt is partial")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--show", metavar="SLUG", help="print the full prompt of one entry")
    p.add_argument("--stats", action="store_true")
    a = p.parse_args()

    videos = json.loads(DATA.read_text(encoding="utf-8"))

    if a.stats:
        print(len(videos), "prompts")
        print("categories:", dict(collections.Counter(v["category"] for v in videos)))
        print("tech:", dict(collections.Counter(t for v in videos for t in v["tech_tags"]).most_common()))
        return

    if a.show:
        for v in videos:
            if v["slug"] == a.show:
                print(f"# {v['slug']}  by @{v['author']}  [{v['category']}; {', '.join(v['tech_tags'])}]")
                print(f"# source: {v['post_url']}")
                if v["prompt_partial"]:
                    print("# NOTE: the creator shared only part of the prompt / a description")
                print()
                print(v["prompt"])
                return
        raise SystemExit(f"no entry with slug {a.show!r}")

    words = [w.lower() for w in a.words]
    hits = []
    for v in videos:
        text = v["prompt"].lower()
        if a.category and v["category"] != a.category:
            continue
        if a.tech and a.tech.lower() not in v["tech_tags"]:
            continue
        if a.full_only and v["prompt_partial"]:
            continue
        if not all(w in text for w in words):
            continue
        hits.append((sum(text.count(w) for w in words), len(v["prompt"]), v))
    # most keyword hits first, then the most detailed prompts
    hits.sort(key=lambda h: (-h[0], -h[1]))

    print(f"{len(hits)} match(es), showing {min(a.limit, len(hits))}")
    for _, _, v in hits[: a.limit]:
        snippet = " ".join(v["prompt"].split())[:160]
        flag = " (partial)" if v["prompt_partial"] else ""
        print(f"\n{v['slug']}  [{v['category']}; {', '.join(v['tech_tags'])}]{flag}  {len(v['prompt'])} chars")
        print(f"  {snippet}")


if __name__ == "__main__":
    main()
