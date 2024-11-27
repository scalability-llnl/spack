# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hevea(MakefilePackage):
    """Hevea a fast Latex to HTML translator"""

    homepage = "http://hevea.inria.fr/"
    url = "https://github.com/maranget/hevea/archive/v2.35.tar.gz"
    git = "https://github.com/maranget/hevea.git"

    maintainers("scemama", "cessenat")

    license("LGPL-2.0-only")

    version("develop", branch="master")
    version("2.35", sha256="78f834cc7a8112ec59d0b8acdfbed0c8ac7dbb85f964d0be1f4eed04f25cdf54")
    version("2.34", sha256="f505a2a5bafdc2ea389ec521876844e6fdcb5c1b656396b7e8421c1631469ea2")
    version("2.33", sha256="122f9023f9cfe8b41dd8965b7d9669df21bf41e419bcf5e9de5314f428380d0f")
    version("2.32", sha256="f0c12ee3936364a3aa26da384e3d2ad2344be0091f04f9531f04ecb1dca98aca")

    depends_on("c", type="build")  # generated

    # Dependency demands ocamlbuild
    depends_on("ocaml")
    depends_on("ocamlbuild")

    def edit(self, spec, prefix):
        env["PREFIX"] = self.spec.prefix
