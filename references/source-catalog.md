# Authoritative Source Catalog

## Purpose

> **Scope:** Registry of the authoritative external sources Lens relies on, each mapped to the
> local corpus file that consolidates it
> **Key items:** canonical addresses, publishers, consuming reference files, consolidation status

This catalog is the single registry mapping each live source to its bundled static digest.

When an audit cannot fetch a source, the catalog points at the corpus file that already
consolidated it, so every reference resolves statically offline.

Each corpus file records its own snapshot date. This catalog tracks the consolidation state of
the mapping rather than the snapshot content.

Statuses: `pending` (registered, not yet consolidated), `distilled` (consolidated into the
named file), `paywalled` (public summary only), `restricted` (license limits reproduction to
identifiers and names), `alternate` (fallback address for the row above).

## Contents

| Section                            | Line | What it covers                                   |
|------------------------------------|------|--------------------------------------------------|
| Sources                            | 30   | Source registry grouped by consuming corpus file |
| Session-Derived Files              | 497  | Corpus files built from session knowledge        |
| Unresolved And Alternate Addresses | 508  | Fetch failures and working alternates            |
| Maintenance                        | 528  | Row-addition and canonicalization rules          |

## Sources

### references/stacks/nodejs.md

| Source                            | Publisher                  | URL                                                                             | Status    |
|-----------------------------------|----------------------------|---------------------------------------------------------------------------------|-----------|
| Node.js security best practices   | OpenJS Foundation          | https://nodejs.org/en/learn/getting-started/security-best-practices             | distilled |
| Node.js API documentation         | OpenJS Foundation          | https://nodejs.org/api/                                                         | distilled |
| crypto API                        | OpenJS Foundation          | https://nodejs.org/api/crypto.html                                              | distilled |
| Test runner                       | OpenJS Foundation          | https://nodejs.org/api/test.html                                                | distilled |
| https API                         | OpenJS Foundation          | https://nodejs.org/api/https.html                                               | distilled |
| Previous releases                 | OpenJS Foundation          | https://nodejs.org/en/about/previous-releases                                   | distilled |
| Node release data                 | endoflife.date             | https://endoflife.date/api/node.json                                            | distilled |
| Express security best practice    | Express.js project         | https://expressjs.com/en/advanced/best-practice-security.html                   | distilled |
| Express error handling            | Express.js project         | https://expressjs.com/en/guide/error-handling.html                              | distilled |
| Migrating to Express 5            | Express.js project         | https://expressjs.com/en/guide/migrating-5.html                                 | distilled |
| Express 5 API                     | Express.js project         | https://expressjs.com/en/5x/api.html                                            | distilled |
| npm package.json reference        | npm                        | https://docs.npmjs.com/cli/v11/configuring-npm/package-json                     | distilled |
| npm package-lock reference        | npm                        | https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json                | distilled |
| npm ci                            | npm                        | https://docs.npmjs.com/cli/v11/commands/npm-ci                                  | distilled |
| npm audit                         | npm                        | https://docs.npmjs.com/cli/v11/commands/npm-audit                               | distilled |
| npm provenance                    | npm                        | https://docs.npmjs.com/generating-provenance-statements                         | distilled |
| eslint-plugin-security            | ESLint community           | https://github.com/eslint-community/eslint-plugin-security                      | distilled |
| eslint-plugin-n                   | ESLint community           | https://github.com/eslint-community/eslint-plugin-n                             | distilled |
| ESLint core rules                 | ESLint project             | https://eslint.org/docs/latest/rules/                                           | distilled |
| node-jsonwebtoken                 | Auth0                      | https://github.com/auth0/node-jsonwebtoken                                      | distilled |
| helmet                            | helmet maintainers         | https://helmetjs.github.io/                                                     | distilled |
| express-rate-limit                | express-rate-limit project | https://github.com/express-rate-limit/express-rate-limit                        | distilled |
| supertest                         | Forward Email              | https://github.com/forwardemail/supertest                                       | distilled |
| Command Line Interface Guidelines | clig.dev                   | https://clig.dev/                                                               | distilled |
| publint                           | publint project            | https://publint.dev/                                                            | distilled |
| arethetypeswrong                  | arethetypeswrong project   | https://arethetypeswrong.github.io/                                             | distilled |
| Fastify server reference          | Fastify project            | https://fastify.dev/docs/latest/Reference/Server/                               | distilled |
| Fastify repository                | Fastify project            | https://github.com/fastify/fastify                                              | alternate |
| Node.js security cheat sheet      | OWASP                      | https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html | distilled |

### references/stacks/typescript.md

