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

from kcl import RecordProcessor, RecordProcessorBase, JSONRecordProcessor, KCLProcess

def start(record_processor):
    """
    Start the processor.  This is a blocking call and will use stdin/stdout to communicate
    with the KCL Multi Lang Daemon.

    Use KCLProcess explicitly if you want more control on how this is run.
    """
    KCLProcess(record_processor=record_processor).run()
