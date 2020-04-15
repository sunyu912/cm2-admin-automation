# Note: please do not copy this file to the course repos!!

import boto3

session = boto3.Session(
    aws_access_key_id='AKIAZADLXOUBVZJ7CFPK',
    aws_secret_access_key='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'
)

# Let's use Amazon S3
s3 = session.resource('s3')

config_file_name_path = "course_host_config.json"

# Upload
s3.Bucket('cm2-config').upload_file(config_file_name_path, config_file_name_path, ExtraArgs={'ACL':'public-read', 'ContentType': "application/json"})
