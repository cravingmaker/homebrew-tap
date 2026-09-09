# cravingmaker/tap

Personal Homebrew tap for casks and formulae. No packages are currently hosted here;
the tap remains available for future additions.

## Setup

```sh
brew tap cravingmaker/tap
brew trust --tap cravingmaker/tap
```

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
cask "stockbit"
```

## Maintenance

Add casks under `Casks/` and formulae under `Formula/`. CI validates the migration
map and runs Homebrew style, online audits, and livecheck when packages are present.
Stockbit's update and installation workflows have been retired; its maintenance
now belongs to Homebrew Cask.
