# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Docui(GoPackage):
    """docui is a TUI Client for Docker."""

    homepage = "https://github.com/skanehira/docui"
    url      = "https://github.com/skanehira/docui/archive/2.0.4.tar.gz"

    version('2.0.4', sha256='9af1a720aa7c68bea4469f1d7eea81ccb68e15a47ccfc9c83011a06d696ad30d')

    depends_on('go@1.13:', type='build')  # go.mod value overrides default

    import_resources("resources-2.0.4.json")

    executables = ['docui']
