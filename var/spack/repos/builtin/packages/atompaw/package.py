# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Atompaw(Package):
    """A Projector Augmented Wave (PAW) code for generating
    atom-centered functions.

    Official website: http://pwpaw.wfu.edu

    User's guide: ~/doc/atompaw-usersguide.pdf
    """
    homepage = "http://users.wfu.edu/natalie/papers/pwpaw/man.html"
    url = "http://users.wfu.edu/natalie/papers/pwpaw/atompaw-4.0.0.13.tar.gz"

    version('4.0.0.13', sha256='cbd73f11f3e9cc3ff2e5f3ec87498aeaf439555903d0b95a72f3b0a021902020')
    version('3.1.0.3', sha256='15fe9a0369bdcc366370a0ecaa67e803ae54534b479ad63c4c7494a04fa3ea78')

    depends_on("lapack")
    depends_on("blas")

    # pin libxc version
    depends_on("libxc@2.2.1")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]

        linalg = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            "--with-linalg-libs=%s" % linalg.ld_flags,
            "--enable-libxc",
            "--with-libxc-incs=-I%s" % spec["libxc"].prefix.include,
            "--with-libxc-libs=-L%s -lxcf90 -lxc" % spec["libxc"].prefix.lib,
        ])

        configure(*options)
        make(parallel=False)  # parallel build fails
        make("check")
        make("install")
