import boto3
import logging
import json

# Create a client
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    
    instanceDict = {"started_instance":[],"stopped_instance":[]}
    
    def stop_tagged_instances():
        # List all instances with auto-stop as tags and status running
        auto_stop_instances = ec2_client.describe_instances(Filters=[
            {
                "Name":"tag:Action",
                "Values":["Auto-Stop"]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ])
        
        for reservation in auto_stop_instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                # Stop all instances one by one
                ec2_client.stop_instances(InstanceIds=[instance_id])
                instanceDict["stopped_instance"].append(instance_id)
        
    def start_tagged_instances():
    # List all instances with auto-start as tags and status stopped
        auto_start_instances = ec2_client.describe_instances(Filters=[
            {
                "Name":"tag:Action",
                "Values":["Auto-Start"]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ])
        
        for reservation in auto_start_instances['Reservations']:
           for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                 # Start all instances one by one
                ec2_client.start_instances(InstanceIds=[instance_id])
                instanceDict["started_instance"].append(instance_id)
        
    start_tagged_instances()
    stop_tagged_instances()
    
    return {
        "status":200,
        "body": json.dumps(instanceDict)
    }