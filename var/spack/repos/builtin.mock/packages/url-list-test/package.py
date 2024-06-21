# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import spack.paths
from spack.package import *


class UrlListTest(Package):
    """Mock package with url_list."""

    homepage = "http://www.url-list-example.com"

    drive_escape = "/" if sys.platform == "win32" else ""
    web_data_path = join_path(spack.paths.test_path, "data", "web")
    url = "file://" + drive_escape + web_data_path + "/foo-0.0.0.tar.gz"
    list_url = "file://" + drive_escape + web_data_path + "/index.html"
    list_depth = 3

    version("0.0.0", md5="00000000000000000000000000000000")
    version("1.0.0", md5="00000000000000000000000000000100")
    version("3.0", md5="00000000000000000000000000000030")
    version("4.5", md5="00000000000000000000000000000450")
    version("2.0.0b2", md5="000000000000000000000000000200b2")
    version("3.0a1", md5="000000000000000000000000000030a1")
    version("4.5-rc5", md5="000000000000000000000000000045c5")
