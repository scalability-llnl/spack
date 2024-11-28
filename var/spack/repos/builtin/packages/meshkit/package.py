# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Meshkit(AutotoolsPackage):
    """MeshKit is an open-source library of mesh generation functionality.
    Its design philosophy is two-fold: it provides a collection of
    meshing algorithms for use in real meshing problems, along with
    other tools commonly needed to support mesh generation"""

    homepage = "https://sigma.mcs.anl.gov/meshkit-library"
    url = "https://ftp.mcs.anl.gov/pub/fathom/meshkit-1.5.0.tar.gz"

    version("1.5.0", sha256="6a4c119af191e24ef40644acb7cfbe967af0678ac3412f38a943fb28d661cac7")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="enable mpi support")
    variant("netgen", default=False, description="enable netgen support")
    variant("debug", default=False, description="enable debug symbols")
    variant("shared", default=False, description="enable shared builds")

    depends_on("mpi", when="+mpi")
    depends_on("netgen", when="+netgen")
    depends_on("cgm")
    depends_on("moab+cgm+irel+fbigeom")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-igeom={0}".format(spec["cgm"].prefix),
            "--with-imesh={0}".format(spec["moab"].prefix),
        ]
        if "+mpi" in spec:
            args.extend(
                [
                    "--with-mpi",
                    "CC={0}".format(spec["mpi"].mpicc),
                    "CXX={0}".format(spec["mpi"].mpicxx),
                    "FC={0}".format(spec["mpi"].mpifc),
                ]
            )
        #       FIXME without-mpi is not working
        #       else:
        #           args.append("--without-mpi")
        if "+netgen" in spec:
            args.append("--with-netgen={0}".format(spec["netgen"].prefix))
        else:
            args.append("--without-netgen")

        if "+debug" in spec:
            args.append("--enable-debug")
        else:
            args.append("--disable-debug")

        if "+shared" in spec:
            args.append("--enable-shared")
        else:
            args.append("--disable-shared")

        return args
