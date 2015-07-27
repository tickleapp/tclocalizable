#!/usr/bin/env python3
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
from collections import namedtuple
import os
import tempfile
import unittest
from tclocalizable.strings_table import StringsTable
from tclocalizable.localized_string import LocalizedString

source_root = os.path.abspath(os.path.dirname(__file__))
ExpectedResult = namedtuple('ExpectedResult', ['souce', 'localized', 'comment'])


class TestStringsTableContentMixin(object):
    default_expected_results = (
        ExpectedResult("%@ doesn't have a list named %@.", "%1$@ は %2$@ というリストをもっていません。", "Some comemnt"),
        ExpectedResult("Cannot get the version of this Tickle document.",
                       "Cannot get the version of this Tickle document.",
                       'Error message when Tickle tries to open a document but fails to fetch the version info,\n'
                       '   English source is "Cannot get the version of this Tickle document."'),
        ExpectedResult("No comment", "沒有註解", None),
        ExpectedResult("String with \"quote\".\"", "有引號的字\"", "Comment with \"quote\""),
        ExpectedResult("String with =", "String with =", "String with ="),
        ExpectedResult("String with ;", "String with ;", "String with semicolon"),
        ExpectedResult(r"String\twith \n", r"String\twith \n", "String with spaces"),
        ExpectedResult("String not translated", "String not translated", "Not translated"),
    )
    """:type: tuple[ExpectedResult]"""

    # noinspection PyUnresolvedReferences
    def _test_strings_table_content(self, strings_table, expected_results=default_expected_results):
        self.assertEqual(len(strings_table), len(expected_results))
        for idx, localized_strings in enumerate(strings_table.values()):
            expected_result = expected_results[idx]
            self.assertEqual(expected_result.souce, localized_strings.source)
            self.assertEqual(expected_result.localized, localized_strings.localized)
            self.assertEqual(expected_result.comment, localized_strings.comment)


class TestIOStringsFile(unittest.TestCase, TestStringsTableContentMixin):

    def test_read_16(self):
        self._test_strings_table_content(StringsTable(os.path.join(source_root, 'example16.strings')))

    def test_read_8(self):
        self._test_strings_table_content(StringsTable(os.path.join(source_root, 'example.strings'), encoding='utf-8'))

    def test_write_16(self):
        self.maxDiff = 1024
        strings_table = StringsTable(os.path.join(source_root, 'example16.strings'))

        with tempfile.TemporaryDirectory() as tmp_dir:
            strings_table['String with ;'].localized = '有分號的字'
            strings_table['String with ='].comment = 'String with "equal" sign'
            strings_table.insert('String not translated 2', comment='Another not translated')

            output_file_path = os.path.join(tmp_dir, 'example16.strings')
            strings_table.write_file(output_file_path)
            with open(output_file_path, 'r', encoding='utf-16') as f:
                result = f.read()

            self.assertEqual(result, r'''/* Some comemnt */
"%@ doesn't have a list named %@." = "%1$@ は %2$@ というリストをもっていません。";

/* Error message when Tickle tries to open a document but fails to fetch the version info,
   English source is "Cannot get the version of this Tickle document." */
"Cannot get the version of this Tickle document." = "Cannot get the version of this Tickle document.";

"No comment" = "沒有註解";

/* Comment with "quote" */
"String with \"quote\".\"" = "有引號的字\"";

/* String with "equal" sign */
"String with =" = "String with =";

/* String with semicolon */
"String with ;" = "有分號的字";

/* String with spaces */
"String\twith \n" = "String\twith \n";

/* Not translated */
"String not translated" = "";

/* Another not translated */
"String not translated 2" = "";
''')

    def test_write_8(self):
        self.maxDiff = 1024
        strings_table = StringsTable(os.path.join(source_root, 'example.strings'), encoding='utf-8')

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_file_path = os.path.join(tmp_dir, 'example.strings')
            strings_table.write_file(output_file_path, encoding='utf-8')

            with open(output_file_path, 'r') as f:
                result = f.read()

            self.assertEqual(result, r'''/* Some comemnt */
"%@ doesn't have a list named %@." = "%1$@ は %2$@ というリストをもっていません。";

/* Error message when Tickle tries to open a document but fails to fetch the version info,
   English source is "Cannot get the version of this Tickle document." */
"Cannot get the version of this Tickle document." = "Cannot get the version of this Tickle document.";

"No comment" = "沒有註解";

/* Comment with "quote" */
"String with \"quote\".\"" = "有引號的字\"";

/* String with = */
"String with =" = "String with =";

/* String with semicolon */
"String with ;" = "String with ;";

/* String with spaces */
"String\twith \n" = "String\twith \n";

/* Not translated */
"String not translated" = "";
''')

    def test_write_not_translated(self):
        self.maxDiff = 1024
        strings_table = StringsTable(os.path.join(source_root, 'example.strings'), encoding='utf-8')

        with tempfile.TemporaryDirectory() as tmp_dir:
            strings_table["String not translated"].localized = "QQ"

            output_file_path = os.path.join(tmp_dir, 'example.strings')
            strings_table.write_file(output_file_path, encoding='utf-8')
            with open(output_file_path, 'r') as f:
                result = f.read()

            self.assertEqual(result, r'''/* Some comemnt */
"%@ doesn't have a list named %@." = "%1$@ は %2$@ というリストをもっていません。";

/* Error message when Tickle tries to open a document but fails to fetch the version info,
   English source is "Cannot get the version of this Tickle document." */
"Cannot get the version of this Tickle document." = "Cannot get the version of this Tickle document.";

"No comment" = "沒有註解";

/* Comment with "quote" */
"String with \"quote\".\"" = "有引號的字\"";

/* String with = */
"String with =" = "String with =";

/* String with semicolon */
"String with ;" = "String with ;";

/* String with spaces */
"String\twith \n" = "String\twith \n";

/* Not translated */
"String not translated" = "QQ";
''')