| Source                     | Publisher                 | URL                                                     | Status    |
|----------------------------|---------------------------|---------------------------------------------------------|-----------|
| TypeScript Handbook        | Microsoft                 | https://www.typescriptlang.org/docs/handbook/intro.html | distilled |
| TSConfig reference         | Microsoft                 | https://www.typescriptlang.org/tsconfig                 | distilled |
| typescript-eslint rules    | typescript-eslint project | https://typescript-eslint.io/rules/                     | distilled |
| Vitest coverage config     | Vitest project            | https://vitest.dev/config/#coverage                     | distilled |
| Vitest guide               | Vitest project            | https://vitest.dev/guide/#configuring-vitest            | distilled |
| Playwright best practices  | Microsoft                 | https://playwright.dev/docs/best-practices              | distilled |
| Testing Library principles | Testing Library           | https://testing-library.com/docs/guiding-principles     | distilled |
| Vite build options         | Vite project              | https://vite.dev/config/build-options                   | distilled |
| Vite guide                 | Vite project              | https://vite.dev/guide/                                 | distilled |
| Zustand documentation      | Poimandres                | https://zustand.docs.pmnd.rs/                           | distilled |
| Jest configuration         | Meta/OpenJS               | https://jestjs.io/docs/configuration                    | distilled |
| zod                        | zod project               | https://zod.dev/                                        | distilled |
| valibot                    | valibot project           | https://valibot.dev/                                    | distilled |

### references/stacks/python.md

| Source                        | Publisher                  | URL                                                        | Status    |
|-------------------------------|----------------------------|------------------------------------------------------------|-----------|
| What's New index              | Python Software Foundation | https://docs.python.org/3/whatsnew/index.html              | distilled |
| Release cycle and versions    | Python devguide            | https://devguide.python.org/versions/                      | distilled |
| PEP 585 builtin generics      | Python Software Foundation | https://peps.python.org/pep-0585/                          | distilled |
| PEP 563 postponed annotations | Python Software Foundation | https://peps.python.org/pep-0563/                          | distilled |
| PEP 604 union syntax          | Python Software Foundation | https://peps.python.org/pep-0604/                          | distilled |
| PEP 8 style guide             | Python Software Foundation | https://peps.python.org/pep-0008/                          | distilled |
| PyPA packaging guide          | PyPA                       | https://packaging.python.org/en/latest/                    | distilled |
| unittest documentation        | Python Software Foundation | https://docs.python.org/3/library/unittest.html            | distilled |
| pytest documentation          | pytest project             | https://docs.pytest.org/en/stable/                         | distilled |
| Bandit plugin list            | Bandit project             | https://bandit.readthedocs.io/en/latest/plugins/index.html | distilled |

### references/stacks/php.md

| Source                        | Publisher        | URL                                                                               | Status    |
|-------------------------------|------------------|-----------------------------------------------------------------------------------|-----------|
| PSR-4 autoloader              | PHP-FIG          | https://www.php-fig.org/psr/psr-4/                                                | distilled |
| PSR-12 coding style           | PHP-FIG          | https://www.php-fig.org/psr/psr-12/                                               | distilled |
| PHP security manual           | PHP project      | https://www.php.net/manual/en/security.php                                        | distilled |
| Composer CLI reference        | Composer project | https://getcomposer.org/doc/03-cli.md                                             | distilled |
| PHPUnit documentation         | PHPUnit project  | https://docs.phpunit.de/                                                          | distilled |
| PHPStan rule levels           | PHPStan project  | https://phpstan.org/user-guide/rule-levels                                        | distilled |
| PHP configuration cheat sheet | OWASP            | https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html | distilled |

### references/stacks/go.md

| Source                     | Publisher        | URL                                                  | Status    |
|----------------------------|------------------|------------------------------------------------------|-----------|
| Effective Go               | Go project       | https://go.dev/doc/effective_go                      | distilled |
| Code Review Comments       | Go project       | https://go.dev/wiki/CodeReviewComments               | distilled |
| Module version numbering   | Go project       | https://go.dev/doc/modules/version-numbers           | distilled |
| Managing dependencies      | Go project       | https://go.dev/doc/modules/managing-dependencies     | distilled |
| Module reference           | Go project       | https://go.dev/ref/mod                               | distilled |
| Go security policy         | Go project       | https://go.dev/doc/security/                         | distilled |
| Go vulnerability database  | Go project       | https://pkg.go.dev/vuln/                             | distilled |
| govulncheck                | Go project       | https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck | distilled |
| crypto/subtle              | Go project       | https://pkg.go.dev/crypto/subtle                     | distilled |
| Go Secure Coding Practices | OWASP            | https://github.com/OWASP/Go-SCP                      | distilled |
| gosec                      | securego         | https://github.com/securego/gosec                    | distilled |
| Cobra                      | spf13            | https://github.com/spf13/cobra                       | distilled |
| x/crypto/ssh               | Go project       | https://pkg.go.dev/golang.org/x/crypto/ssh           | distilled |
| Go project layout          | golang-standards | https://github.com/golang-standards/project-layout   | distilled |
| go-keyring                 | Zalando          | https://github.com/zalando/go-keyring                | distilled |

