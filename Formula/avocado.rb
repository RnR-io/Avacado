class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "57e2155df62218a726731e2c9972c06403db851f83f3be8be33858e78f92e6d7"
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
