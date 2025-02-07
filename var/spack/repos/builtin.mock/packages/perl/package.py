# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Perl(Package):
    """Dummy Perl package to allow a dummy perl-extension in repo."""

    homepage = "http://www.python.org"
    url = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"

    extendable = True

    version("0.0.0", md5="abcdef1234567890abcdef1234567890")

    variant("shared", default=True, description="Build shared libraries")
