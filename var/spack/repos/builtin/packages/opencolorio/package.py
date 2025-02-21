# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opencolorio(CMakePackage):
    """OpenColorIO (OCIO) is a complete color management solution geared towards motion
    picture production with an emphasis on visual effects and computer animation."""

    homepage = "https://opencolorio.readthedocs.io"
    git = "https://github.com/AcademySoftwareFoundation/OpenColorIO"
    url = (
        "https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v2.4.0.tar.gz"
    )
    license("Apache-2.0")

    version("2.4.0", sha256="0ff3966b9214da0941b2b1cbdab3975a00a51fc6f3417fa860f98f5358f2c282")

    # Core dependencies
    depends_on("cmake@3.14:", type="build")
    depends_on("expat@2.2.8:")
    depends_on("yaml-cpp@0.6.3:")
    depends_on("imath@3.0.5:")
    depends_on("pystring@1.1.3:")

    # Optional dependencies
    variant("lcms", default=False, description="Little CMS for ociobakelut")
    depends_on("lcms@2.2:", when="+lcms")

    variant("python", default=False, description="Build python bindings")
    extends("python", when="+python")
    depends_on("py-pybind11", when="+python", type=("build", "run"))

    def cmake_args(self):
        args = ["-DOCIO_BUILD_PYTHON={0}".format("ON" if "+python" in self.spec else "OFF")]
        return args
