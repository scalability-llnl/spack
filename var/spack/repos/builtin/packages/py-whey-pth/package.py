# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWheyPth(PythonPackage):
    """Extension to whey to support .pth files."""

    homepage = "https://github.com/repo-helper/whey-pth"
    pypi = "whey-pth/whey-pth-0.0.5.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("0.0.5", sha256="cbfcc723bc587ecde44c6b0c83270673d38d88c3fc8f8268a49b21db1fd60747")

    depends_on("py-wheel@0.34.2:", type="build")
    depends_on("py-setuptools@40.6.0:60,62:", type="build")
    depends_on("py-dom-toml@0.4.0:", type=("build", "run"))
    depends_on("py-whey@0.0.15:", type=("build", "run"))
