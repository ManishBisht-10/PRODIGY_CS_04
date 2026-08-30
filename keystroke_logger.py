"""Consent-based keystroke logging demonstration.

This program records only text entered at its own prompt. It does not use
global keyboard hooks and cannot see keys typed in other applications.
"""

from pathlib import Path
from typing import Callable


LOG_FILE = Path("keystrokes.txt")
STOP_COMMAND = ":stop"


def _display_keys(text: str, output_func: Callable[[str], None]) -> None:
    """Show every character in a line using repr(), including spaces."""
    for character in text:
        output_func(f"  {character!r}")


def stop_logging(output_func: Callable[[str], None] = print) -> None:
    """Tell the user that recording has stopped."""
    output_func("\nRecording stopped.")


def start_logging(
    log_path: Path = LOG_FILE,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> None:
    """Record lines entered at this program's prompt until :stop is entered."""
    output_func("\nRecording started.")
    output_func(f"Type text below. Enter {STOP_COMMAND!r} on its own line to stop.")

    try:
        with log_path.open("a", encoding="utf-8") as log:
            while True:
                try:
                    line = input_func("record> ")
                except (EOFError, KeyboardInterrupt):
                    output_func("\nInput ended.")
                    break

                if line == STOP_COMMAND:
                    break

                _display_keys(line, output_func)
                log.write(line + "\n")
                log.flush()
    except OSError as error:
        output_func(f"Could not save the log: {error}")
    finally:
        stop_logging(output_func)


def view_log(
    log_path: Path = LOG_FILE,
    output_func: Callable[[str], None] = print,
) -> None:
    """Display the saved log, without interpreting its contents."""
    try:
        contents = log_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        output_func("No saved log exists yet.")
    except OSError as error:
        output_func(f"Could not read the log: {error}")
    else:
        output_func("\nSaved log:")
        output_func(contents if contents else "(The log is empty.)")


def clear_log(
    log_path: Path = LOG_FILE,
    output_func: Callable[[str], None] = print,
) -> None:
    """Clear the saved log after the user has selected this menu option."""
    try:
        log_path.write_text("", encoding="utf-8")
    except OSError as error:
        output_func(f"Could not clear the log: {error}")
    else:
        output_func("Saved log cleared.")


def main() -> None:
    """Run the interactive menu."""
    menu = """
1. Start recording
2. Stop recording
3. View the saved log
4. Clear the log
5. Exit
"""

    while True:
        print(menu)
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if choice == "1":
            start_logging()
        elif choice == "2":
            print("Recording can only be stopped from the recording prompt.")
        elif choice == "3":
            view_log()
        elif choice == "4":
            clear_log()
        elif choice == "5":
            print("Goodbye.")
            return
        else:
            print("Please choose an option from 1 to 5.")


if __name__ == "__main__":
    main()
