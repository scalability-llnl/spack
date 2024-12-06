# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


# Note: should probably be named 'mgridgen+mpi' (as per scotch, metis etc)
class Parmgridgen(Package):
    """MGRIDGEN is a serial library written entirely in ANSI C that implements
    (serial) algorithms for obtaining a sequence of successive coarse grids
    that are well-suited for geometric multigrid methods.
    ParMGridGen is the parallel version of MGridGen.
    """

    homepage = "https://github.com/mrklein/ParMGridGen"
    url = "http://www.stasyan.com/devel/distfiles/ParMGridGen-1.0.tar.gz"

    version("1.0", sha256="62cdb6e48cfc59124e5d5d360c2841e0fc2feecafe65bda110b74e942740b395")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Activate the compilation of parallel libraries")

    depends_on("mpi", when="+mpi")

    def install(self, spec, prefix):
        make_opts = [
            "make=make",
            "COPTIONS={0}".format(self.compiler.cc_pic_flag),
            "LDOPTIONS={0}".format(self.compiler.cc_pic_flag),
            "CC={0}".format(self.compiler.cc),
            "LD={0}".format(self.compiler.cc),
            "LIBDIR=-L../..",
            "LIBS=-L../.. -lmgrid -lm",
        ]

        if "+mpi" in spec:
            make_opts.extend(
                [
                    "PARCC={0}".format(spec["mpi"].mpicc),
                    "PARLD={0}".format(spec["mpi"].mpicc),
                    "PARLIBS=-L../.. -lparmgrid -lmgrid -lm",
                    "parallel",
                ]
            )
        else:
            make_opts.append("serial")

        make(*make_opts, parallel=False)

        mkdirp(prefix.include, prefix.lib, prefix.bin)

        install("mgridgen.h", prefix.include)
        install("libmgrid.a", prefix.lib)
        install("mgridgen", prefix.bin)

        if "+mpi" in spec:
            install("parmgridgen.h", prefix.include)
            install("libparmgrid.a", prefix.lib)
            install("parmgridgen", prefix.bin)
