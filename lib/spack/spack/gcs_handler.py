# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import six.moves.urllib.response as urllib_response

import spack.util.url as url_util
import spack.util.web as web_util


def gcs_open(req, *args, **kwargs):
    import spack.util.gcs as gcs_util


    url = url_util.parse(req.get_full_url())
    gcsblob = gcs_util.GCSBlob(url)

    if not gcsblob.gcs_blob_exists():
        raise web_util.SpackWebError('GCS blob {} does not exist'.format(
            gcsblob.blob_path))
    stream = gcsblob.get_blob_byte_stream()
    headers = gcsblob.get_blob_headers()

    return urllib_response.addinfourl(stream, headers, url)
