# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yq(GoPackage):
    """yq is a portable command-line YAML, JSON, XML, CSV, TOML and properties processor.
    This is different from the py-yq package that is a wrapper around jq."""

    homepage = "https://mikefarah.gitbook.io/yq"
    url = "https://github.com/mikefarah/yq/archive/refs/tags/v4.43.1.tar.gz"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version("4.44.3", sha256="ea950f5622480fc0ff3708c52589426a737cd4ec887a52922a74efa1be8f2fbf")
    version("4.43.1", sha256="e5581d28bae2bcdf70501dfd251233c592eb3e39a210956ee74965b784435d63")
    version("4.41.1", sha256="25d61e72887f57510f88d1a30d515c7e2d79e7c6dce5c96aea7c069fcbc089e7")
    version("4.40.7", sha256="c38024d40ee37d26caba1824965d9ea1d65468f48b2bacd45647ff4f547fa59f")
    version("4.35.2", sha256="8b17d710c56f764e9beff06d7a7b1c77d87c4ba4219ce4ce67e7ee29670f4f13")

    # from go.mod
    depends_on("go@1.21:", type="build", when="@4.40:")
    depends_on("go@1.20:", type="build", when="@4.31:")
