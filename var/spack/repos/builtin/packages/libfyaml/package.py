# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfyaml(AutotoolsPackage):
    """Fully feature complete YAML parser and emitter, supporting the latest
    YAML spec and passing the full YAML testsuite."""

    homepage = "https://github.com/pantoniou/libfyaml"
    url = "https://github.com/pantoniou/libfyaml/releases/download/v0.5.7/libfyaml-0.5.7.tar.gz"

    license("MIT")

    version("0.9", sha256="7731edc5dfcc345d5c5c9f6ce597133991a689dabede393cd77bae89b327cd6d")
    version("0.8", sha256="dc4d4348eedca68e8e2394556d57f71410e7d61791a71cbe178302ebe5f26b99")
    version("0.7.12", sha256="485342c6920e9fdc2addfe75e5c3e0381793f18b339ab7393c1b6edf78bf8ca8")
    version("0.5.7", sha256="3221f31bb3feba97e544a82d0d5e4711ff0e4101cca63923dc5a1a001c187590")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
