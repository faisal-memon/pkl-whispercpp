import pathlib
import shutil
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PKL = shutil.which("pkl") or str(pathlib.Path.home() / ".local/bin" / "pkl")


class GenerationTest(unittest.TestCase):
    def test_example_renders_valid_compose(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = pathlib.Path(temporary_directory) / "deployment.yaml"
            subprocess.run(
                [PKL, "eval", "-o", str(output), "examples/deployment.pkl"],
                cwd=ROOT,
                check=True,
            )
            rendered = output.read_text()

        self.assertIn("whisper-server", rendered)
        self.assertIn(
            "ghcr.io/ggml-org/whisper.cpp:main-cuda@sha256:8a9def3eea0615dbee85cac1e0fa3898dce214fe9bb7955635ba25667da3884a",
            rendered,
        )
        self.assertIn("/var/lib/whispercpp/models:/models:ro", rendered)
        self.assertIn("service_completed_successfully", rendered)
        self.assertIn("nvidia", rendered)


if __name__ == "__main__":
    unittest.main()
