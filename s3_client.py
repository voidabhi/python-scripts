
"""
The server application uses AWS S3 in various places.
This utility provides a common place for interacting
with S3 and handles the authentication in a unified manner.
"""

import os.path
import logging
import boto3
from settings import S3_ACCESS_KEY, S3_SECRET_KEY


class S3Client():

    def __init__(self, aws_access_key=S3_ACCESS_KEY, aws_secret_key=S3_SECRET_KEY):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.client = self._client()

    def list_folder_contents(self, bucket_name, folder_name=None, exclude_self=True):
        """
        List the contents (keys) of the objects in the folder.
        :param bucket_name: (str) name of the bucket to list
        :param folder_name: (str) name of the folder to list the contents of. If omitted or None, will list all folders
        :param exclude_self: (boolean) under some odd circumstances, the folder itself might get listed. Normally the method will remove that. This flag, set to false, will not try to eliminate it. Default is True
        :returns: list of key names in folder
        """

        if folder_name:
            folder_name = os.path.join(folder_name, '') # ensure it ends in a slash
        else:
            folder_name = '' # non-prefixed -- all folders

        objects = []
        incomplete = True
        continuation_token = None

        while incomplete:
            if continuation_token:
                response = self.client.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=folder_name,
                    ContinuationToken=continuation_token,
                )
            else:
                response = self.client.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=folder_name,
                )

            objects += response.get('Contents', [])
            if response.get('isTruncated', False):
                continuation_token = response['NextContinuationToken']
            else:
                incomplete = False

        if exclude_self:
            contents = [obj['Key'] for obj in objects if obj['Key'] != folder_name]
        else:
            contents = [obj['Key'] for obj in objects]

        return contents

    def move_object(self, source_bucket_name=None, source_name=None, target_name=None, target_bucket_name=None):
        """
        Moving an object on S3 requires two steps:
        1) copy to destination
        2) delete from source
        :param source_bucket_name: (str) name of bucket to copy from
        :param source_name: (str) object key to copy from
        :param target_name: (str) object key to copy to
        :param target_bucket_name: (str) name of bucket to copy to. If None, use the source_bucket_name
        :return None:
        """

        if target_bucket_name is None:
            target_bucket_name = source_bucket_name

        response = self.client.copy_object(
            Bucket=target_bucket_name,
            Key=target_name,
            CopySource={
                'Bucket': source_bucket_name,
                'Key': source_name
            }
        )

        if response.get('CopyObjectResult', False):
            # Assume it worked
            response = self.client.delete_object(
                Bucket=source_bucket_name,
                Key=source_name
            )


    def upload_file(self, source_name, target_name, bucket_name):
        """
        Uploads the source to the target in the bucket
        :params source_name: (str) name of file to upload
        :params target_name: (str) name of object on S3 (include any folder or path)
        :params bucket_name: (str) bucket to receive file
        :returns: None
        """
        self.client.upload_file(
            source_name,
            bucket_name,
            target_name
        )

    def download_file(self, source_name, target_name, bucket_name):
        """
        Downloads the source object from the bucket into the target file. Note that the target_name paths should already exist.
        :params source_name: (str) object key to download
        :params target_name: (str) destination for download -- all paths to the base file must already exist
        :params bucket_name: (str) name of bucket to download from
        :returns: None
        """
        self.client.download_file(
            bucket_name,
            source_name,
            target_name
        )

    def _client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key)
