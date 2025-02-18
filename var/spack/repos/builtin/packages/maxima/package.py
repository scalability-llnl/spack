# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Maxima(AutotoolsPackage):
    """
    Maxima is a fairly complete computer algebra system written in Lisp
    with an emphasis on symbolic computation.
    """

    homepage = "https://maxima.sourceforge.io/"
    url = "https://sourceforge.net/projects/maxima/files/Maxima-source/5.47.0-source/maxima-5.47.0.tar.gz/download"

    license("BSD-3-Clause", checked_by="adaell")

    maintainers("adaell")

    version("5.47.0", sha256="9104021b24fd53e8c03a983509cb42e937a925e8c0c85c335d7709a14fd40f7a")

    depends_on("sbcl")

    def configure_args(self):
        args = ["--disable-build-docs"]
        return args

    def install(self, spec, prefix):
        make()
        make("install")
