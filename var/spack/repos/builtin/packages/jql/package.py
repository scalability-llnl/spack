# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jql(CargoPackage):
    """A JSON Query Language CLI tool built with Rust"""

    homepage = "https://github.com/yamafaktory/jql"
    crates_io = "jql"
    git = "https://github.com/yamafaktory/jql.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('2.7.2', sha256='dd14894364600cc6667801b01ad93eb665610e9de81fc64734de074ab1f1b2e5')

    # jql doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )
