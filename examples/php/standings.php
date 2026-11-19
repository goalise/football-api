<?php
// Print a league table.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   php standings.php 646 2026        # league_id season, 646 = Serie A
//
// Needs PHP 7.4+ with allow_url_fopen enabled and nothing else.

$leagueId = $argv[1] ?? 646;
$season = $argv[2] ?? date('Y');
$query = http_build_query(['league_id' => $leagueId, 'season' => $season]);

$context = stream_context_create(['http' => [
    'header' => "Authorization: Bearer " . getenv('GOALISE_TOKEN') . "\r\nAccept: application/json",
    'ignore_errors' => true, // read the JSON body of 4xx answers too
    'timeout' => 20,
]]);
$body = file_get_contents("https://api.goalise.com/api/v3/league-standing?$query", false, $context);
$data = json_decode((string) $body, true);

if (($data['status'] ?? null) !== 'success') {
    $codes = array_column($data['errors'] ?? [], 'code');
    fwrite(fopen('php://stderr', 'w'), 'API error: ' . ($codes ? implode(', ', $codes) : 'no answer') . PHP_EOL);
    exit(1);
}

// A league has one group; a cup group stage or a split league has several.
foreach ($data['response'] as $group) {
    if ($group['name']) {
        echo PHP_EOL . $group['name'] . PHP_EOL;
    }
    printf("%3s  %-26s %3s %4s %4s  %s" . PHP_EOL, '#', 'Team', 'P', 'GD', 'Pts', 'Form');
    foreach ($group['standings'] as $row) {
        printf(
            "%3d  %-26s %3s %4s %4s  %s" . PHP_EOL,
            $row['rank'],
            mb_substr($row['team']['name'] ?? '?', 0, 26),
            $row['all']['matches_played'] ?? '-',
            $row['goals_diff'] ?? '-',
            $row['points'] ?? '-',
            $row['form'] ?? ''
        );
    }
}
