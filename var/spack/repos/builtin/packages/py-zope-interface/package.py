# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZopeInterface(PythonPackage):
    """This package provides an implementation of "object interfaces" for
    Python. Interfaces are a mechanism for labeling objects as conforming to a
    given API or contract. So, this package can be considered as implementation
    of the Design By Contract methodology support in Python."""

    homepage = "https://github.com/zopefoundation/zope.interface"
    pypi = "zope.interface/zope.interface-4.5.0.tar.gz"

    license("ZPL-2.1", checked_by="wdconinc")

    version("7.0.3", sha256="cd2690d4b08ec9eaf47a85914fe513062b20da78d10d6d789a792c0b20307fb1")
    version("7.0.2", sha256="f1146bb27a411d0d40cc0e88182a6b0e979d68ab526c8e5ae9e27c06506ed017")
    version("7.0.1", sha256="f0f5fda7cbf890371a59ab1d06512da4f2c89a6ea194e595808123c863c38eff")
    version("7.0", sha256="a6699621e2e9565fb34e40677fba6eb0974afc400063b3110d8a14d5b0c7a916")
    version("6.3", sha256="f83d6b4b22262d9a826c3bd4b2fbfafe1d0000f085ef8e44cd1328eea274ae6a")
    version("6.2", sha256="3b6c62813c63c543a06394a636978b22dffa8c5410affc9331ce6cdb5bfa8565")
    version("6.1", sha256="2fdc7ccbd6eb6b7df5353012fbed6c3c5d04ceaca0038f75e601060e95345309")
    version("6.0", sha256="aab584725afd10c710b8f1e6e208dbee2d0ad009f57d674cb9d1b3964037275d")
    version("5.5.2", sha256="bfee1f3ff62143819499e348f5b8a7f3aa0259f9aca5e0ddae7391d059dce671")
    version("5.5.1", sha256="6d678475fdeb11394dc9aaa5c564213a1567cc663082e0ee85d52f78d1fbaab2")
    version("5.5.0", sha256="700ebf9662cf8df70e2f0cb4988e078c53f65ee3eefd5c9d80cf988c4175c8e3")
    version("5.4.0", sha256="5dba5f530fec3f0988d83b78cc591b58c0b6eb8431a85edd1569a0539a8a5a0e")
    version("5.1.0", sha256="40e4c42bd27ed3c11b2c983fecfb03356fae1209de10686d03c02c8696a1d90e")
    version("4.5.0", sha256="57c38470d9f57e37afb460c399eb254e7193ac7fb8042bd09bdc001981a9c74c")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@4.5.0")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@5.1.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@6:")
    depends_on("python@3.8:", type=("build", "run"), when="@7:")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools@:45", type=("build", "run"), when="@4.5.0")
