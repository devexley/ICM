<?php

require __DIR__ . '/../lib/bootstrap.php';

system('php ' . escapeshellarg(__DIR__ . '/../seed.php') . ' > /dev/null', $rc);
if ($rc !== 0) {
    fwrite(STDERR, "seed failed\n");
    exit(1);
}

$pass = 0;
$fail = 0;

function test(string $name, callable $fn): void {
    global $pass, $fail;
    try {
        $fn();
        echo "  [ok] {$name}\n";
        $pass++;
    } catch (Throwable $e) {
        echo "  [FAIL] {$name}: " . $e->getMessage() . "\n";
        $fail++;
    }
}

function assert_true($cond, string $msg = ''): void {
    if (!$cond) {
        throw new RuntimeException($msg !== '' ? $msg : 'expected true');
    }
}

echo "\nRunning tests:\n";

test('feature columns exist via migrations and not in baseline schema.sql', function () {
    $schema = file_get_contents(__DIR__ . '/../schema.sql');
    assert_true(stripos($schema, 'public_id') === false, 'public_id must not be in schema.sql');
    assert_true(stripos($schema, 'published_at') === false, 'published_at must not be in schema.sql');

    $cols = db()->query('PRAGMA table_info(documents)')->fetchAll();
    $names = array_column($cols, 'name');
    assert_true(in_array('public_id', $names, true), 'public_id column missing after migrations');
    assert_true(in_array('published_at', $names, true), 'published_at column missing after migrations');

    $m = db()->query('SELECT COUNT(*) AS n FROM schema_migrations')->fetch();
    assert_true((int) $m['n'] >= 2, 'expected at least two applied migrations');
});

test('seeded share link resolves to the seeded document', function () {
    $stmt = db()->prepare('
        SELECT d.title
        FROM shares s
        JOIN documents d ON d.id = s.document_id
        LIMIT 1
    ');
    $stmt->execute();
    $row = $stmt->fetch();
    assert_true($row !== false, 'expected the seeded share to resolve');
    assert_true($row['title'] === 'Welcome Packet', 'unexpected title: ' . var_export($row['title'], true));
});

test('normalize_publish_at stores UTC from Central datetime-local input', function () {
    $central = new DateTimeImmutable('2026-06-15 14:30:00', app_timezone());
    $input = $central->format('Y-m-d\TH:i');
    $stored = normalize_publish_at($input);
    $expected = $central->setTimezone(utc_timezone())->format('Y-m-d H:i:s');
    assert_true($stored === $expected, "expected UTC {$expected}, got {$stored}");
});

test('document is hidden before published_at', function () {
    $publicId = generate_public_id('Scheduled Future');
    $future = now_utc()->modify('+1 day')->format('Y-m-d H:i:s');
    $stmt = db()->prepare('
        INSERT INTO documents (title, body, created_by, public_id, published_at)
        VALUES (?, ?, 1, ?, ?)
    ');
    $stmt->execute(['Scheduled Future', 'Body', $publicId, $future]);
    $fetch = db()->prepare('SELECT * FROM documents WHERE public_id = ?');
    $fetch->execute([$publicId]);
    $doc = $fetch->fetch();
    assert_true($doc !== false, 'expected inserted document');
    assert_true(!document_is_visible($doc), 'future published_at should not be visible');
});

test('document becomes visible once published_at passes (UTC in DB)', function () {
    $publicId = generate_public_id('Scheduled Past');
    $past = now_utc()->modify('-1 minute')->format('Y-m-d H:i:s');
    $stmt = db()->prepare('
        INSERT INTO documents (title, body, created_by, public_id, published_at)
        VALUES (?, ?, 1, ?, ?)
    ');
    $stmt->execute(['Scheduled Past', 'Body', $publicId, $past]);
    $fetch = db()->prepare('SELECT * FROM documents WHERE public_id = ?');
    $fetch->execute([$publicId]);
    $doc = $fetch->fetch();
    assert_true(document_is_visible($doc), 'past published_at should be visible');
});

test('title prefix search finds matching documents', function () {
    $stmt = db()->prepare('SELECT COUNT(*) AS n FROM documents WHERE title LIKE ?');
    $stmt->execute(['Welcome%']);
    $row = $stmt->fetch();
    assert_true((int) $row['n'] >= 1, 'expected Welcome Packet to match prefix search');
});

test('documents have unique human-readable public_id values', function () {
    $stmt = db()->query('SELECT public_id FROM documents');
    $ids = array_column($stmt->fetchAll(), 'public_id');
    assert_true(count($ids) >= 1, 'expected at least one document');
    foreach ($ids as $id) {
        assert_true($id !== null && $id !== '', 'public_id must be set');
        assert_true(
            (bool) preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*-[a-z0-9]{4}$/', $id),
            'unexpected public_id shape: ' . $id
        );
    }
    assert_true(count($ids) === count(array_unique($ids)), 'public_id values must be unique');
});

echo "\n{$pass} passed, {$fail} failed.\n";
exit($fail > 0 ? 1 : 0);