### references/stacks/java-spring.md

| Source                               | Publisher           | URL                                                                                                 | Status    |
|--------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------|-----------|
| Authorize HTTP requests              | Spring project      | https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html | distilled |
| Spring Boot SSL                      | Spring project      | https://docs.spring.io/spring-boot/reference/features/ssl.html                                      | distilled |
| Password storage                     | Spring project      | https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html      | distilled |
| Micrometer Prometheus                | Micrometer project  | https://micrometer.io/docs/registry/prometheus                                                      | alternate |
| maven-lockfile                       | chains-project      | https://github.com/chains-project/maven-lockfile                                                    | distilled |
| Gradle dependency verification       | Gradle              | https://docs.gradle.org/current/userguide/dependency_verification.html                              | distilled |
| Secure Coding Guidelines for Java SE | Oracle              | https://www.oracle.com/java/technologies/javase/seccodeguide.html                                   | distilled |
| FindSecBugs patterns                 | FindSecBugs project | https://find-sec-bugs.github.io/bugs.htm                                                            | distilled |
| japicmp                              | japicmp project     | https://github.com/siom79/japicmp                                                                   | distilled |
| Revapi                               | Revapi project      | https://revapi.org/                                                                                 | distilled |
| Kotlin coding conventions            | JetBrains           | https://kotlinlang.org/docs/coding-conventions.html                                                 | distilled |
| Jakarta Persistence                  | Eclipse             | https://jakarta.ee/specifications/persistence/                                                      | distilled |
| Spring transaction reference         | Spring project      | https://docs.spring.io/spring-framework/reference/data-access/transaction.html                      | distilled |

### references/stacks/dotnet-aspnet.md

| Source                           | Publisher | URL                                                                                                         | Status    |
|----------------------------------|-----------|-------------------------------------------------------------------------------------------------------------|-----------|
| Framework Design Guidelines      | Microsoft | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/                                        | distilled |
| Security analysis rules          | Microsoft | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/security-warnings         | distilled |
| Breaking-change rules            | Microsoft | https://learn.microsoft.com/en-us/dotnet/core/compatibility/                                                | distilled |
| Enforcing SSL                    | Microsoft | https://learn.microsoft.com/aspnet/core/security/enforcing-ssl                                              | distilled |
| Authentication and authorization | Microsoft | https://learn.microsoft.com/aspnet/core/security/authentication/                                            | distilled |
| Rate limiting middleware         | Microsoft | https://learn.microsoft.com/aspnet/core/performance/rate-limit                                              | distilled |
| Package references and locking   | Microsoft | https://learn.microsoft.com/nuget/consume-packages/package-references-in-project-files                      | distilled |
| FixedTimeEquals                  | Microsoft | https://learn.microsoft.com/dotnet/api/system.security.cryptography.cryptographicoperations.fixedtimeequals | distilled |
| MSBuild project SDK properties   | Microsoft | https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props                                     | distilled |
| Code analysis overview           | Microsoft | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview                                | distilled |

### references/stacks/rust.md

| Source              | Publisher     | URL                                                   | Status    |
|---------------------|---------------|-------------------------------------------------------|-----------|
| Rust API Guidelines | Rust project  | https://rust-lang.github.io/api-guidelines/           | distilled |
| Clippy lint list    | Rust project  | https://rust-lang.github.io/rust-clippy/master/       | distilled |
| RustSec advisories  | RustSec       | https://rustsec.org/                                  | distilled |
| Cargo SemVer rules  | Rust project  | https://doc.rust-lang.org/cargo/reference/semver.html | distilled |
| Tokio tutorial      | Tokio project | https://tokio.rs/tokio/tutorial                       | distilled |

### references/stacks/c-cpp.md

| Source                   | Publisher | URL                                                                       | Status    |
|--------------------------|-----------|---------------------------------------------------------------------------|-----------|
| C++ Core Guidelines      | isocpp    | https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines              | distilled |
| CERT C++ Coding Standard | SEI       | https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682 | distilled |
| CERT C Coding Standard   | SEI       | https://wiki.sei.cmu.edu/confluence/display/c                             | alternate |

### references/stacks/shell.md

| Source                   | Publisher          | URL                                                 | Status    |
|--------------------------|--------------------|-----------------------------------------------------|-----------|
| ShellCheck wiki          | ShellCheck project | https://www.shellcheck.net/wiki/                    | distilled |
| Google Shell Style Guide | Google             | https://google.github.io/styleguide/shellguide.html | distilled |
| PSScriptAnalyzer         | Microsoft          | https://github.com/PowerShell/PSScriptAnalyzer      | distilled |

