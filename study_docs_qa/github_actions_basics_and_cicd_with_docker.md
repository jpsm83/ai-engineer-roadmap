# GitHub Actions — CI/CD Workflows — Q&A

---

## Part 1 — Model

### Workflow, job, step, action

**Q: What is GitHub Actions?**
A: GitHub's system for running automation when something happens in a repository. A **workflow** is one YAML file under `.github/workflows`. A **job** is a group of steps on one fresh machine. A **step** is a shell command (`run`) or an **action** (`uses: owner/repo@ref`), a reusable unit whose repository contains `action.yml`. `with` passes inputs into that action.

**Q: How do continuous integration, delivery, and deployment differ?**
A: **Continuous integration** builds and tests every pull request and reports a status check. **Continuous delivery** keeps a releasable artifact, and a person or a protection rule promotes it. **Continuous deployment** promotes every green commit on `main` with no extra click. All three fail closed: a red check does not merge, and a failed test does not deploy.

**Q: What are the stages of a CI/CD pipeline?**
A: (1) Checkout. (2) Restore the dependency cache and install the toolchain. (3) Lint and test. (4) Build the artifact. (5) Scan dependencies and the image. (6) Publish the artifact from a trusted ref. (7) Deploy into an environment. (8) Record the URL and the commit so you can roll back. Stages 1–5 run on pull requests. Stages 6–8 run only after those checks pass on `main`, a tag, or a release.

**Q: What is a gate?**
A: A condition that stops the next stage. A required status check stops the merge. `needs` stops a later job when the earlier one failed. An environment's required reviewers stop a deploy before GitHub assigns a runner. A job `if` stops a publish on a pull request.

**Q: In what order does a run actually happen?**
A: The event matches `on` and its branch, tag, and path filters. Concurrency queues or cancels. The job `if` is evaluated, and for a matrix it is evaluated before the matrix expands. Environment protection rules pass before any runner is assigned. The runner starts, steps run in order, and each action's post step cleans up even when the main step failed.

**Q: What from the 2020 tutorial is still true?**
A: Events start workflows. Jobs run on GitHub-hosted machines, one fresh machine per job, in parallel unless `needs` orders them. `runs-on` selects Ubuntu, Windows, or macOS. A matrix repeats a job. Secrets stay out of the YAML. Ubuntu images already include Docker.

**Q: What from that tutorial should you stop copying?**
A: Trigger on `main`, not `master`. `actions/setup-java` requires `distribution: temurin` and the project's Java version, not a bare `1.8`. Publish with `docker/login-action` and `docker/build-push-action`, not a Marketplace action that takes a Docker password. Set `permissions`. Pass files with artifacts, because `needs` does not copy the workspace. Push only from a trusted ref, and tag the image with `github.sha`.

---

## Part 2 — Triggers

### Events and filters

**Q: Which events does a CI/CD workflow use?**
A: `push` and `pull_request` for integration. `workflow_dispatch` for a manual run from the Actions tab. `workflow_call` when another workflow calls this file. A tag push or `release` for a versioned delivery. `schedule` for a cron of at least 5 minutes, in UTC unless you set an IANA `timezone`, always on the latest commit of the default branch.

**Q: How do you limit a trigger to a branch, a tag, or a path?**
A: Under the event, `branches` and `tags` select refs, and `paths` or `paths-ignore` select changed files. A docs-only change can skip a Java build. A release workflow listens to `tags: ['v*']` instead of every commit on `main`.

**Q: What do `github.ref`, `github.ref_name`, and `github.sha` contain?**
A: For a branch, `github.ref` is `refs/heads/main` and `github.ref_name` is `main`. For a tag, `github.ref` is `refs/tags/v1.2.3`. `github.sha` is the full commit SHA and is the immutable thing you tag an image with. `github.event_name`, `github.actor`, and `github.repository` are the other values a workflow reads constantly.

