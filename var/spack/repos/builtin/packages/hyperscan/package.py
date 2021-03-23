# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost
import platform

_versions = {
    'v5.2.1': {
        'Linux-aarch64': ('d2ac1669154ec27b794b64d026ad09caecee6e5e17fd35107595a7517711d2b9', 'https://github.com/kunpengcompute/hyperscan/archive/v5.2.1.aarch64.tar.gz'),
        'Linux-x86_64': ('fd879e4ee5ecdd125e3a79ef040886978ae8f1203832d5a3f050c48f17eec867', 'https://github.com/intel/hyperscan/archive/v5.2.1.tar.gz')
    }
}


class Hyperscan(CMakePackage):
    """High-performance regular expression matching library."""

    homepage = "https://www.hyperscan.io/"
    url      = "https://github.com/intel/hyperscan/archive/v5.2.1.tar.gz"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('pcre')
    depends_on('ragel', type='build')
