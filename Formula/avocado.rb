class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "1e1e4806fedec9d2d607338f8523ced13a34554ca45a4b9da702c5ffab1573d4"
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
