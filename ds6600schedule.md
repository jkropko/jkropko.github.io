# DS 6600: Data Engineering 1 — Day-by-Day Schedule, Fall 2026 (Draft)

Tuesdays and Thursdays, 2:00–3:15pm | Data Science 246

**31 meeting slots** between Tue 8/25 and Tue 12/8, minus three university holidays, minus one optional work session = **27 substantive class sessions.**

*Year inferred as 2026 — Aug 25, Oct 6, and Nov 3 fall on Tuesdays and Nov 26 on Thanksgiving Thursday only in that year.*

**Design principle:** every unit answers a problem the students have already hit themselves, and every week moves their own project forward.

Every session carries a **Dashboard build** block: the specific thing we do to the Congress Transparency Dashboard that day. The dashboard is never a motivating anecdote — it is the artifact under the knife in all 27 sessions, and it exists in a running (if terrible) state from the second class onward.

---

## Data sources — status for Fall 2026

| Source | Access | Role in course | Set-up lead time |
|---|---|---|---|
| **api.congress.gov** | REST API, instant key | Members, bills, committees, sponsorship | None |
| **Voteview** | Bulk CSV, no auth | Roll-call votes, NOMINATE scores, ICPSR IDs | None |
| **GPO govinfo bulk data** | Bulk XML ZIPs, no auth | Congressional Record — floor proceedings, and the entity resolution problem | None |
| **openFEC** | REST API, api.data.gov key | Contributions, **outside spending / dark money** | Minutes |
| **GPO Congressional Record** | Bulk XML, no auth | Floor proceedings — and the entity resolution problem | None |
| **OpenSecrets bulk** | Manual download, approval-gated | Industry/sector classification only | **Weeks — register in August** |
| **unitedstates/congress-legislators** | YAML on GitHub | bioguide ↔ ICPSR ↔ FEC ID crosswalk | None |

> ### ⚠️ Bill text comes from GPO, not from scraping congress.gov
> The Congress.gov API does **not** serve bill text — `/bill/{congress}/{type}/{number}/text` returns *links* to documents hosted elsewhere. Fetching text therefore costs one API call plus one or more document downloads per bill, and those downloads hit congress.gov directly, where **disregarding the robots.txt disallow rules gets you blocked**. Fifteen students pulling simultaneously from one university IP range is the fastest way to lose access to the metadata pipeline too.
>
> **GPO publishes the same text in bulk** at `govinfo.gov/bulkdata/BILLS`, back to the 113th Congress and current through the 119th, organized by Congress and bill type with a ZIP per type. That converts roughly twenty thousand requests into about eight downloads, needs no key, and is public domain. `BILLSTATUS` bulk XML at `govinfo.gov/bulkdata/BILLSTATUS` refreshes every four hours and is a useful cross-check on API-sourced metadata.
>
> Two conveniences: appending `/xml` or `/json` to any bulkdata URL returns the directory listing in that format, but you must set the Accept header or you'll get a 406.

> ### ⚠️ OpenSecrets changed since this course last ran
> **The OpenSecrets API was discontinued on April 15, 2025**, after 17 years. Only bulk data remains, and getting it means agreeing to educational-use terms, registering a Bulk Data account, confirming email, and *waiting for approval*. The files are CC BY-NC-SA and lag the live site by months.
>
> **OpenSecrets is therefore demoted from an API source to a flat-file source**, and it is no longer load-bearing. Campaign finance moves to the FEC directly. Keep OpenSecrets for the one thing the FEC genuinely cannot give you — industry and sector classification of contributors — and design the dashboard so it degrades gracefully if approvals don't arrive for every student.

> ### The principle these two changes teach
> **When a bulk distribution exists, use it. APIs are for incremental updates and targeted queries.** State it on 9/29 when we decline to scrape congress.gov, and again on 11/10 when the API becomes the delta on top of a bulk backfill. It's one of the most transferable rules in the course and the old schedule never said it out loud.

---

## Assessments at a glance

| Stream | Count | Points each | Total | What it measures |
|---|---|---|---|---|
| GitHub check-ins | 5 | 12 | 60 | Did you type along in class |
| Labs (Part A + Part B) | 8 | 20 | 160 | Did the skill transfer |
| Data pipeline project | 1 | 180 | 180 | Can you build one end to end |
| | | **Total** | **400** | |

**Three artifacts, three different jobs.** The check-ins cover the **Congress dashboard repo** students type along with in class. Part A covers a **different dataset entirely**. Part B covers **their own pipeline**. Nothing in either lab part touches the in-class repo, so the check-ins are the only thing watching it — and without them, typing along becomes optional and live coding degrades into watching someone else code, which is the one failure the format exists to prevent.

**Check-ins are not assessment.** As in the original syllabus: the code doesn't have to be perfect and doesn't have to run without error, so long as it's the work we did in class and not something irrelevant. The low stakes are the design — they're what make the promise credible, and 12 points each keeps them cheap enough to stay that way.

> **Grade on commit timestamps, not just contents.** A student who typed along has commits clustered around 3:10pm on Tuesdays and Thursdays; a student who reconstructed the repo the night before has one commit at 11:47pm. Reading `git log` measures the ritual directly and takes seconds — and it's the only check that still means anything now that an agent can generate a plausible session repo in thirty seconds. Stay good-faith about it: someone who missed a class and caught up from the session tag gets full credit, because that's exactly the recovery path the tags exist for.

> **Late policy: two 72-hour extension tokens per student, per semester.** No questions, no permission — the student notes it on submission. Chosen over dropping the lowest lab score because Part B is *cumulative*: a dropped Lab 6 still leaves the student needing a schema for Labs 7, 8, 9 and the project, so dropping forgives the grade but not the work and reads as permission to skip a week. Tokens absorb a bad week without implying any week is optional, and they leave the arithmetic alone — **all eight labs count**, which is why the totals above hold.

**Project check-ins are eliminated** — Part B of each lab *is* the check-in, and it now happens eight times instead of twice. That's what frees the project's own points down to 160.

### How the two parts work

**Part A — instructor-chosen application.** Same task for everyone, known answer, autograded by pytest inside the course container. Tests correctness. *Deliberately not Congress data* — it's the transfer test that proves the technique generalizes past the in-class example.

**Part B — the student's own pipeline.** Idiosyncratic per student. **Graded on movement, not correctness** — did the pipeline advance, is the reasoning sound? A skim of the diff, not a code review.

Every Part B carries a short **written design rationale**. Mandatory, never optional: it requires the student's own data and judgment, it's the one component a coding agent can't produce for them, and it's where the real teaching signal is.

So each week has three passes at the same technique: **we do it to Congress in class, they do it to a new dataset in Part A, they do it to their own data in Part B.**

### Standing rules for Part B

- **Not every technique fits every project.** Part B is always: apply the day's technique to your pipeline, *or* justify in a paragraph why it doesn't apply and complete the stated alternative. The justification is graded as design reasoning and earns full credit.
- **Topic and sources lock Friday 9/4** (Lab 1B) — far earlier than the old first check-in. Part B is a dependency chain; a student blocked on data access in week five is blocked all semester.
- **Keep an approved fallback dataset ready.** Some students' first-choice source will fall through — an API approval that never arrives, a site that blocks scrapers, a license that won't permit republication. Plan for it in August rather than improvising in October.

