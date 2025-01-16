# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class PyPycuda(PythonPackage):
    """PyCUDA gives you easy, Pythonic access to Nvidia's CUDA parallel
    computation API
    """

    homepage = "https://mathema.tician.de/software/pycuda/"
    pypi = "pycuda/pycuda-2019.1.2.tar.gz"

    license("MIT")

    version("2024.1.2", sha256="d110b727cbea859da4b63e91b6fa1e9fc32c5bade02d89ff449975996e9ccfab")
    version("2021.1", sha256="ab87312d0fc349d9c17294a087bb9615cffcf966ad7b115f5b051008a48dd6ed")
    version("2020.1", sha256="effa3b99b55af67f3afba9b0d1b64b4a0add4dd6a33bdd6786df1aa4cc8761a5")
    version("2019.1.2", sha256="ada56ce98a41f9f95fe18809f38afbae473a5c62d346cfa126a2d5477f24cc8a")
    version("2016.1.2", sha256="a7dbdac7e2f0c0d2ad98f5f281d5a9d29d6673b3c20210e261b96e9a2d0b6e37")

    depends_on("cxx", type="build")  # generated

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    # TODO: for versions before 2024.1.2, find out the exact requirements with version constraints
    # and enter them below. See https://github.com/spack/spack/pull/48547
    depends_on("python@3.6:3", type=("build", "run"), when="@2020.1:")
    depends_on("python@3.8:3", type=("build", "run"), when="@2024.1.2:")
    depends_on("boost+python")
    depends_on("cuda", type=("build", "run"))
    depends_on("cuda@:8.0.61", when="@2016.1.2")
    depends_on("py-appdirs@1.4.0:", type=("build", "run"), when="@:2021.1")
    depends_on("py-decorator@3.2.0:", type=("build", "run"), when="@:2020.1")
    depends_on("py-mako", type=("build", "run"))
    depends_on("py-numpy@1.6:", type=("build", "run"), when="@:2021.1")
    depends_on("py-numpy@1.24:", type=("build", "run"), when="@2024.1.2:")
    depends_on("py-platformdirs@2.2:", type=("build", "run"), when="@2024.1.2:")
    depends_on("py-pytools@2011.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type="run", when="@:2020.1")
    depends_on("py-pytools@2011.2:", type=("build", "run"), when="@2024.1.2:")

    @run_before("install")
    def configure(self):
        pyver = self.spec["python"].version.up_to(2).joined
        boostlib = "boost_python{0}".format(pyver)
        configure_args = [
            "--no-use-shipped-boost",
            "--boost-inc-dir={0}".format(self.spec["boost"].prefix.include),
            "--boost-lib-dir={0}".format(self.spec["boost"].libs.directories[0]),
            "--boost-python-libname={0}".format(boostlib),
        ]
        python("configure.py", *configure_args)
