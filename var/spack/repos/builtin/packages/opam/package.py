# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opam(AutotoolsPackage):
    """OPAM: OCaml Package Manager

    OPAM is a source-based package manager for OCaml. It supports
    multiple simultaneous compiler installations, flexible package
    constraints, and a Git-friendly development workflow."""

    homepage = "https://opam.ocaml.org/"
    url = "https://github.com/ocaml/opam/releases/download/1.2.2/opam-full-1.2.2.tar.gz"

    maintainers("scemama")

    version("2.2.1", sha256="07ad3887f61e0bc61a0923faae16fcc141285ece5b248a9e2cd4f902523cc121")
    version("2.2.0", sha256="39334f36adbe280683487cf204b7b0642080fc5965747f7d6f7cc7b83cd7a192")
    version("2.1.6", sha256="d2af5edc85f552e0cf5ec0ddcc949d94f2dc550dc5df595174a06a4eaf8af628")
    version("2.1.5", sha256="09f8d9e410b2f5723c2bfedbf7970e3b305f5017895fcd91759f05e753ddcea5")
    version("2.1.4", sha256="1643609f4eea758eb899dc8df57b88438e525d91592056f135e6e045d0d916cb")
    version("2.1.3", sha256="cb2ab00661566178318939918085aa4b5c35c727df83751fd92d114fdd2fa001")
    version("2.0.6", sha256="7c4bff5e5f3628ad00c53ee1b044ced8128ffdcfbb7582f8773fb433e12e07f4")
    version("2.0.5", sha256="776c7e64d6e24c2ef1efd1e6a71d36e007645efae94eaf860c05c1929effc76f")
    version("2.0.4", sha256="debfb828b400fb511ca290f1bfc928db91cad74ec1ccbddcfdbfeff26f7099e5")
    version("2.0.3", sha256="0589da4da184584a5445d59385009536534f60bc0e27772245b2f49e5fa8f0e2")
    version("2.0.2", sha256="eeb99fdda4b10ad3467a700fa4d1dfedb30714837d18d2faf1ef9c87d94cf0bc")
    version("2.0.1", sha256="81f7f1b661a0c1e04642fe02d0bea5524b32aa2cbed0ecf9b18d7145324ed97c")
    version("2.0.0", sha256="9dad4fcb4f53878c9daa6285d8456ccc671e21bfa71544d1f926fb8a63bfed25")
    version("1.2.2", sha256="15e617179251041f4bf3910257bbb8398db987d863dd3cfc288bdd958de58f00")
    version("1.2.1", sha256="f210ece7a2def34b486c9ccfb75de8febd64487b2ea4a14a7fa0358f37eacc3b")

    depends_on("c", type="build")  # generated

    # OCaml 4.10.0 has removed the -safe-string flag, which is necessary
    # for OPAM 1i (see docstring of setup_build_environment).
    depends_on("ocaml@:4.09.0", type="build", when="@:1.2.2")
    depends_on("ocaml", type="build", when="@2.0.0:")

    # While this package is a makefile package, 'make' is really only used to
    # call the locally built copy of dune, which is itself parallel, so there's
    # no sense in calling make with >1 job.
    # See: ocaml/opam#3585 spack/spack#46535
    parallel = False

    sanity_check_is_file = ["bin/opam"]

    @property
    def build_directory(self):
        return self.stage.source_path

    @when("@:1.2.2")
    def setup_build_environment(self, env):
        """In OCaml <4.06.1, the default was -safe-string=0, and this has
        changed in OCaml >=4.06.1. OPAM version 1 was written before 4.06.1
        was released, so OPAM <2.0 assumes mutable strings and requires the
        safe-string=0 flag. This is not true with OPAM >=2.0, so the flag
        should not be set."""

        # Environment variable setting taken from
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/opam.rb
        env.set("OCAMLPARAM", "safe-string=0,_")  # OCaml 4.06.0 compat

    def configure(self, spec, prefix):
        args = ["--prefix={0}".format(prefix)]

        with when("@:2.2"):
            # NOTE: The config script really wants the vendored third party
            # libraries to live in the <source prefix>/src_ext directory, not
            # in the build directory when this flag is enabled. This is why the
            # build directory must be set to the source path above.
            args.append("--with-vendored-deps")

        return configure(*args)

    def build(self, spec, prefix):
        # https://github.com/dbuenzli/cmdliner/issues/34#issuecomment-145236209
        if spec.satisfies("@:2.1"):
            make("lib-ext")

        make()

        if spec.satisfies("@:1.2.2"):
            make("man")

    def install(self, spec, prefix):
        make("install")