### Lab due dates (all 11:59pm)

| Lab | Topic | Issued | Due | Pts |
|---|---|---|---|---|
| 0 | Setup (ungraded) | before term | **before 8/25** | — |
| 1 | Environments + **topic lock** | Thu 9/3 | **Fri 9/4** | 20 |
| 2 | Dockerfiles and Compose | Thu 9/10 | **Fri 9/11** | 20 |
| 3 | Secrets and flat files | Thu 9/17 | **Fri 9/18** | 20 |
| 4 | APIs at scale | Thu 9/24 | **Fri 9/25** | 20 |
| 5 | Scraping + entity resolution *(double)* | Thu 10/1 | **Fri 10/16** | 20 |
| 6 | Schema design + SQL *(double)* | Tue 10/20 | **Fri 10/30** | 20 |
| 7 | Idempotency, testing, code review | Thu 11/12 | **Fri 11/20** | 20 |
| 8 | Visualization + working dashboard *(double)* | Thu 11/19 | **Fri 12/4** | 20 |

### GitHub check-in dates (all 11:59pm)

Five checkpoints on the in-class Congress repo, placed at the end of each unit so each one covers a coherent block of live coding.

| Check-in | Covers | Due | Pts |
|---|---|---|---|
| 1 | Sessions 1–7 — skeleton through Compose and secrets | **Fri 9/18** | 12 |
| 2 | Sessions 8–13 — flat files, APIs, scraping, entity resolution | **Fri 10/9** | 12 |
| 3 | Sessions 14–19 — wrangling, schema, SQL, database engines | **Fri 10/30** | 12 |
| 4 | Sessions 20–24 — EDA, orchestration, testing, visualization, Dash | **Fri 11/20** | 12 |
| 5 | Sessions 25–26 — dashboard build and deployment | **Fri 12/4** | 12 |

Check-ins 1 and 5 land on the same dates as Labs 3 and 8, and 3 and 4 share dates with Labs 6 and 7 — but a check-in is a glance at `git log` on a repo they've been pushing to all along, not a new deliverable, so the collision costs students nothing.

---

# Schedule

## Part 0 — The Walking Skeleton

The whole pipeline, badly, in the first week. Everything after this is a repair.

### **Tue 8/25 — Session 1: Introductions, syllabus, and the first pull**

**No prior Git experience assumed, and no session spent on it.** Installation and — critically — GitHub authentication happen before the semester in the Lab 0 module, so class time goes to the ritual rather than the setup. Git is not a topic in this course; it's something we do 27 times.

**Ten minutes on Git, total:** confirm every clone worked, hand out the command card, and do one `add` / `commit` / `push` together as a group. Five commands, no branching. State the **amnesty policy out loud** — if Git breaks in a way you can't fix, delete the folder, re-clone, and message me; anything pushed is safe. Every cohort has a student who lands in a detached HEAD and quietly stops pushing out of embarrassment, and naming the escape hatch in advance is worth more than any tutorial. Pair anyone who looks nervous with a Git-experienced classmate; the collaboration policy already permits it.

> **Dashboard build.** Everyone clones the course repo. We write `pull_members.py`: a single `GET /v3/member?limit=20`, `json_normalize` the response, write `data/members_raw.csv`. **We paste the API key directly into the script** — and I say out loud that this is a security bug we will fix on 9/15, so it lands as foreshadowing rather than sloppiness. Commit, push, verify on GitHub before anyone leaves.

> **Git thereafter — 90 seconds per week, at the push ritual that already ends every class.** `git log` on 9/1. `.gitignore` on 9/15, which that session needs anyway for `.env`. `git diff` on 9/22. `git switch -c catchup <date-tag>` on 10/1, doubling as the make-up mechanism for a missed class and the most persuasive possible demonstration of what version control is for. Branches and pull requests on 11/12, when Session 22 wires validation into GitHub Actions and Lab 8 needs a PR for CI to run against — by then they have twenty sessions of muscle memory and it takes ten minutes. Total added cost across the semester: about fifteen minutes.

### **Thu 8/27 — Session 2: Skeleton, part 2 — chart, app, push**

> **Dashboard build.** A seaborn countplot of our 20 members by party, saved to `figures/`. Then a 30-line Dash app: one dropdown of 20 names, one callback, a div showing name, state, and party. It runs on `localhost:8050` and it is genuinely ugly. Push it.

Spend the last 20 minutes cataloguing aloud everything wrong with what we just built. **Write the list on the board and photograph it.** It's the course roadmap, generated by the students rather than handed to them, and every subsequent session opens by crossing something off it.

Let them name the problems — they will find most of these unprompted, and the ones they own are the ones that stick. Prompt for anything missing. The list, with where each one gets fixed:

| # | "What's wrong with this?" | Fixed |
|---|---|---|
| 1 | The API key is sitting in the script, in a public repo | **9/15** — `.env`, `.gitignore`, and rotating the leaked key |
| 2 | It only runs on my machine — undeclared dependencies | **9/1** — conda environments and pinned requirements |
| 3 | It won't run on *your* machine, and I can't prove it will | **9/3–9/8** — Docker images, built once and run anywhere |
| 4 | 20 members isn't 535, and bills number in the thousands | **9/24** — pagination, rate limits, backoff, caching |
| 5 | A pile of CSVs is not a place to keep data | **9/10, 10/20–10/22** — Postgres, schema design, 3NF |
| 6 | Re-running it gives different numbers, and nothing catches that | **11/10, 11/12** — idempotent upserts, watermarks, validation |
| 7 | The data is frozen the moment we pull it; Congress votes daily | **11/10** — incremental loading and scheduling |
| 8 | One source is one story — where are votes, money, and news? | **9/17, 9/24, 9/29** — flat files, the FEC, scraping |
| 9 | The names in Voteview don't match the names from this API | **10/1, 10/8** — crosswalks, fuzzy matching, provenance |
| 10 | Some of this text won't fit in a table at all | **10/29** — named as a category; we choose not to build one |
| 11 | The chart is ugly and says nothing to a non-specialist | **11/17, 11/19** — visualization for a public audience |
| 12 | Nobody outside this room can open it | **12/3** — deployment to a real host |
| 13 | *(Ask if nobody raises it)* Should all of this be public? | **12/3** — the ethics of the artifact |

Item 13 rarely comes up on day two, and that's worth noticing out loud: we build first and ask later, which is the default failure mode of the field and the reason 12/3 exists.

> **LAB 0 — opens two weeks before the semester, due before Session 1. Ungraded.** Moved off 8/28 and out of class entirely. Four installs, a GitHub account with working authentication, one line pushed to a **fork** of `jkropko/ds6600-warmup`, and all four credential requests submitted. Verification is just reading the repo's fork list before 8/25 — two minutes at this cohort size, and it hands you the roster of who is stuck **before** the first class rather than after.
>
> Distributed as a written module only. The real time sink is never `commit` and `push`; it's SSH keys, personal access tokens, 2FA, and the Windows credential manager — individually variable, and exactly what evaporates twenty minutes of class while everyone watches one student fight a passphrase prompt. Since there's no video to fall back on, the module leans on an explicit "email me if you're stuck more than 15 minutes" instruction, and it's worth checking the fork list a few days before 8/25 so you can reach out to anyone who hasn't appeared rather than waiting for them to ask.

