# Tickle Localizable

A utility tool for manipulating content of the `strings` file. (Localization table of OS X and iOS).

## Install

You can install this lib by pip like:
```shell
pip install tclocalizable
```

Note that this utility is written for Python 3, so you must use Python 3.

## Quickstart

### I/O

There are 2 mandatary I/O methods: `read_file` and `write_file`.

```python
from tclocalizable.strings_table import StringsTable
strings_table = StringsTable()
strings_table.read_file(some_file_path)
# After some manipulation
strings_table.write_file(some_file_path)
```

`tclocalizable` reads/writes only UTF-16 strings file by default.
It you're manipulating UTF-8 or other encoding files, remember to set encoding argument. Like:
```python
strings_table.read_file(some_file_path, encoding='utf-8')
```

Another shortcut method to read a strings file in is to pass file path to the constructor directly. Like:
```python
from tclocalizable.strings_table import StringsTable
strings_table = StringsTable(some_file_path, encoding='utf-8')
```

### I/O Helpers

`tclocalizable` also provides a helper to iterate the content of a strings file by:
```python
from tclocalizable.strings_table import StringsTable
for localized_string in StringsTable.localized_strings_in_file(some_file_path, encoding='utf-8'):
    pass  # The `localized_string` is an instance of `tclocalizable.localized_string.LocalizedString`
```

### Dictionary Interface

The `StringsTable` class extends from
[`collections.OrderedDict`](https://docs.python.org/3/library/collections.html#collections.OrderedDict),
so you can use it just like how you use `OrderedDict`.

The `key` of the dictionary would be the original untranslated string, and the value would be instances of
`tclocalizable.localized_string.LocalizedString`.

For example:
```python
from tclocalizable.strings_table import StringsTable
strings_table = StringsTable(some_file_path, encoding='utf-8')

for key, localized_string in strins_table.values():
    pass  # Here, key is `str` and localized_string is `tclocalizable.localized_string.LocalizedString`
```

### LocalizedString instances

There are 3 main properties:

property  | description
----------|-------------
source    | the original key string.
localized | translated string
comment   | comment of an entry

```
/* comment */
"source" = "localized";
```


## Tests

Run tests by

```shell
./tests.py
```
