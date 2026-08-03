class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.7.0.tar.gz"
  sha256 "303be1243bc69ef611ab4a748df769688825c6cf7e4cbdb20d10eb6a0cec128d"
  license "MIT"

  depends_on "python@3"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/avocado" => "avocado"
    bin.install_symlink libexec/"bin/avocado" => "avacado"
  end

  def caveats
    <<~EOS
      Avocado Native macOS Terminal App installed!
      
      To start the terminal dashboard, run:
        avocado
      or
        avacado
    EOS
  end

  test do
    assert_predicate libexec/"bin/avocado", :exist?
  end
end
