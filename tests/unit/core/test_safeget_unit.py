# Copyright (c) 2016 Michael Orion McManus
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

import tight.core.safeget as safeget

def test_no_boom():
    assert True, 'Module can be imported.'

def test_safeget():
    some_dict = {
        'a_key': 'a value'
    }

    success = safeget.safeget(some_dict, 'a_key')
    assert success == 'a value', 'An existing key is retrieved.'
    failure = safeget.safeget(some_dict, 'a_non_existent_key')
    assert failure == None
