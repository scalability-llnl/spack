# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IbmDatabroker(CMakePackage, PythonExtension):
    """The Data Broker (DBR) is a distributed, in-memory container of key-value
    stores enabling applications in a workflow to exchange data through one or
    more shared namespaces. Thanks to a small set of primitives, applications
    in a workflow deployed in a (possibly) shared nothing distributed cluster,
    can easily share and exchange data and messages with applications."""

    homepage = "https://github.com/IBM/data-broker"
    git = "https://github.com/IBM/data-broker"
    url = "https://github.com/IBM/data-broker/archive/0.6.1.tar.gz"

    # IBM dev team should take over
    maintainers("bhatiaharsh")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.7.0", sha256="5460fa1c5c05ad25c759b2ee4cecee92980d4dde5bc7c5f6da9242806cf22bb8")
    version("0.6.1", sha256="2c7d6c6a269d4ae97aad4d770533e742f367da84758130c283733f25df83e535")
    version("0.6.0", sha256="5856209d965c923548ebb69119344f1fc596d4c0631121b230448cc91bac4290")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("python", default=False, description="Build Python bindings")

    depends_on("cmake@2.8:", type="build")
    depends_on("redis@5.0.2:", type="run")
    depends_on("libevent@2.1.8", type=("build", "run"))

    extends("python", when="+python")
    depends_on("python@3.7:", when="+python")
    depends_on("py-setuptools", when="+python")

    patch("fixes_in_v0.6.1.patch", when="@0.6.1")
    patch("fixes_in_v0.7.0.patch", when="@0.7.0")

    def cmake_args(self):
        args = []
        args.append("-DDEFAULT_BE=redis")
        if self.spec.satisfies("+python"):
            args.append("-DPYDBR=1")
        return args
