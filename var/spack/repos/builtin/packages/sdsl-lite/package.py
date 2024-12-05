# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SdslLite(Package):
    """SDSL - Succinct Data Structure Library

    The Succinct Data Structure Library (SDSL) is a powerful and flexible
    C++11 library implementing succinct data structures."""

    homepage = "https://github.com/simongog/sdsl-lite"

    version(
        "2.1.1",
        sha256="2f192977b47406ae8992292c7e841ef23d4656bf72f6140540bed53af68e06ed",
        expand=False,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("tar", type="build")

    def url_for_version(self, version):
        line = "https://github.com/simongog/sdsl-lite/releases/download/v{0}/sdsl-lite-{0}.tar.gz.offline.install.gz"
        return line.format(version.dotted)

    def install(self, spec, prefix):
        # spack will fail to expand the archive on its own due to a link loop
        # expand it manually here and run the install helper

        tar = which("tar")
        tar("-xvf", self.stage.archive_file)

        with working_dir("sdsl-lite-{0}".format(spec.version.dotted)):
            if self.spec.satisfies("%fj"):
                filter_file("stdlib=libc", "stdlib=libstdc", "./CMakeLists.txt")
            helper = Executable("./install.sh")
            helper(prefix)
