"""Download counter for the published files.

GitHub counts downloads per release asset, but the daily file is replaced every day and its counter starts again
at zero. `collect` therefore adds the count of the file about to be replaced to downloads.json; `report` prints the
totals for status.md.

Usage (in the workflow):  python -m agps.downloads collect   (before replacing the daily file)
                          python -m agps.downloads report    (after publishing, output appended to status.md)
"""
import datetime, json, os, subprocess, sys

STORE = "downloads.json"
DAILY = "NML_28A.ee"


def assets(release):
    """[(name, download count)] of a release, empty if the release does not exist."""
    r = subprocess.run(["gh", "release", "view", release, "--json", "assets"], capture_output=True, text=True)
    if r.returncode != 0:
        return []
    return [(a["name"], int(a.get("downloadCount", 0))) for a in json.loads(r.stdout).get("assets", [])]


def load():
    if os.path.exists(STORE):
        with open(STORE) as f:
            return json.load(f)
    return {"since": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"), "previous_versions": 0, "daily": []}


def collect():
    data = load()
    count = next((n for name, n in assets("current") if name == DAILY), None)
    if count is not None:
        data["previous_versions"] += count
        data["daily"].append({"replaced": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"), "downloads": count})
    with open(STORE, "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    print("downloads of the replaced daily file:", count)


def report():
    data = load()
    current = next((n for name, n in assets("current") if name == DAILY), 0)
    arch = assets("archive")
    arch_total = sum(n for _, n in arch)
    daily_total = data["previous_versions"] + current
    lines = ["", "## Downloads", "", "- Total: %d" % (daily_total + arch_total)]
    print("\n".join(lines))


if __name__ == "__main__":
    {"collect": collect, "report": report}[sys.argv[1]]()
