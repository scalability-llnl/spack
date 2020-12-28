# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Workrave(AutotoolsPackage):
    """Workrave is a program that assists in the recovery and prevention of
       Repetitive Strain Injury (RSI). The program frequently alerts you to
       take micro-pauses, rest breaks and restricts you to your daily limit.
       The program runs on GNU/Linux and Microsoft Windows.
    """

    homepage = "http://www.workrave.org/"
    url      = "https://github.com/rcaelers/workrave/archive/v1_10_20.tar.gz"

    version('1_10_20', sha256='a89c6e82d5bbbaae5e171100b87c4efd8316ab8a18d82b83714035e1116983ec')
    version('1_10_19', sha256='3a24d87e22fc9f463b6a9319843751038cbf6acfab9cd67893221a0071cf5405')
    version('1_10_18', sha256='f0de5abd2c3a29106b915f1c051808f6083e1052b46c5143ff96e2334757e91b')
    version('1_10_17', sha256='d911fd4738b6b4737cc2fc54c1683eb5d290f2764398c432fcc3b61bb326e71a')
    version('1_10_16', sha256='4368306db0d06e76a3a90fc8e81b3648c1218259833b01cdc6899b1e98e5895c')
    version('1_10_15', sha256='fa05bedbb32baae9d22ef2b1ac25e90bc9f1363ce588b396190b0240559f471c')
    version('1_10_14', sha256='de342be4ff131645ff29fe003b476816965a65a44f4ddc85109960502d9e7310')
    version('1_10_13', sha256='cbb5dab1073d2715e5b9cb8ccf8b3362ab6fa8ab05aa44629ecc78d6b93769e3')
    version('1_10_12', sha256='eb7a4b7ba137e6997d7b44ed38b705daf391e9c646a5a068c9b002830f35be47')
    version('1_10_10', sha256='84f9dca7634e291631017053a63ac20cd23c4da8c8f09ca4beef6f1419d904e3')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('libx11')
    depends_on('py-cheetah')
    depends_on('glib')
    depends_on('glibmm')
    depends_on('gtkplus')
    depends_on('gtkmm@2.17.1')
    depends_on('libsigcpp')

    # adds #include <time.h> to a workrave test
    patch('add_time_header.patch')

    # removes call to missing gtkmm api function
    patch('dont_get_widget.patch')

    # removes gettext which canot be use with intltool
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=724555
    # https://bugzilla.gnome.org/show_bug.cgi?id=708673#c4
    patch('no_gettext.patch')

    # add a couple m4 macros used during autoreconf
    # https://github.com/rcaelers/workrave/issues/95
    m4files = ['ax_cxx_compile_stdcxx_11', 'ax_cxx_compile_stdcxx']
    resource(name=m4files[0],
             url='http://git.savannah.gnu.org/gitweb/?p=autoconf-archive.git;a=blob_plain;f=m4/ax_cxx_compile_stdcxx_11.m4',
             sha256='d75fc9fe4502eea02e8c5bfb61b88a04cd08aa6d5bd757fe66e9a9a1e4781b46',
             expand=False,
             destination='',
             placement=m4files[0])
    resource(name=m4files[1],
             url='http://git.savannah.gnu.org/gitweb/?p=autoconf-archive.git;a=blob_plain;f=m4/ax_cxx_compile_stdcxx.m4',
             sha256='0c08d2f64147f65eb7e255019102c1042ab695c60fd49add19793951a1279a1a',
             expand=False,
             destination='',
             placement=m4files[1])

    def setup_build_environment(self, env):
        # unset PYTHONHOME to let system python script with explict
        # system python sbangs like glib-mkenums work, see #6968
        # Without this, we will get
        # ImportError: No module named site
        # during build phase when make runs glib-mkenums
        env.unset('PYTHONHOME')

    @run_before('autoreconf')
    def extra_m4(self):
        # move m4 macros, which we added with the resource() directive,
        # to the m4 directory, where aclocal will pick them up
        for fname in self.m4files:
            src = '%s/%s/%s.m4' % (self.stage.source_path, fname, fname)
            dest = '%s/m4/%s.m4' % (self.stage.source_path, fname)
            copy(src, dest)
