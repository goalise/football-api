"""Print the football matches of one day, or every match that is live now.

Usage:
    export GOALISE_TOKEN=your_api_token
    python matches.py --date 2026-09-12
    python matches.py --date 2026-09-12 --timezone Europe/London
    python matches.py --live

Needs Python 3.8+ and nothing else.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.goalise.com/api/v3"


def get(path, params):
    request = urllib.request.Request(
        "{}{}?{}".format(API, path, urllib.parse.urlencode(params)),
        headers={
            "Authorization": "Bearer " + os.environ.get("GOALISE_TOKEN", ""),
            "Accept": "application/json",
            "User-Agent": "goalise-examples/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            return json.load(error)  # errors use the same JSON envelope
        except ValueError:
            sys.exit("HTTP {} from the API".format(error.code))


def main():
    parser = argparse.ArgumentParser(description="Football matches from the Goalise API")
    parser.add_argument("--date", help="one day, YYYY-MM-DD")
    parser.add_argument("--live", action="store_true", help="every match in progress")
    parser.add_argument("--timezone", default="UTC", help="IANA zone for kick-off times, default UTC")
    args = parser.parse_args()
    if not args.date and not args.live:
        parser.error("pass --date YYYY-MM-DD or --live")

    params = {"timezone": args.timezone}
    if args.live:
        params["live"] = "all"
    else:
        params["date"] = args.date

    page = 1
    while True:
        data = get("/matches", dict(params, page=page))
        if data["status"] != "success":
            sys.exit("API error: " + ", ".join(error["code"] for error in data["errors"]))

        for match in data["response"]:
            kick_off = (match["start_date"] or "")[11:16]
            home = (match["home_team"] or {}).get("name", "?")
            away = (match["away_team"] or {}).get("name", "?")
            league = (match["league"] or {}).get("name", "")
            status = match["status"]["short"] or ""
            # Both scores are 0 before kick-off, so show them only once the match has started.
            score = "{}-{}".format(match["score"]["home"], match["score"]["away"]) if status not in ("NS", "TBD", "PST", "CANC") else "v"
            print("{:<5} {:<4} {:>24} {:^5} {:<24} {}".format(kick_off, status, home[:24], score, away[:24], league))

        if page >= data["pagination"]["page_count"]:
            break
        page += 1


if __name__ == "__main__":
    main()
