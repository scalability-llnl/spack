# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Activeharmony(MakefilePackage):
    """Active Harmony: a framework for auto-tuning (the automated search for
    values to improve the performance of a target application)."""

    homepage = "http://www.dyninst.org/harmony"
    url      = "http://www.dyninst.org/sites/default/files/downloads/harmony/ah-4.5.tar.gz"

    version('4.6.0', sha256='9ce5009cfd8e2f4cf5f3536e1fea9993414fc25920fc90d0a2cb56f044787dbb')
    version('4.5',   sha256='31d9990c8dd36724d336707d260aa4d976e11eaa899c4c7cc11f80a56cdac684')

    patch('fix_logical_bug_in_slave_list_parsing.patch', sha256='3e000616f84de80b262efcae7559d65eed0efcd53e915580dab63b0ffbbb8bf2', when='@4.6.0')

    cflags = ['-O3', '-fPIC']

    def setup_build_environment(self, spack_env):
        spack_env.set('CFLAGS', ' '.join(self.cflags))

    @when('@:4.5')
    def install(self, spec, prefix):
        make("install", 'PREFIX=%s' % prefix)

    @when('@4.6.0:')
    def install(self, spec, prefix):
        make("install")
        install_tree("./bin", prefix.bin)
        install("./src/harmony.cfg", prefix.bin)
        install_tree("./lib", prefix.lib)
        install_tree("./libexec", prefix.libexec)
        install_tree("./include", prefix.include)
        install_tree("./doc", prefix.doc)
