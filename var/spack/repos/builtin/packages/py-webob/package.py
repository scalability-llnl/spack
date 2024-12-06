# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebob(PythonPackage):
    """WebOb provides objects for HTTP requests and responses."""

    homepage = "https://webob.org/"
    pypi = "WebOb/WebOb-1.8.7.tar.gz"

    license("MIT")

    version("1.8.7", sha256="b64ef5141be559cfade448f044fa45c2260351edcb6a8ef6b7e00c7dcef0c323")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
