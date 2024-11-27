# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hmmer(Package):
    """HMMER is used for searching sequence databases for sequence homologs,
    and for making sequence alignments. It implements methods using
    probabilistic models called profile hidden Markov models (profile HMMs).
    """

    homepage = "http://www.hmmer.org"
    url = "http://eddylab.org/software/hmmer/hmmer-3.3.tar.gz"

    version("3.4", sha256="ca70d94fd0cf271bd7063423aabb116d42de533117343a9b27a65c17ff06fbf3")
    version("3.3.2", sha256="92fee9b5efe37a5276352d3502775e7c46e9f7a0ee45a331eacb2a0cac713c69")
    version("3.3", sha256="0186bf40af67032666014971ed8ddc3cf2834bebc2be5b3bc0304a93e763736c")
    version("3.2.1", sha256="a56129f9d786ec25265774519fc4e736bbc16e4076946dcbd7f2c16efc8e2b9c")
    version("3.1b2", sha256="dd16edf4385c1df072c9e2f58c16ee1872d855a018a2ee6894205277017b5536")
    version("3.0", sha256="6977e6473fcb554b1d5a86dc9edffffa53918c1bd88d7fd20d7499f1ba719e83")
    version("2.4i", sha256="73cb85c2197017fa7a25482556ed250bdeed256974b99b0c25e02854e710a886")
    version("2.3.2", sha256="d20e1779fcdff34ab4e986ea74a6c4ac5c5f01da2993b14e92c94d2f076828b4")
    version("2.3.1", sha256="3956d53af8de5bb99eec18cba0628e86924c6543639d290293b6677a9224ea3f")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Compile with MPI")
    variant("gsl", default=False, description="Compile with GSL")

    depends_on("mpi", when="+mpi")
    depends_on("gsl", when="+gsl")

    # https://github.com/EddyRivasLab/hmmer/issues/283
    conflicts(
        "target=aarch64:", when="@:3.3", msg="hmmer is only available for x86_64 and PowerPC"
    )

    def install(self, spec, prefix):
        configure_args = ["--prefix={0}".format(prefix)]

        if self.spec.satisfies("+gsl"):
            configure_args.extend(["--with-gsl", "LIBS=-lgsl -lgslcblas"])

        if self.spec.satisfies("+mpi"):
            configure_args.append("--enable-mpi")

        configure(*configure_args)
        make()

        if self.run_tests:
            make("check")

        make("install")