### references/stacks/web.md

| Source                      | Publisher | URL                                                              | Status    |
|-----------------------------|-----------|------------------------------------------------------------------|-----------|
| WHATWG HTML Living Standard | WHATWG    | https://html.spec.whatwg.org/multipage/                          | distilled |
| WHATWG DOM Standard         | WHATWG    | https://dom.spec.whatwg.org/                                     | distilled |
| ECMA-262 mirror             | TC39      | https://tc39.es/ecma262/                                         | distilled |
| MDN JavaScript              | MDN       | https://developer.mozilla.org/en-US/docs/Web/JavaScript          | distilled |
| MDN CSS                     | MDN       | https://developer.mozilla.org/en-US/docs/Web/CSS                 | distilled |
| MDN Web Storage             | MDN       | https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API | distilled |
| MDN Web Audio               | MDN       | https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API   | distilled |
| MDN Web MIDI                | MDN       | https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API    | distilled |
| MDN Web Security            | MDN       | https://developer.mozilla.org/en-US/docs/Web/Security            | distilled |

### references/stacks/spa.md

| Source                       | Publisher     | URL                                                                 | Status    |
|------------------------------|---------------|---------------------------------------------------------------------|-----------|
| React documentation          | React project | https://react.dev/                                                  | distilled |
| Rules of Hooks               | React project | https://react.dev/reference/rules/rules-of-hooks                    | distilled |
| You Might Not Need an Effect | React project | https://react.dev/learn/you-might-not-need-an-effect                | distilled |
| MDN Service Worker API       | MDN           | https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API | distilled |

### references/stacks/electron-desktop.md

| Source                        | Publisher        | URL                                                               | Status    |
|-------------------------------|------------------|-------------------------------------------------------------------|-----------|
| Electron security checklist   | Electron project | https://www.electronjs.org/docs/latest/tutorial/security          | distilled |
| Electron IPC guide            | Electron project | https://www.electronjs.org/docs/latest/tutorial/ipc               | distilled |
| Context isolation             | Electron project | https://www.electronjs.org/docs/latest/tutorial/context-isolation | distilled |
| Process model                 | Electron project | https://www.electronjs.org/docs/latest/tutorial/process-model     | distilled |
| electron-builder code signing | electron-builder | https://www.electron.build/docs/features/code-signing/            | distilled |

### references/stacks/docker.md

| Source                      | Publisher           | URL                                                                             | Status    |
|-----------------------------|---------------------|---------------------------------------------------------------------------------|-----------|
| docker-node best practices  | docker-node project | https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md           | distilled |
| Dockerfile best practices   | Docker Inc.         | https://docs.docker.com/build/building/best-practices/                          | distilled |
| Docker security cheat sheet | OWASP               | https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html | distilled |
| Compose file reference      | Docker Inc.         | https://docs.docker.com/compose/compose-file/                                   | distilled |

### references/stacks/github-actions.md

| Source                     | Publisher | URL                                                                                                                  | Status    |
|----------------------------|-----------|----------------------------------------------------------------------------------------------------------------------|-----------|
| Actions security hardening | GitHub    | https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions | distilled |
| Workflow syntax            | GitHub    | https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax                                   | distilled |

### references/stacks/openapi-rest.md

| Source                       | Publisher          | URL                                                                           | Status    |
|------------------------------|--------------------|-------------------------------------------------------------------------------|-----------|
| OpenAPI Specification 3.1    | OpenAPI Initiative | https://spec.openapis.org/oas/v3.1                                            | distilled |
| OAI specification repository | OpenAPI Initiative | https://github.com/OAI/OpenAPI-Specification                                  | alternate |
| Spectral documentation       | Stoplight          | https://docs.stoplight.io/docs/spectral/                                      | alternate |
| REST security cheat sheet    | OWASP              | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | distilled |
| RFC 9457 problem details     | IETF               | https://datatracker.ietf.org/doc/html/rfc9457                                 | distilled |

### references/stacks/delphi.md

| Source                    | Publisher   | URL                                           | Status     |
|---------------------------|-------------|-----------------------------------------------|------------|
| Object Pascal Style Guide | Embarcadero | https://edn.embarcadero.com/article/10280     | distilled  |
| RAD Studio DocWiki        | Embarcadero | https://docwiki.embarcadero.com/RADStudio/en/ | restricted |

### references/stacks/zig.md

| Source            | Publisher               | URL                                       | Status    |
|-------------------|-------------------------|-------------------------------------------|-----------|
| Zig documentation | Zig Software Foundation | https://ziglang.org/documentation/master/ | distilled |

### references/methodology/owasp-baselines.md

