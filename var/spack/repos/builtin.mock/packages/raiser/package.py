# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import builtins

from spack.package import *


class Raiser(Package):
    """A package that can raise a built-in exception
    of any kind with any message
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("2.0", md5="abcdef0123456789abcdef0123456789")

    variant(
        "exc_type",
        values=lambda x: isinstance(x, str),
        default="RuntimeError",
        description="type of the exception to be raised",
        multi=False,
    )

    variant(
        "msg",
        values=lambda x: isinstance(x, str),
        default="Unknown Exception",
        description="message that will be tied to the exception",
        multi=False,
    )

    def install(self, spec, prefix):
        print("Raiser will raise ")
        exc_typename = self.spec.variants["exc_type"].value
        exc_type = getattr(builtins, exc_typename)
        msg = self.spec.variants["msg"].value
        raise exc_type(msg)
