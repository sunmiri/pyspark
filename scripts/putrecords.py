import json
import boto3
kinesis = boto3.client("kinesis")
response = kinesis.put_record(
    StreamName="pyspark-kinesis",
    Data=json.dumps({
        'message': 'fromlocal',
        'number': 134,
        }),
    PartitionKey="AdjustAsNeeded"
)
print(response)