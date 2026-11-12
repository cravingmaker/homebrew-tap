cask "ajaib-terminal" do
  version "1.14.0"
  sha256 "6cc421acd69a756a9a764818679be780eda309e6d927835e5365fee6cdc28e4a"

  url "https://storage.googleapis.com/storage-ajaib-prd-platform-desktop/releases/v#{version}/Ajaib%20Terminal.app.tar.gz"
  name "Ajaib Terminal"
  desc "Indonesian stock trading platform"
  homepage "https://ajaib.co.id/terminal"

  livecheck do
    url "https://storage.googleapis.com/storage-ajaib-prd-platform-desktop/releases/latest.json"
    strategy :json do |json|
      json["version"]
    end
  end

  auto_updates true
  depends_on macos: :monterey

  app "Ajaib Terminal.app"
end
