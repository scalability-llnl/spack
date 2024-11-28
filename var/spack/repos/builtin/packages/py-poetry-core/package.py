# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoetryCore(PythonPackage):
    """Poetry PEP 517 Build Backend."""

    homepage = "https://github.com/python-poetry/poetry-core"
    pypi = "poetry-core/poetry_core-1.6.1.tar.gz"

    license("MIT")

    version("1.8.1", sha256="67a76c671da2a70e55047cddda83566035b701f7e463b32a2abfeac6e2a16376")
    version("1.7.0", sha256="8f679b83bd9c820082637beca1204124d5d2a786e4818da47ec8acefd0353b74")
    version("1.6.1", sha256="0f9b0de39665f36d6594657e7d57b6f463cc10f30c28e6d1c3b9ff54c26c9ac3")
    version("1.2.0", sha256="ceccec95487e46c63a41761fbac5211b809bca22658e25a049f4c7da96269f71")
    version("1.1.0", sha256="d145ae121cf79118a8901b60f2c951c4edcc16f55eb8aaefc156aa33aa921f07")
    version("1.0.8", sha256="951fc7c1f8d710a94cb49019ee3742125039fc659675912ea614ac2aa405b118")
    version("1.0.7", sha256="98c11c755a16ef6c5673c22ca94a3802a7df4746a0853a70b6fae8b9f5cac206")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:3", when="@1.7.0:", type=("build", "run"))
    depends_on("python@3.7:3", when="@1.1.0:", type=("build", "run"))
    depends_on("python@:3", type=("build", "run"))
    depends_on("py-importlib-metadata@1.7:", when="@1.1:1.6 ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@1.7:1", when="@:1.0 ^python@:3.7", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/p/poetry-core/{0}-{1}.tar.gz"
        if version >= Version("1.4"):
            letter = "poetry_core"
        else:
            letter = "poetry-core"
        return url.format(letter, version)

    # https://github.com/python-poetry/poetry/issues/5547
    def setup_build_environment(self, env):
        env.set("GIT_DIR", join_path(self.stage.source_path, ".git"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("GIT_DIR", join_path(dependent_spec.package.stage.source_path, ".git"))
