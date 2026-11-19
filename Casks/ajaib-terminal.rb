cask "ajaib-terminal" do
  version "1.15.0"
  sha256 "fe2c50d3cbd42e56b382f1261d721e5b7bef4dc75c54afc28c320bd30f693da7"

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
