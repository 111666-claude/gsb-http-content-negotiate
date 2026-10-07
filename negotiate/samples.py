"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "q":
        out = core.choose("text/html;q=0.5, application/json;q=1.0",
                          ["text/html", "application/json"], core.Counter())
        _line({"type": out})
        return 0
    if name == "wildcard":
        out = core.choose("text/*;q=1.0, application/json;q=0.5",
                          ["text/plain", "application/json"], core.Counter())
        _line({"type": out})
        return 0
    if name == "all":
        out = core.choose("*/*", ["text/plain"], core.Counter())
        _line({"type": out})
        return 0
    if name == "zeroq":
        out = core.choose("text/html;q=0", ["text/html"], core.Counter())
        _line({"type": out})
        return 0
    if name == "work":
        header = ", ".join("t%04d/x" % i for i in range(800))
        types = ["s%04d/x" % i for i in range(800)]
        counter = core.Counter()
        core.choose(header, types, counter)
        _line({"types": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
