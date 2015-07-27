#
# Copyright 2015 Tickle Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
import shlex

from tclocalizable.localized_string import LocalizedString


class StringsTable(OrderedDict):

    def __init__(self, file_path=None, encoding='utf-16', save_when_exits=True):
        super(StringsTable, self).__init__()
        self._save_when_exits = save_when_exits

        if file_path:
            self.read_file(file_path, encoding=encoding)

    # I/O --------------------------------------------------------------------------------------------------------------

    def read_file(self, file_path, encoding='utf-16'):
        with open(file_path, 'r', encoding=encoding) as f:
            pending_comment_lines = ''
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith('"') and stripped_line.endswith(';'):
                    line_components = shlex.split(stripped_line[:-1])
                    if len(line_components) != 3 or line_components[1] != '=':
                        raise ValueError('Failed to parse line: {}'.format(line))
                    source = line_components[0]
                    localized = line_components[2]
                    comment = pending_comment_lines.strip().lstrip('/*').rstrip('*/').strip() or None
                    pending_comment_lines = ''
                    localized_string = LocalizedString(source, localized, comment)
                    self[source] = localized_string
                elif stripped_line.startswith('/*') or stripped_line.endswith('*/'):
                    pending_comment_lines += line

    def write_file(self, file_path, encoding='utf-16'):
        with open(file_path, 'w', encoding=encoding) as f:
            item_count = len(self)
            for idx, localized_string in enumerate(self.strings()):
                f.write(repr(localized_string))
                f.write('\n')
                if idx != item_count-1:
                    f.write('\n')

    # Interfaces -------------------------------------------------------------------------------------------------------

    def insert(self, source, localized=None, comment=None):
        localized_string = LocalizedString(source, localized=localized, comment=comment)
        self[source] = localized_string
        return localized_string

    def merge(self, another_strings_table, keep_comment=True, keep_localized=True, exclude_extra=False):
        """
        :param StringsTable another_strings_table: another strings table to merge in
        :param bool keep_comment: keep comment of duplicated/existed localized strings
        :param bool keep_localized: keep localized content of duplicated/existed localized strings
        :param bool exclude_extra: exclude localized strings which don't exist in another strings table
        """
        if exclude_extra:
            for key_to_remove in set(self.keys()) - set(another_strings_table.keys()):
                del self[key_to_remove]

        for source, another_localized_string in another_strings_table.items():
            if source in self:
                self_localized_string = self[source]
                if not keep_comment:
                    self_localized_string.comment = another_localized_string.comment
                if not keep_localized:
                    self_localized_string.localized = another_localized_string.localized
            else:
                self[source] = another_localized_string

    # Collections / Iters ----------------------------------------------------------------------------------------------

    def __getitem__(self, item):
        """
        :rtype: tclocalizable.localized_string.LocalizedString
        """
        return super(StringsTable, self).__getitem__(item)

    def get(self, key, **kwargs):
        """
        :rtype: tclocalizable.localized_string.LocalizedString
        """
        return super(StringsTable, self).get(key, **kwargs)

    # noinspection PyMethodOverriding
    def __setitem__(self, key, value):
        """
        :type key: str
        :type value: tclocalizable.localized_string.LocalizedString
        """
        if key != value.source:
            raise KeyError('The key and the source of value are not the same')
        super(StringsTable, self).__setitem__(key, value)

    def __iter__(self):
        """
        :rtype: collections.Iterable[str]
        """
        return super(StringsTable, self).__iter__()

    def keys(self):
        """
        :rtype: collections.Iterable[str]
        """
        return super(StringsTable, self).keys()

    # noinspection PyMethodOverriding
    def values(self):
        """
        :rtype: collections.Iterable[tclocalizable.localized_string.LocalizedString]
        """
        return super(StringsTable, self).values()

    def items(self):
        """
        :rtype: collections.Iterable[(str, tclocalizable.localized_string.LocalizedString)]
        """
        return super(StringsTable, self).items()

    def strings(self):
        """
        :rtype: collections.Iterable[tclocalizable.localized_string.LocalizedString]
        """
        return super(StringsTable, self).values()