**Q: Which pull-request activity types run CI by default?**
A: `opened`, `synchronize`, and `reopened`. `synchronize` is a new push to the pull-request branch, so CI re-runs without someone closing and reopening the pull request. Set `types` only when you need a narrower set.

**Q: When does `workflow_dispatch` show a button, and how do inputs work?**
A: The button exists only after the workflow file is on the default branch. Inputs are `string`, `choice`, `boolean`, `number`, or `environment`, at most 25 of them, and the job reads `inputs.<name>`. The `inputs` context keeps booleans as booleans. `github.event.inputs` stringifies them.

**Q: Why would a merge queue stay red after CI passed on the pull request?**
A: A merge queue tests the combined result with the `merge_group` event. A required check that listens only to `pull_request` does not run there. List `merge_group` next to `pull_request` when the repository uses a merge queue.

---

## Part 3 — Jobs and runners

### Order, machines, and matrices

**Q: When do jobs run, and what does `needs` guarantee?**
A: Jobs in one workflow run in parallel. `needs` waits until the named jobs succeed; if one fails or is skipped, every job that needs it is skipped too. It guarantees order and success. It does not copy files, environment variables, installed tools, or a local Docker image onto the next machine.

**Q: Where does a job execute?**
A: `runs-on` picks the machine. GitHub-hosted labels are `ubuntu-latest`, `windows-latest`, and `macos-latest`. Each job gets a new machine, and GitHub destroys it afterward. The default job timeout is 360 minutes. `GITHUB_TOKEN` expires when the job finishes, or after 24 hours.

**Q: When do you use a self-hosted runner?**
A: When the job needs a private network, a special device, or a machine GitHub does not offer. Target it with `runs-on: [self-hosted, linux]`. Do not attach one to a public repository: a pull request runs code on that machine, and the machine is not thrown away between jobs, so a compromise persists.

**Q: What is a matrix, and what do `include`, `exclude`, and `fail-fast` do?**
A: `strategy.matrix` turns one job into one run per combination, up to 256 jobs, each on its own machine. `include` adds a combination, `exclude` removes one, and `runs-on: ${{ matrix.os }}` selects the machine. `fail-fast` defaults to `true`, so the first failure cancels the rest. Set it to `false` when you want every cell's log.

**Q: How do you run a step after a failure or a cancellation?**
A: A step `if` defaults to success. `if: failure()` runs only after a failed step and does not run when the job was cancelled. `if: always()` runs after success, failure, and cancellation. `continue-on-error: true` records the failure and lets the rest of the job continue. `if` on a job is evaluated before its matrix expands.

---

## Part 4 — Expressions and variables

### Contexts, env, vars, and secrets

**Q: What is a context?**
A: An object GitHub fills in before the step runs. The ones a CI/CD file uses are `github`, `env`, `vars`, `secrets`, `steps`, `needs`, `matrix`, `inputs`, `runner`, and `job`. You read them as `${{ github.sha }}` or `${{ steps.id.outputs.name }}`. An `if` is already an expression, so you may omit `${{ }}` there, except when the expression starts with `!`, which YAML would treat as its own syntax.

**Q: Which functions show up in real workflows?**
A: `success()`, `failure()`, `always()`, and `cancelled()` for `if`. `hashFiles('**/gradle/wrapper/gradle-wrapper.properties')` for a cache key. `contains()` and `startsWith()` for refs. `toJSON()` when you need to print a whole context while debugging. Expressions are resolved while the script text is being built, which is why untrusted event data must not sit inside `run`.

**Q: How do `env`, `vars`, and `secrets` differ?**
A: `env` is an environment variable on the runner, set in the workflow, the job, or the step. The more specific level wins: step overrides job, job overrides workflow. `vars` are configuration values from Settings → Secrets and variables → Actions, read as `${{ vars.NAME }}`. `secrets` are the same screen's credentials, read as `${{ secrets.NAME }}`, and they are masked in logs. A Docker Hub username is a variable. Its access token is a secret.

