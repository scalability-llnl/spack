# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Externalprereq(Package):
    homepage = "http://somewhere.com"
    url = "http://somewhere.com/prereq-1.0.tar.gz"

    version("1.4", md5="f1234567890abcdef1234567890abcde")
