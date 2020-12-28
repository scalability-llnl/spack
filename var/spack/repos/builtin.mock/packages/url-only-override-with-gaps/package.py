# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UrlOnlyOverrideWithGaps(Package):
    homepage = 'http://www.example.com'

    version('1.0.5', 'abcdef0')
    version('1.0.0', 'bcdef0a', url='http://a.example.com/url_override-1.0.0.tar.gz')
    version('0.9.5', 'cdef0ab')
    version('0.9.0', 'def0abc', url='http://b.example.com/url_override-0.9.0.tar.gz')
    version('0.8.5', 'ef0abcd')
    version('0.8.1', 'f0abcde', url='http://c.example.com/url_override-0.8.1.tar.gz')
    version('0.7.0', '0abcdef')