**Q: Which secret wins when the same name exists in several places?**
A: The most specific one. An environment secret overrides a repository secret, which overrides an organization secret. The same order applies to variables. Put production credentials on the `production` environment so a job that does not name that environment cannot read them.

**Q: How do you set an environment variable from a step?**
A: Append to `$GITHUB_ENV`: `echo "NAME=value" >> "$GITHUB_ENV"`. Later steps in the same job see `NAME`. That does not cross jobs. A value the next job must read goes through job outputs or an artifact, not through `GITHUB_ENV`.

---

## Part 5 — Artifacts and cache

### Passing products, speeding up installs

**Q: How does a later step read a value from an earlier step?**
A: Give the step an `id` and append `name=value` to `$GITHUB_OUTPUT`. Later steps read `steps.<id>.outputs.name`. Map those onto `jobs.<id>.outputs`, and the next job reads `needs.<id>.outputs.name`. Outputs are small strings, at most 1 MB per job. An empty string is dropped. A secret inside an output is redacted and the output is skipped.

**Q: How do you pass a jar, a test report, or an image tarball?**
A: With an **artifact**. The producing job uses `actions/upload-artifact@v7` with `name` and `path`. The consuming job checks out if it needs the Dockerfile, then uses `actions/download-artifact@v8` with the same `name`. Artifacts are the build products you keep and download from the run. Set `retention-days` when the default retention is wrong.

**Q: How is a cache different from an artifact?**
A: A **cache** speeds up a later run by restoring dependencies. `actions/cache@v4` saves `path` under `key` only when the job succeeds, and it never updates an existing key. An exact key is a hit. Otherwise `restore-keys` supply a prefix match, and on a miss the job rebuilds and, if it succeeds, saves a new key. A cache is not a build product. Anyone who can open a pull request can read a cache the pull request is allowed to restore, so the cache must not contain secrets.

**Q: How should a cache key be built?**
A: Include the OS and a hash of the lockfile, for example `${{ runner.os }}-gradle-${{ hashFiles('**/gradle/wrapper/gradle-wrapper.properties') }}`. Change the lockfile and the key changes, so you do not restore stale dependencies. `gradle/actions/setup-gradle` does this for the Gradle user home, which is why a Java job often needs no handwritten `actions/cache` step.

**Q: How can a workflow poison a cache, and what stops it?**
A: A cache saved for the default branch can be restored by a later privileged job. `pull_request` writes only to the pull request's merge ref, so it cannot overwrite `main`, though it can restore `main`'s cache. Events that run as the default branch and can be started by an outsider, such as `pull_request_target`, `issue_comment`, and `workflow_run`, are read-only on that cache unless the file sets `cache-mode: write`, which brings the risk back.

**Q: Why does a Docker build miss a jar that Gradle just compiled?**
A: `docker/build-push-action` reads the Git commit unless you set `context: .`. Files created on the runner are invisible to that Git context. Check out, compile, then build with `context: .`, and point the Dockerfile `COPY` at `build/libs/`. A multi-stage Dockerfile that compiles inside the image does not need the jar on the runner, and it can use the default Git context.

---

## Part 6 — Continuous integration

### The pipeline that runs on every change

**Q: What should CI do on a pull request, and what must it not do?**
A: Check out, install the toolchain, restore the dependency cache, and run the build and tests. It does not deploy and it does not push an image. `permissions: contents: read` is enough. The Gradle wrapper (`gradlew`, committed as executable, and `gradle/wrapper/`) has to be in the repository.

**Q: Which actions replace a hand-installed JDK and Gradle?**
A: `actions/checkout@v7`, then `actions/setup-java@v6` with `distribution: temurin` and `java-version` set to the version the project compiles with, then `gradle/actions/setup-gradle@v6`, then `./gradlew build`. The Gradle action caches the Gradle user home between runs.

