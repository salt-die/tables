# Tables

Pretty print tabular data:
```py
>>> t = Table(
...     ['John Smith', '356 Grove Rd', '123-4567'],
...     ['Mary Sue', '311 Penny Lane', '555-2451'],
...     labels=['Name', 'Address', 'Phone Number'],
... )

>>> print(t)
┌────────────┬────────────────┬──────────────┐
│ Name       │ Address        │ Phone Number │
├────────────┼────────────────┼──────────────┤
│ John Smith │ 356 Grove Rd   │ 123-4567     │
│ Mary Sue   │ 311 Penny Lane │ 555-2451     │
└────────────┴────────────────┴──────────────┘
```
```py
>>> t = Table(
...     ['spotted','dog','pants','heavily'],
...     ['black','cat','meows','loudly'],
...     ['tall','man','runs','quickly'],
...     labels=['adjective','noun','verb','adverb'],
...     centered=True,
...     style='double',
...     padding=3,
... )

>>> print(t)
╔═══════════════╦══════════╦═══════════╦═════════════╗
║   adjective   ║   noun   ║   verb    ║   adverb    ║
╠═══════════════╬══════════╬═══════════╬═════════════╣
║    spotted    ║   dog    ║   pants   ║   heavily   ║
║     black     ║   cat    ║   meows   ║   loudly    ║
║     tall      ║   man    ║   runs    ║   quickly   ║
╚═══════════════╩══════════╩═══════════╩═════════════╝

>>> t.add_row(['red', 'fox', 'jumped', 'incredibly']); t.add_column(label='article', index=0, default='a'); print(t)
╔═════════════╦═══════════════╦══════════╦════════════╦════════════════╗
║   article   ║   adjective   ║   noun   ║    verb    ║     adverb     ║
╠═════════════╬═══════════════╬══════════╬════════════╬════════════════╣
║      a      ║    spotted    ║   dog    ║   pants    ║    heavily     ║
║      a      ║     black     ║   cat    ║   meows    ║     loudly     ║
║      a      ║     tall      ║   man    ║    runs    ║    quickly     ║
║      a      ║      red      ║   fox    ║   jumped   ║   incredibly   ║
╚═════════════╩═══════════════╩══════════╩════════════╩════════════════╝
```

Tables have fancy indexing, table below describes possible keys:

```
                         ╷
    key                  │ value
  ╶──────────────────────┼──────────────────────────────────────────────────╴
    n: int               │ row `n`
    ..., m: int          │ column `m`
    n: int, m:int        │ cell `n, m`
    label: str           │ column labeled `label`
    ns: list[int]        │ Table with rows selected from `ns`
    ..., ms: list[int]   │ Table with columns seleced from `ms`
    labels: list[str]    │ Table with columns with labels given by `labels`
                         ╵
```