# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UrlOnlyOverride(Package):
    homepage = 'http://www.example.com'

    version('1.0.0', 'cxyzab', url='http://a.example.com/url_override-1.0.0.tar.gz')
    version('0.9.0', 'bcxyza', url='http://b.example.com/url_override-0.9.0.tar.gz')
    version('0.8.1', 'cxyzab', url='http://c.example.com/url_override-0.8.1.tar.gz')
