// Live football scores in the terminal, refreshed every 30 seconds.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   node live-scores.mjs
//
// Needs Node.js 18+ and nothing else. Stop with Ctrl+C.

const API = "https://api.goalise.com/api/v3";
const REFRESH_SECONDS = 30;

async function liveMatches() {
  const response = await fetch(`${API}/matches?live=all`, {
    headers: {
      Authorization: `Bearer ${process.env.GOALISE_TOKEN ?? ""}`,
      Accept: "application/json",
    },
  });
  const data = await response.json();
  if (data.status !== "success") {
    throw new Error(data.errors.map((error) => error.code).join(", "));
  }
  return { matches: data.response, remaining: response.headers.get("x-rate-limit-remaining") };
}

for (;;) {
  let result;
  try {
    result = await liveMatches();
  } catch (error) {
    console.error("API error:", error.message);
    process.exit(1);
  }

  console.clear();
  console.log(`Live now: ${result.matches.length} matches (${new Date().toLocaleTimeString()})\n`);
  for (const match of result.matches) {
    const minute = match.status.elapsed != null ? `${match.status.elapsed}'` : match.status.short;
    const home = match.home_team?.name ?? "?";
    const away = match.away_team?.name ?? "?";
    console.log(
      `${String(minute).padEnd(4)} ${home.padStart(24)} ${match.score.home}-${match.score.away} ${away.padEnd(24)} ${match.league?.name ?? ""}`
    );
  }
  console.log(`\nrequests left in the current window: ${result.remaining}`);

  await new Promise((resolve) => setTimeout(resolve, REFRESH_SECONDS * 1000));
}
