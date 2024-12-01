# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libpsml(AutotoolsPackage):
    """libPSML is a library to handle pseudopotentials in PSML format."""

    homepage = "https://gitlab.com/siesta-project/libraries/libpsml"
    git = "https://gitlab.com/siesta-project/libraries/libpsml.git"
    url = "https://gitlab.com/siesta-project/libraries/libpsml/-/archive/libpsml-1.1.10/libpsml-libpsml-1.1.10.tar.gz"

    license("BSD-3-Clause")

    version("1.1.10", sha256="ba87ece7d443a42a5db3a119c555a29a391a060dd6f3f5039a2c6ea248b7fe84")
    version("1.1.9", sha256="04b8de33c555ae94a790116cd3cf7b6c9e8ec9a018562edff544a2e04876cf0c")
    version("1.1.8", sha256="77498783be1bc7006819f36c42477b5913464b8c660203f7d6b7f7e25aa29145")
    version("1.1.7", sha256="b3f5431fd3965b66fe01b899c0c3ef73d9f969d67329cd1f5aba84fb056b5dd1")
    version("1.1.6", sha256="521647dbd945b208e5d468fceeb2bc397737d9a659e2c7549597bf4eb29f60df")

    depends_on("fortran", type="build")  # generated

    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4.2:", type="build")
    depends_on("m4", type="build")
    depends_on("xmlf90")

    def configure_args(self):
        return ["--with-xmlf90=%s" % self.spec["xmlf90"].prefix]
