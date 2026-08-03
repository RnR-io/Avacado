class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.1.0.tar.gz"
  sha256 "fff943d13451a1c6b67557d663daa68535baa46605a0fc0a6f57c6c1649e746d"
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
