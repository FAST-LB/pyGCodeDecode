"""Test for progress bar and custom_print interaction."""

import time

from pyGCodeDecode.helpers import ProgressBar, custom_print, set_verbosity_level


def test_progress_bar_with_interruptions(capsys):
    """Run the test and capture output."""
    set_verbosity_level(3)
    pb1 = ProgressBar("Test Process 1", 20)
    for i in range(101):
        pb1.update(i / 100.0)
        if i == 30:
            custom_print("This is a warning message during progress", lvl=1)
        elif i == 60:
            custom_print("This is an info message during progress", lvl=2)
        time.sleep(0.001)
    assert pb1.last_progress_update == 100

    pb2 = ProgressBar("Test Process 2", 15, verbosity_level=1)
    for i in range(101):
        pb2.update(i / 100.0)
        if i == 50:
            custom_print("Another message in the middle", lvl=2)
        time.sleep(0.001)
    assert pb2.last_progress_update == 100

    custom_print("All tests completed!", lvl=2)

    out, _ = capsys.readouterr()
    expected = (
        "[WARN] This is a warning message during progress\n"
        "[INFO] This is an info message during progress\n"
        "[INFO] ✅ Done with Test Process 1\n"
        "[INFO] Another message in the middle\n"
        "[WARN] ✅ Done with Test Process 2\n"
        "[INFO] All tests completed!\n"
    )
    # expected = (
    #     "[WARNING] This is a warning message during progress\n"
    #     "[  INFO ] This is an info message during progress\n"
    #     "[  INFO ] ✅ Done with Test Process 1\n"
    #     "[  INFO ] Another message in the middle\n"
    #     "[WARNING] ✅ Done with Test Process 2\n"
    #     "[  INFO ] All tests completed!\n"
    # )

    # Normalize whitespace for progress bar lines
    def normalize(line):
        return line.rstrip()

    out_lines = [normalize(lin) for lin in out.splitlines()]
    exp_lines = [normalize(lin) for lin in expected.splitlines()]
    # Only keep lines that are expected (messages and final progress bars)
    filtered_out_lines = [
        lin for lin in out_lines if lin.startswith("[WARN]") or lin.startswith("[INFO]") or "✅ Done" in lin
    ]
    # filtered_out_lines = [
    #     lin
    #     for lin in out_lines
    #     if lin.startswith("[WARNING]") or lin.startswith("[  INFO ]") or "✅ Done" in lin
    # ]
    assert exp_lines == filtered_out_lines


def test_progress_bar_no_interruptions(capsys):
    """Test progress bar without interruptions."""
    set_verbosity_level(3)
    pb = ProgressBar("No Interruptions", 10)
    for i in range(101):
        pb.update(i / 100.0)
        time.sleep(0.001)
    assert pb.last_progress_update == 100
    custom_print("Done without interruptions", lvl=2)
    out, _ = capsys.readouterr()
    assert "[INFO] ✅ Done with No Interruptions" in out
    assert "[INFO] Done without interruptions" in out


def test_progress_bar_multiple_messages(capsys):
    """Test progress bar with multiple messages at different points."""
    set_verbosity_level(3)
    pb = ProgressBar("Multiple Messages", 5)
    for i in range(101):
        pb.update(i / 100.0)
        if i == 20:
            custom_print("First info", lvl=2)
        if i == 40:
            custom_print("Second warning", lvl=1)
        if i == 80:
            custom_print("Third info", lvl=2)
        time.sleep(0.001)
    assert pb.last_progress_update == 100
    out, _ = capsys.readouterr()
    assert "[INFO] First info" in out
    assert "[WARN] Second warning" in out
    assert "[INFO] Third info" in out
    assert "[INFO] ✅ Done with Multiple Messages" in out
