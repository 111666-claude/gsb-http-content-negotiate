"""解析 Accept 头并按 q 值选择类型。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def parse_accept(header, counter):
    out = []
    for part in header.split(","):
        counter.scanned += 1
        piece = part.strip()
        if not piece:
            continue
        bits = piece.split(";")
        mtype = bits[0].strip()
        q = 1.0
        for bit in bits[1:]:
            bit = bit.strip()
            if bit.startswith("q="):
                try:
                    q = float(bit[2:])
                except ValueError:
                    q = 1.0
        out.append((mtype, q))
    return out


def choose(header, server_types, counter):
    for stype in server_types:
        counter.scanned += 1
        for mtype, _q in parse_accept(header, counter):
            counter.scanned += 1
            if mtype == stype:
                return stype
    return ""
