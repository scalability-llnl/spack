# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Netgen(AutotoolsPackage):
    """NETGEN is an automatic 3d tetrahedral mesh generator. It accepts
    input from constructive solid geometry (CSG) or boundary
    representation (BRep) from STL file format. The connection to
    a geometry kernel allows the handling of IGES and STEP files.
    NETGEN contains modules for mesh optimization and hierarchical
    mesh refinement."""

    homepage = "https://ngsolve.org/"
    url = "https://sourceforge.net/projects/netgen-mesher/files/netgen-mesher/5.3/netgen-5.3.1.tar.gz"

    version("5.3.1", sha256="cb97f79d8f4d55c00506ab334867285cde10873c8a8dc783522b47d2bc128bf9")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="enable mpi support")
    variant("oce", default=False, description="enable oce geometry kernel")
    variant("gui", default=False, description="enable gui")
    variant("metis", default=False, description="use metis for partitioning")

    depends_on("zlib-api")
    depends_on("mpi", when="+mpi")
    depends_on("oce+X11", when="+oce")
    depends_on("metis", when="+metis")

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/netgen-mesher/files/netgen-mesher/{0}/netgen-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec
        args = []
        if "+mpi" in spec:
            args.extend(["CC={0}".format(spec["mpi"].mpicc), "CXX={0}".format(spec["mpi"].mpicxx)])
        else:
            args.append("--without-mpi")

        if "+oce" in spec:
            args.append("--with-occ={0}".format(spec["oce"].prefix))
        #  FIXME
        # due to a bug in netgen config, when --without-occ is specified
        #   or --with-occ=no, OCC flags is turned true, and build fails
        #   later; so do not specify anything like that
        # else:
        #    args.append("--without-occ")

        if "~gui" in spec:
            args.append("--disable-gui")
        else:
            args.append("--enable-gui")
        if "+metis" in spec:
            args.append("--with-metis=%s" % spec["metis"].prefix)
        else:
            args.append("--without-metis")

        return args
