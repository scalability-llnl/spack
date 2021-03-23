# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfyaml(AutotoolsPackage):
    """Fully feature complete YAML parser and emitter, supporting the latest
    YAML spec and passing the full YAML testsuite."""

    homepage = "https://github.com/pantoniou/libfyaml"
    url      = "https://github.com/pantoniou/libfyaml/releases/download/v0.5.7/libfyaml-0.5.7.tar.gz"

    version('0.5.7', sha256='3221f31bb3feba97e544a82d0d5e4711ff0e4101cca63923dc5a1a001c187590')

    depends_on('m4', type='build')
