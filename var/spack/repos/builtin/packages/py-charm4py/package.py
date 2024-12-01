# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCharm4py(PythonPackage):
    """Charm4py (Charm++ for Python) is a distributed computing and parallel
    programming framework for Python, for the productive development of fast,
    parallel and scalable applications. It is built on top of Charm++, a C++
    adaptive runtime system that has seen extensive use in the scientific and
    high-performance computing (HPC) communities across many disciplines, and
    has been used to develop applications that run on a wide range of devices:
    from small multi-core devices up to the largest supercomputers."""

    homepage = "https://charmpy.readthedocs.io"
    pypi = "charm4py/charm4py-1.0.tar.gz"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("payerle")

    version("1.0", sha256="8ddb9f021b7379fde94b28c31f4ab6a60ced2c2a207a2d75ce57cb91b6be92bc")

    variant(
        "mpi",
        default=True,
        description="build Charm++ library with the MPI instead of TCP" " communication layer",
    )

    # Builds its own charm++, so no charmpp dependency
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")
    depends_on("py-cython@:2", type="build")
    depends_on("py-cffi@1.7:", type="build")
    depends_on("py-numpy@1.10.0:", type=("build", "run"))
    depends_on("py-greenlet", type=("build", "run"))

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("cuda")
    depends_on("mpi", when="+mpi")

    # setup.py builds its own charm++, but libcharm.so
    # ends up with a cuda dependency causing unresolved symbol errors
    # when setup.py tries to load it to get version.  We need to explicitly
    # link libcudart when building the charm++ library.
    # To do this, the following patch:
    # 1) hacks setup.py to apply a patch to the charm++ Makefile
    # causing the Makefile to include libcudart when building libcharm.so
    # 2) inserts the patchfile needed to do so.
    # This is convoluted, but best way I see since setup.py untars the
    # charm++ sources and we need to patch a file that is in the tarball.
    #
    # The patch to the Makefile adds SPACK_CHARM4PY_EXTRALIBS to the link
    # arguments.  This needs to be set in the environment to be effective.
    patch("py-charm4py.makefile.patch", when="@1.0")

    # This sets the SPACK_CHARM4PY_EXTRALIBS env var which the
    # py-charm4py.makefile.patch adds to the build/link command for
    # libcharm.so.
    def setup_build_environment(self, env):
        env.set("SPACK_CHARM4PY_EXTRALIBS", self.spec["cuda"].libs.ld_flags)

    def install_options(self, spec, prefix):
        args = []
        if "+mpi" in spec:
            args.append("--mpi")
        return args
