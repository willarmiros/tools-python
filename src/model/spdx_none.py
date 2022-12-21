# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class SpdxNone:
    """
    Represents the SPDX NONE value.
    """

    _string_value = "NONE"

    def __str__(self):
        return self._string_value

    def __repr__(self):
        return self._string_value

    def __eq__(self, other):
        return isinstance(other, SpdxNone)