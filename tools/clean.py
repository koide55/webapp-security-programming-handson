from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    ROOT / "app" / "data.db",
    ROOT / "app" / "mail_outbox.txt",
    ROOT / "stolen_cookies.log",
    ROOT / "badscript_ran.txt",
    ROOT / "downloaded_badscript.py",
    ROOT / "command_injection_result.txt",
]


def main():
    removed = []
    for path in TARGETS:
        try:
            path.unlink()
            removed.append(path.relative_to(ROOT))
        except FileNotFoundError:
            pass

    if removed:
        print("Removed:")
        for path in removed:
            print(f"  {path}")
    else:
        print("Nothing to remove.")


if __name__ == "__main__":
    main()
