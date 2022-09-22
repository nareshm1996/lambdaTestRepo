import boto3
import os 

def available_regions():
    client = boto3.client("ec2")
    regions = []
    
    response = client.describe_regions()

    for item in response["Regions"]:
        regions.append(item["RegionName"])

    return regions

def getInstanceFromTags(tags):
    instanceName="NA"
    for tag in tags:
        if tag['Key'] == 'Name':
            instanceName=tag['Value']
        else:
            continue
    return instanceName       

def shutdownInstances(instanceId,instanceState):
    shutdownAction="Unknown"
    ignoreList=['shutting-down','terminated','stopping','stopped']
    if instanceState not in ignoreList:
        ec2 = boto3.resource('ec2')
        ec2.Instance(instanceId).stop()
        shutdownAction="Completed"    
    else:
        shutdownAction="Not Required"
    return shutdownAction       

def main():
    regionName=os.environ['AWS_REGION']
    try:
        client = boto3.client("ec2",region_name=regionName)
        describe_instances_response = client.describe_instances()
        instanceDetails=describe_instances_response['Reservations']
        print(f"Region Name: {regionName}")
        
        Tags=[]
        lenInstanceDetails = int(len(instanceDetails))
        print("Length of instance:",lenInstanceDetails)
        if lenInstanceDetails == 0:
            print("No EC2 instances are currently available in this account.")
            print("------------------------------------------------")
        else:
            for instanceDetail in instanceDetails:
                for instance in instanceDetail['Instances']:
                    print("------------------------------------------------")
                    instanceId=instance['InstanceId']
                    print("Instance ID:",instanceId)            
                    Tags=instance['Tags']
                    instanceName=getInstanceFromTags(Tags)
                    print("Instance Name:",instanceName)
                    instanceState=instance['State']['Name']
                    print("Instance State:",instanceState)
                    print("Region:",regionName)
                    print("Tags:",Tags)
                    print("Shutdown Action:",shutdownInstances(instanceId,instanceState)) 
            print("------------------------------------------------")                
    except Exception as e:
        print("Exception:",e)            

def lambda_handler(event, context):    
    main() 