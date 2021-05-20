# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Motif(AutotoolsPackage):
    """"
    Motif - Graphical user interface (GUI)
    specification and the widget toolkit
    """
    force_autoreconf = True

    homepage = "http://motif.ics.com/"
    url = "http://cfhcable.dl.sourceforge.net/project/motif/Motif%202.3.8%20Source%20Code/motif-2.3.8.tar.gz"

    version('2.3.8', sha256='859b723666eeac7df018209d66045c9853b50b4218cecadb794e2359619ebce7')

    depends_on("flex")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("libxft")
    depends_on("libxcomposite")
    depends_on("libxfixes")
    depends_on("xbitmaps")
    depends_on("jpeg")

    # we need the following for autoreconf
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")

    patch('add_xbitmaps_dependency.patch')

    # Solve "implicit declaration of function is invalid in C99 error" with apple-clang:
    def setup_build_environment(self, spack_env):
        if spec.satisfies('%apple-clang'):
            spack_env.set('CFLAGS', '-Wno-implicit-function-declaration')

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        with working_dir(self.configure_directory):
            autoreconf('-ivf')
