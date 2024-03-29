import builtins
from functools import wraps
from warnings import warn

def stringify(iterable):
    return [str(item).strip() for item in iterable]

def needs_rebuild(method):
    """Indicate a method will mutate the table.
    """
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        self._needs_rebuild = True
        method(self, *args, **kwargs)

    return wrapped


class Table:
    """
    Pretty-prints tabular data.

    Notes
    -----
    Tables have fancy indexing, table below describes possible keys:
                                     ╷
                   key               │                      value
    ╶────────────────────────────────┼─────────────────────────────────────────────────╴
                 `n: int`            │                     row `n`
              `..., m: int`          │                   column `m`
             `n: int, m:int`         │                   cell `n, m`
               `label: str`          │             column labeled `label`
             `ns: list[int]`         │       Table with rows selected from `ns`
           `..., ms: list[int]`      │      Table with columns selected from `ms`
      `ns: list[int], ms: list[int]` │ Table with rows from `ns` and columns from `ms`
           `labels: list[str]`       │  Table with columns with labels from `labels`
                                     ╵

    Additional Notes
    ----------------
    Table.STYLES contains the various options for `styles` kwarg.

    Example
    -------
    ```
    >>> t = Table(
    ...     [
    ...         ['John Smith', '356 Grove Rd', '123-4567'],
    ...         ['Mary Sue', '311 Penny Lane', '555-2451'],
    ...     ],
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

    # Characters in STYLES come in the following order:
    #    vertical (outer), horizontal (outer), vertical (inner), horizontal (inner),
    #    top-left, top-middle, top-right, middle-left, middle-middle (4-way), middle-right,
    #    bottom-left, bottom-middle, bottom-right, top-middle (inner)
    STYLES = {
        "light"            : '│─│─┌┬┐├┼┤└┴┘┬',
        "heavy"            : '┃━┃━┏┳┓┣╋┫┗┻┛┳',
        'light-inner'      : '  │─ ╷ ╶┼╴ ╵ ┬',
        'heavy-inner'      : '  ┃━ ╻ ╺╋╸ ╹ ┳',
        "curved"           : '│─│─╭┬╮├┼┤╰┴╯┬',
        'ascii'            : '|-|-++++++++++',
        "double"           : '║═║═╔╦╗╠╬╣╚╩╝╦',
        'double-vertical'  : '║─║─╓╥╖╟╫╢╙╨╜╥',
        'double-horizontal': '│═│═╒╤╕╞╪╡╘╧╛╤',
        'whitespace'       : '              ',
    }

    def __init__(self, rows, labels=None, centered=False, padding=1, style="light", title=None, min_width=0):
        self.columns = [stringify(column) for column in zip(*rows, strict=True)]
        self.labels = labels
        self.centered = centered
        self.padding = padding
        self.style = style
        self.title = title
        self.min_width = min_width

    def _build_table(self):
        """Creates a representation of this table as a string.
        """
        if not self.columns:
            self._as_string = ''
            return

        if self.labels:
            columns = [[label] + column for label, column in zip(self.labels, self.columns, strict=True)]
        else:
            columns = [column.copy() for column in self.columns]

        padding = self.padding
        pad = ' ' * padding

        # Strings in each column will be made same length.
        for column in columns:
            max_length = max(map(len, column))
            width = max(max_length, self.min_width)
            for i, item in enumerate(column):
                column[i] = f'{pad}{item:^{width}}{pad}' if self.centered else f'{pad}{item:<{width}}{pad}'

        # For brevity's sake, we've given our line characters short names.  Respectively, they stand for:
        # outer-vertical, outer-horizontal, inner-vertical, inner-horizontal, top-left, top-middle, top-right
        # middle-left, 'x' for 'cross', middle-right, bottom-left, bottom-middle, bottom-right, top-middle-inner
        ov, oh, iv, ih, tl, tm, tr, ml, x, mr, bl, bm, br, tmi = Table.STYLES[self.style]

        outer_horiz = tuple(oh * len(column[0]) for column in columns)
        inner_horiz = tuple(ih * len(column[0]) for column in columns)

        rows = [f'{ov}{f"{iv}".join(row)}{ov}' for row in zip(*columns, strict=True)]

        if self.labels:
            label_border_bottom = f'{ml}{x.join(inner_horiz)}{mr}'
            rows.insert(1, label_border_bottom)

        if self.title:
            max_title_width = len(rows[0]) - 2 * self.padding - 2
            if len(self.title) > max_title_width:
                title = f'{ov}{pad}{self.title[:max_title_width - 3]}...{pad}{ov}'
            else:
                title = f'{ov}{pad}{self.title:^{max_title_width}}{pad}{ov}'

            title_border_top = f'{tl}{oh * (max_title_width + 2 * padding)}{tr}'
            title_border_bottom = f'{ml}{tmi.join(inner_horiz)}{mr}'
            rows = [title_border_top, title, title_border_bottom] + rows
        else:
            top_border =  f'{tl}{tm.join(outer_horiz)}{tr}'
            rows.insert(0, top_border)

        bottom_border = f'{bl}{bm.join(outer_horiz)}{br}'
        rows.append(bottom_border)

        self._as_string = '\n'.join(rows)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, new_labels):
        if new_labels is not None:
            new_labels = stringify(new_labels)
            if len(new_labels) != len(self.columns):
                raise ValueError('labels inconsistent with number of columns')

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
            raise ValueError('need column data or a default value')

        if column is not None and default is not None:
            warn('default ignored if column provided')

        if self.labels is not None and label is None:
            raise ValueError('label is required')

        if self.labels is None and label is not None:
            warn(f'label ignored: {type(self).__name__} has no labels')

        if index is None:
            index = len(self.columns)

        if column is not None:
            column_as_strings = stringify(column)

            if self.columns and len(column_as_strings) != len(self.columns[0]):
                raise ValueError('column length mismatch')

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
            warn('no columns: expanding table to fit row')
            self.columns = [[item] for item in row_as_strings]
            return

        if len(row_as_strings) != len(self.columns):
            raise ValueError('row length mismatch')

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
        table = type(self)([])
        for attr in type(self).__slots__:
            if attr == 'columns':
                setattr(table, 'columns', [column.copy() for column in self.columns])
            elif attr != '_as_string':
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
        match key:
            case tuple((int() as row, int() as col)):
                self.columns[col][row] = str(item).strip()
            case _:
                raise ValueError('invalid key')

    def __getitem__(self, key):
        """
        Tables have fancy indexing, table below describes possible keys:
                                         ╷
                       key               │                      value
        ╶────────────────────────────────┼─────────────────────────────────────────────────╴
                     `n: int`            │                     row `n`
                  `..., m: int`          │                   column `m`
                 `n: int, m:int`         │                   cell `n, m`
                   `label: str`          │             column labeled `label`
                 `ns: list[int]`         │       Table with rows selected from `ns`
               `..., ms: list[int]`      │      Table with columns selected from `ms`
          `ns: list[int], ms: list[int]` │ Table with rows from `ns` and columns from `ms`
               `labels: list[str]`       │  Table with columns with labels from `labels`
                                         ╵
        """
        match key:
            case list((int(), *_)):
                rows, cols = key, ...
            case list((str(), *_)) if self.labels:
                rows, cols = ..., [self.labels.index(label) for label in key]
            case str() if self.labels:
                rows, cols = ..., self.labels.index(key)
            case int():
                rows, cols = key, ...
            case tuple((rows, cols)):
                pass
            case _:
                raise ValueError('invalid key')

        match (rows, cols):
            case (builtins.Ellipsis, int()):
                return self.columns[cols]  # Return column
            case (builtins.Ellipsis, list()):
                table = self.copy()
                table.columns = [self.columns[i] for i in cols]

                if self.labels:
                    table.labels = [self.labels[i] for i in cols]

                return table
            case (int(), builtins.Ellipsis):
                return [column[rows] for column in self.columns]  # Return row
            case (int(), int()):
                return self.columns[cols][rows]
            case (list(), builtins.Ellipsis):
                table = self.copy()
                table.columns = [[column[row] for row in rows] for column in self.columns]
                return table
            case (list(), list()):
                table = self.copy()
                columns = [self.columns[i] for i in cols]
                table.columns = [[column[row] for row in rows] for column in columns]

                if self.labels:
                    table.labels = [self.labels[i] for i in cols]

                return table
            case _:
                raise ValueError('invalid key')

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
