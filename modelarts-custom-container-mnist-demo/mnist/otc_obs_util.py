# https://www.thepythoncode.com/code/encrypt-decrypt-files-symmetric-python
import glob
import tempfile
from shutil import copyfile
import os
import boto3

s3prefix = ""
def download_files_from_s3(Bucket, Prefix=s3prefix, input_dir=None, output_dir=None):
    """
    download files from S3 bucket / directory
    :param Bucket:
    :param Prefix:
    :param input_dir:
    :param output_dir:
    :return:
    """
    print(" download_files_form_s3:", Bucket, s3prefix, input_dir, output_dir)

    s3client = get_client()
    if not input_dir or not output_dir:
        raise Exception("Missing input or output directory !")

    results = s3client.list_objects_v2(Bucket=Bucket, Prefix=Prefix + input_dir)["Contents"]
    for result in results:
        print("download result key:", result["Key"], Prefix)
        filepart = "/".join(result["Key"].split("/")[-2:])
        if len(filepart) == 0:
            continue

        filedir = result["Key"].split("/")[-2]
        filedir = os.path.join(output_dir, filedir)
        print("filedir !!!!!", filedir)

        if not os.path.exists(filedir):
            os.makedirs(filedir)
        # filepart = result["Key"].split(Prefix + input_dir)[1]
        # if len(filepart)==0:
        #    continue
        full_output_filename = os.path.join(output_dir, filepart)
        print("download_files_form_s3 full_output_filename RESULT KEY:", result["Key"], "out:", full_output_filename)
        s3client.download_file(Bucket, result["Key"], full_output_filename)
        # if need to delete the file s3client.delete_object(myBucket,result["Key"])


def upload_files_to_s3(Bucket, Prefix=s3prefix, input_dir=None, output_dir=None):
    """
    upload files to S3 bucket output_dir is a source dir in this case
    :param Bucket:
    :param Prefix:
    :param input_dir:
    :param output_dir:
    :return:
    """
    s3client = get_client()
    if not output_dir and not input_dir:
        raise Exception("Please specify the input and output directory!")

    onlyfiles = [input_dir]
    if os.path.isdir(input_dir):
        onlyfiles = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    print("upload localfiles:", onlyfiles)

    for result in onlyfiles:
        localfilename = input_dir + '/' + result
        targetfilename = Prefix + output_dir + result
        print("local filename:", localfilename)
        print("upload target filename:", targetfilename)
        s3client.upload_file(localfilename, Bucket, targetfilename)
        # if need to delete the file s3client.delete_object(myBucket,result["Key"])


def get_client():
    """
    create S3 client object
    :return: client object
    """
    region = 'eu-de'
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID",None)
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY",None)
    endpoint = os.environ.get("S3_ENDPOINT",None)


    s3client = boto3.client('s3',
                            region_name=region,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                               endpoint_url="https://" + endpoint,
                               #verify=False
    )
    return s3client

if __name__ == "__main__":
   download_files_from_s3(Bucket="customcontainer",
                               input_dir='mnist/mnist_data/mnist.pkl.gz',
                               # FERI COULD USE DIRECTORY ALSO input_dir='mnist/mnist_data/',
                               output_dir="/tmp"
                               )
   upload_files_to_s3(Bucket="customcontainer",
                               input_dir="feridockerfile", # this is directory
                               output_dir="tmpinobs/"
                     )

