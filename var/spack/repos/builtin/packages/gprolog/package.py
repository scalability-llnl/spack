# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gprolog(Package):
    """A free Prolog compiler with constraint solving over finite domains."""

    homepage = "http://www.gprolog.org/"
    url = "http://www.gprolog.org/gprolog-1.4.5.tar.gz"

    license("LGPL-3.0-or-later")

    version("1.5.0", sha256="670642b43c0faa27ebd68961efb17ebe707688f91b6809566ddd606139512c01")
    version("1.4.5", sha256="bfdcf00e051e0628b4f9af9d6638d4fde6ad793401e58a5619d1cc6105618c7c")

    depends_on("c", type="build")  # generated

    parallel = False

    def install(self, spec, prefix):
        with working_dir("src"):
            configure("--with-install-dir=%s" % prefix, "--without-links-dir")
            make()
            make("install")
