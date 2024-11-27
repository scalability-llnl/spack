# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libyaml(AutotoolsPackage):
    """A C library for parsing and emitting YAML."""

    homepage = "https://pyyaml.org/wiki/LibYAML"
    url = "https://pyyaml.org/download/libyaml/yaml-0.2.4.tar.gz"
    git = "https://github.com/yaml/libyaml.git"

    license("MIT")

    version("master", branch="master")
    version("0.2.5", sha256="c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4")
    version("0.2.4", sha256="d80aeda8747b7c26fbbfd87ab687786e58394a8435ae3970e79cb97882e30557")
    version("0.2.3", sha256="08bbb80284d77092e68a6f69f1e480e8ed93e215c47b2ca29290e3bd5a191108")
    version("0.2.2", sha256="4a9100ab61047fd9bd395bcef3ce5403365cafd55c1e0d0299cde14958e47be9")
    version("0.2.1", sha256="78281145641a080fb32d6e7a87b9c0664d611dcb4d542e90baf731f51cbb59cd")
    version("0.1.7", sha256="8088e457264a98ba451a90b8661fcb4f9d6f478f7265d48322a196cec2480729")
    version("0.1.6", sha256="7da6971b4bd08a986dd2a61353bc422362bd0edcc67d7ebaac68c95f74182749")
    version("0.1.5", sha256="fa87ee8fb7b936ec04457bc044cd561155e1000a4d25029867752e543c2d3bef")
    version("0.1.4", sha256="7bf81554ae5ab2d9b6977da398ea789722e0db75b86bffdaeb4e66d961de6a37")
    version("0.1.3", sha256="a8bbad7e5250b3735126b7e3bd9f6fce9db19d6be7cc13abad17a24b59ec144a")
    version("0.1.2", sha256="5beb94529cc7ac79b17e354f9b03aea311f5af17be5d48bc39e6f1db5059f70f")
    version("0.1.1", sha256="76444692a94de4e6776a1bdf3b735e8f016bb374ae7c60496f8032fdc6085889")

    depends_on("c", type="build")  # generated

    depends_on("automake", when="@master")
    depends_on("autoconf", when="@master")
    depends_on("libtool", when="@master")
    depends_on("m4", when="@master")

    @run_before("configure")
    def bootstrap(self):
        if self.spec.satisfies("@master"):
            bootstrap = Executable("./bootstrap")
            bootstrap()
