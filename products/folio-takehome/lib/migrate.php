<?php

function run_migrations(PDO $pdo): void {
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    ");

    $dir = __DIR__ . '/../migrations';
    $files = glob($dir . '/*.sql') ?: [];
    sort($files);

    foreach ($files as $file) {
        $version = basename($file);
        $check = $pdo->prepare('SELECT 1 FROM schema_migrations WHERE version = ?');
        $check->execute([$version]);
        if ($check->fetch()) {
            continue;
        }

        $sql = file_get_contents($file);
        if ($sql === false || trim($sql) === '') {
            throw new RuntimeException("Empty migration: {$version}");
        }

        $pdo->exec($sql);
        $pdo->prepare('INSERT INTO schema_migrations (version) VALUES (?)')->execute([$version]);
    }
}
