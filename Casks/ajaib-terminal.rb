cask "ajaib-terminal" do
  version "1.8.2"
  sha256 "1a791d28737fccbd979cdf508861e013ed285fdd101a8c89827b38b4b9b1fbb7"

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
