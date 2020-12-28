# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class SharedMimeInfo(AutotoolsPackage):
    """Database of common MIME types."""

    homepage = "https://freedesktop.org/wiki/Software/shared-mime-info"
    url      = "http://freedesktop.org/~hadess/shared-mime-info-1.8.tar.xz"

    version('1.9', sha256='5c0133ec4e228e41bdf52f726d271a2d821499c2ab97afd3aa3d6cf43efcdc83')
    version('1.8', sha256='2af55ef1a0319805b74ab40d331a3962c905477d76c086f49e34dc96363589e9')

    parallel = False

    depends_on('glib')
    depends_on('libxml2')
    depends_on('intltool', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)
