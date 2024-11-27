# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbclient(PythonPackage):
    """A client library for executing notebooks.

    Formally nbconvert's ExecutePreprocessor."""

    homepage = "https://jupyter.org/"
    pypi = "nbclient/nbclient-0.5.0.tar.gz"
    git = "https://github.com/jupyter/nbclient.git"

    license("BSD-3-Clause")

    version("0.8.0", sha256="f9b179cd4b2d7bca965f900a2ebf0db4a12ebff2f36a711cb66861e4ae158e55")
    version("0.7.2", sha256="884a3f4a8c4fc24bb9302f263e0af47d97f0d01fe11ba714171b320c8ac09547")
    version("0.6.7", sha256="3c5a7fc6bb74be7d31edf2817b44501a65caa99e5e56363bc359649b97cd24b9")
    version("0.6.6", sha256="0df76a7961d99a681b4796c74a1f2553b9f998851acc01896dce064ad19a9027")
    version("0.5.13", sha256="40c52c9b5e3c31faecaee69f202b3f53e38d7c1c563de0fadde9d7eda0fdafe8")
    version("0.5.5", sha256="ed7d18431393750d29a64da432e0b7889274eb5a5056682be5691b1b1dc8f755")
    version("0.5.0", sha256="8ad52d27ba144fca1402db014857e53c5a864a2f407be66ca9d74c3a56d6591d")

    depends_on("python@3.7:", when="@0.5.13:", type=("build", "run"))
    depends_on("python@3.6.1:", when="@0.5.5:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.7.0", type="build")
    depends_on("py-hatchling@1.10:", when="@0.7.1:", type="build")

    depends_on("py-jupyter-client@6.1.12:", when="@0.7.1:", type=("build", "run"))
    depends_on("py-jupyter-client@6.1.5:", type=("build", "run"))
    depends_on("py-jupyter-core@4.12:4,5.1:", when="@0.7.1:", type=("build", "run"))
    depends_on("py-nbformat@5.1:", when="@0.7.1:", type=("build", "run"))
    depends_on("py-nbformat@5.0:", type=("build", "run"))
    depends_on("py-traitlets@5.4:", when="@0.8:", type=("build", "run"))
    depends_on("py-traitlets@5.3:", when="@0.7.1:", type=("build", "run"))
    depends_on("py-traitlets@5.2.2:", when="@0.6:", type=("build", "run"))
    depends_on("py-traitlets@5:", when="@0.5.13:", type=("build", "run"))
    depends_on("py-traitlets@4.2:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-async-generator", when="@0.5.0", type=("build", "run"))
    depends_on("py-nest-asyncio", when="@:0.7.0", type=("build", "run"))