class TestManipulateStringsFile(unittest.TestCase):

    def test_create(self):
        self.assertEqual(len(StringsTable()), 0)

    def test_create_item(self):
        localized_string = LocalizedString('A key', 'una chiave', 'Name of object used to open locks')
        self.assertEqual(localized_string.source, 'A key')
        self.assertEqual(localized_string.localized, 'una chiave')
        self.assertEqual(localized_string.comment, 'Name of object used to open locks')

        localized_string = LocalizedString('A key', 'ένα κλειδί', None)
        self.assertEqual(localized_string.source, 'A key')
        self.assertEqual(localized_string.localized, 'ένα κλειδί')
        self.assertIsNone(localized_string.comment)

    def test_item_equal(self):
        localized_string_1 = LocalizedString('A string', '一個字串', None)
        localized_string_2 = LocalizedString('A string', '一個字串', 'a type used to represent words')
        localized_string_3 = LocalizedString('A string', '一個字串', None)

        self.assertIsNot(localized_string_1, localized_string_3)
        self.assertEqual(localized_string_1, localized_string_3)
        self.assertNotEqual(localized_string_1, localized_string_2)

    def test_get(self):
        strings_table_16 = StringsTable(os.path.join(source_root, 'example16.strings'))
        self.assertEqual(strings_table_16["No comment"].source, "No comment")
        self.assertEqual(strings_table_16["No comment"].localized, "沒有註解")
        self.assertIsNone(strings_table_16["No comment"].comment)

        with self.assertRaises(KeyError):
            # noinspection PyStatementEffect
            strings_table_16['No such key']

    def test_set(self):
        strings_table = StringsTable()

        localized_string = LocalizedString('A key', 'キー', None)
        strings_table['A key'] = localized_string
        self.assertEqual(len(strings_table), 1)
        self.assertEqual(strings_table['A key'].source, 'A key')
        self.assertEqual(strings_table['A key'].localized, 'キー')
        self.assertIsNone(strings_table['A key'].comment)

        with self.assertRaises(KeyError):
            localized_string = LocalizedString('A key', 'キー', None)
            strings_table['keys'] = localized_string

    def test_del(self):
        strings_table = StringsTable()

        localized_string = LocalizedString('A key', 'キー', None)
        strings_table['A key'] = localized_string

        del strings_table['A key']
        self.assertEqual(len(strings_table), 0)

        with self.assertRaises(KeyError):
            del strings_table['A key']

    def test_insert(self):
        strings_table = StringsTable()

        localized_string = strings_table.insert('A string', '一個字串')
        self.assertEqual(len(strings_table), 1)
        self.assertEqual(strings_table['A string'], localized_string)
        self.assertEqual(strings_table['A string'].source, 'A string')
        self.assertEqual(strings_table['A string'].localized, '一個字串')
        self.assertIsNone(strings_table['A string'].comment)

        localized_string = strings_table.insert('A number', '수', 'a digits value')
        self.assertEqual(len(strings_table), 2)
        self.assertEqual(strings_table['A number'], localized_string)
        self.assertEqual(strings_table['A number'].source, 'A number')
        self.assertEqual(strings_table['A number'].localized, '수')
        self.assertEqual(strings_table['A number'].comment, 'a digits value')


