from warnings import warn

from .utils import strict_zip, stringify, needs_rebuild


class Table:
    """
    Pretty-prints tabular data.

    Notes
    -----
    Tables have fancy indexing, table below describes possible keys:
                               ╷
          key                  │ value
        ╶──────────────────────┼──────────────────────────────────────────────────╴
          `n: int`             │ row `n`
          `..., m: int`        │ column `m`
          `n: int, m:int`      │ cell `n, m`
          `label: str`         │ column labeled `label`
          `ns: list[int]`      │ Table with rows selected from `ns`
          `..., ms: list[int]` │ Table with columns seleced from `ms`
          `labels: list[str]`  │ Table with columns with labels given by `labels`
                               ╵

    Additional Notes
    ----------------
    Table.STYLES contains the various options for `styles` kwarg.

    Example
    -------
    ```
    >>> t = Table(
    ...     ['John Smith', '356 Grove Rd', '123-4567'],
    ...     ['Mary Sue', '311 Penny Lane', '555-2451'],
    ...     labels=['Name', 'Address', 'Phone Number'],
    ... )
    ...
    >>> print(t)
    ┌────────────┬────────────────┬──────────────┐
    │ Name       │ Address        │ Phone Number │
    ├────────────┼────────────────┼──────────────┤
    │ John Smith │ 356 Grove Rd   │ 123-4567     │
    │ Mary Sue   │ 311 Penny Lane │ 555-2451     │
    └────────────┴────────────────┴──────────────┘
    ```
    """

    __slots__ = (
        '_needs_rebuild',
        '_as_string',
        'columns',
        '_labels',
        'centered',
        'padding',
        '_style',
        'title',
        'min_width',
    )

    STYLES = {
        "light"            : "│─│─┌┬┐├┼┤└┴┘┬",
        "heavy"            : "┃━┃━┏┳┓┣╋┫┗┻┛┳",
        'light-inner'      : '  │─ ╷ ╶┼╴ ╵ ┬',
        'heavy-inner'      : '  ┃━ ╻ ╺╋╸ ╹ ┳',
        "curved"           : "│─│─╭┬╮├┼┤╰┴╯┬",
        'ascii'            : '|-|-++++++++++',
        "double"           : "║═║═╔╦╗╠╬╣╚╩╝╦",
        'double-vertical'  : '║─║─╓╥╖╟╫╢╙╨╜╥',
        'double-horizontal': '│═│═╒╤╕╞╪╡╘╧╛╤',
        'whitespace'       : '              ',
    }

    def __init__(self, *rows, labels=None, centered=False, padding=1, style="light", title=None, min_width=0):
        self.columns = [stringify(column) for column in strict_zip(*rows)]

        self.labels = labels
        self.centered = centered
        self.padding = padding
        self.style = style
        self.title = title
        self.min_width = 0

    def _build_table(self):
        """Creates a representation of this table as a string.
        """
        if not self.columns:
            self._as_string = ''
            return

        if self.labels:
            table = [[label] + column for label, column in strict_zip(self.labels, self.columns)]
        else:
            table = [column.copy() for column in self.columns]

        # Strings in each column made same length
        for column in table:
            max_length = max(map(len, column))
            width = max(max_length, self.min_width)
            for i, item in enumerate(column):
                column[i] = f'{item:^{width}}' if self.centered else f'{item:<{width}}'

        rows = list(strict_zip(*table))  # Transpose

        # For brevity's sake, we've given our line characters short names.  Respectively, they stand for:
        # outer-vertical, outer-horizontal, inner-vertical, inner-horizontal, top-left, top-middle, top-right
        # middle-left, 'x' for 'cross', middle-right, bottom-left, bottom-middle, bottom-right, top-middle-inner
        ov, oh, iv, ih, tl, tm, tr, ml, x, mr, bl, bm, br, tmi = Table.STYLES[self.style]
        pad = self.padding * " "

        joined_rows = [f'{ov}{pad}{f"{pad}{iv}{pad}".join(row)}{pad}{ov}' for row in rows]

        outer_horiz = tuple(oh * (len(item) + 2 * self.padding) for item in rows[0])
        inner_horiz = tuple(ih * (len(item) + 2 * self.padding) for item in rows[0])

        if self.labels:
            label_border_bottom = f'{ml}{x.join(inner_horiz)}{mr}'
            joined_rows.insert(1, label_border_bottom)

        if self.title:
            max_title_width = len(joined_rows[0]) - 2 * self.padding - 2
            if len(self.title) > max_title_width:
                title = f'{ov}{pad}{self.title[:max_title_width - 3]}...{pad}{ov}'
            else:
                title = f'{ov}{pad}{self.title:^{max_title_width}}{pad}{ov}'

            title_border_top = f'{tl}{oh * (max_title_width + 2 * self.padding)}{tr}'
            title_border_bottom = f'{ml}{tmi.join(inner_horiz)}{mr}'
            joined_rows = [title_border_top, title, title_border_bottom] + joined_rows
        else:
            top_border =  f'{tl}{tm.join(outer_horiz)}{tr}'
            joined_rows.insert(0, top_border)

        bottom_border = f'{bl}{bm.join(outer_horiz)}{br}'
        joined_rows.append(bottom_border)

        self._as_string = "\n".join(joined_rows)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, new_labels):
        if new_labels is not None:
            new_labels = stringify(new_labels)
            if len(new_labels) != len(self.columns):
                raise ValueError("labels inconsistent with number of columns")

        self._labels = new_labels

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        if style not in Table.STYLES:
            styles = ', '.join(map(repr, Table.STYLES))
            raise ValueError(f'Style must be one of {styles}')
        self._style = style

    @needs_rebuild
    def add_column(self, column=None, index=None, label=None, default=None):
        """Add a new column to the table.
        """
        if column is None and default is None:
            raise ValueError("need column data or a default value")

        if column is not None and default is not None:
            warn("default ignored if column provided")

        if self.labels is not None and label is None:
            raise ValueError("label is required")

        if self.labels is None and label is not None:
            warn(f"label ignored: {type(self).__name__} has no labels")

        if index is None:
            index = len(self.columns)

        if column is not None:
            column_as_strings = stringify(column)

            if self.columns and len(column_as_strings) != len(self.columns[0]):
                raise ValueError("column length mismatch")

            self.columns.insert(index, column_as_strings)
        else:
            if not self.columns:
                self.columns.append([])
            else:
                self.columns.insert(index, [str(default).strip()] * len(self.columns[0]))

        if label is not None:
            self.labels.insert(index, str(label).strip())

    @needs_rebuild
    def add_row(self, row, index=None):
        """Add a new row to the table.
        """
        row_as_strings = stringify(row)

        if not self.columns:
            warn("no columns: expanding table to fit row")
            self.columns = [[item] for item in row_as_strings]
            return

        if len(row_as_strings) != len(self.columns):
            raise ValueError("row length mismatch")

        if index is None:
            index = len(self.columns[0])

        for i, item in enumerate(row_as_strings):
            self.columns[i].insert(index, item)

    @needs_rebuild
    def remove_column(self, index):
        """
        Notes
        -----
        'index' can also be a column label
        """
        if isinstance(index, str):
            index = self.labels.index(index)

        self.columns.pop(index)
        if self.labels:
            self.labels.pop(index)

    @needs_rebuild
    def remove_row(self, index):
        for column in self.columns:
            column.pop(index)

    def copy(self):
        table = type(self)()
        for attr in type(self).__slots__:
            if attr != '_as_string':  # A newly created table might not have this attribute.
                setattr(table, attr, getattr(self, attr))
        return table

    @needs_rebuild
    def relabel(self, old, new):
        """Replace the label `old` with the label `new`.
        """
        i = self.labels.index(old)
        self.labels[i] = new

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if attr != '_needs_rebuild':  # Indicate that table needs to be rebuilt
            self._needs_rebuild = attr != '_as_string'

    @needs_rebuild
    def __setitem__(self, key, item):
        if not isinstance(key, tuple) and len(key) != 2 and not isinstance(key[0], int) and not isinstance(key[1], int):
            raise ValueError("invalid key")

        row, col = key
        self.columns[col][row] = str(item).strip()

    def __getitem__(self, key):
        """
        Tables have fancy indexing, table below describes possible keys:
                               ╷
          key                  │ value
        ╶──────────────────────┼──────────────────────────────────────────────────╴
          `n: int`             │ row `n`
          `..., m: int`        │ column `m`
          `n: int, m:int`      │ cell `n, m`
          `label: str`         │ column labeled `label`
          `ns: list[int]`      │ Table with rows selected from `ns`
          `..., ms: list[int]` │ Table with columns seleced from `ms`
          `labels: list[str]`  │ Table with columns with labels given by `labels`
                               ╵
        """
        if isinstance(key, list):
            if isinstance(key[0], int):
                key = key, ...
            elif isinstance(key[0], str):
                if not self.labels:
                    raise ValueError('table has no labels')
                key = ..., [self.labels.index(label) for label in key]

        elif isinstance(key, str):
            if not self.labels:
                raise ValueError('table has no labels')
            key = ..., self.labels.index(key)

        elif isinstance(key, int):
            key = key, ...

        if not isinstance(key, tuple) and len(key) != 2:
            raise ValueError("invalid key")

        rows, cols = key
        if rows is ...:
            if isinstance(cols, int):
                return self.columns[cols]  # Return column
            elif isinstance(cols, list):   # Return Table with selected columns
                table = self.copy()
                table.columns = [self.columns[i] for i in cols]
                if self.labels:
                    table.labels = [self.labels[i] for i in cols]
                return table

        elif isinstance(rows, int):
            if cols is ...:
                return [column[rows] for column in self.columns]  # Return row
            elif isinstance(cols, int):
                return self.columns[cols][rows]

        elif isinstance(rows, list):
            if cols is ...:
                table = self.copy()
                table.columns = [[column[row] for row in rows] for column in self.columns]
                return table

        raise KeyError(key)

    def __str__(self):
        if self._needs_rebuild:
            self._build_table()
        return self._as_string

    def __repr__(self):
        return (
            f'{type(self).__name__}[{len(self.columns[0])}, {len(self.columns)}]'
            f'(labels={bool(self.labels)}, centered={self.centered}, padding={self.padding}, style={self.style!r}, '
            f'title={self.title!r}, min_width={self.min_width})'
        )

    def show(self):
        print(str(self))
