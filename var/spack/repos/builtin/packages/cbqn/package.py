# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cbqn(MakefilePackage):
    """A BQN implementation in C"""

    # Alternative homepage not specific to this implementation:
    # https://mlochbaum.github.io/BQN/index.html
    homepage = "https://github.com/dzaima/CBQN"
    git = "https://github.com/dzaima/CBQN"

    maintainers("ashermancinelli")

    # Licenses listed in the order they appear in the repo's licensing section
    # https://github.com/dzaima/CBQN/tree/master#licensing
    license(
        "MIT AND Apache-2.0 AND BSL-1.0 AND LGPL-3.0-only AND GPL-3.0-only AND MPL-2.0",
        checked_by="ashermancinelli",
    )

    version("master", branch="master")
    version("develop", branch="develop")
    version("0.7.0", tag="v0.7.0")

    depends_on("c", type="build")

    variant("repl", default=True, description="Enable built-in REPL")
    variant("ffi", default=True, description="Enable FFI support")
    variant(
        "build_type",
        values=("o3n", "o3", "o3g", "c", "shared-o3", "debug", "static-bin", "static-lib"),
        default="o3",
        multi=False,
        description="Make target to use.",
    )

    depends_on("cxx", when="+repl", type="build")
    depends_on("libffi", when="+ffi")

    def build(self, spec, prefix):
        make_args = []
        make_args.append("FFI={0}".format(int(spec.satisfies("+ffi"))))
        make_args.append("REPLXX={0}".format(int(spec.satisfies("+repl"))))

        # Makes logs easier to read
        make_args.append("notui=1")

        # The build types map directly to the make target
        make_args.append(spec.variants["build_type"].value)

        if spec.version not in ("develop", "master"):
            make_args.append("version={0}".format(spec.version))

        make(*make_args)

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