**Q: How do you stop an old test run when the branch moves?**
A: Put `concurrency` on the test job, with `group: ci-${{ github.ref }}` and `cancel-in-progress: true`. A newer push cancels the older test for that ref. Keep this off the publish job. A workflow-level group would cancel a publish that has already started.

**Q: How does CI block a merge?**
A: Each job becomes a status check. A branch protection rule or a ruleset requires that check by the job's `name`, or by the job id when `name` is absent. A green local build does not merge until the check on the pull request is green. Require the check, a pull request, and a review before `main` accepts the commit.

**Q: How do integration tests reach a database?**
A: `services` starts a container beside the job, with `image`, `env`, and `ports`. Steps that run directly on the runner connect to `localhost` and the published port. Steps that run inside a job container connect to the service's label as the hostname. The service dies with the runner.

**Q: Why did CI not start on a pull request from a fork?**
A: Public repositories can require approval before workflows run for a first-time contributor or a fork. That approval is a setting, not a bug in the YAML. Dependabot pull requests are a separate case: they get a read-only `GITHUB_TOKEN` and cannot read ordinary repository secrets.

---

## Part 7 — Continuous delivery

### Publish, deploy, and roll back

**Q: When is it safe to push an image or deploy?**
A: After the test job has succeeded, and only for a trusted event: a push to `main`, a version tag, or a published release. Gate the job with `needs: test` and `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`. A pull request, including one from a fork, builds and does not publish.

**Q: How should the image be tagged, and how do you roll back?**
A: Push `ghcr.io/<owner>/<repo>:${{ github.sha }}` and, if operators want a moving name, also `:latest`. Deploy the SHA tag. A rollback is a deploy of the previous SHA, not a rebuild and not a hope that `:latest` still points at the good image.

**Q: What are the usual deploy strategies?**
A: Recreate replaces the whole running set. Rolling replaces instances a few at a time. Blue-green keeps two full environments and switches traffic. Canary sends a fraction of traffic to the new revision. GitHub Actions does not implement these. The deploy job calls the platform, and the environment's reviewers are the gate in front of that call.

**Q: How do you publish to GitHub Container Registry?**
A: On that job set `permissions` to `contents: read` and `packages: write`. Log in with `docker/login-action@v4` to `ghcr.io`, username `${{ github.actor }}`, password `${{ secrets.GITHUB_TOKEN }}`. Then `docker/setup-buildx-action@v4` and `docker/build-push-action@v7` with `context: .` and `push: true`. A job-level `permissions` block replaces the workflow block, so repeat `contents: read`.

**Q: How do you publish to Docker Hub instead?**
A: Create an access token in Docker Hub. Store it as the secret `DOCKERHUB_TOKEN` and the account name as the variable `DOCKERHUB_USERNAME`. Log in to `docker.io` with those. Do not put the account password in the workflow or in a secret if a token will do.

**Q: What does an environment add to a deploy job?**
A: `environment: production` ties the job to protection rules, and GitHub will not send the job to a runner until those rules pass. Rules include required reviewers, a wait timer, and a limit on which branches may deploy. Environment secrets and variables override repository ones. `url` records the deployment address. `deployment: false` reads the secrets without creating a deployment.

**Q: How should concurrency work for a production deploy?**
A: One group for that environment, on the deploy job, with `cancel-in-progress: false`. A deploy that has started is left to finish. The default queue keeps a single pending run, so an older waiting deploy is replaced by the latest commit.

**Q: How do you give a workflow access to AWS, Azure, or GCP without a stored cloud key?**
A: **OpenID Connect.** The job needs `id-token: write`. The issuer is `https://token.actions.githubusercontent.com`. The cloud role trusts the `sub` claim, and the trust policy needs at least one condition so other repositories cannot assume the role. A branch job uses `repo:ORG/REPO:ref:refs/heads/BRANCH`. A pull-request job with no environment uses `repo:ORG/REPO:pull_request`. A job that sets `environment` uses `repo:ORG/REPO:environment:NAME`, which is the claim you want on a production role.

