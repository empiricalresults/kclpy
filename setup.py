"""
Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""

from distutils.core import setup

PACKAGE_NAME = 'kclpy'
PACKAGE_VERSION = '0.1.0'

if __name__ == '__main__':
    setup(
        name=PACKAGE_NAME,
        version=PACKAGE_VERSION,
        description='A python interface for the Amazon Kinesis Client Library MultiLangDaemon',
        license='Amazon Software License',
        packages=[PACKAGE_NAME],
        url='https://github.com/empiricalresults/kclpy',
        download_url='https://github.com/empiricalresults/kclpy/tarball/0.1.0',
        keywords=['amazon', 'kinesis', 'kinesis-client-library', 'client-library', 'library'],
        )
