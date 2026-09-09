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
the app's official update service and verifies its SHA-256. Its app bundle is
identical to the official DMG's bundle for version 1.8.2.

The app has a built-in updater. To check the latest vendor release with Homebrew:

```sh
brew livecheck --cask cravingmaker/tap/ajaib-terminal
```

Livecheck reports new versions; it does not update the cask automatically.
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
Stockbit's update and installation workflows have been retired; its maintenance
now belongs to Homebrew Cask.