| Source                      | Publisher | URL                                                                              | Status    |
|-----------------------------|-----------|----------------------------------------------------------------------------------|-----------|
| OWASP Top 10                | OWASP     | https://owasp.org/www-project-top-ten/                                           | distilled |
| OWASP ASVS                  | OWASP     | https://owasp.org/www-project-application-security-verification-standard/        | distilled |
| OWASP API Security project  | OWASP     | https://owasp.org/API-Security/                                                  | distilled |
| OWASP API Top 10 2023       | OWASP     | https://owasp.org/API-Security/editions/2023/en/0x11-t10/                        | distilled |
| OWASP LLM Top 10            | OWASP     | https://genai.owasp.org/llm-top-10/                                              | distilled |
| LLM Top 10 project portal   | OWASP     | https://owasp.org/www-project-top-10-for-large-language-model-applications/      | alternate |
| OWASP Agentic Skills Top 10 | OWASP     | https://owasp.org/www-project-agentic-skills-top-10/                             | distilled |
| Agentic Applications 2026   | OWASP     | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | distilled |
| Cheat Sheet Series index    | OWASP     | https://cheatsheetseries.owasp.org/                                              | distilled |
| OWASP SAMM                  | OWASP     | https://owaspsamm.org/                                                           | distilled |
| OWASP Secure Headers        | OWASP     | https://owasp.org/www-project-secure-headers/                                    | distilled |

### references/methodology/risk-modeling.md

| Source                    | Publisher | URL                                                                                   | Status    |
|---------------------------|-----------|---------------------------------------------------------------------------------------|-----------|
| NIST SP 800-30 Rev 1      | NIST      | https://csrc.nist.gov/pubs/sp/800/30/r1/final                                         | distilled |
| NIST SP 800-37 Rev 2      | NIST      | https://csrc.nist.gov/pubs/sp/800/37/r2/final                                         | distilled |
| NIST RMF overview         | NIST      | https://csrc.nist.gov/Projects/risk-management/about-rmf                              | distilled |
| STRIDE threat categories  | Microsoft | https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats | distilled |
| Threat modeling overview  | OWASP     | https://owasp.org/www-community/Threat_Modeling                                       | distilled |
| Threat modeling assurance | Microsoft | https://learn.microsoft.com/en-us/compliance/assurance/assurance-threat-modeling      | alternate |
| CVSS v4 specification     | FIRST     | https://www.first.org/cvss/v4-0/specification-document                                | distilled |
| CVSS v4 user guide        | FIRST     | https://www.first.org/cvss/v4.0/user-guide                                            | distilled |
| CWE Top 25                | MITRE     | https://cwe.mitre.org/top25/                                                          | distilled |
| CWE Top 25 2024 archive   | MITRE     | https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html                          | distilled |
| CWE home                  | MITRE     | https://cwe.mitre.org/                                                                | distilled |
| CWE-494                   | MITRE     | https://cwe.mitre.org/data/definitions/494.html                                       | distilled |

### references/methodology/quality-models.md

| Source                       | Publisher        | URL                                                                        | Status     |
|------------------------------|------------------|----------------------------------------------------------------------------|------------|
| ISO/IEC 25010 portal         | ISO 25000 portal | https://iso25000.com/index.php/en/iso-25000-standards/iso-25010            | distilled  |
| ISO/IEC 25010 standard page  | ISO              | https://www.iso.org/standard/78176.html                                    | paywalled  |
| ISO 19011 page               | ISO              | https://www.iso.org/standard/70017.html                                    | paywalled  |
| CISQ                         | CISQ             | https://www.it-cisq.org/                                                   | distilled  |
| CISQ code-quality standards  | CISQ             | https://www.it-cisq.org/standards/code-quality-standards/                  | distilled  |
| SQALE site                   | SQALE            | http://www.sqale.org/                                                      | distilled  |
| SQALE method article         | Cutter           | https://www.cutter.com/article/managing-technical-debt-sqale-method-490726 | restricted |
| Practical test pyramid       | Martin Fowler    | https://martinfowler.com/articles/practical-test-pyramid.html              | distilled  |
| Google engineering practices | Google           | https://google.github.io/eng-practices/                                    | distilled  |

### references/methodology/delivery-metrics.md

| Source                       | Publisher         | URL                                                   | Status    |
|------------------------------|-------------------|-------------------------------------------------------|-----------|
| DORA                         | Google Cloud DORA | https://dora.dev/                                     | distilled |
| DORA capabilities            | Google Cloud DORA | https://dora.dev/capabilities/                        | distilled |
| DORA four keys guide         | Google Cloud DORA | https://dora.dev/guides/dora-metrics-four-keys/       | distilled |
| SRE service-level objectives | Google SRE        | https://sre.google/sre-book/service-level-objectives/ | distilled |
| NIST SSDF SP 800-218         | NIST              | https://csrc.nist.gov/pubs/sp/800/218/final           | distilled |

