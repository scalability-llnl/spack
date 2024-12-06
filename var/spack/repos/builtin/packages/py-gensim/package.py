# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGensim(PythonPackage):
    """Gensim is a Python library for topic modelling, document indexing and
    similarity retrieval with large corpora. Target audience is the natural
    language processing (NLP) and information retrieval (IR) community."""

    homepage = "https://radimrehurek.com/gensim"
    pypi = "gensim/gensim-3.8.1.tar.gz"

    maintainers("adamjstewart")

    license("LGPL-2.1-only")

    version("4.3.1", sha256="8b5f11c0e6a5308086b48e8f6841223a4fa1a37d513684612b7ee854b533015f")
    version("3.8.3", sha256="786adb0571f75114e9c5f7a31dd2e6eb39a9791f22c8757621545e2ded3ea367")
    version("3.8.1", sha256="33277fc0a8d7b0c7ce70fcc74bb82ad39f944c009b334856c6e86bf552b1dfdc")
    version("3.8.0", sha256="ec5de7ff2bfa8692fa96a846bb5aae52f267fc322fbbe303c1f042d258af5766")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@4.3.1:")
    depends_on("py-setuptools", type="build")

    depends_on("py-cython", type=("build", "run"), when="@4.3.1:")

    depends_on("py-numpy@1.11.3:", type=("build", "run"))
    depends_on("py-numpy@1.18.5:", type=("build", "run"), when="@4.3.1:")

    depends_on("py-scipy@0.18.1:", type=("build", "run"))
    depends_on("py-scipy@1.7.0:", type=("build", "run"), when="@4.3.1:")

    depends_on("py-six@1.5.0:", type=("build", "run"), when="@:3.8.3")

    depends_on("py-smart-open@1.7.0:", when="@3.8.0", type=("build", "run"))
    depends_on("py-smart-open@1.8.1:", when="@3.8.1:", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("GENSIM_CYTHON_REQUIRES", "Cython=={0}".format(self.spec["py-cython"].version))
