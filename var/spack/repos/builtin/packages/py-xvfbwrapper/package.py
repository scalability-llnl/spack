# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXvfbwrapper(PythonPackage):
    """run headless display inside X virtual framebuffer (Xvfb)"""

    pypi = "xvfbwrapper/xvfbwrapper-0.2.9.tar.gz"

    license("MIT")

    version("0.2.9", sha256="bcf4ae571941b40254faf7a73432dfc119ad21ce688f1fdec533067037ecfc24")

    depends_on("py-setuptools", type="build")
    # Eventually add xvfb!
