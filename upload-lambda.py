import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:185831608739:deployLambdaTopic')

    location = {
        "bucketName": "lambdabuild.pellikka.net",
        "objectKey": "lambdabuild.zip"
    }
    try:
        job = event.get('CodePipeline.job')
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building project from " + str(location)

        s3 = boto3.resource('s3')

        lambda_bucket = s3.Bucket('lambda.pellikka.net')
        build_bucket = s3.Bucket(location['bucketName'])

        lambda_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location['objectKey'], lambda_zip)

        with zipfile.ZipFile(lambda_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                lambda_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={ 'ContentType': mimetypes.guess_type(nm)[0] })
                lambda_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Deployed", Message="Deployed successfully!")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])

    except:
        topic.publish(Subject="Deploy failed", Message="Deployment failed!")
        raise

    return 'Hello from Lambda'
