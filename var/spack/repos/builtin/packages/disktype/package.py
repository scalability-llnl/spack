# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Disktype(MakefilePackage):
    """A fork of the disktype disk and disk image format detection tool."""

    homepage = "https://github.com/kamwoods/disktype"
    url = "https://github.com/kamwoods/disktype/archive/9.2.1.tar.gz"

    license("MIT")

    version("9.2.1", sha256="fb274d6ce6b69c0d36eb23fcc9f01db3c32c3996b404900d46bb743ce4fa8154")

    depends_on("c", type="build")  # generated

    build_directory = "src"

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir(self.build_directory):
            install("disktype", prefix.bin)
