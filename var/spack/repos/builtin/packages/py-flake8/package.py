# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    pypi = "flake8/flake8-4.0.1.tar.gz"

    license("MIT")

    version("6.1.0", sha256="d5b3857f07c030bdb5bf41c7f53799571d75c4491748a3adcd47de929e34cd23")
    version("6.0.0", sha256="c61007e76655af75e6785a931f452915b371dc48f56efd765247c8fe68f2b181")
    version("5.0.4", sha256="6fbe320aad8d6b95cec8b8e47bc933004678dc63095be98528b7bdd2a9f510db")
    version("5.0.2", sha256="9cc32bc0c5d16eacc014c7ec6f0e9565fd81df66c2092c3c9df06e3c1ac95e5d")
    version("5.0.1", sha256="9c51d3d1426379fd444d3b79eabbeb887849368bd053039066439523d8486961")
    version("5.0.0", sha256="503b06b6795189e55298a70b695b1eb4f6b8d479fae81352fc97c72ca242509e")
    version("4.0.1", sha256="806e034dda44114815e23c16ef92f95c91e4c71100ff52813adf7132a6ad870d")
    version("4.0.0", sha256="b52d27e627676b015340c3b1c72bc9259a6cacc9341712fb8f01ddfaaa2c651a")
    version("3.9.2", sha256="07528381786f2a6237b061f6e96610a4167b226cb926e2aa2b6b1d78057c576b")
    version("3.8.2", sha256="c69ac1668e434d37a2d2880b3ca9aafd54b3a10a3ac1ab101d22f29e29cf8634")
    version("3.7.8", sha256="19241c1cbc971b9962473e4438a2ca19749a7dd002dd1a946eaba171b4114548")
    version("3.7.7", sha256="859996073f341f2670741b51ec1e67a01da142831aa1fdc6242dbf88dffbe661")
    version("3.5.0", sha256="7253265f7abd8b313e3892944044a365e3f4ac3fcdcfb4298f55ee9ddf188ba0")
    version("3.0.4", sha256="b4c210c998f07d6ff24325dd91fbc011f2c37bcd6bf576b188de01d8656e970d")
    version("2.5.4", sha256="cc1e58179f6cf10524c7bfdd378f5536d0a61497688517791639a5ecc867492f")

    depends_on("python@3.8.1:", when="@6:", type=("build", "run"))
    depends_on("python@3.6.1:", when="@5:", type=("build", "run"))
    depends_on("python@3.6:", when="@4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@3.9.2:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on("py-setuptools@30:", type=("build", "run"))

    # Flake8 uses ranges for its dependencies to enforce a stable list of
    # error codes within each minor release:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    # http://flake8.pycqa.org/en/latest/internal/releases.html#releasing-flake8

    # Flake8 6.1.X
    depends_on("py-mccabe@0.7", when="@6.1", type=("build", "run"))
    depends_on("py-pycodestyle@2.11", when="@6.1", type=("build", "run"))
    depends_on("py-pyflakes@3.1", when="@6.1", type=("build", "run"))

    # Flake8 6.0.X
    depends_on("py-mccabe@0.7", when="@6.0", type=("build", "run"))
    depends_on("py-pycodestyle@2.10", when="@6.0", type=("build", "run"))
    depends_on("py-pyflakes@3.0", when="@6.0", type=("build", "run"))

    # Flake8 5.0.X
    depends_on("py-mccabe@0.7", when="@5.0", type=("build", "run"))
    depends_on("py-pycodestyle@2.9", when="@5.0", type=("build", "run"))
    depends_on("py-pyflakes@2.5", when="@5.0", type=("build", "run"))

    # Flake8 4.0.X
    depends_on("py-mccabe@0.6", when="@4.0", type=("build", "run"))
    depends_on("py-pycodestyle@2.8", when="@4.0", type=("build", "run"))
    depends_on("py-pyflakes@2.4", when="@4.0", type=("build", "run"))

    # Flake8 3.9.X
    depends_on("py-pyflakes@2.3", when="@3.9", type=("build", "run"))
    depends_on("py-pycodestyle@2.7", when="@3.9", type=("build", "run"))
    depends_on("py-mccabe@0.6", when="@3.9", type=("build", "run"))

    # Flake8 3.8.X
    depends_on("py-pyflakes@2.2", when="@3.8", type=("build", "run"))
    depends_on("py-pycodestyle@2.6", when="@3.8", type=("build", "run"))
    depends_on("py-mccabe@0.6", when="@3.8", type=("build", "run"))

    # Flake8 3.7.X
    depends_on("py-entrypoints@0.3", when="@3.7", type=("build", "run"))
    depends_on("py-pyflakes@2.1", when="@3.7", type=("build", "run"))
    depends_on("py-pycodestyle@2.5", when="@3.7", type=("build", "run"))
    depends_on("py-mccabe@0.6", when="@3.7", type=("build", "run"))

    # Flake8 3.5.X
    depends_on("py-pyflakes@1.5:1.6", when="@3.5", type=("build", "run"))
    depends_on("py-pycodestyle@2.0:2.4", when="@3.5", type=("build", "run"))
    depends_on("py-mccabe@0.6", when="@3.5", type=("build", "run"))

    # Flake8 3.0.X
    depends_on("py-pyflakes@0.8.1:1.1,1.2.3:1.2", when="@3.0", type=("build", "run"))
    depends_on("py-pycodestyle@2.0", when="@3.0", type=("build", "run"))
    depends_on("py-mccabe@0.5", when="@3.0", type=("build", "run"))

    # Flake8 2.5.X
    depends_on("py-pyflakes@0.8.1:1.0", when="@2.5", type=("build", "run"))
    depends_on("py-pycodestyle@1.5.7:1.5,1.6.3:", when="@2.5", type=("build", "run"))
    depends_on("py-mccabe@0.2.1:0.4", when="@2.5", type=("build", "run"))

    # Python version-specific backports
    depends_on("py-importlib-metadata", when="@3.8:3.9.2 ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@:4.2", when="@4: ^python@:3.7", type=("build", "run"))
    depends_on("py-importlib-metadata@1.1:4.2", when="@5.0.4: ^python@:3.7", type=("build", "run"))

    @when("@:3.5")
    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", "setup.py", string=True)