> **Fork for Lab 0; save GitHub Classroom for the graded labs.** A fork needs no infrastructure, uses a URL that already exists, and teaches a real GitHub concept. It also can't self-verify — Actions are disabled by default on forked repos — but automated verification isn't worth building for a one-off ungraded check with a PhD-sized cohort. From **Lab 1 onward** the calculus flips: Part A is autograded through Actions, submissions should be private rather than public forks, and per-student repos from a template are worth the setup. Stand Classroom up in August for Labs 1–9, not for Lab 0.

> **Before the semester:** send the Lab 0 module with the welcome email. Congress.gov and api.data.gov keys are instant; **OpenSecrets bulk approval can take weeks and must be started in August.** Nothing else needs a credential.

---

## Part 1 — Reproducibility and Environments

Cut from seven sessions to five. Each one opens by crossing an item off the 8/27 board.

### **Tue 9/1 — Session 3: Python environments and conda**

> **Dashboard build.** Our skeleton imports pandas, requests, seaborn, and dash, and declares none of them. We build a clean `ds6600` conda environment from nothing, install into it until `pull_members.py` runs, and export both `environment.yml` and a pinned `requirements.txt`. Then I deliberately install a wrong pandas version, run the script, and we read the traceback together — this is why pinning is not pedantry.

### **Thu 9/3 — Session 4: Introduction to Docker**

> **Dashboard build.** I ask a Mac student and a Windows student to run the same skeleton and we compare what breaks. Then we pull `python:3.12-slim`, run it interactively, `pip install requests` inside it, and execute the member pull from within the container — proving the same code produces the same result on every laptop in the room.

> ### **LAB 1 — due Fri 9/4**
> **Part A:** A repo whose `requirements.txt` fails on a clean machine. Diagnose it, produce a working conda environment and a correctly pinned requirements file, reproduce a specified output.
> **Part B — TOPIC LOCK:** Topic proposal plus three candidate sources. For each: license and terms-of-use check, access mechanism, current status of the credential request. *Rationale:* why this topic, and what question the dashboard answers — and how you expect these sources to relate to each other, since **the final project requires a database with at least two related tables.** Flagging that here, ten weeks before it binds in Lab 6, is what keeps a student from locking a single-source topic in September and discovering the problem in November.

### **Tue 9/8 — Session 5: Dockerfiles; running images from DockerHub**

> **Dashboard build.** We write the project's first Dockerfile — `FROM python:3.12-slim`, copy requirements, `pip install`, `CMD python pull_members.py` — and build `congress-pipeline:0.1`. Push to DockerHub, then everyone pulls a *neighbor's* image and runs it. The member CSV comes out identical, which is the whole point.

### **Thu 9/10 — Session 6: Docker Compose — app plus a real database service**

> **Dashboard build.** We add a `postgres` service to `docker-compose.yml` and rewrite the pull to `INSERT` the 20 members into a `members` table instead of writing CSV. The first attempt fails on connection refused, because the script says `localhost` and Compose networking wants the service name — a five-minute error worth every second, since it's the same error they'll hit in December on the deployed host.

> ### **LAB 2 — due Fri 9/11**
> **Part A:** Write a Dockerfile for a given application, build it, produce a specified output. Then a compose file adding a Postgres service; demonstrate the app connects.
> **Part B:** Containerize your own repo and push the image to DockerHub. One successful "hello world" pull from each of your three sources, proving access is real. *Rationale:* which source is primary, and what breaks if it disappears?

### **Tue 9/15 — Session 7: Volumes, networking, environment variables, and secrets**

> **Dashboard build.** `docker compose down`, then `up` — our members table is empty. We add a named volume and watch the data survive. Then we cross the first item off the 8/27 board: the Congress API key moves out of `pull_members.py` into `.env`, referenced by `env_file` in Compose, with `.env` in `.gitignore`. We now have four credentials to manage, not one. I demonstrate that a key baked in with `ARG` is still readable via `docker history`.

> **⚠️ You cannot rotate the Congress key, and that changes this session.** api.data.gov — which serves both Congress.gov and openFEC — has **no self-service key regeneration**. Their agency manual describes revocation as something agency admins do on request, after the user proves ownership by email. There is no button.
>
> **Demo rotation with a GitHub or DockerHub access token instead.** Both have clean create-and-revoke flows, both are one settings page, and every student has both accounts from Lab 0. Create, use, revoke, watch it fail — three minutes, and they see a credential actually stop working, which is the part that lands.
>
> **Then use the Congress key as the counterexample, which is the better lesson.** It's a real credential, genuinely exposed in a public repo since 8/25, and the provider gives you no way to revoke it yourself — you'd have to email the agency and prove you own it. That's a more honest picture of incident response than a tidy button. The practical substitute is **abandonment**: generate a fresh key, use that one, stop using the exposed one. Name it as weaker than revocation, because it is.
>
> **On whether exposing it on 8/25 is acceptable — yes, and say why out loud.** A Congress key is read-only access to public data with no billing attached; the worst case is someone burning your hourly rate limit, which clears itself. It has no black-market value because anyone can get one free in thirty seconds. **That's precisely why it's the right credential to be careless with**: the habit has to form on a key where a leak costs nothing, so that it holds on one where it doesn't. Say the risk accurately rather than dramatizing it — a student who later works out that the key was harmless will discount the whole lesson if you implied otherwise. Offer an opt-out for anyone uncomfortable; they've simply done the fix early.
>
> One detail worth teaching: these keys are plain 40-character alphanumeric strings with no distinctive prefix, so GitHub's secret scanning almost certainly won't flag them. Well-designed credentials carry identifiable prefixes precisely so scanners can catch leaks. This one doesn't — so nothing will catch it but you.

### **Thu 9/17 — Session 8: Flat files**

CSV, Excel, fixed-width, and **Parquet**. Stata/SAS/SPSS demoted to a reading with a `pandas` one-liner — keep them discoverable, stop spending a third of a session on them.

> **Dashboard build.** Two flat-file sources arrive with no API between them. Voteview's `HSall_members.csv` and `HSall_rollcalls.csv` download freely; **the OpenSecrets bulk files require the account we registered in August**, and we talk about why a source that was a REST API in 2024 is a gated ZIP file in 2026 — data access is a moving target and pipelines have to survive it. We inspect dtypes and find ICPSR numbers silently read as integers, `state_icpsr` losing leading zeros, and NOMINATE columns typed as strings wherever a footnote character appears. OpenSecrets' pipe-delimited format needs its own reader entirely. We fix dtypes on read, write to Parquet, and compare file size and load time against the CSV.

> ### **LAB 3 — due Fri 9/18**
> **Part A:** A deliberately awful file set — fixed-width with a separate layout document, Excel with merged multi-row headers, Parquet with conflicting dtypes. Load all three, reconcile the schemas, report reconciled row counts.
> **Part B:** One raw pull from each source landed in `data/raw/` as Parquet. Credentials in `.env`, `.env` in `.gitignore`. *Rationale:* state the grain of each source — one row equals what, exactly?

