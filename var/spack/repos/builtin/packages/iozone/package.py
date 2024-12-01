# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Iozone(MakefilePackage):
    """IOzone is a filesystem benchmark tool. The benchmark generates and
    measures a variety of file operations. Iozone has been ported to many
    machines and runs under many operating systems."""

    homepage = "https://www.iozone.org/"
    url = "https://www.iozone.org/src/current/iozone3_465.tar"

    license("custom")

    version("3_506", sha256="114ce5c071873b9a2c7ba6e73d05d5ef7e66564392acbfcdc0b3261db10fcbe7")
    version("3_491", sha256="2cc4842d382e46a585d1df9ae1e255695480dcc0fc05c3b1cb32ef3493d0ec9a")
    version("3_465", sha256="2e3d72916e7d7340a7c505fc0c3d28553fcc5ff2daf41d811368e55bd4e6a293")

    depends_on("c", type="build")  # generated

    # TODO: Add support for other architectures as necessary
    build_targets = ["linux-AMD64"]

    build_directory = "src/current"

    def edit(self, spec, prefix):
        for dirpath, dirnames, filenames in os.walk(self.stage.source_path):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                os.chmod(path, 0o644)

        with working_dir(self.build_directory):
            filter_file(r"^CC\t= cc", r"CC\t= {0}".format(spack_cc), "makefile")

    def install(self, spec, prefix):
        install_tree("docs", join_path(prefix, "docs"))

        with working_dir(self.build_directory):
            install_tree(".", prefix.bin)
