import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/tanlabs-clean/scripts/clean_text.py"
spec = importlib.util.spec_from_file_location("clean", SCRIPT)
clean = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clean)


class CleanTests(unittest.TestCase):
    def test_defaults_and_report(self):
        text, report = clean.clean_text("\ufeffAção\u00a0com\u200b café\u2060.")
        self.assertEqual(text, "Ação com café.")
        self.assertEqual((report["removed"], report["normalized"]), (3, 1))
        self.assertNotIn("café", json.dumps(report, ensure_ascii=False))

    def test_emojis_and_languages(self):
        value = "cafe\u0301 العربية فارسی می\u200cروم हिन्दी 👩🏽‍💻 👨‍👩‍👧‍👦 ❤️ 🏳️‍🌈 🏴\U000e0067\U000e0062\U000e007f"
        self.assertEqual(clean.clean_text(value)[0], value)

    def test_options_and_idempotence(self):
        value = "“Ação”\u202e…\u200b"
        result, report = clean.clean_text(value, bidi=True, typography=True)
        self.assertEqual(result, '"Ação"...')
        self.assertEqual(report["changed"], 5)
        self.assertEqual(clean.clean_text(result, bidi=True, typography=True)[1]["changed"], 0)
        self.assertEqual(clean.clean_text("A\u200b\u00a0", invisible=False, spaces=False)[0], "A\u200b\u00a0")

    def test_all_spaces(self):
        source = "".join(map(chr, clean.SPACES))
        self.assertEqual(clean.clean_text(source)[0], " " * len(source))
        self.assertEqual(clean.clean_text("A  B\tC\r\nD\n\nE")[0], "A  B\tC\r\nD\n\nE")

    def test_limit_matches_utf16(self):
        self.assertEqual(clean.clean_text("🙂" * 250_000)[1]["changed"], 0)
        with self.assertRaises(ValueError):
            clean.clean_text("🙂" * 250_001)

    def test_stdin_and_inspect(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "-", "--inspect"], input="A\u200b".encode(), capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["removed"], 1)
        run = subprocess.run([sys.executable, str(SCRIPT), "-"], input="A\u200b🙂".encode(), capture_output=True)
        self.assertEqual(run.stdout.decode(), "A🙂")

    def test_output_and_original_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            original, output, report = [Path(folder) / p for p in ("entrada.txt", "saida.txt", "relatorio.json")]
            original.write_bytes("\ufeffA\u00a0B\r\n🙂".encode())
            args = [sys.executable, str(SCRIPT), str(original), "-o", str(output), "--report", str(report)]
            run = subprocess.run(args, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(output.read_bytes(), "A B\r\n🙂".encode())
            self.assertTrue(original.read_bytes().startswith(b"\xef\xbb\xbf"))
            self.assertEqual(json.loads(report.read_text())["changed"], 2)
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 2)
            self.assertEqual(output.read_bytes(), "A B\r\n🙂".encode())

    def test_invalid_inputs_no_output(self):
        for data in (b"PK\x03\x04\0", b"caf\xe9", b"a" * (clean.MAX_BYTES + 1)):
            run = subprocess.run([sys.executable, str(SCRIPT), "-"], input=data, capture_output=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(run.stdout, b"")

    def test_pdf_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "entrada.pdf"
            file.write_bytes(b"%PDF-1.7")
            run = subprocess.run([sys.executable, str(SCRIPT), str(file)], capture_output=True)
            self.assertEqual(run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
