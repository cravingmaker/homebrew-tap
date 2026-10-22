cask "ajaib-terminal" do
  version "1.12.0"
  sha256 "da852fcac140602e8a1d227cb5b93b8232050205c13feb769f642559effcdb82"

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