### references/methodology/supply-chain.md

| Source                   | Publisher   | URL                                                        | Status    |
|--------------------------|-------------|------------------------------------------------------------|-----------|
| SLSA specification       | SLSA        | https://slsa.dev/spec/v1.2/                                | distilled |
| OpenSSF Scorecard checks | OpenSSF     | https://github.com/ossf/scorecard/blob/main/docs/checks.md | distilled |
| Scorecard repository     | OpenSSF     | https://github.com/ossf/scorecard                          | distilled |
| GitHub Advisory Database | GitHub      | https://github.com/advisories                              | distilled |
| OSV                      | OSV project | https://osv.dev/                                           | distilled |
| OSV schema docs          | OSV project | https://osv.dev/docs/                                      | distilled |

### references/methodology/versioning-release.md

| Source                  | Publisher               | URL                                              | Status    |
|-------------------------|-------------------------|--------------------------------------------------|-----------|
| Semantic Versioning     | semver.org              | https://semver.org/spec/v2.0.0.html              | distilled |
| Keep a Changelog        | keepachangelog.com      | https://keepachangelog.com/en/1.1.0/             | distilled |
| Conventional Commits    | conventionalcommits.org | https://www.conventionalcommits.org/en/v1.0.0/   | distilled |
| npm semantic versioning | npm                     | https://docs.npmjs.com/about-semantic-versioning | distilled |
| securitytxt             | securitytxt.org         | https://securitytxt.org/                         | distilled |

### references/methodology/sbom-licensing.md

| Source                          | Publisher              | URL                                                                                               | Status    |
|---------------------------------|------------------------|---------------------------------------------------------------------------------------------------|-----------|
| CISA 2026 SBOM minimum elements | CISA                   | https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom | distilled |
| CISA SBOM minimum requirements  | CISA                   | https://www.cisa.gov/resources-tools/resources/minimum-requirements-software-bill-materials-sbom  | alternate |
| SPDX License List               | SPDX                   | https://spdx.org/licenses/                                                                        | distilled |
| SPDX specification              | SPDX                   | https://spdx.github.io/spdx-spec/v2.3/                                                            | distilled |
| CycloneDX overview              | CycloneDX              | https://cyclonedx.org/specification/overview/                                                     | distilled |
| ECMA-424 CycloneDX              | Ecma TC54              | https://ecma-tc54.github.io/ECMA-424/                                                             | distilled |
| REUSE specification             | FSFE                   | https://reuse.software/spec/                                                                      | distilled |
| OSI license list                | Open Source Initiative | https://opensource.org/licenses                                                                   | distilled |

### references/methodology/crypto-auth.md

| Source                       | Publisher    | URL                                                                                      | Status    |
|------------------------------|--------------|------------------------------------------------------------------------------------------|-----------|
| Password Storage cheat sheet | OWASP        | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html         | distilled |
| TLS cheat sheet              | OWASP        | https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | distilled |
| RFC 7519 JWT                 | IETF         | https://datatracker.ietf.org/doc/html/rfc7519                                            | distilled |
| RFC 8725 JWT BCP             | IETF         | https://datatracker.ietf.org/doc/html/rfc8725                                            | distilled |
| RFC 6749 OAuth 2.0           | IETF         | https://www.rfc-editor.org/rfc/rfc6749                                                   | distilled |
| RFC 6750 Bearer tokens       | IETF         | https://www.rfc-editor.org/rfc/rfc6750                                                   | distilled |
| Authentication cheat sheet   | OWASP        | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html           | distilled |
| JWT cheat sheet              | OWASP        | https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html  | alternate |
| 12-factor config             | 12factor.net | https://12factor.net/config                                                              | distilled |
| Logging cheat sheet          | OWASP        | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html                  | distilled |

### references/topics/accessibility-baseline.md

| Source                   | Publisher | URL                                                        | Status    |
|--------------------------|-----------|------------------------------------------------------------|-----------|
| WCAG 2.2                 | W3C       | https://www.w3.org/TR/WCAG22/                              | distilled |
| WCAG overview            | W3C WAI   | https://www.w3.org/WAI/standards-guidelines/wcag/          | distilled |
| ARIA Authoring Practices | W3C WAI   | https://www.w3.org/WAI/ARIA/apg/                           | distilled |
| MDN accessibility        | MDN       | https://developer.mozilla.org/en-US/docs/Web/Accessibility | distilled |

### references/topics/frontend-security.md

