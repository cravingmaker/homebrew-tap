cask "ajaib-terminal" do
  version "1.12.1"
  sha256 "1069fc30e1e6c1cd51f6260956e10b835d5bf91abc3a67ccbffcfc57f825ab10"

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
