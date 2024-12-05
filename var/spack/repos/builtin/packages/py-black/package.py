# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlack(PythonPackage):
    """Black is the uncompromising Python code formatter. By using it, you agree to
    cede control over minutiae of hand-formatting. In return, Black gives you
    speed, determinism, and freedom from pycodestyle nagging about formatting.
    """

    homepage = "https://github.com/psf/black"
    pypi = "black/black-22.1.0.tar.gz"

    license("MIT", checked_by="tgamblin")
    maintainers("spack/spack-releasers")

    version("24.3.0", sha256="a0c9c4a0771afc6919578cec71ce82a3e31e054904e7197deacbc9382671c41f")
    version("24.2.0", sha256="bce4f25c27c3435e4dace4815bcb2008b87e167e3bf4ee47ccdc5ce906eb4894")
    version("24.1.1", sha256="48b5760dcbfe5cf97fd4fba23946681f3a81514c6ab8a45b50da67ac8fbc6c7b")
    version("24.1.0", sha256="30fbf768cd4f4576598b1db0202413fafea9a227ef808d1a12230c643cefe9fc")
    version("23.12.1", sha256="4ce3ef14ebe8d9509188014d96af1c456a910d5b5cbf434a09fef7e024b3d0d5")
    version("23.12.0", sha256="330a327b422aca0634ecd115985c1c7fd7bdb5b5a2ef8aa9888a82e2ebe9437a")
    version("23.11.0", sha256="4c68855825ff432d197229846f971bc4d6666ce90492e5b02013bcaca4d9ab05")
    version("23.10.1", sha256="1f8ce316753428ff68749c65a5f7844631aa18c8679dfd3ca9dc1a289979c258")
    version("23.10.0", sha256="31b9f87b277a68d0e99d2905edae08807c007973eaa609da5f0c62def6b7c0bd")
    version("23.9.1", sha256="24b6b3ff5c6d9ea08a8888f6977eae858e1f340d7260cf56d70a49823236b62d")
    version("23.9.0", sha256="3511c8a7e22ce653f89ae90dfddaf94f3bb7e2587a245246572d3b9c92adf066")
    version("23.7.0", sha256="022a582720b0d9480ed82576c920a8c1dde97cc38ff11d8d8859b3bd6ca9eedb")
    version("23.3.0", sha256="1c7b8d606e728a41ea1ccbd7264677e494e87cf630e399262ced92d4a8dac940")
    version("23.1.0", sha256="b0bd97bea8903f5a2ba7219257a44e3f1f9d00073d6cc1add68f0beec69692ac")
    version("22.12.0", sha256="229351e5a18ca30f447bf724d007f890f97e13af070bb6ad4c0a441cd7596a2f")
    version("22.10.0", sha256="f513588da599943e0cde4e32cc9879e825d58720d6557062d1098c5ad80080e1")
    version("22.8.0", sha256="792f7eb540ba9a17e8656538701d3eb1afcb134e3b45b71f20b25c77a8db7e6e")
    version("22.6.0", sha256="6c6d39e28aed379aec40da1c65434c77d75e65bb59a1e1c283de545fb4e7c6c9")
    version("22.3.0", sha256="35020b8886c022ced9282b51b5a875b6d1ab0c387b31a065b84db7c33085ca79")
    version("22.1.0", sha256="a7c0192d35635f6fc1174be575cb7915e92e5dd629ee79fdaf0dcfa41a80afb5")

    variant("colorama", default=False, description="enable colorama support")
    variant("uvloop", default=False, description="enable uvloop support")
    variant("d", default=False, description="enable blackd HTTP server")
    variant("jupyter", default=False, description="enable Jupyter support")

    depends_on("py-hatchling@1.20:", when="@23.12.1:", type="build")
    depends_on("py-hatchling@1.8:", when="@22.10:", type="build")
    depends_on("py-hatch-vcs", when="@22.10:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@22.10:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@23.7:")
        depends_on("python@3.7:", when="@22.10:")
        depends_on("py-click@8:")
        depends_on("py-mypy-extensions@0.4.3:")
        depends_on("py-packaging@22:", when="@23.1:")
        depends_on("py-pathspec@0.9:")
        depends_on("py-platformdirs@2:")
        depends_on("py-tomli@1.1:", when="@22.8: ^python@:3.10")
        depends_on("py-tomli@1.1:", when="@21.7:22.6")
        depends_on("py-typing-extensions@4.0.1:", when="@23.9: ^python@:3.10")
        depends_on("py-typing-extensions@3.10:", when="@:23.7 ^python@:3.9")

        depends_on("py-colorama@0.4.3:", when="+colorama")
        depends_on("py-uvloop@0.15.2:", when="+uvloop")
        depends_on("py-aiohttp@3.7.4:", when="+d")
        depends_on("py-ipython@7.8:", when="+jupyter")
        depends_on("py-tokenize-rt@3.2:", when="+jupyter")

    # Historical dependencies
    depends_on("py-setuptools@45:", when="@:22.8", type=("build", "run"))
    depends_on("py-setuptools-scm@6.3.1:+toml", when="@:22.8", type="build")
    depends_on("py-typed-ast@1.4.2:", when="^python@:3.7", type=("build", "run"))

    # Needed because this package is used to bootstrap Spack (Spack supports Python 3.6+)
    depends_on("py-dataclasses@0.6:", when="^python@:3.6", type=("build", "run"))

    # see: https://github.com/psf/black/issues/2964
    # note that pip doesn't know this constraint.
    depends_on("py-click@:8.0", when="@:22.2", type=("build", "run"))

    @property
    def import_modules(self):
        modules = ["blib2to3", "blib2to3.pgen2", "black"]

        if "+d" in self.spec:
            modules.append("blackd")

        return modules
