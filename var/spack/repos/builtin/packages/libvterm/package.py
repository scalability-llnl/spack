# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libvterm(Package):
    """An abstract library implementation of a terminal emulator"""
    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url      = "http://www.leonerd.org.uk/code/libvterm/libvterm-0.1.3.tar.gz"

    version('0.1.4', sha256='bc70349e95559c667672fc8c55b9527d9db9ada0fb80a3beda533418d782d3dd')
    version('0.1.3', sha256='e41724466a4658e0f095e8fc5aeae26026c0726dce98ee71d6920d06f7d78e2b')
    version('0.0.0', sha256='6344eca01c02e2270348b79e033c1e0957028dbcd76bc784e8106bea9ec3029d', url='http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr726.tar.gz')

    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
