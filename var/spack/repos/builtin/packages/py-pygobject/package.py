# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygobject(PythonPackage):
    """bindings for the GLib, and GObject,
       to be used in Python."""

    homepage = "https://pypi.python.org/pypi/pygobject"

    version('3.38.0', sha256='0372d1bb9122fc19f500a249b1f38c2bb67485000f5887497b4b205b3e7084d5')
    version('3.28.3', sha256='3dd3e21015d06e00482ea665fc1733b77e754a6ab656a5db5d7f7bfaf31ad0b0')
    version('2.28.6', sha256='fb8a1d4f665130a125011659bd347c7339c944232163dbb9a34fd0686577adb8')
    version('2.28.3', sha256='7da88c169a56efccc516cebd9237da3fe518a343095a664607b368fe21df95b6',
            url='http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.3.tar.bz2')

    extends('python')

    depends_on('py-setuptools', type='build')
    depends_on('pkgconfig', type='build')
    depends_on("libffi")
    depends_on('glib')
    depends_on('python@2:2.99', when='@2:2.99', type=('build', 'run'))
    depends_on('py-pycairo', type=('build', 'run'), when='@3:')
    depends_on('py-py2cairo', type=('build', 'run'), when='@2:2.99')
    depends_on('gobject-introspection')
    depends_on('gtkplus', when='@3:')

    patch('pygobject-2.28.6-introspection-1.patch', when='@2.28.3:2.28.6')

    # patch from https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/python-modules/pygobject/pygobject-2.28.6-gio-types-2.32.patch
    # for https://bugzilla.gnome.org/show_bug.cgi?id=668522
    patch('pygobject-2.28.6-gio-types-2.32.patch', when='@2.28.6')

    # pygobject links directly using the compiler, not spack's wrapper.
    # This causes it to fail to add the appropriate rpaths. This patch modifies
    # pygobject's setup.py file to add -Wl,-rpath arguments for dependent
    # libraries found with pkg-config.
    patch('pygobject-3.28.3-setup-py.patch', when='@3.28.3')

    def url_for_version(self, version):
        url = 'http://ftp.gnome.org/pub/GNOME/sources/pygobject'
        return url + '/%s/pygobject-%s.tar.xz' % (version.up_to(2), version)

    # pygobject version 2 requires an autotools build
    @when('@2:2.99')
    def build(self, spec, prefix):
        configure('--prefix=%s' % spec.prefix)

    @when('@2:2.99')
    def install(self, spec, prefix):
        make('install', parallel=False)

    @when('^python@3:')
    def patch(self):
        filter_file(
            r'Pycairo_IMPORT',
            r'//Pycairo_IMPORT',
            'gi/pygi-foreign-cairo.c')
