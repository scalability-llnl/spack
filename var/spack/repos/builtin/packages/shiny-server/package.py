# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ShinyServer(CMakePackage):
    """Shiny server lets you put shiny web applications and interactive
       documents online. Take your shiny apps and share them with your
       organization or the world."""

    #
    # HEADS UP:
    # 1. The shiny server installation step will download various node
    #    and npm bits from the net.  They seem to have them well
    #    constrained ("npm shrinkwrap"?), but this package is not
    #    "air gappable".
    # 2. Docs say that it requires 'gcc'.  depends_on() won't do the
    #    right thing, it's Up To You.
    #
    homepage = "https://www.rstudio.com/products/shiny/shiny-server/"
    url = "https://github.com/rstudio/shiny-server/archive/v1.5.3.838.tar.gz"

    version('1.5.3.838', sha256='6fd1b12cd1cbe5c64cacbec4accefe955353f9c675e5feff809c0e911a382141')

    depends_on('python@:2.8')  # docs say: "Really.  3.x will not work"
    depends_on('cmake@2.8.10:', type='build')
    depends_on('git')
    depends_on('r+X')
    depends_on('openssl')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.append("-DPYTHON=%s" % spec['python'].command.path)

        return options

    # Recompile the npm modules included in the project
    @run_after('build')
    def build_node(self):
        bash = which('bash')
        mkdirp('build')
        bash('-c', 'bin/npm --python="$PYTHON" install')
        bash('-c', 'bin/node ./ext/node/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js --python="$PYTHON" rebuild')  # noqa: E501

    def setup_run_environment(self, env):
        env.prepend_path('PATH', join_path(self.prefix, 'shiny-server', 'bin'))
        # shiny comes with its own pandoc; hook it up...
        env.prepend_path('PATH', join_path(
            self.prefix, 'shiny-server', 'ext', 'pandoc', 'static'))
