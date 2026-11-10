"""Serve the built page over local HTTP with engine/ beside it, the way GitHub Pages serves it.

A web worker can't start from a file:// page, so everything that needs the engine runs against this copy.
It is the build without accounts (data/build/playbook.html), so nothing is fetched from another host."""
import shutil, socket, subprocess, sys, tempfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pipeline'))
from assemble import site_html  # noqa: E402


class Site:
    def start(self):
        self.dir = tempfile.mkdtemp(prefix='playbook-site-')
        (Path(self.dir) / 'index.html').write_text(site_html((ROOT / 'data' / 'build' / 'playbook.html').read_text(), None))
        shutil.copytree(ROOT / 'docs' / 'engine', Path(self.dir) / 'engine')
        s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
        self.srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=self.dir,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.8)
        self.url = f'http://127.0.0.1:{port}/'
        return self.url

    def stop(self):
        self.srv.terminate(); shutil.rmtree(self.dir, ignore_errors=True)
