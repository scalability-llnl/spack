# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UrlOnlyOverrideWithGaps(Package):
    homepage = "http://www.example.com"

    version("1.0.5", md5="abcdef0123456789abcdef0123456789")
    version(
        "1.0.0",
        md5="bcdef0123456789abcdef0123456789a",
        url="http://a.example.com/url_override-1.0.0.tar.gz",
    )
    version("0.9.5", md5="cdef0123456789abcdef0123456789ab")
    version(
        "0.9.0",
        md5="def0123456789abcdef0123456789abc",
        url="http://b.example.com/url_override-0.9.0.tar.gz",
    )
    version("0.8.5", md5="ef0123456789abcdef0123456789abcd")
    version(
        "0.8.1",
        md5="f0123456789abcdef0123456789abcde",
        url="http://c.example.com/url_override-0.8.1.tar.gz",
    )
    version("0.7.0", md5="0123456789abcdef0123456789abcdef")
