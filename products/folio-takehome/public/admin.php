<?php

require __DIR__ . '/../lib/bootstrap.php';
require __DIR__ . '/../lib/layout.php';

$staff = current_staff();
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = trim($_POST['title'] ?? '');
    $body = trim($_POST['body'] ?? '');

    if ($title === '' || $body === '') {
        $error = 'Title and body are required.';
    } else {
        try {
            $publishedAt = normalize_publish_at((string) ($_POST['publish_at'] ?? ''));
        } catch (InvalidArgumentException $e) {
            $error = $e->getMessage();
        }
    }

    if ($error === null && $title !== '' && $body !== '') {
        $stmt = db()->prepare('
            INSERT INTO documents (title, body, created_by, published_at)
            VALUES (?, ?, ?, ?)
        ');
        $stmt->execute([$title, $body, $staff['id'], $publishedAt]);
        $docId = (int) db()->lastInsertId();
        $publicId = assign_public_id($docId, $title);

        audit_log('create', 'document', $docId, [
            'title' => $title,
            'public_id' => $publicId,
            'published_at' => $publishedAt,
        ]);
        if (parse_published_at($publishedAt) > now_utc()) {
            audit_log('schedule', 'document', $docId, ['published_at' => $publishedAt]);
        }

        header('Location: /admin.php?created=' . urlencode($publicId));
        exit;
    }
}

$search = trim($_GET['q'] ?? '');
if ($search !== '') {
    audit_log('search', 'document', 0, ['query' => $search]);
    $stmt = db()->prepare('
        SELECT d.*, s.name AS creator_name
        FROM documents d
        JOIN staff s ON s.id = d.created_by
        WHERE d.title LIKE ? ESCAPE \'\\\'
        ORDER BY d.created_at DESC
    ');
    $stmt->execute([str_replace(['\\', '%', '_'], ['\\\\', '\\%', '\\_'], $search) . '%']);
    $docs = $stmt->fetchAll();
} else {
    $docs = db()->query('
        SELECT d.*, s.name AS creator_name
        FROM documents d
        JOIN staff s ON s.id = d.created_by
        ORDER BY d.created_at DESC
    ')->fetchAll();
}

render_header('Admin', $staff);
?>

<h1 class="page-title">Admin</h1>
<p class="page-subtitle">Create documents and generate share links for recipients.</p>

<div class="banner banner-warn">Customer agent running from customer-test</div>

<?php if (!empty($_GET['created'])): ?>
    <div class="banner banner-success">Document <code><?= h((string) $_GET['created']) ?></code> created.</div>
<?php endif ?>

<?php if ($error): ?>
    <div class="banner banner-error"><?= h($error) ?></div>
<?php endif ?>

<section class="card">
    <h2 class="card-title">New document</h2>
    <form method="post">
        <div class="form-field">
            <label for="title">Title</label>
            <input type="text" id="title" name="title" required>
        </div>
        <div class="form-field">
            <label for="body">Body</label>
            <textarea id="body" name="body" required></textarea>
        </div>
        <div class="form-field">
            <label for="publish_at">Publish at (optional, Central Time)</label>
            <input type="datetime-local" id="publish_at" name="publish_at">
            <p class="field-hint">Times are interpreted as US Central (America/Chicago). Leave blank to publish immediately.</p>
        </div>
        <button type="submit" class="btn">Create document</button>
    </form>
</section>

<section class="card">
    <h2 class="card-title">Documents</h2>
    <form method="get" class="search-form">
        <div class="form-field">
            <label for="q">Search by title</label>
            <input type="search" id="q" name="q" value="<?= h($search) ?>" placeholder="Start typing a title…">
        </div>
        <button type="submit" class="btn">Search</button>
        <?php if ($search !== ''): ?>
            <a href="/admin.php" class="btn-link">Clear</a>
        <?php endif ?>
    </form>
    <?php if (empty($docs)): ?>
        <p class="empty"><?= $search !== '' ? 'No documents match that title prefix.' : 'No documents yet.' ?></p>
    <?php else: ?>
        <table class="data">
            <thead>
                <tr>
                    <th>Public ID</th>
                    <th>Title</th>
                    <th>Creator</th>
                    <th>Created</th>
                    <th>Publish at</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($docs as $d): ?>
                    <tr>
                        <td class="id"><code><?= h($d['public_id'] ?? ('#' . (int) $d['id'])) ?></code></td>
                        <td><?= h($d['title']) ?></td>
                        <td><?= h($d['creator_name']) ?></td>
                        <td><?= h($d['created_at']) ?></td>
                        <td><?= $d['published_at'] !== null && $d['published_at'] !== ''
                            ? h(format_published_at_for_ui($d['published_at']))
                            : '—' ?></td>
                        <td><a href="/share.php?doc=<?= (int) $d['id'] ?>" class="btn-link">Create share →</a></td>
                    </tr>
                <?php endforeach ?>
            </tbody>
        </table>
    <?php endif ?>
</section>

<?php render_footer(); ?>
