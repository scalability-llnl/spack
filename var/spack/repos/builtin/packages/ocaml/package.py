# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ocaml(Package):
    """OCaml is an industrial strength programming language supporting
    functional, imperative and object-oriented styles"""

    homepage = "https://ocaml.org/"
    url = "https://caml.inria.fr/pub/distrib/ocaml-4.06/ocaml-4.06.0.tar.gz"

    maintainers("scemama")
    version("5.2.0", sha256="3a7b5fb6d81bb42bbda84aadf5d84ff8bcbb149988087e7863bf5c2f4b27b187")
    version("5.1.1", sha256="33b8c1df88700ba1f5123aa4bdbc7a125482feafc77e5081ef1725fddf290be1")
    version("5.1.0", sha256="5e91492d87b193728a0729122b679039c73e75820dcf2724a31b262390d210c2")
    version("5.0.0", sha256="969e1f7939736d39f2af533cd12cc64b05f060dbed087d7b760ee2503bfe56de")
    version("4.13.1", sha256="66a5353c5e7b33a8981446e857657aad45a3b82080ea5c67d4baa434eacfcf5f")
    version("4.12.0", sha256="9825e5903b852a7a5edb71a1ed68f5d5d55d6417e2dda514dda602bc6efeed7b")
    version("4.11.0", sha256="b5bd04bf794a676389b167633f01f8275acdd853149b137f7575f2c2ddef1377")
    version("4.10.0", sha256="58d431dde66f5750ebe9b15d5a1c4872f80d283dec23448689b0d1a498b7e4c7")
    version("4.09.0", sha256="2b728f8a0e90da14f22fdc04660f2ab33819cdbb12bff0ceae3fdbb0133cf7a6")
    version("4.08.1", sha256="ee50118ee88472fd4b64311fa560f8f8ab66a1899f0117815c69a16070980f78")
    version("4.08.0", sha256="e6e244f893f2070ebcdeac0637fbe2054fd82deebefefa3e3ed85a405cd4ecd8")
    version("4.07.1", sha256="2ad43be17ed5c74ea27887ae0cc4793b835408180c0b9175bc9ad53082a59af4")
    version("4.07.0", sha256="50e10b0c4e28300cb889e56839ec9e07e2847a85e04bfbd5a7ed0290b7239ef8")
    version("4.06.1", sha256="0c38c6f531103e87fab1c218a7e76287d7cb4d7ee4dea64e7f85952af3b1b50e")
    version("4.06.0", sha256="c17578e243c4b889fe53a104d8927eb8749c7be2e6b622db8b3c7b386723bf50")
    version("4.03.0", sha256="7fdf280cc6c0a2de4fc9891d0bf4633ea417046ece619f011fd44540fcfc8da2")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("fix-duplicate-defs.patch", when="@4.08.0:4.09.0 %gcc@10.0:")
    # #9969, #9981: Added mergeable flag to ELF sections containing mergeable
    # constants.  Fixes compatibility with the integrated assembler in clang 11.0.0.
    # (Jacob Young, review by Nicolas Ojeda Bar)
    patch(
        "https://github.com/ocaml/ocaml/pull/9981.patch?full_index=1",
        sha256="12700c697f0d5227e8eddd62e4308ec3cd67c0a5a5a1b7eec376686a5fd63a5c",
        when="@:4.11.0 %clang@11:",
    )
    depends_on("ncurses")

    sanity_check_file = ["bin/ocaml"]

    variant("force-safe-string", default=True, description="Enforce safe (immutable) strings")

    def url_for_version(self, version):
        url = "https://caml.inria.fr/pub/distrib/ocaml-{0}/ocaml-{1}.tar.gz"
        return url.format(str(version)[:-2], version)

    def install(self, spec, prefix):
        base_args = ["-prefix", "{0}".format(prefix)]

        if self.spec.satisfies("~force-safe-string"):
            base_args += ["--disable-force-safe-string"]

        # This patch is aarch64-linux-fj only.
        # However, similar patch is needed for other arch/OS/compiler
        # to use correct assembler. (See #17918)
        if self.spec.satisfies("%fj"):
            filter_file(
                'aspp="${toolpref}clang -c -Wno-trigraphs"',
                'aspp="{0} -c"'.format(spack_cc),
                "configure",
                string=True,
            )
            if self.spec.satisfies("@4.11.0:"):
                filter_file(
                    'as="${toolpref}clang -c -Wno-trigraphs"',
                    'as="${toolpref}as"',
                    "configure",
                    string=True,
                )

        configure(*(base_args), f"CC={self.compiler.cc}")

        make("world.opt")
        make("install", "PREFIX={0}".format(prefix))
