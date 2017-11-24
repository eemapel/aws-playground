import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:185831608739:deployLambdaTopic')

    try:
        s3 = boto3.resource('s3')

        lambda_bucket = s3.Bucket('lambda.pellikka.net')
        build_bucket = s3.Bucket('lambdabuild.pellikka.net')

        lambda_zip = StringIO.StringIO()
        build_bucket.download_fileobj('lambdabuild.zip', lambda_zip)

        with zipfile.ZipFile(lambda_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                lambda_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={ 'ContentType': mimetypes.guess_type(nm)[0] })
                lambda_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Deployed", Message="Deployed successfully!")

    except:
        topic.publish(Subject="Deploy failed", Message="Deployment failed!")
        raise

    return 'Hello from Lambda'
