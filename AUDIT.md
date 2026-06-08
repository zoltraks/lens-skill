# Informacje o dokumencie

**Wersja**: 1.0

**Data**: 2026-06-08

**Stan**: Final

**Poziom szczegolowosci**: Szczegolowy

---

# Stos technologiczny

| Warstwa            | Technologie                                                             |
|--------------------|-------------------------------------------------------------------------|
| Jezyki             | TypeScript 5.5, Java 21, C# 8.0, Go 1.22                                |
| Frameworki         | Fastify 4.28 (Node), Spring Boot 3.3 (Java), ASP.NET 8.0 (C#)          |
| Srodowisko         | Node.js 22, JVM 21, .NET 8, Go 1.22+; Docker + Docker Compose            |
| Narzedzia budowania| npm (Node), Maven 3.6+ (Java), .NET CLI (C#), go build (Go)            |
| Narzedzia testowe  | Vitest (Node), JUnit 5 (Java), xUnit (C#), Go testing, Jest (integracja) |
| Menadzer pakietow  | npm (Node), Maven Central (Java), NuGet (C#), Go modules                  |
| Kluczowe biblioteki| ExcelJS 4.4, Apache POI 5.2.5, ClosedXML 0.102.3, Zod, yaml, SnakeYAML  |
| Magazyny danych    | Lokalny system plikow (*.xlsx, *.lock); brak zewnetrznej bazy danych     |
| Platformy docelowe | Konteneryzowane serwery Docker; klient CLI jako pojedynczy binarny plik  |

Dowody: `excel-api-node/package.json` (wiersze 1-40), `excel-api-java/pom.xml` (wiersze 1-96), `excel-api-csharp/src/ExcelApi/ExcelApi.csproj` (wiersze 1-23), `excel-api-go/go.mod` (wiersze 1-3).

---

# Podsumowanie wykonawcze

| Pole                  | Wartosc                                                                   |
|-----------------------|---------------------------------------------------------------------------|
| Typ systemu           | Codebase w fazie wczesnego rozwoju                                        |
| Poziom dojrzalosci    | Early development                                                         |
| Stan docelowy         | Pre-production                                                            |
| Przejety zakres       | Trzy implementacje serwerowe (Node, Java, C#), klient CLI (Go), testy   |
| Ocena ogolna          | Wynik: 5/10                                                               |

**Krytyczne przed uruchomieniem w srodowisku produkcyjnym**

System wymaga zakoczenia prac w kilku kluczowych obszarach przed uzyskaniem statusu produkcyjnego.
Najwazniejsze to:
wprowadzenie pipelinu CI/CD z automatycznymi bramkami jakosci (RSK-001),
usuniecie szerokiego CORS w implementacji C# (RSK-003),
zdefiniowanie procedury rollback (RSK-005),
oraz wdrozenie rate limitingu i hardeningu TLS (RSK-004).
Bez spelnienia tych warunkow istnieje realne ryzyko wprowadzenia regresji, nieautoryzowanego dostepu i trudnych do odwrocenia incydentow konfiguracyjnych.

---

# Panel zdrowia

## Scorecard - podsumowanie

| Wymiar                  | Wynik | Uwagi                                                              |
|-------------------------|-------|--------------------------------------------------------------------|
| Testowalnosc            | 5/10  | Testy jednostkowe i integracyjne obecne, brak CI i dowodow pokrycia |
| Poprawnosc projektowa   | 6/10  | Modularna architektura, ale brak wspolnej abstrakcji miedzy implementacjami |
| Jakosc kodu             | 6/10  | Strict TS, ESLint, Checkstyle, ale brak enforcement i niekonsekwencje |
| Zgodnosc ze stosem      | 7/10  | Aktualne frameworki i biblioteki, idiomy stosowane poprawnie       |
| Zdrowie zaleznosci      | 6/10  | Lockfiles czesciowe, brak skanowania podatnosci i SBOM             |
| Utrzymywalnosc          | 6/10  | Czytelna struktura i dokumentacja, ale triplikacja kosztow utrzymania |
| Wdrazalnosc             | 5/10  | Obrazy Docker obecne, brak pipelinu i automatyzacji               |
| Skalowalnosc            | 4/10  | Architektura oparta na lokalnym FS ogranicza skalowanie horyzontalne |
| Bezpieczenstwo          | 5/10  | Podstawowe auth obecne, ale CORS, brak rate limitingu i TLS domyslnie wylaczone |
| Zgodnosc                | ND    | System nie przetwarza danych regulowanych; rejestr audytu nieobecny |
| Observability           | 5/10  | Logi JSON, health, metryki, brak tracingu i alertow                |
| Bezpieczenstwo operacyjne| 4/10 | Brak runbookow, procedur backup i reagowania na incydenty          |
| Pochodzenie AI          | 7/10  | Brak wyraznych sygnalow AI-generated code, brak polisy uzycia AI   |
| Oryginalnosc i licencjonowanie | 7/10 | MIT na poziomie repozytorium, brak SBOM i naglowkow licencyjnych w plikach |

## Mapa ciepla ryzyk

| Ryzyko                | Wplyw   | Prawdopodobienstwo | Waznosc     |
|-----------------------|---------|--------------------|-------------|
| RSK-001 Brak CI/CD    | WYSOKIE | WYSOKIE            | KRYTYCZNE   |
| RSK-003 Szeroki CORS  | WYSOKIE | SREDNIE            | WYSOKIE     |
| RSK-004 Brak rate limit | SREDNIE | SREDNIE          | SREDNIE     |
| RSK-005 Brak rollback | WYSOKIE | SREDNIE            | WYSOKIE     |
| RSK-007 Lokalny FS    | WYSOKIE | NISKIE             | SREDNIE     |

---

# Kluczowe obserwacje

- **Brak pipelinu CI/CD** uniemozliwia automatyczna walidacje zmian i gwarantuje, ze testy degradoja w czasie.
FND-INF-001.

- **Szeroki CORS w implementacji C#** (`AllowAnyOrigin`, `AllowAnyMethod`) otwiera potencjalne wektory atakow cross-origin w srodowiskach produkcyjnych.
FND-SEC-001.

- **Architektura oparta na lokalnym systemie plikow** zablokuje skalowanie horyzontalne i wprowadzi pojedynczy punkt awarii przy wielu instancjach bez wspoldzielonego magazynu.
FND-ARC-003.

- **Triplikacja logiki biznesowej** w trzech implementacjach serwerowych zwieksza koszt utrzymania i ryzyko niespojnosci przy zmianach w kontrakcie.
FND-ARC-001.

- **Brak rejestru audytu dostepu do plikow** w implementacjach uniemozliwia sledzenie, kto i kiedy modyfikowal dane biznesowe.
FND-SEC-004.

---

# Metodologia audytu

Audyt przeprowadzono zgodnie z procedura `process/workflow.md` skill LENS.

**Zakres audytu**

W zakresie: repozytorium `excel-api` w calosci, obejmujace trzy implementacje serwerowe (Node.js/TypeScript, Java/Spring Boot, C#/ASP.NET), klienta CLI w Go, zestaw testow integracyjnych, dokumentacje architektoniczna i operacyjna, konfiguracje Docker oraz pliki manifestow zaleznosci.

Poza zakresem: dzialajace srodowiska produkcyjne, infrastruktura chmurowa, dane uzytkownikow.

**Procedura zbierania dowodow**

Przeanalizowano strukture katalogow, pliki zrodlowe, konfiguracje budowania, testy, dokumentacje oraz metadane repozytorium.
Dla kazdej kategorii oceny otwarto odpowiedni plik `assessment/*.md` i zastosowano zawarte w nim checklisty.
Kazdy status zostal oparty na konkretnym fakcie z dostarczonego materialu.

---

# Skale oceny

| Pasmo       | Zakres wyniku | Definicja                                                            |
|-------------|---------------|----------------------------------------------------------------------|
| Doskonale   | 9-10          | Mozliwosc kompleksowa i potwierdzona mocnymi dowodami                 |
| Dobre       | 7-8           | Mozliwosc solidna ogolnie; istnieja drobne lub zauwazalne luki        |
| Srednie     | 4-6           | Mozliwosc obecna, ale nierowna, ograniczona lub niespojna             |
| Slabe       | 1-3           | Mozliwosc minimalna, fragmentaryczna lub nieobecna tam, gdzie wymagana |

| Wynik | Znaczenie                                                              |
|-------|------------------------------------------------------------------------|
| 10    | Mozliwosc kompleksowa i potwierdzona mocnymi dowodami                  |
| 9     | Mozliwosc niemal kompleksowa, z jedynie trywialnymi lukami             |
| 8     | Mozliwosc solidna z drobnymi lukami                                     |
| 7     | Mozliwosc dobra ogolnie, z kilkoma zauwazalnymi lukami                  |
| 6     | Mozliwosc adekwatna, ale nierowna                                       |
| 5     | Mozliwosc obecna, ale ograniczona lub niespojna                        |
| 4     | Mozliwosc obecna, ale znaczaco ograniczona                              |
| 3     | Mozliwosc minimalna lub ledwo udokumentowana                            |
| 2     | Fragmenty obecne, glownie bez dowodow                                   |
| 1     | Mozliwosc nieobecna tam, gdzie wymagana, z dowodem nieobecnosci         |

---

# Kontekst systemu

**Cel systemu**

Excel API dostarcza interfejs HTTP umozliwiajacy dostep do danych arkuszy Excel w formacie JSON, z kolejkowanymi operacjami zapisu i blokada plikowa dla dostepu wspolbieznego.

**Model wdrozenia**

System jest projektowany jako konteneryzowana usluga sieciowa, wdrazana przez Docker lub Docker Compose.
Kazda implementacja serwerowa buduje samowystarczalny obraz Docker.
Dane (pliki Excel) przechowywane sa na lokalnym lub zamontowanym systemie plikow.

**Ograniczenia**

- Brak wsparcia dla horyzontalnego skalowania wielu instancji bez wspoldzielonego systemu plikow.
- Brak chmurowych backendow magazynowania (S3, GCS, Azure Blob).
- Model plikowy wyklucza edycje wspolbiezna w czasie rzeczywistym.

**Dojrzalosc**

Wersja 0.0.2 wskazuje na wczesna faze rozwoju.
CHANGELOG.md dokumentuje historie zmian.
Dokumentacja DEPLOYMENT.md opisuje podstawowe wdrozenie, ale brak zaawansowanych procedur operacyjnych.

---

# Ocena architektury

System zostal zaprojektowany jako zestaw trzech wymiennych implementacji serwerowych wspoldzielacych jeden kontrakt OpenAPI 3.1.
To podejscie umozliwia wybor stosu technologicznego w zaleznosci od srodowiska, ale wprowadza wysoki koszt utrzymania i ryzyko niespojnosci.

**Dobrze udokumentowana separacja konfiguracji**

`config.yaml` (niewrazliwe) i `access.yaml` (wrazliwe) tworza przejrzysty podzial zgodny z dobrymi praktykami.
`docs/ARCHITECTURE.md` (wiersze 36-38) opisuje te separacje i wymagane uprawnienia 0600 dla `access.yaml`.

**Wspoldzielony protokol blokad**

Warstwa kolejki i blokad zostala zaprojektowana jako wspoldzielona miedzy implementacjami.
To umozliwia jednoczesne uruchomienie roznych serwerow na tych samych danych bez konfliktow.

**Wady architektoniczne**

Brak wspolnej biblioteki abstrakcyjnej dla operacji na Excelu oznacza, ze kazda zmiana kontraktu API musi byc recznie powielona w trzech kodbazach.
To jest istotne zrodlo technicznego dlugu.

Architektura oparta na lokalnym systemie plikow jest prosta i skuteczna dla pojedynczej instancji, ale staje sie bariery przy probie skalowania horyzontalnego.
Brak wyraznej strategii przechodzenia do magazynow obiektowych lub baz danych wskazuje na to, ze skalowalnosc nie byla priorytetem w tej fazie.

---

# Mocne strony i co dziala

- **Kompleksowa dokumentacja projektowa.** Repozytorium zawiera ponad 10 plikow dokumentacyjnych opisujacych architekture, specyfikacje, standardy kodowania, strategie testowania i wdrazania.
Dowod: `docs/ARCHITECTURE.md`, `docs/PROJECT.md`, `docs/TESTING.md`, `docs/DEPLOYMENT.md`.

- **Wspolny kontrakt OpenAPI 3.1 jako jedno zrodlo prawdy.** Wszystkie implementacje musza byc zgodne z `docs/contract/openapi.yaml`, co zapobiega niespojnosc interfejsow.

- **Separacja konfiguracji wrazliwej i niewrazliwej.** `config.yaml` i `access.yaml` tworza przejrzysty model konfiguracyjny z roznymi wymaganiami dotyczacymi bezpieczenstwa.

- **Testy integracyjne black-box.** Suite `excel-api-test` zawiera 8 zestawow testow integracyjnych (auth, workbooks, sheets, rows, operations, locking, concurrency, openapi-endpoint), ktore sa niezalezne od implementacji serwera.

- **Testy jednostkowe we wszystkich implementacjach.** Node (11 plikow testowych), Java (10), C# (8), Go (6) pokazuja systematyczne podejscie do testowania na poziomie modulu.

- **Obrazy Docker dla kazdej implementacji.** Kazda z czterech komponentow posiada wlasny `Dockerfile`, co wspiera powtarzalne budowanie i izolacje srodowiskowa.

- **Struktura modularna w kazdej implementacji.** Podzial na `auth/`, `cache/`, `lock/`, `queue/`, `routes/` (Node), `controller/`, `service/`, `config/` (Java), `Endpoints/`, `Services/` (C#) demonstruje konsekwentna separacje zagadnien.

- **Health endpoint i logi JSON we wszystkich implementacjach.** Wspolne podejscie do observability na poziomie logowania i sprawdzania stanu.

- **Wspoldzielony protokol blokad miedzy implementacjami.** Umozliwia bezkonfliktowe uruchamianie roznych serwerow na wspolnych danych.

---

# Szczegolowe wyniki techniczne

## Indeks wynikow

| ID          | Filtr                    | Kategoria                           | Status         | Waznosc      | Stan naprawy |
|-------------|--------------------------|-------------------------------------|----------------|--------------|--------------|
| FND-INF-001 | Infrastruktura i CI/CD   | Brak pipelinu CI/CD                 | NIEZALICZONE   | KRYTYCZNE    | Otwarty      |
| FND-SEC-001 | Bezpieczenstwo           | Szeroki CORS w implementacji C#       | CZESCIOWO      | WYSOKIE      | Otwarty      |
| FND-SEC-002 | Bezpieczenstwo           | TLS domyslnie wylaczone             | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-SEC-003 | Bezpieczenstwo           | Brak rate limitingu                 | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-SEC-004 | Bezpieczenstwo           | Brak rejestru audytu dostepu        | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-SEC-005 | Bezpieczenstwo           | Brak walidacji rozmiaru plikow      | NIEZNANE       | NISKIE       | Otwarty      |
| FND-ARC-001 | Architektura i projekt   | Triplikacja logiki biznesowej       | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-ARC-002 | Architektura i projekt   | Brak wspolnej abstrakcji operacji   | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-ARC-003 | Architektura i projekt   | Lokalny FS jako jedyny backend      | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-CQ-001  | Jakosc kodu              | Niezgodnosc ESLint z TS strict      | CZESCIOWO      | NISKIE       | Otwarty      |
| FND-CQ-002  | Jakosc kodu              | TODO w kodzie produkcyjnym Java     | CZESCIOWO      | NISKIE       | Otwarty      |
| FND-CQ-003  | Jakosc kodu              | Brak pre-commit hooks               | CZESCIOWO      | NISKIE       | Otwarty      |
| FND-DEP-001 | Zaleznosci               | Brak lockfile w Java (Maven)        | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-DEP-002 | Zaleznosci               | Brak skanowania podatnosci          | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-DEP-003 | Zaleznosci               | Brak SBOM                         | CZESCIOWO      | NISKIE       | Otwarty      |
| FND-OPS-001 | Operacyjnosc             | Brak runbookow operacyjnych         | NIEZNANE       | SREDNIE      | Otwarty      |
| FND-OPS-002 | Operacyjnosc             | Brak procedury rollback             | NIEZNANE       | SREDNIE      | Otwarty      |
| FND-OBS-001 | Observability            | Brak distributed tracing            | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-OBS-002 | Observability            | Brak alertow i dashboardow          | CZESCIOWO      | SREDNIE      | Otwarty      |
| FND-AIP-001 | Pochodzenie AI           | Brak polisy uzycia narzedzi AI      | NIEZNANE       | NISKIE       | Otwarty      |
| FND-CPR-001 | Prawa autorskie          | Brak naglowkow licencyjnych w plikach| CZESCIOWO     | NISKIE       | Otwarty      |
| FND-CPR-002 | Prawa autorskie          | Brak pliku THIRD-PARTY-NOTICES      | CZESCIOWO      | NISKIE       | Otwarty      |

---

### Infrastruktura i CI/CD

**FND-INF-001: Brak pipelinu CI/CD** `NIEZALICZONE` `KRYTYCZNE`

W repozytorium nie znaleziono katalogu `.github/workflows/`, `.gitlab-ci.yml` ani innych plikow konfiguracyjnych pipelinu CI/CD.
Testy jednostkowe i integracyjne istnieja, ale brak dowodow, ze sa one automatycznie uruchamiane przy kazdej zmianie kodu.
W konsekwencji nie ma bramki jakosci blokujacej zmiany powodujace regresje.

Dowod: Brak katalogu `.github/workflows/` w repozytorium.
Weryfikacja: `ls -la .github/workflows/` zwraca "NO_CI_WORKFLOWS_FOUND".

---

### Bezpieczenstwo i zgodnosc

**FND-SEC-001: Szeroki CORS w implementacji C#** `CZESCIOWO` `WYSOKIE`

`excel-api-csharp/src/ExcelApi/Program.cs` (wiersze 28-35 i 52-57) zawiera konfiguracje CORS z `AllowAnyOrigin()`, `AllowAnyMethod()` i `AllowAnyHeader()`.
To ustawienie otwiera API na dowolne zrodlo, co w srodowisku produkcyjnym jest powaznym zagrozeniem bezpieczenstwa, umozliwiajac potencjalne ataki CSRF i nieautoryzowane zapytania z przegladarek.

Dowod: `excel-api-csharp/src/ExcelApi/Program.cs`, wiersze 28-35, 52-57.

**FND-SEC-002: TLS domyslnie wylaczone** `CZESCIOWO` `SREDNIE`

`config/config.example.yaml` (wiersze 5-6) ustawia `server.tls.enabled: false` jako wartosc domyslna.
Chociaz dokumentacja DEPLOYMENT.md wspomina o mozliwosci wlaczenia TLS, domyslna konfiguracja nie wymusza szyfrowania transportu.
W srodowisku produkcyjnym to zwieksza ryzyko przechwytywania danych wrazliwych, w tym tokenow JWT.

Dowod: `excel-api-node/config/config.example.yaml`, wiersze 5-6.

**FND-SEC-003: Brak rate limitingu** `CZESCIOWO` `SREDNIE`

W zadnej z trzech implementacji serwerowych nie znaleziono mechanizmu ograniczania liczby zapytan (rate limiting).
Bez takiego mechanizmu API jest podatne na ataki DoS i na nadmierne zuzywanie zasobow przez pojedynczego klienta.

Dowod: Brak biblioteki ani middleware rate limiting w `package.json`, `pom.xml`, `ExcelApi.csproj`.

**FND-SEC-004: Brak rejestru audytu dostepu do plikow** `CZESCIOWO` `SREDNIE`

System autentykuje uzytkownikow i autoryzuje dostep na podstawie zakresow (scopes), ale brak dowodow na prowadzenie rejestru audytu logujacego kto i kiedy uzyskal dostep do ktorych plikow Excel.
W kontekscie danych biznesowych przechowywanych w arkuszach brak sledzenia dostepu jest luka w zgodnosci i bezpieczenstwie.

Dowod: Brak modulu audytu w strukturze katalogow ani w dokumentacji.

**FND-SEC-005: Brak walidacji rozmiaru plikow** `NIEZNANE` `NISKIE`

Nie znaleziono dowodow na obecnosc walidacji maksymalnego rozmiaru plikow Excel przesylanych do API ani ograniczenia liczby rekordow w operacjach wsadowych poza parametrem `batch_max_size: 50`.
Moze to prowadzic do problemow z wykorzystaniem pamieci przy bardzo duzych plikach.

Dowod: `config/config.example.yaml` okresla `batch_max_size: 50`, ale brak walidacji rozmiaru samego pliku.

---

### Architektura i projekt

**FND-ARC-001: Triplikacja logiki biznesowej** `CZESCIOWO` `SREDNIE`

Trzy niezalezne implementacje serwerowe (Node, Java, C#) zawieraja niezalezna logike dla tych samych operacji: autentykacja, autoryzacja, kolejkowanie zapisow, blokady plikowe, operacje Excel, konfiguracja.
Chociaz wspoldziela one kontrakt OpenAPI, brak wspolnej biblioteki lub warstwy abstrakcyjnej oznacza, ze kazda zmiana logiki biznesowej musi byc recznie replikowana trzykrotnie.

Dowod: Porownanie `excel-api-node/src/server.ts`, `excel-api-java/src/main/java/pl/alyx/api/excel/Application.java`, `excel-api-csharp/src/ExcelApi/Program.cs` pokazuje niezalezna inicjalizacje tych samych komponentow.

**FND-ARC-002: Brak wspolnej abstrakcji operacji na Excelu** `CZESCIOWO` `SREDNIE`

Kazda implementacja uzywa innej biblioteki do operacji na Excelu (ExcelJS, Apache POI, ClosedXML) bez wspolnej warstwy abstrakcyjnej.
To oznacza, ze roznice w zachowaniu miedzy bibliotekami moga prowadzic do niespojnych wynikow miedzy implementacjami.

Dowod: `excel-api-node/src/excel/operations.ts`, `excel-api-java/src/main/java/pl/alyx/api/excel/service/ExcelService.java`, `excel-api-csharp/src/ExcelApi/Services/ExcelService.cs`.

**FND-ARC-003: Lokalny system plikow jako jedyny backend danych** `CZESCIOWO` `SREDNIE`

`docs/ARCHITECTURE.md` (wiersze 40-42) jasno stwierdza: "The service does not provide cloud storage backends. Files are registered in configuration rather than discovered."
To podejscie jest proste, ale uniemozliwia skalowanie horyzontalne bez wspoldzielonego systemu plikow (np. NFS) i tworzy pojedynczy punkt awarii.

Dowod: `docs/ARCHITECTURE.md`, wiersze 40-42.

---

### Jakosc kodu

**FND-CQ-001: Niezgodnosc konfiguracji ESLint z TypeScript strict** `CZESCIOWO` `NISKIE`

`excel-api-node/tsconfig.json` wlacza `noUnusedLocals: true` i `noUnusedParameters: true`, ale `.eslintrc.json` (wiersze 17-18) wylacza reguly `@typescript-eslint/no-unused-vars` i `no-unused-vars`.
To tworzy sprzecznosc: TypeScript kompilator wymaga czystosci, ale linter nie wymusza jej, co moze prowadzic do niespojnej polityki w zespole.

Dowod: `excel-api-node/tsconfig.json` (wiersze 9-10) oraz `.eslintrc.json` (wiersze 17-18).

**FND-CQ-002: TODO w kodzie produkcyjnym Java** `CZESCIOWO` `NISKIE`

`excel-api-java/src/main/java/pl/alyx/api/excel/controller/LockStatusController.java` zawiera komentarz `// TODO: Implement actual lock status checking`.
`OpenApiController.java` zawiera `// TODO: Convert YAML to JSON using SnakeYAML`.
Obecnosc TODO w kodzie na galezi glownej wskazuje na niedokonczona prace.

Dowod: `grep -ri TODO` w katalogu `excel-api-java`.

**FND-CQ-003: Brak pre-commit hooks** `CZESCIOWO` `NISKIE`

Brak pliku `.pre-commit-config.yaml`, `husky/` ani innych mechanizmow pre-commit w repozytorium.
Oznacza to, ze formatting i linting nie sa automatycznie wymuszane przed zatwierdzeniem zmiany, co zwieksza ryzyko wprowadzenia nieformatowanego kodu.

Dowod: Brak `.pre-commit-config.yaml` w repozytorium.

---

### Zaleznosci i lancuch dostaw

**FND-DEP-001: Brak lockfile w Java (Maven)** `CZESCIOWO` `SREDNIE`

`pom.xml` uzywa wersji zarzadzanych przez Spring Boot Parent, ale Maven nie generuje lockfile w taki sposob jak npm (`package-lock.json`) czy Go (`go.sum`).
To oznacza, ze wersje zaleznosci transytywnych nie sa zablokowane, co moze prowadzic do niespojnych buildow w roznych momentach czasowych.

Dowod: `excel-api-java/pom.xml` - brak mechanizmu lockfile (Maven nie ma natywnego lockfile, ale mozna uzyc `versions:resolve-ranges` lub `flatten-maven-plugin`).

**FND-DEP-002: Brak skanowania podatnosci** `CZESCIOWO` `SREDNIE`

W repozytorium nie znaleziono konfiguracji narzedzi do skanowania podatnosci (np. `npm audit`, OWASP Dependency-Check, Snyk, Dependabot).
Bez automatycznego skanowania znane podatnosci w zaleznosciach moga pozostac niezauwazone.

Dowod: Brak plikow konfiguracyjnych skanerow podatnosci w repozytorium.

**FND-DEP-003: Brak SBOM** `CZESCIOWO` `NISKIE`

Brak wygenerowanego pliku Software Bill of Materials (SBOM) w formacie SPDX lub CycloneDX.
SBOM jest coraz czesciej wymagany w lancuchach dostaw oprogramowania i ulatwia szybka reakcje na podatnosci w zaleznosciach.

Dowod: Brak plikow `sbom.json`, `bom.xml`, `*.spdx` w repozytorium.

---

### Operacyjnosc

**FND-OPS-001: Brak runbookow operacyjnych** `NIEZNANE` `SREDNIE`

W repozytorium nie znaleziono runbookow opisujacych procedury operacyjne: start, stop, restart, rozszerzanie zasobow, rozwiazywanie problemow.
`docs/DEPLOYMENT.md` (56 wierszy) opisuje jedynie podstawowe budowanie obrazow Docker i ich uruchamianie.

Dowod: Brak katalogu `runbooks/`, `ops/` ani plikow z prefixem `runbook-` w repozytorium.

**FND-OPS-002: Brak procedury rollback** `NIEZNANE` `SREDNIE`

Nie znaleziono dokumentacji ani skryptow opisujacych procedure rollback w przypadku nieudanego wdrozenia.
`docker-compose.yaml` umozliwia uruchomienie uslugi, ale nie zawiera mechanizmu bezpiecznego cofania wersji.
Brak tagow wersji w Dockerfile dodatkowo utrudnia identyfikacje wersji do przywrocenia.

Dowod: Brak plikow `rollback.md`, `rollback.sh` ani odpowiednich sekcji w `docs/DEPLOYMENT.md`.

---

### Observability

**FND-OBS-001: Brak distributed tracing** `CZESCIOWO` `SREDNIE`

System sklada sie z wielu komponentow (serwery, klient CLI), ale brak dowodow na obecnosc distributed tracing (np. OpenTelemetry, Jaeger, Zipkin).
Bez sledzenia rozproszonego diagnozowanie problemow miedzy komponentami jest utrudnione.

Dowod: Brak bibliotek tracing w `package.json`, `pom.xml`, `ExcelApi.csproj`, `go.mod`.

**FND-OBS-002: Brak alertow i dashboardow** `CZESCIOWO` `SREDNIE`

Chociaz wszystkie implementacje eksponuja endpoint `/health` i generuja logi JSON, brak dowodow na obecnosc regol alertowania, dashboardow ani systemu zarzadzania incydentami.
Bez alertow degradacja uslugi moze pozostac niezauwazona przez operatorow.

Dowod: Brak konfiguracji alertow (np. Prometheus Alertmanager, PagerDuty) w repozytorium.

---

### Pochodzenie AI

**FND-AIP-001: Brak polisy uzycia narzedzi AI** `NIEZNANE` `NISKIE`

W repozytorium nie znaleziono polisy dotyczacej uzycia narzedzi generujacych kod (AI), ani wyraznych sygnalow wskazujacych na dominujace uzycie Vibe Coding.
Jednak brak formalnej polisy oznacza, ze zespol nie ma ustalonych zasad recenzji i walidacji kodu generowanego przez AI.

Dowod: Brak pliku `AI_POLICY.md`, `docs/AI.md` ani odpowiednich sekcji w `docs/GUIDELINES.md`.

---

### Prawa autorskie

**FND-CPR-001: Brak naglowkow licencyjnych w plikach zrodlowych** `CZESCIOWO` `NISKIE`

`LICENSE.md` (MIT) jest obecny w katalogu glownym, ale poszczegolne pliki zrodlowe nie zawieraja naglowkow licencyjnych.
To utrudnia identyfikacje licencji przy dystrybucji pojedynczych plikow lub fragmentow kodu.

Dowod: `LICENSE.md` obecny, brak `// SPDX-License-Identifier` lub podobnych naglowkow w plikach zrodlowych.

**FND-CPR-002: Brak pliku THIRD-PARTY-NOTICES** `CZESCIOWO` `NISKIE`

Brak wygenerowanego pliku `THIRD-PARTY-NOTICES` lub `NOTICE` opisujacego zaleznosci i ich licencje.
Taki plik jest wymagany przez niektore organizacje i ulatwia audyt licencyjny.

Dowod: Brak plikow `THIRD-PARTY-NOTICES`, `NOTICE` w repozytorium.

---

# Jednolity rejestr ryzyk

| ID      | Ryzyko                                                               | Zrodlowy wynik | Wplyw   | Prawdopodobienstwo | Waznosc     | Ograniczenie                                              |
|---------|----------------------------------------------------------------------|----------------|---------|--------------------|-------------|-----------------------------------------------------------|
| RSK-001 | Brak CI/CD prowadzi do regresji i niestabilnych buildow             | FND-INF-001    | WYSOKIE | WYSOKIE            | KRYTYCZNE   | Wdrozyć GitHub Actions z bramkami build i test           |
| RSK-002 | Niespojne buildy Maven przez brak lockfile                           | FND-DEP-001    | SREDNIE | SREDNIE            | WYSOKIE     | Zablokowac wersje transytywne lub uzyc Maven flatten      |
| RSK-003 | Szeroki CORS umozliwia ataki cross-origin na API C#                  | FND-SEC-001    | WYSOKIE | SREDNIE            | WYSOKIE     | Ograniczyc do zaufanych zrodel i metod                    |
| RSK-004 | Brak rate limitingu umozliwia ataki DoS                             | FND-SEC-003    | SREDNIE | SREDNIE            | SREDNIE     | Wdrozyć middleware rate limiting we wszystkich implementacjach |
| RSK-005 | Brak procedury rollback wydluza czas naprawy incydentow             | FND-OPS-002    | WYSOKIE | SREDNIE            | WYSOKIE     | Udokumentowac procedure i skrypty rollback                  |
| RSK-006 | Triplikacja logiki zwieksza ryzyko niespojnosci przy zmianach       | FND-ARC-001    | SREDNIE | SREDNIE            | SREDNIE     | Rozwazyc wspolna biblioteke abstrakcyjna lub generowanie kodu |
| RSK-007 | Lokalny FS uniemozliwia skalowanie horyzontalne                      | FND-ARC-003    | WYSOKIE | NISKIE             | SREDNIE     | Rozwazyc NFS lub backend obiektowy                         |

---

# Analiza kompromisow

| Kompromis                  | Kontekst                               | Opcja A: zysk / koszt                   | Opcja B: zysk / koszt                    | Dowod                                                         | Implikacja                                                             |
|----------------------------|----------------------------------------|-----------------------------------------|------------------------------------------|----------------------------------------------------------------|------------------------------------------------------------------------|
| Trojimplementacje vs jedna | Potrzeba elastycznosci wyboru stosu    | Wymiennosc / triplikacja kosztow         | Nizszy koszt utrzymania / brak wyboru    | Trzy implementacje serwerowe w repozytorium                     | Obecny stan pasuje do kontekstu wielojezycznego srodowiska; produkcja wymaga spojnosci |
| Lokalny FS vs magazyn obiektowy | Prototyp, jedna instancja            | Prostota / brak skalowania horyzontalnego| Skalowanie / dodana zlozonosc operacyjna | `docs/ARCHITECTURE.md` wiersze 40-42                           | Dla obecnej fazy prototypowej uzasadnione; migracja w przyszlosci wymaga planu |
| TLS w aplikacji vs reverse proxy | Wdrozenie Docker, elastycznosc dev     | Prostota konfiguracji / ryzyko zapomnienia| Wyzsze bezpieczenstwo / dodana infrastruktura | `config.example.yaml` (TLS disabled) i `DEPLOYMENT.md` (reverse proxy) | Wymaga wyraznej polityki wymuszania TLS w produkcji                    |

---

# Plan dzialania i mapa naprawcza

| Rec ID | Priorytet | Wynik       | Rekomendacja                                                               | Wplyw   | Wysilek | Zlozonosc | Weryfikacja                                                          |
|--------|-----------|-------------|----------------------------------------------------------------------------|---------|---------|-----------|----------------------------------------------------------------------|
| REC-001| P1        | FND-INF-001 | Utworzyc `.github/workflows/ci.yml` z krokami build, lint, test dla wszystkich implementacji | Wysoki  | Sredni  | Niska     | Pipeline przechodzi z sukcesem dla kazdej implementacji            |
| REC-002| P1        | FND-SEC-001 | Ograniczyc CORS w C# do zaufanych zrodel i metod HTTP                    | Wysoki  | Niski   | Niska     | Testy integracyjne przechodza; skaner bezpieczenstwa nie zglasza alertow |
| REC-003| P2        | FND-SEC-002 | Ustawic `server.tls.enabled: true` w produkcyjnych plikach config i dodac walidacje startup | Sredni  | Niski   | Niska     | Health endpoint dziala przez HTTPS; testy odrzucaja plain HTTP       |
| REC-004| P2        | FND-SEC-003 | Wdrozyć rate limiting (np. `fastify-rate-limit`, `Bucket4j`, `AspNetCoreRateLimit`) | Sredni  | Niski   | Niska     | Testy obciazeniowe potwierdzaja ograniczenie liczby zapytan          |
| REC-005| P2        | FND-OPS-002 | Udokumentowac procedure rollback i dodac tagowanie wersji do Dockerfile    | Sredni  | Niski   | Niska     | Proba rollback na srodowisku testowym konczy sie sukcesem          |
| REC-006| P2        | FND-DEP-002 | Skonfigurowac Dependabot i skanowanie podatnosci (npm audit, OWASP DC)     | Sredni  | Niski   | Niska     | Raporty z podatnosciami sa generowane automatycznie                |
| REC-007| P3        | FND-ARC-003 | Opracowac plan migracji do backendu umozliwiajacego skalowanie (NFS lub obiektowy) | Wysoki  | Wysoki  | Wysoka    | Wydajnosc testowana przy wielu instancjach                         |
| REC-008| P3        | FND-OBS-001 | Wdrozyć OpenTelemetry tracing w co najmniej jednej implementacji          | Sredni  | Sredni  | Srednia   | Trace widoczne w Jaeger/Zipkin dla zapytan E2E                     |
| REC-009| P3        | FND-ARC-001 | Rozwazyc wygenerowanie kodu serwera z OpenAPI lub wspolna biblioteke core   | Sredni  | Wysoki  | Wysoka    | Zmiana w kontrakcie propaguje sie automatycznie do implementacji   |
| REC-010| P4        | FND-CPR-002 | Wygenerowac plik THIRD-PARTY-NOTICES i SBOM w formacie CycloneDX         | Niski   | Niski   | Niska     | Plik jest obecny i zawiera pelna liste zaleznosci z licencjami    |
| REC-011| P4        | FND-CQ-002  | Usunac TODO z kodu Java lub przeniesc je do ticketow w trackerze          | Niski   | Niski   | Niska     | `grep -ri TODO` nie zwraca wynikow w galezi glownej               |
| REC-012| P4        | FND-CQ-003  | Dodac pre-commit hooks (husky + lint-staged lub pre-commit framework)    | Niski   | Niski   | Niska     | Nieprawidlowo sformatowany kod jest blokowany przed commitem       |

---

# Wyłączenia z zakresu

- **Srodowiska produkcyjne.** Audyt opiera sie wylacznie na kodzie zrodlowym i dokumentacji repozytorium. Nie audytowano dzialajacych instancji produkcyjnych, ich konfiguracji runtime ani logow operacyjnych.

- **Infrastruktura chmurowa.** Nie sprawdzono konfiguracji chmurowej (VPC, load balancery, sieci, grupy bezpieczenstwa), poniewaz nie byla ona czescia dostarczonego materialu.

- **Testy penetracyjne.** Audyt jest przegladem defensywnym opartym na analizie statycznej. Nie przeprowadzono testow penetracyjnych ani fuzzingu.

- **Dane uzytkownikow.** Nie analizowano zawartosci plikow Excel ani danych biznesowych przechowywanych w arkuszach.
