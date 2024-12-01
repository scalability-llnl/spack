# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEg(PythonPackage):
    """eg provides examples of common uses of command line tools."""

    homepage = "https://github.com/srsudar/eg"
    url = "https://github.com/srsudar/eg/archive/v1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="dfeff9f8c16afec1b621c9484c8cdb670dbc69ab40590d16a9becb740ea289f3")
    version("1.1.1", sha256="99020af6ff24742b3eb93a15a289f36156fdb93abdbec50b614b982b1ba9c399")
    version("1.1.0", sha256="41316c79e8f7a999e82057ac54c6d57c58a50cd37dc91e172b634998f61b1b86")
    version("1.0.2", sha256="f9fa9ed4a9bcfaf594d9b4acc758def5ca5b464e3263a6f0eb2270d818aef3cc")
    version("1.0.1", sha256="b52aa86a2b2d018c17bb99637c07e9f42f53fdf8890ef2beaaa774a425350ac4")
    version("1.0.0", sha256="e811b1006002fa80bcac66f5c86cd412f9816969d087296cfd360752d31a85fd")

    depends_on("py-setuptools", type="build")
