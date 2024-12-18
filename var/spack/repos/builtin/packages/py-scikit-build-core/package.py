# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuildCore(PythonPackage):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    homepage = "https://github.com/scikit-build/scikit-build-core"
    pypi = "scikit_build_core/scikit_build_core-0.2.0.tar.gz"
    git = "https://github.com/scikit-build/scikit-build-core"

    maintainers("wdconinc")

    license("Apache-2.0")

    version("0.10.7", sha256="04cbb59fe795202a7eeede1849112ee9dcbf3469feebd9b8b36aa541336ac4f8")
    version("0.9.5", sha256="2a4cb119cc968fe87ae05582979657cc0e7be45655798446eabbe490e61ce072")
    version("0.8.2", sha256="50ec24b9568c9aa6e27233deeb2978932bc79856212b30575cbfa4049655c436")
    version("0.7.1", sha256="565f33e15f5aa4514248c508ce3ce40fb6f406f8c3983e891561757b1c9f78ab")
    version("0.6.1", sha256="392254a4ca7235c27a4be98cc24cd708f563171961ce37cff66120ebfda20b7a")
    version("0.6.0", sha256="1bea5ed83610b367f3446badd996f2356690548188d6d38e5b93152df311a7ae")
    version("0.2.0", sha256="d2a76d9447a412038dc5e25dd259b03c25278661a0c7c3da766bb971c1a9acd2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("pyproject", default=False, description="Enable pyproject.toml support")

    depends_on("python@3.7:", type=("build", "run"))

    # Build system
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    # Dependencies
    depends_on("py-exceptiongroup@1:", when="@0.9: ^python@:3.10", type=("build", "run"))
    depends_on("py-exceptiongroup", when="^python@:3.10", type=("build", "run"))
    depends_on("py-importlib-metadata@1:", when="@0.9: ^python@:3.7")
    depends_on("py-importlib-metadata", when="@0.3.0: ^python@:3.7")
    depends_on("py-importlib-resources@1.3:", when="^python@:3.8", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"), when="@0.9:")
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-pathspec@0.10.1:", type=("build", "run"), when="@0.9:")
    depends_on("py-tomli@1.2.2:", when="@0.9: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="@0.8: ^python@:3.8", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="@:0.7 ^python@:3.7", type=("build", "run"))
    depends_on("cmake@3.15:", type=("build", "run"))

    # Optional dependencies
    depends_on("py-pyproject-metadata@0.5:", when="@:0.8 +pyproject", type=("build", "run"))
    depends_on("py-pathspec@0.10.1:", when="@:0.8 +pyproject", type=("build", "run"))

    # Test dependencies
    depends_on("py-build@0.8:", when="@0.9:", type="test")
    depends_on("py-build +virtualenv", when="@:0.8", type="test")
    depends_on("py-cattrs@22.2:", type="test")
    depends_on("py-importlib-metadata", when="^python@:3.7", type="test")
    depends_on("py-pybind11@2.12:", when="@0.9:", type="test")
    depends_on("py-pathspec@0.10.1:", when="@:0.8", type="test")
    depends_on("py-pybind11@2.12:", when="@0.9:", type="test")
    depends_on("py-pybind11", type="test")
    depends_on("py-pyproject-metadata@0.5:", when="@:0.8", type="test")
    depends_on("py-pytest@7:", type="test")
    depends_on("py-pytest-subprocess@1.5:", type="test")
    depends_on("py-setuptools@43:", when="@0.9: ^python@:3.8", type="test")
    depends_on("py-setuptools@45:", when="@0.9: ^python@3.9", type="test")
    depends_on("py-setuptools@49:", when="@0.9: ^python@3.10:3.11", type="test")
    depends_on("py-setuptools@66.1:", when="@0.9: ^python@3.12:", type="test")
    depends_on("py-virtualenv@20.0.28:", when="@0.9:", type="test")
    depends_on("py-setuptools", type="test")
    depends_on("py-virtualenv", when="@0.6:", type="test")
    depends_on("py-wheel@0.40:", when="@0.9:", type="test")
    depends_on("py-wheel", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            which("pytest")()
