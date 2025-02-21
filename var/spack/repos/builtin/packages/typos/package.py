# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Typos(CargoPackage):
    """Source code spell checker."""

    homepage = "https://github.com/crate-ci/typos"
    url = "https://github.com/crate-ci/typos/archive/refs/tags/v1.28.4.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0 OR MIT", checked_by="alecbcs")

    version("1.28.4", sha256="acfbaf16d61fb35532ddb91a32e720181450487f60fe60757f72c3879496955d")

    build_directory = "crates/typos-cli"
