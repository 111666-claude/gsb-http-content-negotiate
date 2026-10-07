"""解析 Accept 头并按 q 值选择类型。"""

EXACT = 2
PREFIX = 1
WILDCARD = 0


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def parse_accept(header, counter):
    """解析一次 Accept 头，返回 {媒体范围: q}，所有候选共用。"""
    ranges = {}
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
                    q = float(bit[2:].strip())
                except ValueError:
                    q = 0.0
        if mtype and mtype not in ranges:
            ranges[mtype] = q
    return ranges


def _range_q(ranges, key, counter):
    counter.scanned += 1
    return ranges.get(key)


def best_match(stype, ranges, counter):
    """返回候选类型命中的最高特异性范围 (q, 特异性)，未命中返回 None。"""
    major = stype.split("/", 1)[0].lower()
    q = _range_q(ranges, stype.lower(), counter)
    if q is not None:
        return q, EXACT
    q = _range_q(ranges, major + "/*", counter)
    if q is not None:
        return q, PREFIX
    q = _range_q(ranges, "*/*", counter)
    if q is not None:
        return q, WILDCARD
    return None


def choose(header, server_types, counter):
    ranges = parse_accept(header, counter)
    best = None
    for stype in server_types:
        match = best_match(stype, ranges, counter)
        if match is None:
            continue
        q, specificity = match
        if q <= 0:
            continue
        if best is None or q > best[0] or (q == best[0] and specificity > best[1]):
            best = (q, specificity, stype)
    return "" if best is None else best[2]
