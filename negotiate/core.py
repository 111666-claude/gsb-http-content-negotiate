"""解析 Accept 头并按 q 值选择类型。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def parse_accept(header, counter):
    """把 Accept 头解析成 (精确表, 类型通配表, */* 的 q)。

    同一张表内出现多个相同范围时取最大 q；非法 q 按 0 处理，缺省为 1.0。
    """
    exact = {}
    partial = {}
    wildcard = None

    def put(table, key, q):
        old = table.get(key)
        if old is None or q > old:
            table[key] = q

    for part in header.split(","):
        counter.scanned += 1
        piece = part.strip()
        if not piece:
            continue
        bits = piece.split(";")
        mtype = bits[0].strip().lower()
        q = 1.0
        for bit in bits[1:]:
            bit = bit.strip()
            if bit.startswith("q="):
                try:
                    q = float(bit[2:])
                except ValueError:
                    q = 0.0
        if mtype == "*/*":
            if wildcard is None or q > wildcard:
                wildcard = q
        elif mtype.endswith("/*"):
            put(partial, mtype[:-2], q)
        elif "/" in mtype:
            put(exact, mtype, q)

    return exact, partial, wildcard


def _match(stype, parsed, counter):
    """返回候选类型的 (q, 特异性)；不被接受时返回 None。特异性 2>1>0。"""
    exact, partial, wildcard = parsed
    counter.scanned += 1
    q = exact.get(stype.lower())
    if q is not None:
        return q, 2
    counter.scanned += 1
    maintype = stype.split("/", 1)[0].lower() if "/" in stype else stype.lower()
    q = partial.get(maintype)
    if q is not None:
        return q, 1
    counter.scanned += 1
    if wildcard is not None:
        return wildcard, 0
    return None


def choose(header, server_types, counter):
    parsed = parse_accept(header, counter)
    best_type = ""
    best_q = 0.0
    best_spec = -1
    for stype in server_types:
        match = _match(stype, parsed, counter)
        if match is None:
            continue
        q, spec = match
        if q <= 0:
            continue
        if q > best_q or (q == best_q and spec > best_spec):
            best_type = stype
            best_q = q
            best_spec = spec
    return best_type
