# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEwahBoolUtils(PythonPackage):
    """EWAH Bool Array utils for yt"""

    homepage = "https://github.com/yt-project/ewah_bool_utils"
    pypi = "ewah_bool_utils/ewah_bool_utils-1.2.2.tar.gz"

    license("BSD-3-Clause", checked_by="lgarrison")

    version("1.2.2", sha256="eb901f46caef189de3a0c1f5ca06287cfaba7976ddf76fa1c1f3bce1b60b7ac3")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-setuptools@61.2:", type="build")
    depends_on("py-cython@3.0:", type="build")
    depends_on("py-numpy@2.0.0:", type="build")

    depends_on("py-numpy@1.19.3:2", type=("build", "run"))
