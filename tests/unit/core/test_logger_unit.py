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

import tight.core.logger as logger

def test_no_boom():
    assert True, 'Module can be imported.'

def test_logger_info():
    test_message = 'test message'
    def info_spy(message):
        assert message == 'test message', 'The message is logged'
    original_info = getattr(logger.logger, 'info')
    setattr(logger.logger, 'info', info_spy)
    logger.info(message=test_message)
    setattr(logger.logger, 'info', original_info)
