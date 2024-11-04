# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cgm(AutotoolsPackage):
    """The Common Geometry Module, Argonne (CGMA) is a code library
    which provides geometry functionality used for mesh generation and
    other applications."""

    homepage = "https://sigma.mcs.anl.gov/cgm-library"
    url = "https://ftp.mcs.anl.gov/pub/fathom/cgm-16.0.tar.gz"

    version("16.0", sha256="b98afe70c64efa19decc5ff01602e8c7afc6b22ce646cad30dc92ecfdce6e23d")
    version("13.1.1", sha256="ffde54f0c86055b06cad911bbd4297b88c3fb124c873b03ebee626f807b8ab87")
    version("13.1.0", sha256="c81bead4b919bd0cea9dbc61b219e316718d940bd3dc70825c58efbf0a0acdc3")
    version("13.1", sha256="985aa6c5db4257999af6f2bdfcb24f2bce74191cdcd98e937700db7fd9f6b549")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="enable mpi support")
    variant("oce", default=False, description="enable oce geometry kernel")
    variant("debug", default=False, description="enable debug symbols")
    variant("shared", default=False, description="enable shared builds")

    depends_on("mpi", when="+mpi")
    depends_on("oce+X11", when="+oce")

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("+mpi"):
            args.extend(
                [
                    "--with-mpi",
                    "CC={0}".format(spec["mpi"].mpicc),
                    "CXX={0}".format(spec["mpi"].mpicxx),
                ]
            )
        else:
            args.append("--without-mpi")

        if spec.satisfies("+oce"):
            args.append("--with-occ={0}".format(spec["oce"].prefix))
        else:
            args.append("--without-occ")

        if spec.satisfies("+debug"):
            args.append("--enable-debug")

        if spec.satisfies("+shared"):
            args.append("--enable-shared")

        return args
