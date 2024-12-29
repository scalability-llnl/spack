# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Cbindgen(CargoPackage):
    """A project for generating C bindings from Rust code."""

    homepage = "https://github.com/mozilla/cbindgen"
    url = "https://github.com/mozilla/cbindgen/archive/refs/tags/v0.26.0.tar.gz"

    license("MPL", checked_by="teaguesterling")

    version("0.26.0", sha256="b45e1a64875b615702a86ac3084ef69ae32926241cd2b687a30c12474be15105")
    version("0.25.0", sha256="363ac6317a5788de8f2b0104a472a747883d4b9126fa119c681879509dbdbc28")
    version("0.24.3", sha256="5d693ab54acc085b9f2dbafbcf0a1f089737f7e0cb1686fa338c2aaa05dc7705")
    version("0.24.2", sha256="87ec3c355d08107b72c7b330c54aa2531eac0db754659a98bd58a93516ec9d4c")
    version("0.24.1", sha256="7a7098a7659e8dd166e170ebaf3dcd0a8a30119ef230100ff66041a6b4fc76ba")
    version("0.24.0", sha256="5cbbf8195b3e5bcee6044697b07b54e7701f047e40d7c86190be385736734cd7")
    version("0.23.0", sha256="d7b82a7a4bfe7fc61c6f7c1b848bf586fef4057c84960739484b4f743bf0bab6")
    version("0.22.0", sha256="f129b453df9d84e6d098a446f928961241b2a0edc29f827addca154049dcc434")
    version("0.21.0", sha256="c254a68039a85fe17c63781e67d09b0bfabc32446615d7c63cd805052ac5b155")
    version("0.20.0", sha256="70f810d2b9e5a2db570431872c26377813fb27a63d817cb16b2d69fa3741d066")

    depends_on("rust@1.70:")

    depends_on("rust-clap@4.3:")

    # The following dependencies need more work for spack but are handled by Cargo
    # They are included for reference and as a TODO once the Cargo packaging system
    # improves its support for more complex packages.
    # depends_on("rust-heck@0.4:")
    # depends_on("rust-toml@0.8.8:")
    # depends_on("rust-log@0.4:")
    # depends_on("rust-serde@1.0.103+derive")
    # depends_on("rust-serde-json@1.0:")
    # depends_on("rust-proc-macro2@1.0.60")
    # depends_on("rust-indexmap@2.1.0:")
