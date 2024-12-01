# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtomlc99(Package):
    """TOML in c99; v0.4.0 compliant."""

    homepage = "https://github.com/cktan/tomlc99"
    git = "https://github.com/cktan/tomlc99.git"

    license("MIT")

    # Since there is no official versioning, yet, just use the date and prefix
    # with '0.' to make switching to proper versioning easier later.
    version("0.2020.12.23", commit="e97a56633e54297990158ab56a7e50a089cddf7d")
    version("0.2019.06.24", commit="b701a09579200b1bd87081d1e6a284a89b5576c8")
    # Unfortunately, upstream Makefile does not build shared libaries, so use
    # local changes for now.
    version(
        "0.2019.05.02",
        commit="35118431263dec2a2a7b55e4dd717a5f54992e3e",
        git="https://github.com/obreitwi/tomlc99.git",
    )
    # Does not build shared libraries.
    version("0.2019.03.06", commit="bd76f1276ee5f5df0eb064f1842af5ad1737cf1e")

    depends_on("c", type="build")  # generated

    variant("debug", default=False, description="Build with debug enabled.")

    def install(self, spec, prefix):
        make_args = []
        if spec.satisfies("+debug"):
            make_args.append("DEBUG=1")

        make(*make_args)
        make("prefix={0}".format(prefix), "install")