---

## Part 8 — Security

### Token, secrets, and untrusted code

**Q: What should `permissions` be?**
A: As small as the job allows. Set `contents: read` on the workflow, and add scopes only on the job that needs them. If you list any permission, every permission you omit becomes `none`. `read-all` and `write-all` exist and are broader than a CI job needs. `packages: write` publishes to GitHub Packages. `id-token: write` mints an OIDC token. A write scope on a job that also runs untrusted code is how a pull request becomes a repository takeover.

**Q: Who can see a secret, and when is it withheld?**
A: Anyone with write access to the repository can change a workflow so that it uses the repository secrets. A `pull_request` from a fork receives a read-only `GITHUB_TOKEN` and does not receive those secrets. You generally cannot grant that fork a write token. Environment secrets stay unavailable until the environment's reviewers approve. Masking looks for the exact secret string, so a JSON blob or a Base64 of the secret can appear in the log. Register a derived value with `::add-mask::`, and rotate any secret that reached a log.

**Q: What is a script injection in a workflow?**
A: `${{ }}` is substituted while the shell script is being built. `run: echo "${{ github.event.pull_request.title }}"` lets a title break out of the quotes and run as a command, with the job's token. Put the value in `env` and read the variable inside `run`. The expression is then data, not script text. Issue titles, commit messages, and pull-request bodies are the usual untrusted fields.

**Q: How do `pull_request` and `pull_request_target` differ?**
A: `pull_request` runs the workflow from the pull request's merge commit, checks that commit out, and withholds secrets. `pull_request_target` runs the workflow from the default branch and, by default, checks that branch out, and it does receive secrets and a token that can write. Checking out the pull request head and then running its build, tests, or Makefile is a **pwn request**: the fork's code executes with the base repository's credentials. Prefer `pull_request` unless the job only does trusted work such as labeling.

**Q: How do you pin an action?**
A: A workflow dependency lockfile is the strongest option. It records the commit of every action, including transitive ones, and checks the source at runtime. Without a lockfile, pin a full commit SHA from the action's own repository, not from a fork. A moving tag such as `@v7` is acceptable while you are learning and only if you trust the publisher, because a tag can be moved. Dependabot can open pull requests that bump those pins. `CODEOWNERS` on `.github/workflows` makes those pull requests require your review.

**Q: What can a compromised action do?**
A: Every step in the job shares the machine, the job's secrets, and the job's `GITHUB_TOKEN`. One third-party action can read those secrets and write wherever the token allows. Audit the action. Keep delivery credentials and `id-token: write` on the deploy job, not on the job that builds untrusted pull-request code.

---

## Part 9 — Reuse and debugging

### Actions, reusable workflows, and logs

**Q: When is the reusable unit an action, and when is it a workflow?**
A: An action is one step. It is JavaScript, a Docker container, or a composite action (`runs.using: composite` in its `action.yml`). A **reusable workflow** is an entire workflow. The callee has `on: workflow_call` and may declare inputs, outputs, and secrets. The caller invokes it as a job: `uses: ./.github/workflows/ci.yml` in the same repository, or `uses: org/repo/.github/workflows/ci.yml@ref` in another. Secrets are not visible in the callee unless the caller passes them or sets `secrets: inherit`.