class TestMergeStringsFile(unittest.TestCase, TestStringsTableContentMixin):

    def setUp(self):
        self.strings_table = StringsTable(os.path.join(source_root, 'example.strings'), encoding='utf-8')
        self.another_strings_table = StringsTable(os.path.join(source_root, 'example2.strings'), encoding='utf-8')

    def test_merge_default(self):
        self.strings_table.merge(self.another_strings_table)
        self.assertEqual(len(self.strings_table), 9)
        self._test_strings_table_content(self.strings_table, expected_results=self.default_expected_results + (
            ExpectedResult("a key", "一個鑰匙", "A key"),
        ))

    def test_merge_not_keep_comment(self):
        self.strings_table.merge(self.another_strings_table, keep_comment=False)
        self._test_strings_table_content(self.strings_table, expected_results=(
            ExpectedResult("%@ doesn't have a list named %@.", "%1$@ は %2$@ というリストをもっていません。", "Some comemnt"),
            ExpectedResult("Cannot get the version of this Tickle document.",
                           "Cannot get the version of this Tickle document.",
                           'Error message when Tickle tries to open a document but fails to fetch the version info,\n'
                           '   English source is "Cannot get the version of this Tickle document."'),
            ExpectedResult("No comment", "沒有註解", None),
            ExpectedResult("String with \"quote\".\"", "有引號的字\"", "Comment with \"QUOTE\""),
            ExpectedResult("String with =", "String with =", "String with ="),
            ExpectedResult("String with ;", "String with ;", "String with semicolon"),
            ExpectedResult(r"String\twith \n", r"String\twith \n", "String with spaces"),
            ExpectedResult("String not translated", "String not translated", "Not translated"),
            ExpectedResult("a key", "一個鑰匙", "A key"),
        ))

    def test_merge_not_keep_localized(self):
        self.strings_table.merge(self.another_strings_table, keep_localized=False)
        self._test_strings_table_content(self.strings_table, expected_results=(
            ExpectedResult("%@ doesn't have a list named %@.", "%1$@ は %2$@ というリストをもっていません。", "Some comemnt"),
            ExpectedResult("Cannot get the version of this Tickle document.",
                           "Cannot get the version of this Tickle document.",
                           'Error message when Tickle tries to open a document but fails to fetch the version info,\n'
                           '   English source is "Cannot get the version of this Tickle document."'),
            ExpectedResult("No comment", "kein Kommentar", None),
            ExpectedResult("String with \"quote\".\"", "有引號的字\"", "Comment with \"quote\""),
            ExpectedResult("String with =", "String with =", "String with ="),
            ExpectedResult("String with ;", "String with ;", "String with semicolon"),
            ExpectedResult(r"String\twith \n", r"String\twith \n", "String with spaces"),
            ExpectedResult("String not translated", "String not translated", "Not translated"),
            ExpectedResult("a key", "一個鑰匙", "A key"),
        ))

    def test_merge_exclude_extra(self):
        self.strings_table.merge(self.another_strings_table, exclude_extra=True)
        self._test_strings_table_content(self.strings_table, expected_results=(
            ExpectedResult("%@ doesn't have a list named %@.", "%1$@ は %2$@ というリストをもっていません。", "Some comemnt"),
            ExpectedResult("Cannot get the version of this Tickle document.",
                           "Cannot get the version of this Tickle document.",
                           'Error message when Tickle tries to open a document but fails to fetch the version info,\n'
                           '   English source is "Cannot get the version of this Tickle document."'),
            ExpectedResult("No comment", "沒有註解", None),
            ExpectedResult("String with \"quote\".\"", "有引號的字\"", "Comment with \"quote\""),
            ExpectedResult("String with =", "String with =", "String with ="),
            ExpectedResult(r"String\twith \n", r"String\twith \n", "String with spaces"),
            ExpectedResult("a key", "一個鑰匙", "A key"),
        ))

if __name__ == '__main__':
    unittest.main()
