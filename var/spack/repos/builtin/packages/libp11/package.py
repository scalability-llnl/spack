# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libp11(AutotoolsPackage):
    """The PKCS#11 API is an abstract API to perform operations on
    cryptographic objects such as private keys, without requiring
    access to the objects themselves. That is, it provides a logical
    separation of the keys from the operations. The PKCS #11 API is
    mainly used to access objects in smart cards and Hardware or
    Software Security Modules (HSMs). That is because in these modules
    the cryptographic keys are isolated in hardware or software and
    are not made available to the applications using them."""

    homepage = "https://github.com/OpenSC/libp11/wiki"
    url = "https://github.com/OpenSC/libp11/archive/libp11-0.4.10.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.4.12", sha256="c1a233ecb09ab48595ba36a504c47f82cf53a59aa8db789c02ca72d50e85ca87")
    version("0.4.11", sha256="56d6149879bda379613d89adfd3486ce5a3c20af6c1e3f9e83d15d900ab9e4bc")
    version("0.4.10", sha256="123c1525fa7ce7a34060f9a4148a30717482c517a378f428b704459820c1bf35")
    version("0.4.9", sha256="9d1c76d74c21ca224f96204982097ebc6b956f645b2b0b5f9c502a20e9ffcfd8")
    version("0.4.8", sha256="acccd56b736942dfcc490d102d2cb2b6afa6b2e448dd1dc5a1b773eadb98f83d")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("openssl")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap")
