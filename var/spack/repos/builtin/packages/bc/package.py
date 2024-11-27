# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bc(AutotoolsPackage, GNUMirrorPackage):
    """bc is an arbitrary precision numeric processing language. Syntax is
    similar to C, but differs in many substantial areas. It supports
    interactive execution of statements."""

    homepage = "https://www.gnu.org/software/bc"
    gnu_mirror_path = "bc/bc-1.07.tar.gz"

    license("GPL-3.0-or-later")

    version("1.07.1", sha256="62adfca89b0a1c0164c2cdca59ca210c1d44c3ffc46daf9931cf4942664cb02a")
    version("1.07", sha256="55cf1fc33a728d7c3d386cc7b0cb556eb5bacf8e0cb5a3fcca7f109fc61205ad")

    depends_on("c", type="build")  # generated

    depends_on("ed", type="build")
    depends_on("texinfo", type="build")

    parallel = False
