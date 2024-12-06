# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This file contains the definition of the GCS Blob storage Class used to
integrate GCS Blob storage with spack buildcache.
"""

import os
import sys
import urllib.parse
import urllib.response
from urllib.error import URLError
from urllib.request import BaseHandler

import llnl.util.tty as tty


def gcs_client():
    """Create a GCS client
    Creates an authenticated GCS client to access GCS buckets and blobs
    """

    try:
        import google.auth
        from google.cloud import storage
    except ImportError as ex:
        tty.error(
            "{0}, google-cloud-storage python module is missing.".format(ex)
            + " Please install to use the gs:// backend."
        )
        sys.exit(1)

    storage_credentials, storage_project = google.auth.default()
    storage_client = storage.Client(storage_project, storage_credentials)
    return storage_client


class GCSBucket:
    """GCS Bucket Object
    Create a wrapper object for a GCS Bucket. Provides methods to wrap spack
    related tasks, such as destroy.
    """

    def __init__(self, url, client=None):
        """Constructor for GCSBucket objects

        Args:
          url (str): The url pointing to the GCS bucket to build an object out of
          client (google.cloud.storage.client.Client): A pre-defined storage
                 client that will be used to access the GCS bucket.
        """
        if url.scheme != "gs":
            raise ValueError(
                "Can not create GCS bucket connection with scheme {SCHEME}".format(
                    SCHEME=url.scheme
                )
            )
        self.url = url
        self.name = self.url.netloc
        if self.url.path[0] == "/":
            self.prefix = self.url.path[1:]
        else:
            self.prefix = self.url.path

        self.client = client or gcs_client()

        self.bucket = None
        tty.debug("New GCS bucket:")
        tty.debug("    name: {0}".format(self.name))
        tty.debug("    prefix: {0}".format(self.prefix))

    def exists(self):
        from google.cloud.exceptions import NotFound

        if not self.bucket:
            try:
                self.bucket = self.client.bucket(self.name)
            except NotFound as ex:
                tty.error("{0}, Failed check for bucket existence".format(ex))
                sys.exit(1)
        return self.bucket is not None

    def create(self):
        if not self.bucket:
            self.bucket = self.client.create_bucket(self.name)

    def get_blob(self, blob_path):
        if self.exists():
            return self.bucket.get_blob(blob_path)
        return None

    def blob(self, blob_path):
        if self.exists():
            return self.bucket.blob(blob_path)
        return None

    def get_all_blobs(self, recursive=True, relative=True):
        """Get a list of all blobs
        Returns a list of all blobs within this bucket.

        Args:
            relative: If true (default), print blob paths
                         relative to 'build_cache' directory.
                      If false, print absolute blob paths (useful for
                         destruction of bucket)
        """
        tty.debug("Getting GCS blobs... Recurse {0} -- Rel: {1}".format(recursive, relative))

        converter = str
        if relative:
            converter = self._relative_blob_name

        if self.exists():
            all_blobs = self.bucket.list_blobs(prefix=self.prefix)
            blob_list = []

            base_dirs = len(self.prefix.split("/")) + 1

            for blob in all_blobs:
                if not recursive:
                    num_dirs = len(blob.name.split("/"))
                    if num_dirs <= base_dirs:
                        blob_list.append(converter(blob.name))
                else:
                    blob_list.append(converter(blob.name))

            return blob_list

    def _relative_blob_name(self, blob_name):
        return os.path.relpath(blob_name, self.prefix)

    def destroy(self, recursive=False, **kwargs):
        """Bucket destruction method

        Deletes all blobs within the bucket, and then deletes the bucket itself.

        Uses GCS Batch operations to bundle several delete operations together.
        """
        from google.cloud.exceptions import NotFound

        tty.debug("Bucket.destroy(recursive={0})".format(recursive))
        try:
            bucket_blobs = self.get_all_blobs(recursive=recursive, relative=False)
            batch_size = 1000

            num_blobs = len(bucket_blobs)
            for i in range(0, num_blobs, batch_size):
                with self.client.batch():
                    for j in range(i, min(i + batch_size, num_blobs)):
                        blob = self.blob(bucket_blobs[j])
                        blob.delete()
        except NotFound as ex:
            tty.error("{0}, Could not delete a blob in bucket {1}.".format(ex, self.name))
            sys.exit(1)


class GCSBlob:
    """GCS Blob object

    Wraps some blob methods for spack functionality
    """

    def __init__(self, url, client=None):
        self.url = url
        if url.scheme != "gs":
            raise ValueError(
                "Can not create GCS blob connection with scheme: {SCHEME}".format(
                    SCHEME=url.scheme
                )
            )

        self.client = client or gcs_client()

        self.bucket = GCSBucket(url)

        self.blob_path = self.url.path.lstrip("/")

        tty.debug("New GCSBlob")
        tty.debug("  blob_path = {0}".format(self.blob_path))

        if not self.bucket.exists():
            tty.warn("The bucket {0} does not exist, it will be created".format(self.bucket.name))
            self.bucket.create()

    def get(self):
        return self.bucket.get_blob(self.blob_path)

    def exists(self):
        from google.cloud.exceptions import NotFound

        try:
            blob = self.bucket.blob(self.blob_path)
            exists = blob.exists()
        except NotFound:
            return False

        return exists

    def delete_blob(self):
        from google.cloud.exceptions import NotFound

        try:
            blob = self.bucket.blob(self.blob_path)
            blob.delete()
        except NotFound as ex:
            tty.error("{0}, Could not delete gcs blob {1}".format(ex, self.blob_path))

    def upload_to_blob(self, local_file_path):
        blob = self.bucket.blob(self.blob_path)
        blob.upload_from_filename(local_file_path)

    def get_blob_byte_stream(self):
        return self.bucket.get_blob(self.blob_path).open(mode="rb")

    def get_blob_headers(self):
        blob = self.bucket.get_blob(self.blob_path)

        headers = {
            "Content-type": blob.content_type,
            "Content-encoding": blob.content_encoding,
            "Content-language": blob.content_language,
            "MD5Hash": blob.md5_hash,
        }

        return headers


def gcs_open(req, *args, **kwargs):
    """Open a reader stream to a blob object on GCS"""
    url = urllib.parse.urlparse(req.get_full_url())
    gcsblob = GCSBlob(url)

    if not gcsblob.exists():
        raise URLError("GCS blob {0} does not exist".format(gcsblob.blob_path))
    stream = gcsblob.get_blob_byte_stream()
    headers = gcsblob.get_blob_headers()

    return urllib.response.addinfourl(stream, headers, url)


class GCSHandler(BaseHandler):
    def gs_open(self, req):
        return gcs_open(req)
