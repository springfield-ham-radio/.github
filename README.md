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
