# cravingmaker/tap

Personal, unofficial Homebrew casks for macOS. Installers are downloaded directly
from their vendors; this repository contains recipes only.

## Install

```sh
brew tap cravingmaker/tap
```

On Homebrew versions with tap trust controls, approve this tap before installing:

```sh
brew trust --tap cravingmaker/tap
```

```sh
brew install --cask cravingmaker/tap/stockbit
```

Stockbit requires macOS 12 Monterey or later. Its universal app supports both
Apple Silicon and Intel Macs without separate downloads or Rosetta.

For a Brewfile, trust the tap first when required, then use:

```ruby
tap "cravingmaker/tap"
cask "cravingmaker/tap/stockbit"
```

If Stockbit is already installed manually, Homebrew can adopt it when the
existing app bundle matches the one supplied by the cask:

```sh
brew install --cask --adopt cravingmaker/tap/stockbit
```

## Updates and removal

Stockbit has its own updater. `auto_updates true` tells Homebrew to skip it during
ordinary `brew upgrade` runs; it does not enable or configure Stockbit's updater.
Use Stockbit's **Settings → Software Update** to check for app updates.

Homebrew's recorded installation version may lag behind an app that updates
itself. The version in this tap describes the installer for fresh installations.
To explicitly include self-updating apps in Homebrew's upgrade check:

```sh
brew upgrade --cask --greedy cravingmaker/tap/stockbit
```

Remove the application with:

```sh
brew uninstall --cask cravingmaker/tap/stockbit
```

User settings and data are retained. This cask intentionally has no `zap` stanza
until Stockbit's data directories have been verified; it does not claim to remove
all app data.

## Maintain

Check the vendor's current installer version:

```sh
brew livecheck --cask cravingmaker/tap/stockbit
```

Livecheck reads the official download redirect, so it can discover a release
beyond the pinned version without extracting a DMG. It reports versions; it does
not edit the cask or create update PRs. Installed apps can still update themselves
between tap updates.

When a new release appears, download its versioned DMG from the vendor, calculate
`shasum -a 256 /path/to/Stockbit.dmg`, and update `version` and `sha256` together.
Inspect the app's version, architectures, bundle identifier and signature before
committing. Do not replace the checksum with `:no_check` for a versioned download.

```sh
brew style cravingmaker/tap
brew audit --cask --strict --online --tap cravingmaker/tap
```

GitHub Actions runs those checks on pushes and pull requests. Online audits
download and inspect installers and check livecheck; vendor outages or a newly
released version can cause an audit failure. CI does not launch the application.

For another app, an official download page or DMG URL is usually enough to begin.
Each cask needs a version, SHA-256, name, short description, homepage, and exact
installation artifact. Also verify architecture and macOS requirements, updater
behavior, a release-discovery source, and any special uninstall requirements.
Separate Intel/Apple Silicon downloads need separate checksums. Bundle identifiers
and confirmed data paths are needed for optional targeted cleanup.

## Stockbit verification and reference evaluation

Verified on 2026-09-07 against the
[official download page](https://stockbit.com/desktop) and its
[macOS download endpoint](https://sda-updater.stockbit.com/macos?format=bundle):

- The endpoint redirects to the versioned **2.2.0** DMG used by this cask.
- The DMG contains `Stockbit.app`, version `2.2.0`, bundle ID
  `com.stockbit.desktop`, with `arm64` and `x86_64` executable slices.
- Its SHA-256 was calculated from the downloaded DMG. macOS signature verification
  passed, and Gatekeeper accepted it as a notarized Developer ID application.
- The vendor lists macOS 12 or later. The app's plist says 10.13; this cask uses
  the vendor's published requirement, without claiming older macOS support.
- Stockbit documents its built-in updater in its
  [software update instructions](https://help.stockbit.com/id/article/bagaimana-cara-lihat-dan-update-version-stockbit-app-terbaru-dopflr/).

The [joglomedia reference cask](https://github.com/joglomedia/homebrew-brewery/blob/HEAD/Casks/stockbit.rb)
was evaluated, with download metadata verified independently:

- Its versioned URL, checksum and `auto_updates true` are appropriate.
- Its `extract_plist` livecheck examines the already-pinned DMG and cannot discover
  the next release. This tap checks the current vendor redirect instead.
- `verified:` is unnecessary because the download host belongs to the homepage's
  `stockbit.com` domain.
- This tap adds the published macOS requirement and a concise description, and
  omits unverified cleanup paths and unrelated formulae.

The cask uses Homebrew's declarative DSL without custom installation scripts.
See the [Homebrew Cask Cookbook](https://docs.brew.sh/Cask-Cookbook) for the format.
