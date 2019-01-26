import boto3
import sys
import botocore

if len(sys.argv) < 3:
  print('Usage: python s3.py <the bucket name> <the AWS Region to use>\n' +
    'Example: python s3.py my-test-bucket us-east-2')
  sys.exit()

bucket_name = sys.argv[1]
region = sys.argv[2]

s3 = boto3.client(
  's3',
  region_name = region
)

# Lists all of your available buckets in this AWS Region.
def list_my_buckets(s3):
  resp = s3.list_buckets()

  print('My buckets now are:\n')

  for bucket in resp['Buckets']:
    print(bucket['Name'])

  return

list_my_buckets(s3)

# Create a new bucket.
try:
  print("\nCreating a new bucket named '" + bucket_name + "'...\n")
  s3.create_bucket(Bucket = bucket_name,
    CreateBucketConfiguration = {
      'LocationConstraint': region
    }
  )
except botocore.exceptions.ClientError as e:
  if e.response['Error']['Code'] == 'BucketAlreadyExists':
    print("Cannot create the bucket. A bucket with the name '" +
      bucket_name + "' already exists. Exiting.")
  sys.exit()

list_my_buckets(s3)

# Delete the bucket you just created.
print("\nDeleting the bucket named '" + bucket_name + "'...\n")
s3.delete_bucket(Bucket = bucket_name)

list_my_buckets(s3)
