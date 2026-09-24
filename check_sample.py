"""check_sample.py：按 sample/ops.json 走一圈，打印验收面。"""
import json
import os
import sys

from tombgc import TombStore


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "ops.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    store = TombStore(spec["budget"])
    for step in spec["ops"]:
        if step["op"] == "put":
            store.put(step["key"], step["value"], step["at"])
        else:
            store.delete(step["key"], step["at"])
    first = store.sweep(spec["watermark"])
    second = store.sweep(spec["watermark"])
    blob = store.persist()
    reborn = TombStore(spec["budget"])
    restored = reborn.restore(blob)
    print("第一轮清理的墓碑数 =", first.get("cleared"))
    print("第二轮清理的墓碑数 =", second.get("cleared"))
    print("剩余墓碑数 =", second.get("remaining"))
    print("安全点 =", second.get("watermark"))
    print("可清理但受预算限制的墓碑 =", second.get("deferred"))
    print("恢复后的剩余墓碑 =", restored.get("remaining"))
    print("恢复后的清理计数 =", restored.get("cleared"))
    print("不变量（安全点之后的墓碑一个没清） =", spec["safety_invariant"])
    print("清理预算 =", spec["budget"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
