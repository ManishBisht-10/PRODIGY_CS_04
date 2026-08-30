import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from keystroke_logger import clear_log, start_logging, view_log


class KeystrokeLoggerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "keystrokes.txt"
        self.output = io.StringIO()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_start_logging_saves_and_displays_entered_text(self) -> None:
        entered = iter(["Hi!", ":stop"])

        start_logging(
            self.log_path,
            input_func=Mock(side_effect=entered),
            output_func=self.output.write,
        )

        self.assertEqual(self.log_path.read_text(encoding="utf-8"), "Hi!\n")
        displayed = self.output.getvalue()
        self.assertIn("Recording started.", displayed)
        self.assertIn("'H'", displayed)
        self.assertIn("'i'", displayed)
        self.assertIn("'!'", displayed)
        self.assertIn("Recording stopped.", displayed)

    def test_view_log_displays_saved_contents(self) -> None:
        self.log_path.write_text("hello\n", encoding="utf-8")

        view_log(self.log_path, output_func=self.output.write)

        self.assertIn("Saved log:", self.output.getvalue())
        self.assertIn("hello", self.output.getvalue())

    def test_clear_log_removes_saved_contents(self) -> None:
        self.log_path.write_text("secret-looking test text\n", encoding="utf-8")

        clear_log(self.log_path, output_func=self.output.write)

        self.assertEqual(self.log_path.read_text(encoding="utf-8"), "")
        self.assertIn("Saved log cleared.", self.output.getvalue())


if __name__ == "__main__":
    unittest.main()
