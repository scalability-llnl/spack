# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UrlOverride(Package):
    homepage = 'http://www.doesnotexist.org'
    url      = 'http://www.doesnotexist.org/url_override-1.0.0.tar.gz'

    version('1.0.0', 'cxyzab')
    version('0.9.0', 'bcxyza', url='http://www.anothersite.org/uo-0.9.0.tgz')
    version('0.8.1', 'cxyzab')
