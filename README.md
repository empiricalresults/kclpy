# kclpy

This is a fork of the [Amazon Kinesis Client Library for Python](https://github.com/awslabs/amazon-kinesis-client-python),
aiming to simplify consuming a kinesis stream using the [Amazon's Kinesis Client Library (KCL)](http://docs.aws.amazon.com/kinesis/latest/dev/developing-consumers-with-kcl.html) multi lang daemon interface.


## Why

It should be easy to consume a kinesis stream in python.  This library provides a python API to the KCL.

## Usage

Install it:

```sh
> pip install kclpy
```

Implement a RecordProcessor.  See http://docs.aws.amazon.com/kinesis/latest/dev/kinesis-record-processor-implementation-app-py.html for details on the RecordProcessor interface.

```python
import kclpy
import json

class MyStreamProcessor(kclpy.RecordProcessor):

    def process_record(self, data, partition_key, sequence_number):

        try:
            # assumes the incoming kinesis record is java
            data = json.loads(data)
            user = data.get("user")
            
            # explicitly return True to force a checkpoint (otherwise the default)
            # checkpointing strategy is used
            return True

        except ValueError:
            # not valid json
            log.error("Invalid json placed on queue, nothing we can do")
            return


def main():
    kclpy.start(MyStreamProcessor())

if __name__ == '__main__':
    main()
```

## Running

Running this directly wont do anything other than wait for records via STDIN.  The accompanying [Sylvite](https://github.com/empiricalresults/sylvite) library is an executable jar that will launch our record processor and feed it records.

See the [Sylvite](https://github.com/empiricalresults/sylvite) library for details and a pre-built jar.

```sh
> java -jar sylvite.jar --config=myapp.properties
```

## Logging

This library uses the standard python logging module (all logs under the namespace 'kclpy').  The KCL multi-daemon library expects well formed data on STDOUT, so be sure to configure your logging to use STDERR or a file.  Do not use print statements in your processor!


## Background

The key concept to understand when using the KCL's multi-lang daemon is that there is a Java process doing all communication with the kinesis API and a language agnostic child process that reads and writes from STDIN/STDOUT.  This is very similar to how Hadoop streaming works.  In order to consume the stream, we need to start up a Java process, which will in-turn start up a child process that will actually handle consuming the stream data.

While this sounds complicated, building on the KCL gives us the advantage of all the checkpointing, resharding and monitoring work that is baked into the KCL.  The KCL is also maintained by the awslabs team, so any future enhancements will be handled for free.


## RecordProcessor

kclpy is based on awslabs' sample code, with only a few minor tweaks in logging and checkpointing.

### API

Refer to [Amazon's documentation](http://docs.aws.amazon.com/kinesis/latest/dev/kinesis-record-processor-implementation-app-py.html), this fork maintains compatibility with the original implementation.


### Checkpointing

The KCL uses a DynamoDB table to maintain it's current position in the stream (checkpoint).  kclpy allows you to customize the checkpointing behaviour.  The following kwargs can be passed to kclpy.RecordProcessor:

* checkpoint_freq_seconds - Checkpoint at a fixed interval (in seconds).
* records_per_checkpoint - Checkpoint at a fixed number of records processed.

```python
def main():
    # automatically checkpoint every 60 seconds
    every_minute_processor = MyStreamProcessor(checkpoint_freq_seconds=60)
    
    # or checkpoint every 100 records
    every_hundred_records_processor = MyStreamProcessor(records_per_checkpoint=100)
    
    #todo: start the processor
```

Alternatively, you can force an explict checkpoint by returning True in your *process_record* call.  But be warned, doing this every record will result in a lot of writes to your DynamoDB table.

```python
import kclpy

def process_data(data):
    # if this is a special record, tell the library to checkpoint so we don't process
    # it again.
    return True

class MyStreamProcessor(kclpy.RecordProcessor):

    def process_record(self, data, partition_key, sequence_number):
        should_checkpoint = process_data(data)
        return should_checkpoint
        
def main():
    # checkpoints will only be made if process_record() returns True
    # probably not a great idea in the general case
    manual_checkpointer = MyStreamProcessor(
        checkpoint_freq_seconds=0, 
        records_per_checkpoint=0
    )        
    
    #todo: start the processor
```

