# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class OldExternal(Package):
    """A package that has an old version declared in packages.yaml"""

    homepage = "https://www.example.com"
    url = "https://www.example.com/old-external.tar.gz"

    version('1.2.0', '0123456789abcdef0123456789abcdef')
    version('1.1.4', '0123456789abcdef0123456789abcdef')
    version('1.1.3', '0123456789abcdef0123456789abcdef')
    version('1.1.2', '0123456789abcdef0123456789abcdef')
    version('1.1.1', '0123456789abcdef0123456789abcdef')
    version('1.1.0', '0123456789abcdef0123456789abcdef')
    version('1.0.0', '0123456789abcdef0123456789abcdef')
