# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Libpeas(AutotoolsPackage):
    """libpeas is a gobject-based plugins engine, and is targeted at
    giving every application the chance to assume its own
    extensibility."""

    homepage = "http://developer.gnome.org/libpeas/stable"
    url = 'https://download.gnome.org/sources/libpeas/1.22/libpeas-1.22.0.tar.xz'

    version('1.22.0', sha256='5b2fc0f53962b25bca131a5ec0139e6fef8e254481b6e777975f7a1d2702a962')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('atk')
    depends_on('intltool@0.40.0:')
    depends_on('xmlto', type='build')
    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('glib@2.10:')
    depends_on('gobject-introspection')
    depends_on('libffi')
    depends_on('gtkplus')
    depends_on('gdk-pixbuf')
    depends_on('pango')
    depends_on('gnome-common')
    depends_on('py-pygobject@3:', type='build')
    depends_on('python@3:', type='build')

    def url_for_version(self, version):
        url  = 'https://download.gnome.org/sources/libpeas/'
        url += '{0}/libpeas-{1}.tar.xz'
        return url.format(version.up_to(2), version)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_build_environment(self, env):
        # Let
        #
        # python = self.spec['python']
        # prefix = python.prefix
        # pyversion = python.version.up_to(2)
        # python_lib_path = os.path.join(prefix, 'Frameworks',
        #                                'Python.framework', 'Versions',
        #                                pyversion)
        #
        # self.spec['python'].libs.ld_flags returns (on macOS)
        # '-L{0} -lPython'.format(python_lib_path)
        #
        # e.g., for python@3.7.4 on macOS via Homebrew, python_lib_path is
        # /usr/local/opt/python/Frameworks/Python.framework/Versions/3.7
        #
        # This directory is correct for many purposes, but libpeas uses the
        # link flag '-lpython{0}m'.format(pyversion) and does not use an
        # appropriate -L flag to locate this library, so the correct -L flag
        # must be appended to LDFLAGS. Furthermore, this library is not found
        # in python_lib_path.  However, pkg-config returns the correct
        # directory, so pkg-config is used to generate the correct paths for
        # LDFLAGS.
        pkg_config = which('pkg-config')
        python_prefix = self.spec['python'].prefix.lib.pkgconfig
        python_pc_file = os.path.join(python_prefix, 'python3.pc')
        python_ldflags = pkg_config('--libs', python_pc_file, output=str)

        env.append_path('LDFLAGS', python_ldflags)
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def autoreconf(self, spec, prefix):
        autoreconf_args = ['-ivf']
        aclocal_pkg_list = ['pkg-config',
                            'gettext',
                            'intltool',
                            'glib',
                            'gobject-introspection',
                            'gnome-common',
                            'gtkplus']
        aclocal_path = os.path.join('share', 'aclocal')

        for pkg in aclocal_pkg_list:
            autoreconf_args += ['-I',
                                os.path.join(spec[pkg].prefix, aclocal_path)]

        autoreconf = which('autoreconf')
        autoreconf(*autoreconf_args)

    def configure_args(self):
        args = ['--disable-silent-rules',
                '--enable-gtk',
                '--enable-python3',
                '--disable-python2']
        return args