| Source                       | Publisher | URL                                                                                             | Status    |
|------------------------------|-----------|-------------------------------------------------------------------------------------------------|-----------|
| DOM XSS cheat sheet          | OWASP     | https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html        | distilled |
| XSS prevention cheat sheet   | OWASP     | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | distilled |
| CSP cheat sheet              | OWASP     | https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html         | distilled |
| Web frontend cheat sheet     | OWASP     | https://cheatsheetseries.owasp.org/cheatsheets/Web_Frontend_Security_Cheat_Sheet.html           | distilled |
| MDN CSP guide                | MDN       | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP                                    | distilled |
| MDN Permissions-Policy       | MDN       | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy          | distilled |
| eslint-plugin-no-unsanitized | Mozilla   | https://github.com/mozilla/eslint-plugin-no-unsanitized                                         | distilled |

### references/topics/offline-cache.md

| Source                   | Publisher | URL                                                                                       | Status    |
|--------------------------|-----------|-------------------------------------------------------------------------------------------|-----------|
| Service worker lifecycle | web.dev   | https://web.dev/articles/service-worker-lifecycle                                         | distilled |
| Caching and HTTP caching | web.dev   | https://web.dev/articles/service-worker-caching-and-http-caching                          | distilled |
| Offline cookbook         | web.dev   | https://web.dev/articles/offline-cookbook                                                 | distilled |
| Using Service Workers    | MDN       | https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers | distilled |

### references/topics/project-health.md

| Source                          | Publisher | URL                                                                                                  | Status    |
|---------------------------------|-----------|------------------------------------------------------------------------------------------------------|-----------|
| OpenSSF Best Practices criteria | OpenSSF   | https://www.bestpractices.dev/en/criteria                                                            | distilled |
| GitHub community health         | GitHub    | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions             | distilled |
| GitHub security policy          | GitHub    | https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository | distilled |
| GitHub gitignore templates      | GitHub    | https://github.com/github/gitignore                                                                  | distilled |

### references/topics/git-integrity.md

| Source              | Publisher    | URL                                                        | Status    |
|---------------------|--------------|------------------------------------------------------------|-----------|
| Git signing chapter | git-scm.com  | https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work | distilled |
| Sigstore gitsign    | Sigstore     | https://docs.sigstore.dev/                                 | distilled |
| TUF specification   | TUF          | https://theupdateframework.io/                             | distilled |
| SHAttered collision | shattered.io | https://shattered.io/                                      | distilled |

### references/topics/markdown-standards.md

| Source            | Publisher  | URL                                 | Status    |
|-------------------|------------|-------------------------------------|-----------|
| CommonMark 0.31.2 | CommonMark | https://spec.commonmark.org/0.31.2/ | distilled |
| Diataxis          | Diataxis   | https://diataxis.fr/                | distilled |

### references/topics/cli-contract.md

| Source                            | Publisher       | URL                                                                      | Status    |
|-----------------------------------|-----------------|--------------------------------------------------------------------------|-----------|
| Command Line Interface Guidelines | clig.dev        | https://clig.dev/                                                        | distilled |
| POSIX utility conventions         | IEEE/Open Group | https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html | distilled |
| NO_COLOR specification            | no-color.org    | https://no-color.org/                                                    | distilled |

### references/topics/mcp-server.md

| Source            | Publisher   | URL                                                | Status    |
|-------------------|-------------|----------------------------------------------------|-----------|
| MCP specification | MCP project | https://modelcontextprotocol.io/specification      | distilled |
| MCP C# SDK        | MCP project | https://github.com/modelcontextprotocol/csharp-sdk | distilled |
| MCP Rust SDK      | MCP project | https://github.com/modelcontextprotocol/rust-sdk   | distilled |

### references/topics/ui-automation.md

| Source                 | Publisher        | URL                                                                                 | Status    |
|------------------------|------------------|-------------------------------------------------------------------------------------|-----------|
| UI Automation overview | Microsoft        | https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview | distilled |
| Inspect tool           | Microsoft        | https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects             | distilled |
| W3C WebDriver          | W3C              | https://w3c.github.io/webdriver/                                                    | distilled |
| Chromium accessibility | Chromium project | https://www.chromium.org/developers/design-documents/accessibility/                 | distilled |
| Gecko accessibility    | Mozilla          | https://firefox-source-docs.mozilla.org/accessible/                                 | distilled |
| AT-SPI                 | GNOME project    | https://gnome.pages.gitlab.gnome.org/at-spi2-core/                                  | distilled |

### references/topics/performance-budgets.md

| Source          | Publisher         | URL                                           | Status    |
|-----------------|-------------------|-----------------------------------------------|-----------|
| Core Web Vitals | web.dev           | https://web.dev/vitals/                       | distilled |
| Lighthouse CI   | Google            | https://github.com/GoogleChrome/lighthouse-ci | distilled |
| k6              | Grafana Labs      | https://k6.io/docs/                           | distilled |
| hyperfine       | hyperfine project | https://github.com/sharkdp/hyperfine          | distilled |

