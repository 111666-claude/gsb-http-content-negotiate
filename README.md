# http-content-negotiate

按 Accept 头做内容协商：q 值、类型通配、精确优先、q=0 拒绝。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m negotiate --sample=q
python3 -m negotiate --sample=wildcard
python3 -m negotiate --sample=all
python3 -m negotiate --sample=zeroq
python3 -m negotiate --sample=work
```

## 口径

- **q 值**：默认为 1.0；不合法时按 0 处理。
- **匹配**：精确 `类型/子类型` 优先于 `类型/*`，`类型/*` 优先于 `*/*`。
- **选择**：先比 q 值，再比特异性，最后按服务端给出的顺序。
- **拒绝**：没有任何 Accept 项匹配、或匹配项的 q 为 0，都表示不可接受，返回空串。
- **解析**：Accept 头只解析一次，所有候选类型共用同一份解析结果。

## 不变量

- 返回的类型一定被 Accept 头接受且 q 大于 0。
- 同 q 同特异性时结果等于服务端顺序里最靠前的那个。
- `scanned` 不随 Accept 项数乘候选类型数放大：八百对八百的 `scanned` 不超过 6000。

## 输出契约

`choose(header, server_types)` 返回选中的类型或空串。场景打印一行 JSON。
`--sample=work` 打印 `{"types": N, "scanned": N}`。
