# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.variant import DisjointSetsOfValues


class Spack(Package):
    """
    Spack is a multi-platform package manager that builds and installs multiple
    versions and configurations of software. It works on Linux, macOS, and many
    supercomputers. Spack is non-destructive: installing a new version of a
    package does not break existing installations, so many configurations of
    the same package can coexist.
    """

    homepage = "https://spack.io/"
    git = "https://github.com/spack/spack.git"
    url = "https://github.com/spack/spack/releases/download/v0.16.2/spack-0.16.2.tar.gz"
    maintainers("haampie")

    license("Apache-2.0 OR MIT")

    version("develop", branch="develop")
    version("0.21.1", sha256="9a66bc8b59d436d5c0bd7b052c36d2177b228665ece6c9a2c339c2acb3f9103e")
    version("0.21.0", sha256="98680e52591428dc194a021e673a79bdc7799f394c1217b3fc22c89465159a84")
    version("0.20.1", sha256="141be037b56e4b095840a95ac51c428c29dad078f7f88140ae6355b2a1b32dc3")
    version("0.20.0", sha256="a189b4e8173eefdf76617445125b329d912f730767048846c38c8a2637396a7d")
    version("0.19.2", sha256="4978b37da50f5690f4e1aa0cfe3975a89ccef85d96c68d417ea0716a8ce3aa98")
    version("0.19.1", sha256="c9666f0b22ccf3cbda2736104d5d4e3b9cad5b4b4f01874a501e97d2c9477452")
    version("0.19.0", sha256="b4225daf4f365a15caa58ef465d125b0d108ac5430b74d53ca4e807777943daf")
    version("0.18.1", sha256="d1491374ce280653ee0bc48cd80527d06860b886af8b0d4a7cf1d0a2309191b7")
    version("0.18.0", sha256="7b8d1e6bb49cd4f46f79a93fa577e00336dafeb5452712e36efeafd02711d38e")
    version("0.17.3", sha256="e9bf38917fa3b5231a65930aa657ef19fd380bebcc9ee44204167b1593f6fa06")
    version("0.17.2", sha256="3c3c0eccc5c0a1fa89223cbdfd48c71c5be8b4645f5fa4e921426062a9b32d51")
    version("0.17.1", sha256="96850f750c5a17675275aa059eabc2ae09b7a8c7b59c5762d571925b6897acfb")
    version("0.17.0", sha256="93df99256a892ceefb153d48e2080c01d18e58e27773da2c2a469063d67cb582")
    version("0.16.3", sha256="26636a2e2cc066184f12651ac6949f978fc041990dba73934960a4c9c1ea383d")
    version("0.16.2", sha256="ed3e5d479732b0ba82489435b4e0f9088571604e789f7ab9bc5ce89030793350")
    version("0.16.1", sha256="8d893036b24d9ee0feee41ac33dd66e4fc68d392918f346f8a7a36a69c567567")
    version("0.16.0", sha256="064b2532c70916c7684d4c7c973416ac32dd2ea15f5c392654c75258bfc8c6c2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("development_tools", default=False, description="Build development dependencies")
    variant(
        "fetchers",
        # TODO: make Spack support default=... with any_combination_of :(
        values=DisjointSetsOfValues(
            ("none",), ("curl", "git", "mercurial", "subversion", "s3")
        ).with_default("git"),
        description="Fetchers for sources and binaries. "
        "By default, urllib is used since Spack 0.17",
    )
    variant(
        "modules",
        # TODO: make Spack support default=... with any_combination_of :(
        values=DisjointSetsOfValues(("none",), ("environment-modules", "lmod")).with_default(
            "environment-modules,lmod"
        ),
        description="This variant makes Spack install the specified module system; "
        "notice that Spack can still generate module files even if modules=none is selected.",
    )

    # This should be read as "require at least curl", not "require curl".
    requires("fetchers=curl", when="@:0.16", msg="Curl is required for Spack < 0.17")

    # Python
    depends_on("python@2.6.0:2.7,3.5:", type="run")
    depends_on("python@2.7.0:2.7,3.5:", type="run", when="@0.18.0:")
    depends_on("python@2.7.0:2.7,3.6:", type="run", when="@0.19.0:")
    depends_on("python@3.6:", type="run", when="@0.20.0:")

    # Old Spack unfortunately depends on distutils, removed in Python 3.12
    depends_on("python@:3.12", type="run", when="@0.18:0.20.1")

    # spack python -i ipython support
    depends_on("py-ipython", type="run")

    # Concretizer
    depends_on("clingo-bootstrap@spack", type="run")

    # Archives
    depends_on("bzip2", type="run")
    depends_on("gzip", type="run")
    depends_on("tar", type="run")
    depends_on("unzip", type="run")
    depends_on("xz", type="run")
    depends_on("zstd +programs", type="run")

    # Build tools
    depends_on("bash", type="run")
    depends_on("file", type="run")
    depends_on("gmake", type="run")
    depends_on("patch", type="run")
    depends_on("ccache", type="run")

    # Fetchers
    depends_on("curl", type="run", when="fetchers=curl")
    depends_on("git", type="run", when="fetchers=git")
    depends_on("mercurial", type="run", when="fetchers=mercurial")
    depends_on("subversion", type="run", when="fetchers=subversion")
    depends_on("py-boto3", type="run", when="fetchers=s3")

    # Modules
    depends_on("environment-modules", type="run", when="modules=environment-modules")

    with when("modules=lmod"):
        depends_on("lmod", type="run")
        # Spack 0.18 uses lmod's depends_on function, which was introduced in v7.5.12
        depends_on("lmod@7.5.12:", type="run", when="@0.18:")

    # Buildcache
    # We really just need the 'strings' from binutils for older versions of spack
    depends_on("binutils", type="run", when="@:0.20")
    depends_on("gnupg", type="run")
    depends_on("patchelf", type="run", when="platform=linux")

    # See https://github.com/spack/spack/pull/24686
    # and #25595, #25726, #25853, #25923, #25924 upstream in python/cpython
    with when("@:0.16.2"):
        conflicts("^python@3.10:")
        conflicts("^python@3.9.6:3.9")
        conflicts("^python@3.8.11:3.8")
        conflicts("^python@3.7.11:3.7")
        conflicts("^python@3.6.14:3.6")

    # https://bugs.python.org/issue45235#msg406121
    # To be fixed in 3.9.9, no other releases are affected
    conflicts("^python@3.9.8", when="@:0.17.0")

    # Development tools
    with when("+development_tools"):
        depends_on("py-isort@4.3.5:", type="run")
        depends_on("py-mypy@0.900:", type="run")
        depends_on("py-black", type="run")
        depends_on("py-flake8", type="run")
        depends_on("py-sphinx@3.4:4.1.1,4.1.3:", type="run")
        depends_on("py-sphinxcontrib-programoutput", type="run")
        depends_on("py-sphinx-rtd-theme", type="run")
        depends_on("graphviz", type="run")

    def setup_run_environment(self, env):
        env.set("SPACK_PYTHON", self.spec["python"].command.path)

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, self.prefix)
