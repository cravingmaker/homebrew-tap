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

Ordinary uninstall retains user settings and data. To also move Stockbit's
verified data folders to the Trash, quit Stockbit and explicitly use `--zap`:

```sh
brew uninstall --cask --zap cravingmaker/tap/stockbit
```

This removes these folders from the current user's Library:

- `~/Library/Application Support/com.stockbit.desktop`
- `~/Library/Caches/com.stockbit.desktop`
- `~/Library/WebKit/com.stockbit.desktop`

These paths were verified on a Mac running Stockbit 2.2.0. Cleanup can reset local
settings and login state. It runs only when `--zap` is requested; normal uninstall
and upgrades do not run it.

If Stockbit was installed before this tap gained cleanup support, Homebrew's
saved installation recipe has no `zap` stanza. When you want to remove that
installation and its data, first uninstall normally, then apply the current
recipe's cleanup to the now-uninstalled cask:

```sh
brew uninstall --cask cravingmaker/tap/stockbit
brew uninstall --cask --zap --force cravingmaker/tap/stockbit
```

Here `--force` allows cleanup after the app has already been uninstalled.

## Maintain

Check the vendor's current installer version:

```sh
brew livecheck --cask cravingmaker/tap/stockbit
```

Livecheck reads the official download redirect, so it can discover a release
beyond the pinned version without extracting a DMG. The command itself only
reports versions; the daily update workflow uses its result to prepare an update
PR. Installed apps can still update themselves between tap updates.

When a new release appears, download its versioned DMG from the vendor, calculate
`shasum -a 256 /path/to/Stockbit.dmg`, and update `version` and `sha256` together.
Inspect the app's version, architectures, bundle identifier and signature before
committing. Do not replace the checksum with `:no_check` for a versioned download.

```sh
brew style cravingmaker/tap
brew audit --cask --strict --online --except=livecheck_version --tap cravingmaker/tap
brew livecheck --cask --tap cravingmaker/tap
```

GitHub Actions runs these checks on pushes and pull requests. Online audits
download and inspect installers. Livecheck reports upstream versions separately:
a newer version is informational, while an actual download, audit or livecheck
error fails the run. CI does not launch the application.

## Automation

| Workflow | When | Behavior |
| --- | --- | --- |
| Validate casks | Push to `main`, pull request, or manual run | Tests update selection, checks style, audits installers, and reports livecheck results |
| Update casks | Daily at 08:17 Asia/Jakarta, or manual run on `main` | Checks Stockbit; updates its version and SHA-256 and opens or updates a PR when a newer release exists |
| Weekly installation test | Monday at 09:43 Asia/Jakarta, or manual run on `main` | Installs and uninstalls Stockbit only if `main` has commits in the preceding seven days |

GitHub schedules use UTC and may start later when runners are busy. The weekly
workflow first runs a small Linux job to query commits reachable from the run's
`main` revision. Any commit counts, including documentation changes and merged
update PRs. If there are none in the preceding seven days, the macOS job is
skipped. Manual runs use the same activity condition. Commits only on unmerged
branches do not count. The installation test checks that the app bundle and
executable exist, uninstalls it, and verifies that the bundle is gone. It uses a
temporary app directory on the runner and never launches Stockbit or uses `--zap`.

The daily updater currently handles Stockbit's numeric stable versions. It uses
`brew bump-cask-pr --write-only` to download the new installer and calculate its
checksum. Style and online audit must pass before it publishes a PR on the
reusable `automation/stockbit` branch. It never commits directly to `main` or
merges automatically. A current version produces no changes or PR. Failed or
unrecognized release results stop the workflow instead of guessing a version.

The updater uses the repository's `GITHUB_TOKEN`; no personal token is needed.
GitHub's **Settings → Actions → General → Allow GitHub Actions to create and
approve pull requests** must be enabled. The updater requests write permissions
only for contents, pull requests, and workflow dispatch. Other workflows are
read-only. After opening or finding the update PR, it explicitly dispatches
validation on that branch so bot-generated changes get a CI run. The validation
run appears on the PR's head commit and in the Actions tab.

Run any workflow manually from the repository's **Actions** tab. For local
automation tests, use `python3 -m unittest discover -s tests`.

## Adding another app

For another app, an official download page or DMG URL is usually enough to begin.
Each cask needs a version, SHA-256, name, short description, homepage, and exact
installation artifact. Also verify architecture and macOS requirements, updater
behavior, a release-discovery source, and any special uninstall requirements.
Separate Intel/Apple Silicon downloads need separate checksums. Bundle identifiers
and confirmed data paths are needed for optional targeted cleanup.

## Stockbit verification

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

The cask uses Homebrew's declarative DSL without custom installation scripts.
See the [Homebrew Cask Cookbook](https://docs.brew.sh/Cask-Cookbook) for the format.
