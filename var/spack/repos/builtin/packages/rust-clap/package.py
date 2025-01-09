# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustClap(CargoPackage):
    """A full featured, fast Command Line Argument Parser for Rust"""

    homepage = "http://docs.rs/clap"
    url = "https://github.com/clap-rs/clap/archive/refs/tags/v4.5.10.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("4.5.10", sha256="854c345f8e1af7067edd4777b5862843f1018b3037658d890619f89678cbc033")
    version("4.5.9", sha256="8e0de093cd01b8a5be700ea807e937b36c54598a1902004ed64e0635a84c8f69")
    version("4.5.8", sha256="9a00964ac907c1d5c0a87ab950ea9b4eec0fec0f5a73d2f5491570d5a9607823")
    version("4.5.7", sha256="206001eda043fd7ba4167874ccd069387cfb98f7935cef44e77219c31e8e9ad6")
    version("4.5.6", sha256="88763b098a791af71534ccf8e92bcf0b8c591bb0d2f36adabbad272906e79aca")
    version("4.5.4", sha256="7023c210ff45a773b588448a803d05bf543cce6e28696967b7f16c0490faaec4")
    version("4.5.3", sha256="01b966f804aba86acfd06ecd3f248c6e523227a157a790f6649a20338b0f2109")
    version("4.5.2", sha256="10962660f531b5a1bbd4c7c8e96fdf4aef0ecbc8ad64ca3d9995b6e59ced765f")
    version("4.5.1", sha256="f3cc654960dc16bf3212d7964e1033c1e4339acbd3ddb1b153ae731b7a9609e7")
    version("4.5.0", sha256="c501afbe05a20d86c62206a66cc3c5e0d39e11bc10b000436a2166fc99a56e65")
