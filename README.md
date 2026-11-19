# Football API

A REST API for football (soccer) data: live scores, fixtures and results, league tables, lineups, match events and statistics, players, transfers, injuries, betting odds, video highlights and news. 46 endpoints, JSON, one token. Every plan includes every endpoint and every competition, from $15 per month.

**[Start a 7-day free trial](https://goalise.com/checkout?product=basic&billing=monthly&utm_source=github&utm_medium=referral&utm_campaign=football-api)** · [Product page](https://goalise.com/football-data-api?utm_source=github&utm_medium=referral&utm_campaign=football-api) · [API reference](https://docs.goalise.com/v3/apireference) · [Support](https://goalise.com/support)

| | |
| --- | --- |
| Base URL | `https://api.goalise.com/api/v3` |
| Auth | `Authorization: Bearer YOUR_API_TOKEN` |
| Format | JSON, the same envelope on every endpoint |
| Coverage | 200+ competitions: Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, Champions League, World Cup 2026 and more |
| Price | Basic $15, Pro $30, Premium $50 per month. All endpoints and all competitions on every plan |
| Trial | 7 days free on the Basic plan (card required, cancel anytime) |

## Try it without a key

The coverage endpoint needs no token. It lists every country and competition in the API and which data each one has:

```bash
curl "https://api.goalise.com/api/v3/country-coverage"
```

## Quick start

1. Pick a plan at [goalise.com/checkout](https://goalise.com/checkout?product=basic&billing=monthly&utm_source=github&utm_medium=referral&utm_campaign=football-api). Basic starts with a 7-day free trial.
2. Copy your API token from the [dashboard](https://goalise.com/account).
3. Make the first request:

```bash
# Every match that is live right now
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/matches?live=all"

# The fixtures of one day, kick-off times in London time
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/matches?date=2026-09-12&timezone=Europe/London"

# One match with its events and lineups in the same call
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/match?id=466659&expand=events,lineup"
```

## What a response looks like

Every answer, success or error, has the same five keys. Example for `GET /matches` (one row, abridged, illustrative values):

```json
{
  "status": "success",
  "pagination": { "total_count": 10, "page_size": 120, "page_count": 1, "current_page": 1 },
  "errors": null,
  "meta": { "api_version": "3.0.0", "timezone": "UTC", "generated_at": 1788805800 },
  "response": [
    {
      "id": 466659,
      "league":    { "id": 646, "name": "Serie A", "logo": "https://...", "type": "League" },
      "home_team": { "id": 404, "name": "Cagliari", "logo": "https://..." },
      "away_team": { "id": 668, "name": "Lecce",    "logo": "https://..." },
      "timestamp": 1788798600,
      "start_date": "2026-09-12 20:45:00",
      "timezone": "UTC",
      "status": { "long": "Match Finished", "short": "FT", "elapsed": 90 },
      "score": {
        "home": 1,
        "away": 0,
        "detailed": { "half_time": "0-0", "full_time": "1-0", "extra_time": "-", "penalty": "-" }
      },
      "round": "Regular Season - 3",
      "season": 2026,
      "winner": "home",
      "has_events": true,
      "has_statistics": true,
      "has_lineup": true
    }
  ]
}
```

A match already carries its competition and both teams with names and crests, so a fixtures screen is one request, not one request per team.

## Endpoints

| Group | Endpoints | What you get |
| --- | --- | --- |
| Matches | `/matches` `/match` `/match-events` `/match-statistics` `/match-lineup` `/head-to-head` `/predictions` | Live scores, fixtures and results by date, competition, team or status; goals, cards and substitutions; team statistics; lineups; head-to-head records; predictions |
| Leagues | `/leagues` `/league` `/league-standing` `/league-seasons` `/league-rounds` | Competitions, league tables with form, seasons and rounds |
| Teams | `/team` `/teams-by-league` `/team-statistics` `/team-players` `/team-coach` | Clubs and national teams, season statistics, squads, coaches |
| Players | `/player` `/player-statistics` `/player-match-statistics` `/teams-by-player` `/top-scorers` `/top-assists` `/top-yellow-cards` `/top-red-cards` | Player profiles, season and per-match statistics, career teams, scoring and card charts |
| Transfers and injuries | `/team-transfers` `/player-transfers` `/injuries` | Transfers by team or player, injuries and suspensions |
| Odds | `/odds` `/live-odds` `/bookmakers` `/bets` `/live-bets` | Pre-match and in-play betting odds by bookmaker and market |
| Video | `/highlights` | Official match highlights and goal clips with embed URLs. See [football-highlights-api](https://github.com/goalise/football-highlights-api) |
| News | `/news-by-date` `/news-by-league` `/news-by-team` `/news-by-category` `/news-categories` `/news-content` | Football news feed. See [football-news-api](https://github.com/goalise/football-news-api) |
| Reference | `/search` `/countries` `/venues` `/country-coverage` | Search for teams, leagues and players; countries, stadiums, coverage |
| Service | `/quota` `/logs` | Your usage and recent requests |

Parameters and response fields for each endpoint are in the [API reference](https://docs.goalise.com/v3/apireference).

## Why developers pick it

- **One request per screen.** Related entities arrive as objects with a name and a logo, not as bare ids you have to look up.
- **`expand` on demand.** Add `?expand=events,lineup` to pull bigger relations into the same call. The payload stays small until you ask for more.
- **One envelope.** `status`, `pagination`, `errors`, `meta`, `response` on every endpoint. Branch on `errors[].code`, never on message text.
- **Your timezone.** `?timezone=Europe/Madrid` renders dates in any IANA zone. Timestamps stay UTC.
- **Cheap polling of dictionaries.** `/countries`, `/venues`, `/league-seasons` and similar endpoints answer with an `ETag`; send it back as `If-None-Match` and get `304` while nothing changed.
- **Flat pricing.** No per-league pricing: every plan includes every competition and every endpoint.

## Code examples

Runnable scripts are in [`examples/`](examples): [Python](examples/python/matches.py), [JavaScript](examples/javascript/live-scores.mjs), [PHP](examples/php/standings.php). They use only the standard library and read the token from the `GOALISE_TOKEN` environment variable.

```python
import json, os, urllib.request

request = urllib.request.Request(
    "https://api.goalise.com/api/v3/matches?live=all",
    headers={"Authorization": "Bearer " + os.environ["GOALISE_TOKEN"]},
)
for match in json.load(urllib.request.urlopen(request))["response"]:
    print(
        match["status"]["elapsed"], "'",
        match["home_team"]["name"], match["score"]["home"], "-",
        match["score"]["away"], match["away_team"]["name"],
    )
```

## Errors and limits

| HTTP | `errors[].code` | When |
| --- | --- | --- |
| 400 | `validation.required`, `validation.invalid`, `expand.unknown` | A required filter is missing, a value has the wrong format, or `expand` names an unknown relation |
| 401 | `auth.required`, `auth.invalid` | Token missing or rejected |
| 404 | `not_found` | The id belongs to nothing |
| 429 | `rate_limit.exceeded` | Limit reached. Wait for the seconds in `Retry-After` |

Limits apply per minute, hour and day. Every answer carries `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining` and `X-Rate-Limit-Reset`, and `GET /quota` shows your usage without spending a request. Lists are paginated with `?page=`, starting at 1.

## Pricing

| Plan | Price | Requests per day |
| --- | --- | --- |
| Basic | $15/month, first 7 days free | 5,000 |
| Pro | $30/month | 50,000 |
| Premium | $50/month | 150,000 |

The plans differ only in the number of requests. Annual billing is 30% cheaper. [See the plans](https://goalise.com/checkout?utm_source=github&utm_medium=referral&utm_campaign=football-api).

## FAQ

**Is there a free football API?**
Goalise has no permanent free tier. The Basic plan starts with a 7-day free trial, then costs $15 per month. A card is required to start the trial and you can cancel at any time. The `/country-coverage` endpoint works without a token, so you can check the coverage before you sign up.

**Which leagues and competitions are covered?**
More than 200, including the Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, Eredivisie, Liga Portugal, MLS, the Champions League, the Europa League and the World Cup 2026. The live list, with the data available for each competition, is `GET /country-coverage` and the [coverage page](https://goalise.com/coverage?utm_source=github&utm_medium=referral&utm_campaign=football-api).

**How do I get live scores?**
`GET /matches?live=all` returns every match in progress. Pass competition ids instead of `all` to narrow it. Add `expand=events` for goals and cards.

**Does the price depend on the number of leagues?**
No. Every plan includes every competition and all 46 endpoints. You pay only for the number of requests per day.

**Does it include betting odds, video and news?**
Yes, with the same token: pre-match and live odds, official video highlights and a football news feed.

**Can I use it in a mobile app, a website or a Telegram bot?**
Yes. It is a plain HTTPS and JSON API. Keep the token on your server and do not ship it in client code.

**Is there an older version?**
Yes. v2 is still served for existing integrations. New projects should use v3, which this page describes.

## Related

- [Football Highlights API](https://github.com/goalise/football-highlights-api): official match highlights and goal clips with embed URLs
- [Football News API](https://github.com/goalise/football-news-api): football news by league, team, category and date
- [Football MCP Server](https://goalise.com/football-mcp-server?utm_source=github&utm_medium=referral&utm_campaign=football-api): the same data for AI assistants
- [Getting started guide](https://docs.goalise.com/v3/get-started)

## License

The example code in this repository is released under the MIT License. Use of the API is subject to the [Goalise terms](https://goalise.com/terms).
