# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class MesaGlu(AutotoolsPackage):
    """This package provides the Mesa OpenGL Utility library."""

    homepage = "https://www.mesa3d.org"
    url = "https://www.mesa3d.org/archive/glu/glu-9.0.0.tar.gz"

    version("9.0.2", sha256="24effdfb952453cc00e275e1c82ca9787506aba0282145fff054498e60e19a65")
    version("9.0.1", sha256="f6f484cfcd51e489afe88031afdea1e173aa652697e4c19ddbcb8260579a10f7")
    version("9.0.0", sha256="4387476a1933f36fec1531178ea204057bbeb04cc2d8396c9ea32720a1f7e264")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gl@3:")
    provides("glu@1.3")

    # When using -std=c++17, using register long will throw an error. This
    # patch switches all instances of register long to long to fix this.
    patch("register-long.patch")

    def configure_args(self):
        args = ["--disable-libglvnd"]

        if self.spec.satisfies("^[virtuals=gl] osmesa"):
            args.append("--enable-osmesa")
        else:
            args.append("--disable-osmesa")

        return args

    @property
    def libs(self):
        return find_libraries("libGLU", self.prefix, recursive=True)
