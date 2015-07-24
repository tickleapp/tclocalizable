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


class LocalizedString(object):

    def __init__(self, source, localized, comment=None):
        self.source = source
        self.localized = localized
        self.comment = comment

    def __str__(self):
        return repr(self)

    def __repr__(self):
        escaped_source = self.source.replace('"', r'\"')
        escaped_localized = self.localized.replace('"', r'\"')
        result = '"{escaped_source}" = "{escaped_localized}";'.format(**locals())

        if self.comment:
            result = '/* {} */\n{}'.format(self.comment, result)

        return result

    def __eq__(self, other):
        if not isinstance(other, LocalizedString):
            return False
        else:
            return self.source == other.source and self.localized == other.localized and self.comment == other.comment
