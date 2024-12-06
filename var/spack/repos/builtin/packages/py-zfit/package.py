# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyZfit(PythonPackage):
    """
    scalable pythonic model fitting for high energy physics
    """

    homepage = "https://github.com/zfit/zfit"
    pypi = "zfit/zfit-0.18.0.tar.gz"

    maintainers("jonas-eschle")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    tags = ["likelihood", "statistics", "inference", "fitting", "hep"]

    version("0.18.2", sha256="099b111e135937966b4c6342c7738731f112aea33e1b9f4a9785d2eac9e530f1")
    version("0.18.1", sha256="fbc6b3a636d8dc74fb2e69dfec5855f534c4583ec18efac9e9107ad45b18eb43")
    version("0.18.0", sha256="21d9479480f74945c67707b715780693bd4e94062c551bf41fe04a2eddb47fab")
    version("0.17.0", sha256="cd60dfc360c82666af4e8dddd78edb0ab95a095b9dd0868457f0981dc03afa5a")
    version("0.16.0", sha256="b3b170af23b61d7e265d6fb1bab1d052003f3fb41b3c537527cc1e5a1066dc10")
    version("0.15.5", sha256="00a1138429e8a7f830c9e229b9c0bcd6071b95dadd8c87eb81191079fb679225")
    version("0.14.1", sha256="66d1e349403f1d6c6350138d0f2b422046bcbdfb34fd95453dadae29a8b0c98a")

    depends_on("python@3.9:3.11", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm-git-archive", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    variant("nlopt", default=False, description="Enable nlopt support")
    variant("hs3", default=True, description="Enable serialization support")

    # TODO: remove "build" once fixed in spack that tests need "run", not "build"
    with default_args(type=("build", "run")):

        depends_on("py-tensorflow@2.15", type=("run"), when="@0.18")
        depends_on("py-tensorflow-probability@0.23", type=("run"), when="@0.18")

        depends_on("py-tensorflow@2.13", when="@0.15:0.17")
        depends_on("py-tensorflow-probability@0.21", when="@0.16:0.17")
        depends_on("py-tensorflow-probability@0.20:0.21", when="@0.15:0.16")

        depends_on("py-tensorflow@2.0:2.12", when="@0.14")
        depends_on("py-tensorflow-probability@0.20", when="@0.14")

        with when("+nlopt"):
            depends_on("nlopt@2.7.1: +python")

        with when("+hs3"):
            depends_on("py-asdf")

        depends_on("py-attrs", when="@0.15:")
        depends_on("py-typing-extensions", when="^python@:3.8")
        depends_on("py-boost-histogram")
        depends_on("py-colorama")
        depends_on("py-colored")
        depends_on("py-colorlog")
        depends_on("py-deprecated")
        depends_on("py-dill")
        depends_on("py-dotmap")
        depends_on("py-frozendict")
        depends_on("py-hist")
        depends_on("py-iminuit@2.3:")
        depends_on("py-jacobi")
        depends_on("py-numdifftools")
        depends_on("py-numpy@1.16:")
        depends_on("py-ordered-set")
        depends_on("py-pandas")
        depends_on("py-pydantic@:1")
        depends_on("py-pyyaml")
        depends_on("py-scipy@1.2:")
        depends_on("py-tabulate")
        depends_on("py-texttable")
        depends_on("py-uhi")
        depends_on("py-uproot@4:")
        depends_on("py-xxhash")
        depends_on("py-zfit-interface")
