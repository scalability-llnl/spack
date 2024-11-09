# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Random123(Package):
    """Random123 is a library of 'counter-based' random number
    generators (CBRNGs), in which the Nth random number can be obtained
    by applying a stateless mixing function to N instead of the
    conventional approach of using N iterations of a stateful
    transformation."""

    homepage = "https://www.deshawresearch.com/resources_random123.html"
    url = "https://github.com/DEShawResearch/random123/archive/refs/tags/v1.14.0.tar.gz"

    maintainers("KineticTheory")

    version("1.14.0", sha256="effafd8656b18030b2a5b995cd3650c51a7c45052e6e1c21e48b9fa7a59d926e")
    version(
        "1.13.2",
        sha256="74a1c6bb66b2684f03d3b1008642a2e9141909103cd09f428d2c60bcaa51cb40",
        url="https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.13.2.tar.gz",
    )
    version(
        "1.10",
        sha256="4afdfba4b941e33e23b5de9b7907b7e3ac326cb4d34b5fa8225edd00b5fe053b",
        url="https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.10.tar.gz",
    )
    version(
        "1.09",
        sha256="cf6abf623061bcf3d17e5e49bf3f3f0ae400ee89ae2e97c8cb8dcb918b1ebabe",
        url="https://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.09.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("ibmxl.patch", when="@1.09")
    patch("arm-gcc.patch", when="@1.09")
    patch("v1132-xl161.patch", when="@1.13.2")
    patch("v1140-hip.patch", when="@1.14.0")

    def install(self, spec, prefix):
        # Random123 doesn't have a build system.
        # We have to do our own install here.
        install_tree("include", prefix.include)
        install("./LICENSE", "%s" % prefix)
        if spec.satisfies("@1.09"):
            # used by some packages, e.g. quinoa
            install("examples/uniform.hpp", join_path(prefix.include, "Random123"))
