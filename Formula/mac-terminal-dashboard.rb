class MacTerminalDashboard < Formula
  desc "Authentic macOS Terminal Dashboard & Landing Page"
  homepage "https://github.com/RnR-io/mac-terminal-app"
  url "https://github.com/RnR-io/mac-terminal-app/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/mac-terminal-app" => "mac-terminal-dashboard"
  end

  def caveats
    <<~EOS
       macOS Terminal Dashboard & Landing Page installed successfully!
      
      To start the dashboard and native system server, run:
        mac-terminal-dashboard
      
      Or open http://127.0.0.1:8765 in your browser.
    EOS
  end

  test do
    assert_predicate libexec/"server.py", :exist?
  end
end
