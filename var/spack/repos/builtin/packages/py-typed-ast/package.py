# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.python
from spack.package import *


class PyTypedAst(PythonPackage):
    """A fork of Python 2 and 3 ast modules with type comment support."""

    homepage = "https://github.com/python/typed_ast"
    pypi = "typed-ast/typed_ast-1.4.0.tar.gz"

    license("Apache-2.0")

    version("1.5.4", sha256="39e21ceb7388e4bb37f4c679d72707ed46c2fbf2a5609b8b8ebc4b067d977df2")
    version("1.4.3", sha256="fb1bbeac803adea29cedd70781399c99138358c26d05fcbd23c13016b7f5ec65")
    version("1.4.2", sha256="9fc0b3cb5d1720e7141d103cf4819aea239f7d136acf9ee4a69b047b7986175a")
    version("1.4.1", sha256="8c8aaad94455178e3187ab22c8b01a3837f8ee50e09cf31f1ba129eb293ec30b")
    version("1.4.0", sha256="66480f95b8167c9c5c5c87f32cf437d585937970f3fc24386f313a4c97b44e34")
    version(
        "1.3.5",
        sha256="5315f4509c1476718a4825f45a203b82d7fdf2a6f5f0c8f166435975b1c9f7d4",
        url="https://files.pythonhosted.org/packages/source/t/typed-ast/typed-ast-1.3.5.tar.gz",
    )

    depends_on("c", type="build")  # generated

    variant(
        "wheel",
        default=False,
        sticky=True,
        description="Install from wheel (required for bootstrapping Spack)",
    )

    depends_on("python@3.3:", type=("build", "link", "run"))
    depends_on("python@3.6:", when="@1.5.4:", type=("build", "link", "run"))
    depends_on("python@:3.8", when="@:1.4.0")  # build errors with 3.9 until 1.4.1
    depends_on("py-setuptools", type="build")


class PythonPipBuilder(spack.build_systems.python.PythonPipBuilder):
    @when("+wheel")
    def install(self, pkg, spec, prefix):
        args = list(filter(lambda x: x != "--no-index", self.std_args(self.pkg)))
        args += [f"--prefix={prefix}", self.spec.format("typed-ast=={version}")]
        pip(*args)