**Q: How do you debug a failed run?**
A: Open the job log. The command is printed apart from its output, including how options and environment variables were applied. Re-run the failed jobs after a fix. For a deeper trace, set the repository secrets `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG` to `true` and re-run. Remove them when you are done. The logs become much more verbose, and debug output is a place secrets can leak if a step prints its environment.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Workflow | A YAML file in `.github/workflows` that runs when its `on` events fire |
| Job | Steps on one fresh runner; jobs run in parallel unless `needs` orders them |
| Action | A reusable step referenced with `uses: owner/repo@ref` and configured with `with` |
| `run` | A shell command; `run: \|` is several commands in one step |
| Gate | A status check, `needs`, an environment reviewer, or a job `if` that stops the next stage |
| `pull_request` | Runs the merge commit with a read-only token and no repository secrets |
| `pull_request_target` | Runs the default-branch workflow with secrets; do not execute the fork's code |
| `workflow_dispatch` | A manual run; the file must be on the default branch, and inputs are read from `inputs` |
| `GITHUB_TOKEN` | A token minted for the job; listed permissions apply, and omitted ones become `none` |
| `env` / `vars` / `secrets` | Runner environment variable, a stored configuration value, and a masked credential |
| Artifact | A build product uploaded in one job and downloaded in another |
| Cache | A dependency snapshot keyed for speed; not a build product, and not a secret store |
| `environment` | Reviewers, branch limits, and deploy secrets applied before the job is scheduled |
| OIDC | A short-lived cloud login from `id-token: write`, trusted by the `sub` claim |
| Concurrency | One run per group; cancel in-progress tests, and let a started deploy finish |
| Reusable workflow | A workflow with `on: workflow_call`, invoked as a job via `uses` |
| Status check | The job name a ruleset or branch protection requires before a merge |

---

## Formulas

One workflow. `test` cancels when the branch moves. `image` runs only after `test` succeeds on a push to `main`, and a publish that has started is not cancelled. Concurrency sits on the job, because a workflow-level group would cancel the publish too. `java-version` must match the project. Add `merge_group` beside `pull_request` when the repository uses a merge queue. The image job checks out again because its machine is empty.

```yaml
name: CI
on:
  push:
    branches: [main]
    paths:
      - "src/**"
      - "gradle/**"
      - "build.gradle*"
      - "Dockerfile"
      - ".github/workflows/**"
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    concurrency:
      group: ci-${{ github.ref }}
      cancel-in-progress: true
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: "17"
      - uses: gradle/actions/setup-gradle@v6
      - run: ./gradlew build
  image:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: production
      cancel-in-progress: false
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: "17"
      - uses: gradle/actions/setup-gradle@v6
      - run: ./gradlew build
      - uses: docker/login-action@v4
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/setup-buildx-action@v4
      - uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
```

`paths` is optional. Leave it off until a docs-only commit is wasting runner time. Add `id-token: write` beside `packages: write` only on a job that assumes a cloud role. The GHCR push uses `GITHUB_TOKEN` and does not need that scope.

```dockerfile
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY build/libs/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Pass a file when the next job must not rebuild:

```yaml
- uses: actions/upload-artifact@v7
  with:
    name: app-jar
    path: build/libs/*.jar
# on the later job, after needs: test and a checkout
- uses: actions/download-artifact@v8
  with:
    name: app-jar
    path: build/libs
```

Hand a string to a later job:

```yaml
- id: meta
  run: echo "sha=${GITHUB_SHA}" >> "$GITHUB_OUTPUT"
# jobs.test.outputs.sha: ${{ steps.meta.outputs.sha }}
# later: ${{ needs.test.outputs.sha }}
```

A dependency cache key. Prefer `gradle/actions/setup-gradle` for Java, and use this shape for anything else:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.gradle/caches
    key: ${{ runner.os }}-gradle-${{ hashFiles('**/gradle/wrapper/gradle-wrapper.properties') }}
    restore-keys: ${{ runner.os }}-gradle-
```

Untrusted text goes through the environment, not through the script text:

```yaml
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "$TITLE"
```

Call a reusable workflow in the same repository. The callee file starts with `on: workflow_call`.

```yaml
jobs:
  ci:
    uses: ./.github/workflows/ci.yml
    secrets: inherit
```

A database beside the test job. From the runner, the port is on `localhost`. From a container job, the hostname is the service label.

```yaml
services:
  db:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: postgres
    ports:
      - 5432:5432
```

---

*Study aid. For authoritative content, refer to GitHub's Actions documentation on workflow syntax, secure use, dependency caching, and OpenID Connect.*
