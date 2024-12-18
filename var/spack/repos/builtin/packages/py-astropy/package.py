# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyAstropy(PythonPackage):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = "https://astropy.org/"
    pypi = "astropy/astropy-4.0.1.post1.tar.gz"
    git = "https://github.com/astropy/astropy.git"

    license("BSD-3-Clause")

    version("6.1.0", sha256="6c3b915f10b1576190730ddce45f6245f9927dda3de6e3f692db45779708950f")
    version("5.1", sha256="1db1b2c7eddfc773ca66fa33bd07b25d5b9c3b5eee2b934e0ca277fa5b1b7b7e")
    version(
        "4.0.1.post1", sha256="5c304a6c1845ca426e7bc319412b0363fccb4928cb4ba59298acd1918eec44b5"
    )
    version("3.2.1", sha256="706c0457789c78285e5464a5a336f5f0b058d646d60f4e5f5ba1f7d5bf424b28")
    version("2.0.14", sha256="618807068609a4d8aeb403a07624e9984f566adc0dc0f5d6b477c3658f31aeb6")
    version("1.1.2", sha256="6f0d84cd7dfb304bb437dda666406a1d42208c16204043bc920308ff8ffdfad1")
    version("1.1.post1", sha256="64427ec132620aeb038e4d8df94d6c30df4cc8b1c42a6d8c5b09907a31566a21")

    depends_on("c", type="build")  # generated

    variant("all", default=False, when="@3.2:", description="Enable all functionality")

    # Required dependencies
    depends_on("python@3.10:", when="@6.1.0:", type=("build", "run"))
    depends_on("python@3.8:", when="@5.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.13:", type="build")
    depends_on("py-cython@0.29.30", when="@5.1:6.0", type="build")
    depends_on("py-cython@3.0.0", when="@6.1.0:", type="build")

    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")

    depends_on("py-astropy-iers-data", when="@6:", type=("build", "run"))
    depends_on("py-numpy@1.23:", when="@6.1:", type=("build", "run"))
    depends_on("py-numpy@1.18:", when="@5.1:", type=("build", "run"))
    depends_on("py-numpy@1.16:", when="@4.0:", type=("build", "run"))
    depends_on("py-numpy@1.13:", when="@3.1:", type=("build", "run"))
    depends_on("py-numpy@1.10:", when="@3.0:", type=("build", "run"))
    depends_on("py-numpy@1.9:", when="@2.0:", type=("build", "run"))
    depends_on("py-numpy@1.7:", when="@1.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/astropy/astropy/issues/16200
    depends_on("py-numpy@:1", when="@:6.0")
    depends_on("py-packaging@19.0:", when="@5.1:", type=("build", "run"))
    depends_on("py-pyyaml@3.13:", when="@5.1:", type=("build", "run"))
    depends_on("py-pyerfa@2.0:", when="@5.1:", type=("build", "run"))
    depends_on("py-pyerfa@2.0.1.1:", when="@6.1.0:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:", when="@5.1:", type="build")
    depends_on("py-extension-helpers", when="@5.1:", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("py-pytest@7:", type="test")
    depends_on("py-pytest-doctestplus@0.12:", type="test")
    depends_on("py-pytest-astropy-header@0.2.1:", type="test")
    depends_on("py-pytest-astropy@0.10:", type="test")
    depends_on("py-pytest-xdist", type="test")

    # Optional dependencies
    with when("+all"):
        depends_on("py-scipy@1.8:", when="@6:", type=("build", "run"))
        depends_on("py-scipy@1.3:", when="@5:", type=("build", "run"))
        depends_on("py-scipy@0.18:", type=("build", "run"))
        depends_on("py-matplotlib@3.3:", when="@6:", type=("build", "run"))
        depends_on("py-matplotlib@3.1:", when="@5:", type=("build", "run"))
        depends_on("py-matplotlib@2.1:", when="@4:", type=("build", "run"))
        depends_on("py-matplotlib@2.0:", type=("build", "run"))
        depends_on("py-certifi", when="@4.3:", type=("build", "run"))
        depends_on("py-dask+array", when="@4.1:", type=("build", "run"))
        depends_on("py-h5py", type=("build", "run"))
        depends_on("py-pyarrow@5:", when="@5:", type=("build", "run"))
        depends_on("py-beautifulsoup4", type=("build", "run"))
        depends_on("py-html5lib", type=("build", "run"))
        depends_on("py-bleach", type=("build", "run"))
        depends_on("py-pandas", type=("build", "run"))
        depends_on("py-sortedcontainers", type=("build", "run"))
        depends_on("py-pytz", type=("build", "run"))
        depends_on("py-jplephem", type=("build", "run"))
        depends_on("py-mpmath", type=("build", "run"))
        depends_on("py-asdf@2.10:", when="@5.1:", type=("build", "run"))
        depends_on("py-asdf@2.5:", when="@4.0.1post1:", type=("build", "run"))
        depends_on("py-asdf@2.3:", type=("build", "run"))
        depends_on("py-bottleneck", type=("build", "run"))
        depends_on("py-ipython@4.2:", when="@4.3:", type=("build", "run"))
        depends_on("py-ipython", type=("build", "run"))
        depends_on("py-pytest@7:", when="@5.0.2:", type=("build", "run"))
        depends_on("py-pytest", type=("build", "run"))
        depends_on("py-fsspec+http@2023.4:", when="@6.1:", type=("build", "run"))
        depends_on("py-s3fs@2023.4:", when="@6.1:", type=("build", "run"))
        depends_on("py-typing-extensions@3.10.0.1:", when="@5.0.2:", type=("build", "run"))

        # Historical optional dependencies
        depends_on("py-pyyaml", when="@:5", type=("build", "run"))
        depends_on("py-scikit-image", when="@:4.0", type=("build", "run"))
        depends_on("py-bintrees", when="@:3.2.1", type=("build", "run"))

        conflicts("^py-matplotlib@3.4.0,3.5.2")

    # System dependencies
    depends_on("erfa")
    depends_on("wcslib")
    depends_on("cfitsio@:3")
    depends_on("expat")

    def patch(self):
        # forces the rebuild of files with cython
        # avoids issues with PyCode_New() in newer
        # versions of python in the distributed
        # cython-ized files
        if os.path.exists("astropy/cython_version.py"):
            os.remove("astropy/cython_version.py")

    def install_options(self, spec, prefix):
        args = [
            "--use-system-libraries",
            "--use-system-erfa",
            "--use-system-wcslib",
            "--use-system-cfitsio",
            "--use-system-expat",
        ]

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("spack-test", create=True):
            python("-c", "import astropy; astropy.test()")

    @property
    def skip_modules(self):
        modules = []

        if self.spec.satisfies("~extras"):
            modules.append("astropy.visualization.wcsaxes")

        return modules
