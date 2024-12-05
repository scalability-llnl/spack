# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    pypi = "isort/isort-4.2.15.tar.gz"

    license("MIT")

    version("5.12.0", sha256="8bef7dde241278824a6d83f44a544709b065191b95b6e50894bdc722fcba0504")
    version("5.11.5", sha256="6be1f76a507cb2ecf16c7cf14a37e41609ca082330be4e3436a18ef74add55db")
    version("5.10.1", sha256="e8443a5e7a020e9d7f97f1d7d9cd17c88bcb3bc7e218bf9cf5095fe550be2951")
    version("5.9.3", sha256="9c2ea1e62d871267b78307fe511c0838ba0da28698c5732d54e2790bf3ba9899")
    version("5.9.1", sha256="83510593e07e433b77bd5bff0f6f607dbafa06d1a89022616f02d8b699cfcd56")
    version(
        "4.3.20",
        sha256="c40744b6bc5162bbb39c1257fe298b7a393861d50978b565f3ccd9cb9de0182a",
        deprecated=True,
    )
    version(
        "4.2.15",
        sha256="79f46172d3a4e2e53e7016e663cc7a8b538bec525c36675fcfd2767df30b3983",
        deprecated=True,
    )

    variant("colors", default=False, description="Install colorama for --color support")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@5.12:")
        depends_on("python@3.7:", when="@5.11")
        # This needs to be @3.6 since for bootstrapping the current Spack interpreter is
        # identified by major.minor (and the new versioning identifies it as @=3.6)
        depends_on("python@3.6:3", when="@5.10")
        depends_on("python@3.6:3", when="@5.9")

    conflicts("python@3.6.0", when="@5:")

    depends_on("py-setuptools", when="@:4", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@5:", type="build")
    depends_on("py-colorama@0.4.3:", when="+colors @5.12:", type=("build", "run"))
    depends_on("py-colorama@0.4.3:0.4", when="+colors @:5.11", type=("build", "run"))

    # https://github.com/PyCQA/isort/issues/2077
    conflicts("^py-poetry-core@1.5:", when="@:5.11.4")
