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

from tight.providers.aws.clients import boto3_client

def test_no_boom():
    assert True, 'Client can be imported.'


def test_session():
    session = boto3_client.session()
    session_2 = boto3_client.session()
    assert session == session_2, 'The session returned from session() is always the same'
