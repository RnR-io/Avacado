class Avocado < Formula
  desc "Native macOS Terminal Dashboard & CLI App"
  homepage "https://github.com/RnR-io/Avacado"
  url "https://github.com/RnR-io/Avacado/archive/refs/tags/v1.5.0.tar.gz"
  sha256 "4ac51d38230e0c7f10176b3f3d079c1940ebf1a43feb33e813dfea53bdf8a452"
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
