# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastjson(MavenPackage):
    """Fastjson is a Java library that can be used to convert Java Objects
    into their JSON representation. It can also be used to convert a JSON
    string to an equivalent Java object."""

    homepage = "https://github.com/alibaba/fastjson/wiki"
    url = "https://github.com/alibaba/fastjson2/archive/2.0.52.tar.gz"

    license("Apache-2.0", checked_by="wdconinc")

    version("2.0.52", sha256="23c84854da465d8cff4e252bf20ef4b82cf2c7bc57944b9a316fd31a8977d2a1")
    version("1.2.83", sha256="82fffe7859b1b6630f9a5e9b11c3cc5d043ba91f578d30cd1a60afa369ad448b")
    version("1.2.68", sha256="0b3f5308830e5e5abacf9dc8e4115c20153c1cdabec228c3eca48a48c9d5f4d7")

    depends_on("java@8", type=("build", "run"))

    def url_for_version(self, version):
        if version < Version("2"):
            return f"https://github.com/alibaba/fastjson/archive/{version}.tar.gz"
        else:
            return f"https://github.com/alibaba/fastjson2/archive/{version}.tar.gz"
