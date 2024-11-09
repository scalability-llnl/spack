# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAccimage(PythonPackage):
    """An accelerated Image loader and preprocessor leveraging Intel IPP.

    accimage mimics the PIL API and can be used as a backend for torchvision.
    """

    homepage = "https://github.com/pytorch/accimage"
    url = "https://github.com/pytorch/accimage/archive/v0.1.1.tar.gz"

    license("BSD-2-Clause")

    version("0.1.1", sha256="573c56866a42683c7cf25185620fe82ec2ce78468e0621c29fac8f4134a785f5")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("jpeg")
    depends_on("ipp")
    depends_on("py-pytest", type="test")
    depends_on("py-numpy", type="test")
    depends_on("py-imageio", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        pytest = which("pytest")
        pytest("test.py")
