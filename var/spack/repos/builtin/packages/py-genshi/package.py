# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenshi(PythonPackage):
    """Python toolkit for generation of output for the web"""
    homepage = "https://genshi.edgewall.org/"
    url      = "http://ftp.edgewall.com/pub/genshi/Genshi-0.7.tar.gz"

    version('0.7', sha256='1d154402e68bc444a55bcac101f96cb4e59373100cc7a2da07fbf3e5cc5d7352')
    version('0.6.1', sha256='fed947f11dbcb6792bb7161701ec3b9804055ad68c8af0ab4f0f9b25e9a18dbd')
    version('0.6', sha256='32aaf76a03f88efa04143bf80700399e6d84eead818fdd19d763fd76af972a4b')

    depends_on("py-setuptools", type='build')