---

## Part 2 — Data Acquisition

### **Tue 9/22 — Session 9: APIs I — authentication, requests, and JSON**

*The FEC is introduced here rather than on 9/24, so that session can do pagination and caching properly on two APIs instead of meeting a new one mid-lesson.*

> **Dashboard build.** We move from the toy 20-member call to the Congress API properly: header-based auth, checking `response.status_code` before parsing, and handling `GET /v3/member/{bioguideId}`, whose response nests `terms`, `partyHistory`, and `leadership` several levels deep. We flatten it with `json_normalize` and hit the real question — one member has many terms, so what is one row? I force a 404 with a bad bioguide ID and a 403 with a bad key so the error paths get written today, not in November.

### **Thu 9/24 — Session 10: APIs II — pagination, rate limits, retries, and caching**

> **Dashboard build.** Two APIs, two pagination strategies — which is the point. The Congress API caps at `limit=250` and pages by `offset`, so all 535 members takes three calls and every bill of the current Congress takes hundreds. **openFEC** pages at 100 results and warns against offset paging entirely on large result sets: we implement **keyset pagination** with `last_index`, and I show why naive page numbers silently drop and duplicate rows when new filings land mid-pull. That's a harder and more honest pagination problem than anything the Congress API poses. We add exponential backoff on 429, cache raw responses keyed by a hash of the request URL, and re-run the whole pull in two seconds with zero API calls — the moment students stop being afraid of re-running their own code.
>
> *Note the rate-limit budget: a registered api.data.gov key allows 1,000 calls/hour at 100 results per page — 100,000 records/hour, which the caching taught today is designed to make sufficient. The FEC will grant 7,200/hour on request to APIinfo@fec.gov, but **send that request yourself in August rather than having fifteen students email a small agency inbox in the same week.** Asking for more capacity before hitting a limit also teaches the wrong reflex; the point of this session is that a well-written client doesn't need the raise.*

> ### **LAB 4 — due Fri 9/25**
> **Part A:** A paginated, rate-limited API. Retrieve the complete result set with backoff and on-disk caching, then prove idempotency: run twice, get byte-identical output.
> **Part B:** A paginated, cached, rate-limit-respecting client for your primary source. *Rationale:* estimate full-pull volume and wall-clock runtime, and say how you'll avoid re-pulling during development.

### **Tue 9/29 — Session 11: Web scraping with BeautifulSoup**

> **Dashboard build.** We need bill text, so the obvious move is to scrape congress.gov — and the first thing we do is read its `robots.txt` and terms of use on screen. They contain disallow rules and an explicit warning that ignoring them gets you blocked. Then we notice something better: **GPO already publishes every bill as bulk XML** at `govinfo.gov/bulkdata/BILLS`, organized by Congress and bill type, one ZIP per type. Twenty thousand requests collapse into eight downloads, with no key and no rate limit.
>
> **So we decide not to scrape it, and that decision is the lesson.** Knowing when *not* to write a scraper is a real skill and almost nobody teaches it. The rule goes on the board: **when a bulk distribution exists, use it; APIs are for incremental updates and targeted queries.** We pull one bill-type ZIP live, unzip it, and look at the XML structure — sections, subsections, the enacting clause as its own element — which is also the answer to a problem we'll hit on 11/5.
>
> **Then we do write a scraper, against a legitimate target.** Member press-release pages and committee sites carry material that exists in no API and no bulk repository. That's where BeautifulSoup earns its keep: parsing the table, following links, sleeping politely between requests. Framing question at the end: the scraper is the most fragile thing we will build all semester, so build one only when nothing else will do.

### **Thu 10/1 — Session 12: Entity resolution I — identifier crosswalks**

> **Dashboard build.** We now hold four identifier systems for the same 535 people: bioguide IDs from Congress.gov, ICPSR numbers from Voteview, FEC candidate IDs from openFEC, and CIDs from OpenSecrets. We try the naive thing — merge Congress API members onto Voteview on name — and look at the match rate together. It's bad, and instructively so: `Michael "Mike" Kelly`, `Robert C. "Bobby" Scott`, suffixes, hyphenated names.
>
> Then we go find the crosswalk instead of building it. Voteview ships a `bioguide_id` column, and the `unitedstates/congress-legislators` YAML carries bioguide, ICPSR, FEC, and OpenSecrets IDs in one file. **The FEC entry is a list, not a scalar** — members accumulate multiple candidate IDs across cycles and across chambers — so the crosswalk is one-to-many the moment campaign finance enters, and every downstream contribution total depends on getting that fan-out right. We build `member_crosswalk` with a row per (bioguide_id, fec_candidate_id) pair and establish that no such bridge exists at all to names in news text, which sets up Thursday.

> **LAB 5 issued today.** The crosswalk half is buildable over the break; fuzzy matching arrives 10/8.

### ~~Tue 10/6~~ — **FALL BREAK, NO CLASS**

### **Thu 10/8 — Session 13: Entity resolution II — fuzzy matching and provenance**

**The highest-value addition in this revision** — it's where a multi-source project actually lives, and it transfers to every dataset these students will ever merge.

> **Dashboard build.** The Congressional Record records who spoke and what they said, and refers to them however the chamber's conventions dictate: "Mr. WARNER," "Senator Warner," "the Senator from Virginia" — and, in the House, **"the gentlewoman from California,"** which contains no name at all. There is no identifier anywhere in the text.
>
> **That last form is why this source beats a news feed for teaching entity resolution.** A name-free reference can't be fuzzy-matched, only *inferred* — from chamber, state, and who held the floor. Blocking stops being an efficiency trick and becomes the only thing that works. We still block, score with `rapidfuzz`, and tune a threshold while watching precision and recall move in opposite directions, but roughly a third of references need a different mechanism entirely, and that's the honest shape of the problem.
>
> We store `match_confidence` and `match_method` on every row — the second column matters more here, because "matched on surname" and "inferred from state and chamber" deserve different trust. Ambiguous pairs go to a review queue rather than being guessed. The dashboard will later show a **low-confidence flag** on speeches resolved by inference, which is what honest provenance looks like in a public product.

> **Three verified cases that defeat naive matching.** Use these; they're checked.
>
> - **Mark Udall (D-CO) and Tom Udall (D-NM), Senate 2009–2015.** First cousins, both Democrats, both senators, six overlapping years. They campaigned on "Vote for the Udall nearest you." Their second cousin Gordon Smith was also in the Senate, so "Udall in the Senate" isn't even a two-way ambiguity.
> - **The two Mike Rogers — the best of the three.** Michigan 2001–2015 and Alabama 2003–present: twelve overlapping years, both Republicans, both Representatives, legally Michael J. and Michael Dennis but neither uses the middle name. **String distance scores them 1.0 — a perfect match, confidently wrong.** Nickname normalization doesn't help; only state does, which is precisely the argument for blocking. The Michigan one is now running for Senate in Michigan, so they may reappear in different chambers.
> - **Loretta Sanchez and Linda Sánchez, both D-CA in the House 2003–2017.** First sisters to serve together, sworn in side by side. Same surname, same state, same chamber, same party. **And the accent is the real lesson**: Linda's own House office writes her as *Sánchez* while Loretta appears in most records as *Sanchez*, so the strings don't match — but stripping diacritics to fix that immediately collides the sisters with each other. The obvious fix creates the harder bug.

