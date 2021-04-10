from warnings import warn

from .utils import strict_zip, stringify, needs_rebuild


class Table:
    """
    Pretty-prints tabular data.

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

    STYLES = {
        "light" : "│─┌┬┐├┼┤└┴┘",
        "heavy" : "┃━┏┳┓┣╋┫┗┻┛",
        "double": "║═╔╦╗╠╬╣╚╩╝",
        "curved": "│─╭┬╮├┼┤╰┴╯",
        'ascii' : '|-+++++++++',
    }

    def __init__(self, *rows, labels=None, centered=False, padding=1, style="light"):
        self._needs_rebuild = True

        self.columns = [stringify(column) for column in strict_zip(*rows)]

        self.labels = labels
        self.centered = centered
        self.padding = padding
        self.style = style

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
            for i, item in enumerate(column):
                column[i] = f'{item:^{max_length}}' if self.centered else f'{item:<{max_length}}'

        rows = list(strict_zip(*table))  # Transpose

        v, h, tl, tm, tr, ml, x, mr, bl, bm, br = self.STYLES[self.style]
        pad = self.padding * " "
        horizontals = tuple(h * (len(item) + 2 * self.padding) for item in rows[0])

        rows = [f'{v}{pad}{f"{pad}{v}{pad}".join(row)}{pad}{v}' for row in rows]

        top = f'{tl}{tm.join(horizontals)}{tr}'
        rows.insert(0, top)

        if self.labels:
            title = f'{ml}{x.join(horizontals)}{mr}'
            rows.insert(2, title)

        bottom = f'{bl}{bm.join(horizontals)}{br}'
        rows.append(bottom)

        self._as_string = "\n".join(rows)

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
        raise NotImplementedError

    @needs_rebuild
    def remove_row(self, index):
        raise NotImplementedError

    def __setattr__(self, attr, value):
        if attr != '_needs_rebuild':  # Indicate that table needs to be rebuilt
            self._needs_rebuild = attr != '_as_string'
        super().__setattr__(attr, value)

    def __setitem__(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __str__(self):
        if self._needs_rebuild:
            self._build_table()
        return self._as_string

    def __repr__(self):
        return (
            f'{type(self).__name__}[{len(self.columns[0])}, {len(self.columns)}]'
            f'(labels={bool(self.labels)}, centered={self.centered}, padding={self.padding}, style={self.style})'
        )

    def show(self):
        print(str(self))
