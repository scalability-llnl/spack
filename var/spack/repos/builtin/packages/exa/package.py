# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exa(CargoPackage):
    """DEPRECATED: The exa upstream is no longer maintained, see the eza package for a
    replacement.

    exa is a replacement for ls written in Rust."""

    homepage = "https://the.exa.website"
    url = "https://github.com/ogham/exa/archive/v0.9.0.tar.gz"

    version(
        "0.10.1",
        sha256="ff0fa0bfc4edef8bdbbb3cabe6fdbd5481a71abbbcc2159f402dea515353ae7c",
        deprecated=True,
    )
    version(
        "0.9.0",
        sha256="96e743ffac0512a278de9ca3277183536ee8b691a46ff200ec27e28108fef783",
        deprecated=True,
    )
