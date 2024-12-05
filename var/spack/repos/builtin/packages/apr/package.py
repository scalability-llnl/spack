# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Apr(AutotoolsPackage):
    """Apache portable runtime."""

    homepage = "https://apr.apache.org/"
    url = "https://archive.apache.org/dist/apr/apr-1.7.0.tar.gz"

    license("Apache-2.0", checked_by="wdconinc")

    version("1.7.5", sha256="3375fa365d67bcf945e52b52cba07abea57ef530f40b281ffbe977a9251361db")

    # https://nvd.nist.gov/vuln/detail/CVE-2023-49582
    with default_args(deprecated=True):
        version("1.7.4", sha256="a4137dd82a185076fa50ba54232d920a17c6469c30b0876569e1c2a05ff311d9")
        version("1.7.3", sha256="af9bfd5b8a04425d6b419673f3e0a7656fade226aae78180d93f8a6f2d3d1c09")
        version("1.7.2", sha256="3d8999b216f7b6235343a4e3d456ce9379aa9a380ffb308512f133f0c5eb2db9")
        version("1.7.0", sha256="48e9dbf45ae3fdc7b491259ffb6ccf7d63049ffacbc1c0977cced095e4c2d5a2")
        version("1.6.2", sha256="4fc24506c968c5faf57614f5d0aebe0e9d0b90afa47a883e1a1ca94f15f4a42e")
        version("1.5.2", sha256="1af06e1720a58851d90694a984af18355b65bb0d047be03ec7d659c746d6dbdb")

    depends_on("c", type="build")

    patch("missing_includes.patch", when="@1.7.0")

    depends_on("uuid", type="link")

    @property
    def libs(self):
        return find_libraries(
            [f"libapr-{self.version.up_to(1)}"], root=self.prefix, recursive=True
        )
