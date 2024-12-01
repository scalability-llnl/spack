# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VirtualWithVersions(AutotoolsPackage):
    """Uses version-test-pkg, as a build dependency"""

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"

    version("17.0.1", md5="0123456789abcdef0123456789abcdef")
    version("16.0.1", md5="0123456789abcdef0123456789abcdef")
    version("11.0.1", md5="0123456789abcdef0123456789abcdef")
    version("1.8.0", md5="0123456789abcdef0123456789abcdef")

    provides("java@17", when="@17.0:17.9")
    provides("java@16", when="@16.0:16.9")
    provides("java@11", when="@11.0:11.9")
    provides("java@10", when="@10.0:10.9")
    provides("java@9", when="@9.0:9.9")
    provides("java@8", when="@1.8.0:1.8.9")
