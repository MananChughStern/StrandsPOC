import boto3

# Test AWS credentials
try:
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    print("AWS credentials configured correctly")
    print(f"Region: {bedrock.meta.region_name}")
except Exception as e:
    print(f"AWS setup issue: {e}")