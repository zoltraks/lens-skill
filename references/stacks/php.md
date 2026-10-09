# PHP Baseline

## Purpose

> **Scope:** Checkable constraints for PHP services and libraries
> **Key items:** PSR-4 autoload layout, PSR-12 style, Composer commands, PHPUnit, PHPStan
> ladder, php.ini hardening

This file distills the PHP-FIG standards, PHP security manual, Composer, PHPUnit, PHPStan, and
OWASP PHP sources listed in `references/source-catalog.md` into constraints an audit can verify
from repository source.

Snapshot date: 2026-09-30.

Feeds `assessment/best-practices.md`, `assessment/security-review.md`,
`assessment/dependency-review.md`, `assessment/testing-review.md`, and
`assessment/baseline-conformance.md` for PHP subjects.

## Autoload And Style

From PSR-4 (https://www.php-fig.org/psr/psr-4/) and PSR-12 (https://www.php-fig.org/psr/psr-12/).

- PSR-4 maps a namespace prefix to a base directory in `composer.json` `autoload`. A class
  `Vendor\Package\Sub\Class` must resolve to `<base>/Sub/Class.php` - a source file outside
  its mapped path is unreachable by autoload.
- `autoload-dev` holds test namespaces. Production autoloads must not require dev paths.
- PSR-12 is the extended style floor: `declare(strict_types=1);` conventions aside, it fixes
  brace placement, visibility keywords on all members, `elseif` (not `else if`), one
  statement per line, and the `?>` closing tag omitted from PHP-only files.
- `strict_types` declarations are opt-in per file. Their absence is a type-safety
  observation, not a violation.

## Composer

From https://getcomposer.org/doc/03-cli.md.

- `composer.json`/`composer.lock` pair semantics mirror npm: applications commit both,
  libraries conventionally commit `composer.json` only.
- `composer validate` checks manifest schema. `composer install` honors the lockfile.
  `composer update` rewrites it - the audit distinguishes install-from-lock evidence from
  update evidence.
- `composer audit` reports known vulnerabilities from the FriendsOfPHP advisory database. Its
  output is advisory evidence.
- `require` versus `require-dev` separation is checkable: test frameworks and debug tooling
  in `require` is a dependency-hygiene finding.
- `platform` config pins the PHP version Composer resolves against. A `platform.php` value
  below the deployed runtime masks incompatibility.

## Testing

From https://docs.phpunit.de/.

- PHPUnit is the de-facto harness. `phpunit.xml` configures bootstrap, testsuite directories,
  and coverage. An empty `testsuite` directory list is a zero-test pass.
- Test classes extend `PHPUnit\Framework\TestCase`. Modern versions use attributes
  (`#[Test]`, `#[CoversClass]`) where PHPUnit 10+ doc-comment annotations were removed.
- `assertSame` versus `assertEquals` distinction matters: `==` coercion hides type bugs.
- `vendor/bin/phpunit` is the project-pinned binary. A global `phpunit` in CI drifts from the
  locked version.

## Static Analysis

From https://phpstan.org/user-guide/rule-levels.

- PHPStan levels form a maturity ladder 0-9 (0 = basic unknown-class checks, 5 = argument
  types, 9 = `mixed` strictness). The configured `level` in `phpstan.neon` states the floor.
- Running at level 0-2 is better than none but shallow. The audit records the configured
  level, not the maximum achievable.
- `baseline.neon` files grandfather existing violations. A large baseline converts
  "passes at level N" into "passes at level N with N suppressed findings" - count the
  baseline entries.
- Larastan/Psalm equivalents inherit the same maturity-ladder reading.

## php.ini Hardening

From the PHP security manual (https://www.php.net/manual/en/security.php) and the OWASP PHP
Configuration cheat sheet
(https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html).

- `display_errors = Off` and `log_errors = On` for production. `expose_php = Off` removes the
  version banner.
- `allow_url_fopen`/`allow_url_include` enabled expands SSRF and remote-include surface.
  `allow_url_include` should always be `Off`.
- `open_basedir`, `disable_functions` (`exec`, `shell_exec`, `system`, `passthru` where
  unused), and `post_max_size`/`upload_max_filesize` bounds are the checkable hardening set.
- Session settings: `session.cookie_httponly`, `session.cookie_secure`, `session.use_strict_mode`
  = 1, and `session.cookie_samesite` per deployment.
- File uploads: `file_uploads`, `upload_tmp_dir` outside web root, and MIME/content
  verification rather than extension trust.

## Live Check

When web fetch is available, spot-check one PSR rule against the PHP-FIG text and one
`php.ini` directive against the OWASP cheat sheet.

Record whichever baseline - this snapshot or the live pages - the audit used, and note drift in
Limitations and Unknowns.

The check is best-effort, never blocks the audit, and never executes the audited project.
