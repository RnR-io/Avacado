class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.2.0.tar.gz"
  sha256 "730ffbcc785fff335bacdfd171329769bb6e846e36274b7e557b14cc977195e3"
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
