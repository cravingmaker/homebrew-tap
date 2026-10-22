# cravingmaker/tap

Personal Homebrew tap for casks and formulae. Installers come directly from their
vendors.

## Setup

```sh
brew tap cravingmaker/tap
brew trust --tap cravingmaker/tap
```

## Ajaib Terminal

```sh
brew install --cask cravingmaker/tap/ajaib-terminal
```

[Ajaib Terminal](https://ajaib.co.id/terminal) requires macOS 12 Monterey or later
and supports Intel and Apple Silicon. The cask downloads a versioned archive from
the app's official update service and verifies its SHA-256. When the cask was
added at version 1.8.2, its app bundle was identical to the official DMG's bundle.

The app has a built-in updater. To check the latest vendor release with Homebrew:

```sh
brew livecheck --cask cravingmaker/tap/ajaib-terminal
```

A daily workflow runs livecheck and, when a new release appears, opens a pull
request that updates the version and checksum. Updates are merged after review.
Homebrew skips self-updating apps during ordinary upgrades; use
`brew upgrade --cask --greedy cravingmaker/tap/ajaib-terminal` to include this app.

Uninstall with `brew uninstall --cask cravingmaker/tap/ajaib-terminal`.
No `zap` paths are defined yet; local settings and data are retained.

## Stockbit

Stockbit is now maintained in [Homebrew Cask](https://formulae.brew.sh/cask/stockbit)
following [PR #285638](https://github.com/Homebrew/homebrew-cask/pull/285638).

```sh
brew install --cask stockbit
```

`tap_migrations.json` redirects the old `cravingmaker/tap/stockbit` name to
`homebrew/cask`. This tap can remain installed and trusted.

For a Brewfile:

```ruby
tap "cravingmaker/tap"
cask "cravingmaker/tap/ajaib-terminal"
cask "stockbit"
```

## Maintenance

Add casks under `Casks/` and formulae under `Formula/`. CI validates the migration
map and runs Homebrew style, online audits, and livecheck when packages are present.
A newer upstream version is reported but doesn't fail CI; the daily `Update casks`
workflow opens a pull request for it instead. To automate another cask, add it to
that workflow's matrix. Stockbit's maintenance now belongs to Homebrew Cask.
