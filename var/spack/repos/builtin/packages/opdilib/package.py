# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opdilib(Package):
    """OpDiLib (Open Multiprocessing Differentiation Library) is a universal add-on for
    reverse mode operator overloading AD tools that enables the differentiation of
    OpenMP parallel code."""

    homepage = "https://github.com/SciCompKL/OpDiLib"
    url = "https://github.com/SciCompKL/OpDiLib/archive/refs/tags/v1.5.tar.gz"

    version("1.5.1", sha256="58bbd4c7105e519b553bd0cbcf1c9797e6e9ca5ea445e4cc55cd32f216300781")
    version("1.5", sha256="47b345954df5e7ee8147e7b29db2ec160ba02ccc93b3b88af0b34bb880170248")
    version("1.4", sha256="f1dd2575a8c3b2328df89b732dbeaa23657731d77e4bf7ee201c6571f20d13d5")
    version("1.3.2", sha256="5da4a99ab1332e5c3746cb6d55ee4cd96ce578b06987e2b10e33ae6413b7cf7a")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "include"))
        install_tree(join_path(self.stage.source_path, "include"), join_path(prefix, "include"))
        mkdirp(join_path(prefix, "syntax"))
        install_tree(join_path(self.stage.source_path, "syntax"), join_path(prefix, "syntax"))
