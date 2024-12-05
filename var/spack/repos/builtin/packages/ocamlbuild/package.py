# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ocamlbuild(MakefilePackage):
    """OCamlbuild is a generic build tool,
    that has built-in rules for building OCaml library and programs."""

    # Add a proper url for your package's homepage here.
    homepage = "https://ocaml.org/learn/tutorials/ocamlbuild/"
    url = "https://github.com/ocaml/ocamlbuild/archive/0.14.0.tar.gz"
    git = "https://github.com/ocaml/ocamlbuild/ocamlbuild.git"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("scemama", "cessenat")

    # Add proper versions here.
    version("master", branch="master")
    version("0.14.0", sha256="87b29ce96958096c0a1a8eeafeb6268077b2d11e1bf2b3de0f5ebc9cf8d42e78")
    version("0.13.1", sha256="79839544bcaebc8f9f0d73d029e2b67e2c898bba046c559ea53de81ea763408c")

    # Add dependencies if required.
    depends_on("ocaml")

    # Installation : https://github.com/ocaml/ocamlbuild/
    def edit(self, spec, prefix):
        makefile_inc = ["BINDIR       = bin", "LIBDIR       = lib", "MANDIR       = man"]
        makefile_inc.append("OCAML_PREFIX       = %s" % self.spec["ocaml"].prefix)
        makefile_inc.append("DESTDIR       = %s/" % self.spec.prefix)
        with open("Makefile.config", "a") as fh:
            fh.write("\n".join(makefile_inc))
        make("configure")
