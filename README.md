# .github

Org-wide defaults for [springfield-ham-radio](https://github.com/springfield-ham-radio).

Files in this repository apply to every org repository that does not define its own copy. Issue forms in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) are the default issue chooser for HamBench and the related driver, API, registry, radio-module, sniffer, docs, and ops repos.

HamBench (`ham-radio-ui`) is a Tauri desktop app for programming ham radios through JSON protocol modules. It currently supports the Baofeng UV-5R and the Kenwood TH-F6, TH-D74, and TM-D710A, and also includes CAT control, a channel library (RepeaterBook and CHIRP CSV import), a station log with a map, and a serial sniffer.

## Issue forms

Blank issues are disabled. Each form sets an organization issue type and the `status: needs triage` label:

| Form | Issue type |
| --- | --- |
| Bug report | Bug |
| Feature request | Feature |
| Enhancement | Enhancement |
| Docs issue | Docs |

An optional area dropdown (ui, driver, modules, cat, channel library, log, sniffer, api, registry) is recorded in the issue body. Issue forms cannot turn that choice into an `area:*` label.

## Label sync

[`labels.yml`](labels.yml) is the source of truth for the shared issue labels: `priority:`, `status:`, `area:`, `radio:`, `cannot reproduce`, and `auto-fix`. [`.github/workflows/sync-labels.yml`](.github/workflows/sync-labels.yml) applies that file to every non-archived repository in the organization, including this repository and repositories created later.

The sync creates labels that are missing and updates the color and description of labels with the same name. Labels that are not listed in `labels.yml` stay as they are, including `released`, Dependabot labels such as `dependencies`, and GitHub's default labels.

It runs when `labels.yml` changes on `main`, every Monday at 12:00 UTC, and from the Actions tab via **Run workflow**. A manual run can set **Preview creates and updates without changing labels** to print the plan and leave every repository unchanged.

`GITHUB_TOKEN` can only edit labels in the repository that is running the workflow. Cross-repository updates use a secret named `LABEL_SYNC_TOKEN`. The workflow stops with an error when that secret is empty.

### Create LABEL_SYNC_TOKEN

Create the token as an organization owner so it is approved immediately. If a member creates it and the organization requires approval, an owner must approve the request under **Settings → Personal access tokens → Pending requests** before the workflow can write labels.

1. Open [Generate a fine-grained token](https://github.com/settings/personal-access-tokens/new?name=label-sync&description=Sync+org+issue+labels+from+the+.github+labels.yml&target_name=springfield-ham-radio&issues=write) (or **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**). The link pre-fills the name, description, resource owner, and Issues permission.
2. Set **Resource owner** to `springfield-ham-radio`.
3. Set **Repository access** to **All repositories**, so repositories created later are included.
4. Under **Repository permissions**, set **Issues** to **Read and write**. **Metadata: Read** is included automatically; leave every other permission at **No access**.
5. Generate the token and copy the value. It is shown only once.

Save that value as a secret named `LABEL_SYNC_TOKEN`, in either place:

- Organization secret: organization **Settings → Secrets and variables → Actions → New organization secret**. Grant it to all repositories, or at least to `.github`.
- Repository secret: `springfield-ham-radio/.github` **Settings → Secrets and variables → Actions → New repository secret**.

The workflow reads an organization secret and a repository secret of the same name. Keep the token out of the repository.