### references/topics/inline-scripting.md

| Source                  | Publisher                  | URL                                                                                       | Status    |
|-------------------------|----------------------------|-------------------------------------------------------------------------------------------|-----------|
| cmd command reference   | Microsoft                  | https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd      | distilled |
| PowerShell about topics | Microsoft                  | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about | distilled |
| Python command line     | Python Software Foundation | https://docs.python.org/3/using/cmdline.html                                              | distilled |
| SS64 command reference  | SS64                       | https://ss64.com/nt/                                                                      | distilled |

### references/topics/data-persistence.md

| Source                       | Publisher      | URL                                                                                      | Status    |
|------------------------------|----------------|------------------------------------------------------------------------------------------|-----------|
| SQLite documentation         | SQLite project | https://sqlite.org/docs.html                                                             | distilled |
| SQL Injection Prevention     | OWASP          | https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html | distilled |
| Jakarta Persistence          | Eclipse        | https://jakarta.ee/specifications/persistence/                                           | distilled |
| Spring transaction reference | Spring project | https://docs.spring.io/spring-framework/reference/data-access/transaction.html           | distilled |

### Agent-facing refresh

Feeds `references/agent-skills.md` and `references/agent-configuration.md`.

| Source                     | Publisher      | URL                                                                              | Status    |
|----------------------------|----------------|----------------------------------------------------------------------------------|-----------|
| Agent Skills specification | agentskills.io | https://agentskills.io/specification                                             | distilled |
| Agent Skills overview      | Anthropic      | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview       | distilled |
| Agent skill best practices | Anthropic      | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | distilled |
| AGENTS.md convention       | agents.md      | https://agents.md/                                                               | distilled |
| MCP specification          | MCP project    | https://modelcontextprotocol.io/specification                                    | distilled |

### Advisory and tooling context

Feeds `references/cwe-analyzer.md` and `references/dependency-manifests.md`.

| Source  | Publisher | URL                  | Status    |
|---------|-----------|----------------------|-----------|
| Semgrep | Semgrep   | https://semgrep.dev/ | distilled |

## Session-Derived Files

These corpus files consolidate session knowledge rather than fetched sources.

| File                                     | Basis                                                    | Status    |
|------------------------------------------|----------------------------------------------------------|-----------|
| `references/topics/evidence-recipes.md`  | Audit-session mechanical evidence patterns               | distilled |
| `references/topics/deployment-ssh.md`    | Audit-session SSH/SCP deployment knowledge               | distilled |
| `references/topics/license-evidence.md`  | Per-ecosystem license evidence locations                 | distilled |
| `references/topics/standards-anatomy.md` | Maintainer-supplied engineering-standard corpora anatomy | distilled |

## Unresolved And Alternate Addresses

Ten registered URLs did not return a retrievable page during the 2026-09-30 and 2026-10-02
fetches.

The working alternates below carry the distilled content where a replacement exists.

| Registered URL                                                                                       | Fetch status | Disposition                                                                                                      |
|------------------------------------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------------------------------------------|
| https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html              | 404          | Renamed upstream - use https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html            |
| https://docs.stoplight.io/docs/spectral/                                                             | 404          | Moved - use https://docs.stoplight.io/docs/spectral/674b27b261c3c-overview                                       |
| https://docwiki.embarcadero.com/RADStudio/en/                                                        | 403          | Bot-blocked - readable in a browser, treated as restricted                                                       |
| https://learn.microsoft.com/en-us/compliance/assurance/assurance-threat-modeling                     | 404          | Retired - use https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool                      |
| https://micrometer.io/docs/registry/prometheus                                                       | 404          | Moved - use https://docs.micrometer.io/micrometer/reference/implementations/prometheus.html                      |
| https://wiki.sei.cmu.edu/confluence/display/c                                                        | timeout      | Space path unreliable - use https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard             |
| https://www.iso.org/standard/70017.html                                                              | 403          | ISO catalogue page bot-blocked - standard text is paywalled                                                      |
| https://www.iso.org/standard/78176.html                                                              | 403          | ISO catalogue page bot-blocked - standard text is paywalled                                                      |
| https://genai.owasp.org/download/52117                                                               | 403          | Permission-gated download - use https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| https://owasp.org/www-project-agentic-skills-top-10/assets/publications/ast10-top10-whitepaper-2.pdf | binary       | PDF not text-retrievable - list content lives at https://owasp.org/www-project-agentic-skills-top-10/            |

## Maintenance

Add a row whenever a corpus file cites a new source, and update the status when the source is
consolidated or re-fetched.

Keep one row per canonical address: versioned or locale variants of the same document share a
row under the canonical URL.
