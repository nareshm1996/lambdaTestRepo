import boto3
region = 'us-west-1'
instances = ['i-12345cb6de4f78g9h', 'i-08ce9b2d7eccf6d26']
ec2 = boto3.client('ec2', region_name=region)

def available_regions(service):
    regions = []
    client = boto3.client(service)
    response = client.describe_regions()

    for item in response["Regions"]:
        regions.append(item["RegionName"])

    return regions

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))


# regions = available_regions("ec2")
# print(f"List of regions in EC2: {regions}")    

print("Hello da mapla")