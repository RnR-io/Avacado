class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.6.0.tar.gz"
  sha256 "23c7944f10dbb091ee1400ede37364cf714abe4e969f9f90149797d2ef7cb3fa"
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
