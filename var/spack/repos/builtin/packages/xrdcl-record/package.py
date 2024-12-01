# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XrdclRecord(CMakePackage):
    """XrdClRecorder Plugin. This XRootD Client Plugin can be used to record
    all user's actions on XrdCl::File object and store them into a csv file."""

    homepage = "https://github.com/xrootd/xrdcl-record"
    url = "https://github.com/xrootd/xrdcl-record/archive/refs/tags/v5.4.2.tar.gz"

    license("BSD-3-Clause")

    version("5.4.2", sha256="fb76284491ff4e723bce4c9e9d87347e98e278e70c597167bc39a162bc876734")

    depends_on("cxx", type="build")  # generated

    depends_on("xrootd")
