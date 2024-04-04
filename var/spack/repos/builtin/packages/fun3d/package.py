# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import AutotoolsPackage, depends_on, variant, version, which, filter_file, find, patch

from os import environ as env

class Fun3d(AutotoolsPackage):
    """NASA's FUN3D CFD Solver"""

    homepage = "https://fun3d.larc.nasa.gov/"
    url = "file:///aerolab/admin/software/dist/fun3d/fun3d_intg-14.0d03712b.tar.gz"

    version("14.0d03712b", sha256="d92cdb39994771389effe99f783fe72094481d6d114518593070017def27c4ac")

    patch("f3d.patch")

    variant(
        "ftune",
        default=True,
        description="Enable FTune (NASA-recommended compiler flags).",
    )
    #variant("yoga",     default=False, description="Enable yoga support")
    #variant("KSOPT",    default=False, description="Enable KSOPT support.")
    #variant("SNOPT",    default=False, description="Enable SNOPT support.")
    #variant("SPARSKIT", default=False, description="Enable SPARSKIT support.")
    variant("tecio",    default=False, description="Enable TecIO support.")
    variant("esp",      default=False, description="Enable ESP support.")
    variant("hefss",    default=False, description="Enable high energy physics.")

    # build tools
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # required dependencies
    depends_on("mpi")
    depends_on("metis", type=("build", "link"))
    depends_on("parmetis", type=("build", "link"))
    depends_on("ruby", type="run")

    # optional dependencies
    #depends_on("nanoflann", type="build", when="+yoga")
    #depends_on("sparskit", type="build", when="+SPARSKIT")
    #depends_on("ksopt", type=("build"), when="+KSOPT")
    #depends_on("snopt +static", type=("build", "link"), when="+SNOPT")
    #depends_on("tecio",     type="build", when="+tecio")
    #depends_on("tecio+mpi", type="build", when="+tecio+mpi") # Only if mpi becomes a variant

    # Right now mpi is requited, so always turn on mpi in tecio
    depends_on("tecio+mpi", type="build", when="+tecio")
    depends_on("esp",    when="+esp")
    depends_on("tetgen", when="+esp", type="run")

    force_autoreconf = True
    autoreconf_extra_args = ["-Im4"]

    def autoreconf(self, spec, prefix):
        which("bash")("bootstrap")

    def configure_args(self):
        spec = self.spec
        args = [
            f"--with-metis={spec['metis'].prefix}",
            f"--with-parmetis={spec['parmetis'].prefix}",
            f"--with-mpi={spec['mpi'].prefix}",
            "--with-mpif90=mpif90",
            "--with-mpicc=mpicc",
            "--with-mpicxx=mpicxx",
        ]
        args += self.enable_or_disable("ftune")

        if spec.satisfies("+yoga"):
            args.append("--enable-yoga")
            args.append("--enable-one-ring")
            args.append(f"--with-nanoflann={spec['nanoflann'].prefix}")

        if spec.satisfies("+KSOPT"):
            args.append(f"--with-KSOPT={spec['ksopt'].prefix}/lib")

        if spec.satisfies("+SNOPT"):
            args.append(f"--with-SNOPT={spec['snopt'].prefix}/lib")

        if spec.satisfies("+SPARSKIT"):
            args.append(f"--with-SPARSKIT={spec['sparskit'].prefix}/lib")

        if spec.satisfies("+esp"):
            args.append(f"--with-EGADS={env['ESP_ROOT']}")
            args.append(f"--with-OpenCASCADE={env['CASROOT']}")

        if spec.satisfies("+hefss"):
            args.append("--enable-hefss")

        return args

    def patch(self):
        """Find all occurrences of #!/bin/csh and replace them with
        #!/usr/bin/env csh."""
        for file in find("fun3d/utils", "*.rb", recursive=True):
            filter_file("File.exists", "File.file", file)
