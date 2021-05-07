# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import spack.hooks.sbang as sbang


class GobjectIntrospection(Package):
    """The GObject Introspection is used to describe the program APIs and
    collect them in a uniform, machine readable format.Cairo is a 2D graphics
    library with support for multiple output"""

    homepage = "https://wiki.gnome.org/Projects/GObjectIntrospection"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gobject-introspection/1.49/gobject-introspection-1.49.2.tar.xz"

    version('1.56.1', sha256='5b2875ccff99ff7baab63a34b67f8c920def240e178ff50add809e267d9ea24b')
    version('1.49.2', sha256='73d59470ba1a546b293f54d023fd09cca03a951005745d86d586b9e3a8dde9ac')
    version('1.48.0', sha256='fa275aaccdbfc91ec0bc9a6fd0562051acdba731e7d584b64a277fec60e75877')

    depends_on("glib@2.49.2:", when="@1.49.2:")
    # version 1.48.0 build fails with glib 2.49.4
    depends_on("glib@2.48.1", when="@1.48.0")
    depends_on("python")
    depends_on("cairo+gobject")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("pkgconfig", type="build")

    # GobjectIntrospection does not build with sed from darwin:
    depends_on('sed', when='platform=darwin', type='build')

    # This package creates several scripts from
    # toosl/g-ir-tool-template.in.  In their original form these
    # scripts end up with a sbang line like
    #
    # `#!/usr/bin/env /path/to/spack/python`.
    #
    # These scripts are generated and then used as part of the build
    # (other packages also use the scripts after they've been
    # installed).
    #
    # The path to the spack python can become too long.  Because these
    # tools are used as part of the build, the normal hook that fixes
    # this problem can't help us.
    # This package fixes the problem in two steps:
    # - it rewrites the g-ir-tool-template so that its sbang line
    #   refers directly to spack's python (filter_file step below); and
    # - it patches the Makefile.in so that the generated Makefile has an
    #   extra sed expression in its TOOL_SUBSTITUTION that results in
    #   an `#!/bin/bash /path/to/spack/bin/sbang` unconditionally being
    #   inserted into the scripts as they're generated.
    patch("sbang.patch")

    # Drop deprecated xml.etree.ElementTree.Element.getchildren() which leads
    # to compilation issues with Python 3.9.
    # https://gitlab.gnome.org/GNOME/gobject-introspection/-/issues/325
    patch('https://gitlab.gnome.org/GNOME/gobject-introspection/-/commit/'
          '1f9284228092b2a7200e8a78bc0ea6702231c6db.patch',
          sha256='7700828b638c85255c87fcc317ea7e9572ff443f65c86648796528885e5b4cea',
          when='@:1.63.1')

    def url_for_version(self, version):
        url = 'http://ftp.gnome.org/pub/gnome/sources/gobject-introspection/{0}/gobject-introspection-{1}.tar.xz'
        return url.format(version.up_to(2), version)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        # we need to filter this file to avoid an overly long hashbang line
        filter_file('#!/usr/bin/env @PYTHON@', '#!@PYTHON@',
                    'tools/g-ir-tool-template.in')
        make()
        make("install")

    def setup_build_environment(self, env):
        env.set('SPACK_SBANG', sbang.sbang_install_path())

    @property
    def parallel(self):
        return not self.spec.satisfies('%fj')