> **Don't supply the name-change example — have students find one.** `congress-legislators` tracks name variants, so "find a member whose name is recorded differently across two of our sources" is a five-minute exercise that produces a real answer, teaches the lookup, and can't go stale on you. It also lands better than a case handed down: a student who finds their own is the one who remembers that identity is something you establish rather than something the data gives you.
>
> *(I had Mary Bono → Mary Bono Mack → Mary Bono in mind and it's probably right, but I couldn't verify it against the Biographical Directory. Check before asserting it — or just don't, and let the exercise above do the work.)*

### **Tue 10/13 — Session 14: Filtering, recoding, aggregation**

> **Dashboard build.** From the full raw member pull: filter to the current Congress, recode `partyName` into a clean D/R/I code, collapse the minor and independent labels, derive `chamber` from whether `district` is null, and compute `tenure_years` by aggregating each member's nested terms. Then the FEC side: aggregate Schedule E rows to expenditure totals per member per cycle, split by the support/oppose indicator, which is the first time the dashboard's outside-spending panel has numbers behind it.

### **Thu 10/15 — Session 15: Merging and reshaping**

> **Dashboard build.** With the crosswalk in hand, the joins finally behave: members to NOMINATE scores one-to-one, members to sponsored bills one-to-many, bills to cosponsors many-to-many resolved into a bridge table, and members to FEC candidate IDs one-to-many — where I deliberately do the join wrong first, double-count a member with two active candidate IDs, and let the inflated total sit on screen until someone catches it. We also pivot roll-call votes from long to wide, look at the 535-column result, and agree it's a fine analysis shape and a terrible storage shape.

> ### **LAB 5 (double-width) — due Fri 10/16**
> Entity resolution doesn't compress into seven days, and a half-taught version is worse than none.
> **Part A:** Scrape a stable instructor-chosen page, then reconcile two provided identifier lists — deliberately dirty, with nicknames, suffixes, married names, and three genuine non-matches. Report match rate, enumerate unmatched records, demonstrate a false-positive check.
> **Part B:** Define join keys across your own sources; build a crosswalk table carrying confidence and provenance columns. *Rationale:* state your matching rule and threshold and defend the threshold; show five edge cases you resolved by hand.

---

## Part 3 — Wrangling and Databases

### **Tue 10/20 — Session 16: Normal forms, schema design, and documentation**

ER diagrams and dbdocs.io folded in as the deliverable of the design exercise rather than a standalone session.

> **Dashboard build.** I put up a deliberately awful single table: one row per member, committees as a comma-separated string, `party_name` and `state_name` repeated on every row, sponsored bill numbers in a list column, and a single `total_outside_spending` field that quietly conflates support and oppose. We break it to 3NF as a class — `members`, `states`, `parties`, `committees`, `committee_memberships`, `bills`, `sponsorships`, `cosponsorships`, `rollcalls`, `votes`, `speeches`, plus `fec_committees` and `independent_expenditures` — arguing over each decomposition. The campaign finance side forces the sharpest argument, because an expenditure's grain is (spender, target, date, support/oppose) and nothing about that fits on a member row. We publish the ER diagram to dbdocs and it becomes the reference document for the rest of the semester.

> **`speeches` is where provenance columns live next to the data**, and it's worth pointing at. Alongside the speech text and date sit `bioguide_id`, `match_confidence`, and `match_method` from 10/8 — because for this table alone, *how we know* a row belongs to a member is part of the row. Everything else in the schema joins on an identifier we trust; this one joins on an inference. That's what lets the dashboard flag a low-confidence attribution, and it's a habit worth carrying into their own projects.

> **LAB 6 issued today.**

### **Thu 10/22 — Session 17: PostgreSQL in Python**

*Trimmed. DuckDB, the pandas comparison and the SQLite aside all moved to 10/29 — this session was carrying five topics and now carries two.*

> **Framing, stated once at the top.** Tuesday's design works unchanged in any relational engine — same tables, same keys, same SQL. **Schema design is a modeling question; engine choice is an engineering question.** Students who conflate them make both badly. We pick the engine properly on Thursday; today we just build it.

> **Dashboard build.** We create the schema in Postgres through SQLAlchemy and load it — and the load fails on a foreign key violation, because a sponsorship points at a bioguide ID that isn't in `members`. **That's an entity resolution defect from 10/8 surfacing as a constraint error two weeks later**, which is the entire argument for constraints: the database caught a mistake that pandas had been carrying quietly since the merge. Trace it back, fix the crosswalk, reload.

> Then connections, transactions, and the loading patterns they'll use for their own data — `to_sql` versus explicit inserts, and why the fast option is the wrong default when you care about types.

### **Tue 10/27 — Session 18: SQL**

> **Dashboard build.** We write the queries the dashboard will actually call. Bills sponsored per member. A self-join on `cosponsorships` for a member's top ten cosponsorship partners. Party-line voting percentage using window functions. The committee roster. And the one this unit has been building toward: **the gray-money query.** Super PACs disclose their donors on Schedule A, so we self-join receipts against committees to find super PACs whose own largest donors are 501(c)(4) organizations — money that is disclosed one layer and dark the next. Each query gets saved to `sql/` as a named file; by December these are the callback bodies.

### **Thu 10/29 — Session 19: DuckDB, and choosing an engine**

*Split off from what used to be a single overloaded database session. 10/22 now does Postgres and the constraint violation; this one does DuckDB and the engine question.*

> **Dashboard build.** DuckDB reads our Voteview and FEC Parquet files **in place** — no server, no load step, no schema declaration — and we time the same aggregation against Tuesday's Postgres tables to see the gap.

> **Two or three minutes on why DuckDB is faster here, and it isn't "because it's local."** It reads only the columns the query touches and processes them in batches of a couple thousand values rather than one row at a time. Postgres walks rows through an operator tree; DuckDB runs tight loops over contiguous typed arrays. Tie it back to 9/17: **Parquet was columnar layout at rest, DuckDB is the same idea in motion.** That one sentence is what students should retain — not a taxonomy.

> **Then the division of labor, stated plainly.** **Postgres is the dashboard's database**: it's the deployment target, it enforces the constraints, it handles concurrent reads from a live web app, and it takes the incremental writes we build on 11/10. **DuckDB is the analyst's tool**: scan-heavy aggregation over files, exploratory work, and anything where standing up a server is more trouble than the question is worth. A student who reaches for DuckDB to serve the dashboard has misread the assignment.

> **Then the question students will actually have: how is this different from pandas?** They learned filtering and aggregation in pandas two weeks ago and SQL two days ago. Left unaddressed, they conclude there are three arbitrary ways to do everything.
>
> The line: **if it's a join or a group-by over something big, write SQL; if it's shaping data for a plot or a model, use pandas.** DuckDB wins on memory (it streams and spills to disk rather than needing the frame in RAM), on joins (its planner reorders them and pushes filters down), and on null handling (an integer column silently becomes float the moment pandas sees a NaN — one of the seeded defects in Lab 8). pandas wins on iterative exploration, row-wise functions, reshaping, and every handoff to seaborn, plotly, and scikit-learn.
>
> Defuse the rivalry by showing they interoperate: `duckdb.sql("SELECT party, AVG(nominate_dim1) FROM members_df GROUP BY party")` queries a pandas DataFrame **by its Python variable name**, zero-copy through Arrow, and `.df()` hands the result back. **Anything headed for a dashboard callback is SQL**, because that query runs against Postgres in December no matter how convenient pandas felt in October.

> **Note on SQLite — ten minutes at the whiteboard, no code.** Most deployed database in the world, `sqlite3` ships in the standard library, and it's the honest fallback for a student whose project data is small. The instructive detail: **SQLite doesn't enforce foreign keys unless you turn on the pragma**, so Tuesday's failed load would have silently succeeded. Good argument for why the simplest possible database is the wrong choice when you want the database catching your mistakes.

> **Document stores — fifteen minutes, concept only, no toolchain.** We are not building one, but students should leave knowing the category exists. Bill text and floor speeches are the example: variable length, nested sections, no sensible column width. Name what a document store is, when you'd reach for one, and why we aren't — our data is overwhelmingly relational, and running a second database for one table is a cost without a return. **The judgment is the transferable part**; MongoDB's syntax is not.

### **Thu 11/5 — Session 20: Non-visual exploratory analysis**

*Un-merged from what was a single EDA-plus-visualization session. Freed up by cutting the document store and TF-IDF.*

> **Dashboard build.** What's actually in the data, before we make any claims about it. Cross-tab of chamber by party. The distribution of bills sponsored, which is severely right-skewed — and a live argument about which number belongs on a public dashboard when the mean and the median disagree substantially. There's a defensible answer either way, and the argument is the point.

> **Then the relationships.** Correlation between tenure and sponsorship count. Party-line voting rates by chamber. And the one worth dwelling on: outside spending against ideology score, where **the interesting cases are the residuals rather than the trend** — members who attract far more spending than their position predicts. That's a finding rather than a summary, and it's the kind of thing the dashboard exists to surface.

> **Frequency tables, cross-tabs, simple hypothesis tests, measurement models.** None of it is glamorous, and all of it is what stops you publishing a chart of an artifact.

> **This session is deliberately unhurried.** It replaces the search-and-TF-IDF session and relieves 11/17, which was carrying EDA and visualization together. If it runs short, the spare time goes to the skew argument — it's the one that changes how students think about summarising anything for a general audience.

### **Tue 11/10 — Session 21: Incremental loading and orchestration**

**This is the session that most distinguishes data engineering from data science with a database.** If anything gets deferred to DE2, defer the hands-on orchestration tooling, not the concepts.

> **Dashboard build, pattern 1 — incremental with a watermark.** Bills change slowly enough that a watermark on `updateDate` handles them: query what's newer, upsert, done.

> **Pattern 2 — supersede-on-amendment.** Independent expenditures do not behave: **groups must report them within 24 or 48 hours**, filings get amended, and amendments supersede earlier rows — so an append-only load double-counts spending, and re-pulling everything nightly is infeasible at FEC volume. We write upserts with `ON CONFLICT DO UPDATE` keyed on filing identifiers, handle the supersede flag, run the load twice, and confirm row counts don't move.

> **Pattern 3 — full-file regeneration with retroactive value changes.** Voteview is the one that breaks the model we just built, which is exactly why it's here. It publishes regenerated bulk CSVs rather than a delta endpoint, so **there is no watermark to read** and truncate-and-reload is often the correct strategy — a useful contradiction of the session's implicit lesson that incremental always wins. Worse: **NOMINATE scores are re-estimated over the full history**, so adding new roll calls shifts the scores of members whose data we thought was settled. This isn't "new rows arrived." It's "values we already stored are now different." Flag out loud that a row-count check cannot detect this, and hand the problem to Thursday.

> **The taxonomy is the real content — put it on the board.** Six sources, five patterns. Implement three, name the rest.
>
> | Source | Pattern | Strategy |
> |---|---|---|
> | Bills (Congress API) | Incremental, append-mostly | Watermark on `updateDate` |
> | Bill text (GPO + API) | Bulk backfill, then API tail | Replace once, then delta |
> | Roll calls (Voteview) | Full-file regen, **retroactive changes** | Truncate-reload + checksum on scores |
> | FEC filings | 24/48-hour notices, amendments supersede | Upsert keyed on filing ID |
> | Congressional Record (GPO) | Append-only, permanent archive | Watermark on issue date |
> | OpenSecrets bulk | Months-lagged | Effectively static this semester |
>
> **Name the lossy category even though we no longer have one.** Every source we use is permanently archived, so nothing here punishes you for skipping a run. That is not typical. Social media firehoses, many commercial news APIs, and most streaming endpoints expose only a rolling window — miss the window and that data is gone, permanently, for everyone. **Several students will have a source like this in their own projects**, and they need to recognize it before they lose a month. Thirty seconds, and it's the one row on the board with no example behind it, which is worth saying out loud.

> **The Congressional Record pipeline completes here, and it's the cleanest illustration of the pattern.** The GPO bulk downloads from 9/29 gave us a **backfill**: every issue through the snapshot date, in a handful of files. Issues published since then aren't in that download, and re-fetching gigabytes nightly to catch a few days would be absurd. So the daily bulk feed becomes the **delta** — fetch only what's newer than the watermark, parse, upsert. **Bulk for history, incremental for the tail.** Say it plainly, because it's the same shape as almost every production pipeline students will meet, and 9/29 set it up specifically so this moment would land.

> **Then orchestration, and start from cron.** Write the pipeline as `0 3 * * * python pipeline.py`, then ask what it tells you when it fails at 3am. Nothing: no retries, no dependency graph, no run history, no alert. That gap is the argument. **Prefect** is the demo — plain Python functions with `@task` and `@flow` decorators, minimal setup, and a local UI that shows a run actually failing at step four. Three cadences make the dependency graph earn itself: nightly bills, hourly FEC during an election window, weekly Voteview. Name **Airflow** (industry standard, heavyweight — scheduler, webserver, metadata DB before the first DAG runs) and **Dagster** (asset-centric: declare the tables you want to exist rather than the tasks to run, which maps unusually well onto this course) as the alternatives they'll meet. Thirty seconds each. Prefect is chosen here only because it's the one that fits in twenty minutes.
>
> **Head off the question students will ask, because it's the right question.** *Do cron and Prefect work together?* They overlap rather than divide: Prefect has its own scheduler and doesn't need cron, and its schedules are often written in cron syntax, which compounds the confusion. The split isn't scheduling versus logic — it's **triggering versus everything around the run**. Cron executes a command at a time and knows nothing else: not what it does, not whether it worked, not whether step three failed while steps one and two succeeded. Prefect wraps execution — retrying a failed task without rerunning successful ones, enforcing that entity resolution waits for both pulls, recording durations, surfacing failures, allowing a single step to be rerun. Note also that Prefect is **not** where validation lives; Pandera and pytest are Thursday's content, and Prefect only decides what to do when a check fails.
>
> **Last task in the flow: refresh the `member_summary` materialized view.** It won't mean much today. It will on 12/1, when we discover the dashboard's performance problem is solved in the pipeline rather than the web layer.

### **Thu 11/12 — Session 22: Testing, data validation, and reviewing generated code**

XKCD #2054 is already printed in the syllabus; this is the session that answers it. Also the natural home for agent code review: **you can only safely delegate what you can verify.**

> **Dashboard build.** We write a Pandera schema for `members` — bioguide ID unique and non-null, state within the valid set including DC and territories, NOMINATE dimension one bounded to [-1, 1], party in the allowed enum — plus a referential integrity check from sponsorships back to members, a row-count delta alarm on the daily load, and a sum check on independent expenditures against the FEC's own published committee totals, which is the only external ground truth we have all semester. One check fails immediately on real data, which is the best outcome available.

> **Then the check that answers Tuesday's cliffhanger.** Voteview re-estimates NOMINATE over the full history, so a reload can change `dim1` for members who haven't cast a new vote — **row counts stay identical while the values underneath move.** Every check written so far is blind to this. The fix is a checksum or a hash over the derived score columns, compared run to run, or an explicit join of old against new on bioguide ID asking whether any existing member's score shifted beyond a tolerance. Then the judgment call, which is the actual lesson: **a changed score is not necessarily an error.** Re-estimation is the data working as designed. What we need is not a failure but an *alert* — something that tells us the dashboard's ideology figures moved and that the methodology note may need updating. Distinguishing "this is broken" from "this changed and someone should know" is most of what validation is for, and it's the distinction a row-count alarm can't express.

> **The agent code review moves into Lab 8 entirely.** In class we spend five minutes setting it up — here's the code, here's what you're looking for, here's why reading generated code is now a large part of the job — and the reviewing itself happens on their own time, where it's worth more anyway. This session was carrying four validation checks, the retroactive-change problem and a code review, and something had to give.

> ### **LAB 7 — issued 11/12, due Fri 11/20**
> **Part A, two pieces.** (i) Given a table and an incoming batch containing overlaps, updates, and one deletion, write an idempotent upsert. (ii) **Agent code review:** you're handed agent-generated pipeline code with five seeded defects — a silent dtype coercion, a non-idempotent insert, an unbounded pagination loop, a hardcoded credential, and a reload that silently overwrites derived values while leaving the row count unchanged. Find them, explain each failure mode, and write the validation check that would have caught it. *Graded on the review, not on rewriting the code.*
> **Part B:** Make your own load idempotent, add four validation checks, wire at least one into GitHub Actions. *Rationale:* what silently wrong output is each check protecting against?

---

## Part 4 — Analysis and Delivery

### **Tue 11/17 — Session 23: Exploratory analysis and static visualization**

*(These were separate sessions in the earlier draft; merging them is what makes room for the optional day on 11/24.)*

> **Dashboard build.** Cross-tab of chamber by party. The distribution of bills sponsored, severely right-skewed, and a live argument about which of mean and median belongs on a public dashboard. Then the analysis this unit was rebuilt for: **outside spending per member, split by support versus oppose and by donor-disclosure status.** The first thing students see is that the distribution is wildly concentrated — a handful of members in competitive races absorb most of it — and the second is that "opposed by $4M" is a very different fact from "supported by $4M" and cannot share an axis. We build the figure with a diverging scale, labeled axes, a source note, and a colorblind-safe palette, because this one is going in front of the general public.

### **Thu 11/19 — Session 24: Interactive visualization, and Dash callbacks**

*Dash syntax moved here from 12/1. It belongs with plotly — same toolchain — and **Lab 9 asks for a two-callback Dash app**, so teaching it after the lab was issued was an ordering bug.*

> **Dashboard build.** The NOMINATE scatter becomes interactive: hover reveals name, state, and party; color encodes party; selection filters the member list. Then the outside-spending panel: a diverging bar of support versus oppose per member, with hover showing the top spending committees and their disclosure status. The design constraint is stated explicitly — our audience is citizens, not political scientists, so every hover label has to make sense without a methods section, and "501(c)(4)" is not a label a general reader can parse.

> ### **LAB 8 (double-width) — issued 11/19, due Fri 12/4**
> Spans Thanksgiving deliberately: the break is the work time, and this replaces the old third project check-in, so nobody discovers on the final weekend that their dashboard doesn't run.
> **Part A:** Convert two provided static figures to interactive plotly, then build a two-callback Dash app against a provided database.
> **Part B:** Three publication-quality figures from your own data, plus a working local dashboard driven by your own database with at least one interactive control. *Rationale:* what claim is each figure making and for whom — and what's still broken, with your plan for the final week?

### **Tue 11/24 — OPTIONAL: Dashboard work session and design clinic**

No new material, nothing assessed, attendance entirely optional. Instructor in the room and on Zoom for drop-in help with Lab 9. Students who need to travel lose nothing.

> **Dashboard build.** Open work time on students' own dashboards. For anyone who attends, I'll take requests against the Congress dashboard — usually the callback that won't fire or the query that takes nine seconds. Announce this in August so travel can be booked early, and confirm it in the 11/19 class.

### ~~Thu 11/26~~ — **THANKSGIVING, NO CLASS**

### **Tue 12/1 — Session 25: Assembling the dashboard, and making it fast**

*Callbacks were taught on 11/19, so this session is assembly plus the performance ladder rather than both syntax and engineering in 75 minutes.*

Students have had a working (bad) Dash app since 8/27 and a better one from Lab 9, so this is refinement rather than first contact.

> **Dashboard build.** The real thing: a dropdown of all 535 members driving a multi-output callback that fills the biography card with photo, party, state, and tenure; the committee list; voting statistics; the sponsored bill table; the outside-spending panel with its disclosure-status breakdown; and floor speeches with their confidence flags. Switching members takes several seconds. Fixing that is the last engineering lesson of the semester, and it goes in a specific order.

> **Step 1 — profile before touching anything.** `EXPLAIN ANALYZE` on the actual callback query, on screen. **Caching a query you haven't read is how you get a fast dashboard serving wrong answers.** A 535-row dropdown should never be slow, so when it is, the cause is almost always one of two things: a **missing index** — `sponsorships(bioguide_id)`, `votes(bioguide_id)`, `independent_expenditures(candidate_id)`, without which every selection sequentially scans a large table — or an **N+1 query**, a callback looping over a member's twenty bills issuing one query each, which is a join wearing a disguise. Adding the indexes often takes the callback from three seconds to thirty milliseconds, and then there is nothing left to cache.

> **Step 2 — the architectural move: precompute rather than cache.** This dashboard is unusual in a way worth naming. **The data changes once a night**, from the Prefect flow we built on 11/10. Recomputing a member's outside-spending total on every page view and then caching it to avoid recomputing is solving the problem one layer too high. Build a `member_summary` materialized view — sponsorship counts, party-line percentage, support and oppose totals, top keyword terms — so the dashboard does one indexed lookup by bioguide ID. Then **make the refresh the last task in the nightly flow**, which puts freshness under the pipeline's control rather than the web layer's. That closes the loop: Session 21 built the pipeline, and Session 25 discovers the pipeline is where the dashboard's performance actually lives.

> **Step 3 — memoize only what's genuinely dynamic.** A search box or a user-chosen date range can't be precomputed, so `@cache.memoize()` from Flask-Caching handles those. `functools.lru_cache` is simpler and works, but say why it's the wrong choice for deployment: it's in-process, so four gunicorn workers means four independent caches and none survive a restart. FileSystemCache is shared across workers on one host; Redis is the answer once there's more than one container — which there will be on Thursday.
>
> **The invalidation trick, which is the part worth remembering.** Put a data version in the cache key — the max `updated_at` from the last load, or the pipeline run ID. New data mints new keys automatically, so nothing goes stale and you never write a flush routine. Contrast with time-based expiry, which is strictly worse here: a 24-hour timeout set at noon still serves yesterday's numbers after the 3am refresh.

> **Step 4 — name two things that look like caching and aren't.** `dcc.Store` puts data in the *user's browser*, per session — fine for small intermediate state, bad for a 535-member reference table you'd be shipping to every visitor. Background callbacks are for genuinely long-running work, not a two-second query. Students reach for both by default; say so before they do.

### **Thu 12/3 — Session 26: Deployment, publication, and the ethics of the artifact**

> **Dashboard build.** We push the dashboard image, deploy against a managed Postgres, set environment variables in the host's secret store rather than a file, and connect through a read-only database user. Then the URL goes on the screen and anyone in the world can open it, which is the moment the second half of the session earns.
>
> **Two ethical questions, not one.** First, the contributor panel lists individuals by name, employer, and ZIP code — every byte lawful FEC public record, but aggregation and searchability change what the record *is*. Second, and newer: **our dark-money panel publishes our own classification.** The FEC tells us a committee spent $2M opposing a member; it does not tell us whether that committee discloses its donors. We inferred that from committee type, filing pattern, and the Schedule A chain, and reasonable analysts would draw the line differently. So the dashboard is publishing a contestable judgment under a factual-looking label. We decide as a class what that panel actually says, how the methodology is disclosed to a reader who won't click through, and whether "dark" is a word a neutral transparency tool should use at all. This is course objective 4, and it lands harder because they built the thing.

> **Settle hosting before the semester starts.** "Publish online" needs a specific target — Render, Fly.io, Heroku, or a school-provisioned VM — with a plan for the database and for what happens to student deployments in January.

### **Tue 12/8 — Session 27: Project presentations**

> **Dashboard build.** None — the Congress dashboard is finished and deployed. Students present their own pipelines, and the comparison across topics is the point: fifteen different domains, the same eleven techniques.

---

## Final Deliverable — Data Pipeline Project (180 points)

**Due Monday 12/14, 11:59pm.**

Because eight rounds of Part B have already produced the pipeline, this is **integration and writing**, not construction.

| Component | Points |
|---|---|
| Deployed dashboard — working, interactive, designed for a general audience | 60 |
| Written report formatted for *Data in Brief* | 60 |
| Database documentation — dbdocs or GitHub Pages, with ER diagram | 30 |
| Repository — organized, containerized, validation checks passing | 30 |
| Gen AI use statement | **required, 0 points** |

> **Why the AI statement carries no points.** Required for acceptance, unscored. If provenance is graded, students optimize for looking independent, which inverts the policy. Same reasoning as the `Assisted-by:` commit trailers — the point is honest reporting, and honest reporting is cheapest when it costs nothing.

> **Why documentation is separate from the repository.** Database documentation is a distinct skill taught on 10/20 and it deserves visible weight rather than being folded into a general reproducibility score.

---

## Revised grading bands

The bands on page 5 of the current syllabus leave 255–305 and 210–251 under no rule at all, and the stated percentages don't match the stated point values. Rewritten against **400 points**, which divides more cleanly than 360 did, using your own percentages:

- **A** — 340 or above (85%)
- **A−** — 280 to 339 (70–84.9%)
- **B+** — 200 to 279 (50–69.9%)
- **F** — below 200
- **A+** — an A plus an exceptional final project

Every point total now falls under exactly one rule, with no gaps.

---

## Notes on this draft

**"Dark money received" is a category error, and correcting it is a feature.** Members do not receive dark money in any meaningful volume — a 501(c)(4) cannot contribute to a federal candidate at scale. It spends *independently*, on ads supporting or opposing them. The measurable quantity is outside spending **about** a member, on FEC Schedule E, with a support/oppose indicator. A panel labeled "dark money received by Rep. X" would be wrong, and a transparency project can't afford to be wrong on its own definitions. Make students say the correct sentence out loud on 10/13 before they draw the figure on 11/17.

**Where the data stops is part of the lesson.** The FEC discloses the spending; the 501(c)(4) behind it files a Form 990 whose Schedule B donor list is redacted in every public copy. The chain terminates there by law. Students should be able to point at the exact record where the public trail ends — that's a more valuable outcome than any dataset that pretends it doesn't.

**The dashboard accumulates rather than restarts.** Every session's build depends on the previous one, which means a missed class leaves a hole. Keep the Zoom recordings, and tag the course repo by date at the end of every class so a student who misses 10/22 can run `git catchup 2026-10-22` and rejoin on 10/27 without rebuilding by hand. Tag *every* class day, including the ones where little changed — one gap teaches students the tags are unreliable and they stop checking.

**Four deliberate failures are scheduled.** The hardcoded API key on 8/25 (fixed 9/15); the Compose connection refused on 9/10; the double-counted FEC join on 10/15; and the foreign key violation on 10/22 that traces back to an entity resolution defect from 10/8. These are the highest-value minutes in the course and they only work if you resist fixing them in advance.

**Part A is never Congress data.** In-class work is Congress; Part A is a different domain entirely. That's what tests whether the technique transferred or whether they just memorized our repo.

**Nine labs, not ten.** The Thanksgiving compression left only three sessions between 11/19 and 12/8. Rather than cram two labs into that window, visualization and the dashboard checkpoint merged into one double-width Lab 9 — which lands cleanly at 20 points each.

**Fall break falls mid-topic, and that's usable.** Lab 5 is issued 10/1 after crosswalks and due 10/16 after fuzzy matching, so the break becomes build time on the half students can already do.

**No catch-up days remain.** Folding in entity resolution, orchestration, and testing consumed both. If you want one back, merge Sessions 24 and 25 — plotly and Dash are closely related and students will have built both in Lab 9 anyway.

**Still to verify before August.** The Congressional Record bulk collection now carries the fuzzy matching session on 10/8 — confirm the collection is current and that recent issues are present. Email APIinfo@fec.gov yourself about the 7,200/hour tier and how they'd like a cohort handled — one faculty message, not fifteen student ones. Start OpenSecrets bulk registration immediately; assume it may not clear in time and confirm the dashboard degrades gracefully without industry codes. Note also that the current syllabus names Windsurf as a Copilot-style autocomplete tool; that product is now Devin Desktop, and the category has moved from completion to delegation.
