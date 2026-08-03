class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "04a2600b5883e663c3b751fc1fd1593ec4ed0e966977c6071c2ef80090f11417"
  license "MIT"

  depends_on "python@3"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/avocado" => "avocado"
  end

  def caveats
    <<~EOS
      Avocado Native macOS Terminal App installed!
      
      To start the terminal dashboard, run:
        avocado
      
      To check laptop status or neofetch:
        avocado --status
        avocado --neofetch
    EOS
  end

  test do
    assert_predicate libexec/"bin/avocado", :exist?
  end
end
