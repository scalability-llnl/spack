# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Teckit(AutotoolsPackage):
    """TECkit is a low-level toolkit intended to be used by applications for
    conversions between text encodings. For example, it can be used when
    importing legacy text into a Unicode-based application.

    The primary component of TECkit is a library: the TECkit engine. The engine
    relies on mapping tables in a specific, documented binary format. The
    TECkit compiler creates these tables from plain-text, human-readable
    descriptions."""

    homepage = "https://scripts.sil.org/cms/scripts/page.php?cat_id=TECkit"
    url      = "https://github.com/silnrsi/teckit/releases/download/v2.5.9/teckit-2.5.9.tar.gz"

    version('2.5.9', sha256='6823fb3142efa34e5d74de35d37cdf4724efbf577f5ff15a8e2b364e6ef47d3d')

    depends_on('expat')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-system-zlib']
        return args
