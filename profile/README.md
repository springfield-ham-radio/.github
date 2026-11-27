# Springfield Ham Radio

**HamBench** is Bryan Hunt’s desktop app for amateur-radio memory and live computer control (CAT). Read and write radio memory, edit channels, keep a portable channel library, log contacts, and debug clone-protocol traffic when you need to. The app ships a generic serial driver; you add only the radios you own as installable JSON modules.

## Downloads and feedback

- **Installers** — [ham-radio-ui Releases](https://github.com/springfield-ham-radio/ham-radio-ui/releases) (macOS Apple Silicon and Intel, Windows, and Linux x64 and arm64). Packaged builds check that feed on launch. Builds are **unsigned** (see the [install guide](https://springfield-ham-radio.github.io/ham-radio-docs/guide/getting-started.html) for macOS quarantine and Windows SmartScreen).
- **Bug reports and feature requests** — [ham-radio-ui Issues](https://github.com/springfield-ham-radio/ham-radio-ui/issues)

Docs: [User guide](https://springfield-ham-radio.github.io/ham-radio-docs/guide/) · [Developer docs](https://springfield-ham-radio.github.io/ham-radio-docs/developer/)

## What HamBench does

- **Memory** — Read and write channels and settings on the Radio page, open and save JSON memory files, and use automatic file backups.
- **Channel library** — A portable channel list in the app database, with import from HamBench, RepeaterBook, or CHIRP CSV and export back to CSV.
- **Live CAT** — VFO frequency, mode, power, and hold-to-transmit on radios whose module declares live control (Kenwood TH-F6, TH-D74, and TM-D710A today).
- **Log** — Station log with ADIF import and export and a world map of Maidenhead grids from your contacts.
- **Stations and antennas** — Operating sites, antennas at a site or mounted on a radio, and license-based transmit warnings (US amateur via Callook, GMRS; FRS always allowed).
- **Propagation** — NOAA solar indices and a local HF band-opening estimate (a WWV-style aide, not a VOACAP forecast).
- **Sniffer** — Inspect clone-protocol serial traffic between your computer and the radio (**Radio → Sniffer**), backed by the standalone [ham-radio-sniffer](https://github.com/springfield-ham-radio/ham-radio-sniffer) bridge.
- **Reference** — Offline ITU phonetics, Q signals, a U.S. amateur band chart, and Morse listening practice. It does not key or transmit on a radio.
- **APRS and packet** — On a Kenwood TM-D710A, the control-head **COM** jack supports a passive monitor of menu 604 traffic, host KISS messaging (with the module’s enter and exit steps), and a **Packet** tab that shares the same host session. On a TH-D74, turn KISS on at the radio and use **Connect (Host)** on the programming USB port; there is no separate APRS serial jack and no monitor-only mode for that path.

HamBench does not bundle every radio. On first launch (or anytime under **Preferences → Drivers**), install official modules from the [catalog](https://springfield-ham-radio.github.io/radio-module-catalog/catalog.json) on GitHub Pages. Each module is a JSON zip from that radio’s GitHub Release.

| Manufacturer | Radios | Memory | Live CAT |
| --- | --- | --- | --- |
| Baofeng | UV-5R family (one config covers UV-5RE Plus; not CHIRP’s BF-F8HP or UV-K5 variants) | Clone | No |
| Kenwood | TH-F6 | Live CAT memories | Yes |
| Kenwood | TH-D74 | Clone | Yes (same PC port) |
| Kenwood | TM-D710A | Clone (body PC port) | Yes |

## Radio support without writing code

Radio support is **declarative JSON**. HamBench does not import TypeScript from a module zip. A generic driver in [`ham-radio-driver`](https://github.com/springfield-ham-radio/ham-radio-driver) runs the **Protocol DSL** (serial exchanges, chunked clone read/write, and optional `catRead` / `catWrite`). [`ham-radio-utils`](https://github.com/springfield-ham-radio/ham-radio-utils) turns image bytes into channels and settings via the **memory-map DSL**. [`ham-radio-registry`](https://github.com/springfield-ham-radio/ham-radio-registry) validates configs and catalog entries.

A module is JSON only: `configs/<modelId>.json` plus schemas and memory maps it `$ref`s, packaged as `radio-module-<modelId>-<version>.zip` on a manufacturer repo’s Releases. Official rows are listed in [`radio-module-catalog`](https://github.com/springfield-ham-radio/radio-module-catalog).

**In the app**, turn on **View → Developer Mode** to open the **Driver editor**. You can draft serial settings, memory segments, protocol steps, channel schema, and the memory map, then export JSON into a module repository — the friendliest way to add a radio without hand-writing every field.

**In git**, start from [`radio-module-template`](https://github.com/springfield-ham-radio/radio-module-template) (**Use this template**). Worked examples: [`radio-module-baofeng`](https://github.com/springfield-ham-radio/radio-module-baofeng) and [`radio-module-kenwood`](https://github.com/springfield-ham-radio/radio-module-kenwood). Install from **Preferences → Drivers**, or try a local zip with **Install from file…** (beta and unverified labels are described in the [install radios](https://springfield-ham-radio.github.io/ham-radio-docs/guide/install-radios.html) guide).

Learn more: [Build a radio driver](https://springfield-ham-radio.github.io/ham-radio-docs/developer/build-a-radio-driver.html) · [Protocol DSL](https://springfield-ham-radio.github.io/ham-radio-docs/developer/protocols/dsl.html) · [Memory-map DSL](https://springfield-ham-radio.github.io/ham-radio-docs/developer/protocols/memory-map.html) · [Driver editor](https://springfield-ham-radio.github.io/ham-radio-docs/developer/driver-editor.html)

## Repositories

| Repository | Role |
| --- | --- |
| [ham-radio-ui](https://github.com/springfield-ham-radio/ham-radio-ui) | HamBench desktop app |
| [ham-radio-docs](https://github.com/springfield-ham-radio/ham-radio-docs) | Documentation site |
| [ham-radio-driver](https://github.com/springfield-ham-radio/ham-radio-driver) | Generic protocol DSL driver |
| [ham-radio-api](https://github.com/springfield-ham-radio/ham-radio-api) | Shared types and JSON schemas |
| [ham-radio-registry](https://github.com/springfield-ham-radio/ham-radio-registry) | Config and catalog validation |
| [ham-radio-utils](https://github.com/springfield-ham-radio/ham-radio-utils) | Memory-map codec, validation, packaging helpers |
| [ham-radio-sniffer](https://github.com/springfield-ham-radio/ham-radio-sniffer) | Headless serial sniffer |
| [radio-module-baofeng](https://github.com/springfield-ham-radio/radio-module-baofeng) | Baofeng UV-5R JSON module |
| [radio-module-kenwood](https://github.com/springfield-ham-radio/radio-module-kenwood) | Kenwood JSON modules |
| [radio-module-catalog](https://github.com/springfield-ham-radio/radio-module-catalog) | Official install index |
| [radio-module-template](https://github.com/springfield-ham-radio/radio-module-template) | Starter for a new module |
| [ham-radio-ops](https://github.com/springfield-ham-radio/ham-radio-ops) | Developer workspace tooling |

## License

HamBench and the Springfield libraries are **MIT**. Copyright (c) 2026 Bryan Hunt. See [ham-radio-ui LICENSE](https://github.com/springfield-ham-radio/ham-radio-ui/blob/main/LICENSE).