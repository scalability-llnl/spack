# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jellyfish(AutotoolsPackage):
    """JELLYFISH is a tool for fast, memory-efficient counting of k-mers in DNA."""

    homepage = "https://www.cbcb.umd.edu/software/jellyfish/"
    url = "https://github.com/gmarcais/Jellyfish/releases/download/v2.3.0/jellyfish-2.3.0.tar.gz"
    list_url = "https://github.com/gmarcais/Jellyfish/releases"

    license("GPL-3.0-only")

    version("2.3.1", sha256="ee032b57257948ca0f0610883099267572c91a635eecbd88ae5d8974c2430fcd")
    version("2.3.0", sha256="e195b7cf7ba42a90e5e112c0ed27894cd7ac864476dc5fb45ab169f5b930ea5a")
    version(
        "2.2.7",
        sha256="d80420b4924aa0119353a5b704f923863abc802e94efeb531593147c13e631a8",
        preferred=True,
    )
    version(
        "1.1.11",
        sha256="496645d96b08ba35db1f856d857a159798c73cbc1eccb852ef1b253d1678c8e2",
        url="https://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("perl", when="@2.2.7:", type=("build", "run"))
    variant("ruby", default=False, description="Enable ruby bindings")
    # Info: python bindings exist, but are for python2 which is no longer supported in spack

    extends("ruby@:2.6", when="+ruby")

    patch("dna_codes.patch", when="@1.1.11")

    # v1.1.11 does not support language bindings
    conflicts("+ruby", when="@1.1.11")

    def configure_args(self):
        if "+ruby" in self.spec:
            return ["--enable-ruby-binding"]
        return []
