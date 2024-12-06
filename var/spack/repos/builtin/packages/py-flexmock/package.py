# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlexmock(PythonPackage):
    """flexmock is a testing library for Python that makes it easy to create
    mocks,stubs and fakes.

    Its API is inspired by a Ruby library of the same name. However, it is not
    a goal of Python flexmock to be a clone of the Ruby version. Instead, the
    focus is on providing full support for testing Python programs and making
    the creation of fake objects as unobtrusive as possible."""

    homepage = "https://flexmock.readthedocs.io/en/latest/"
    pypi = "flexmock/flexmock-0.10.4.tar.gz"

    maintainers("dorton21")

    license("BSD-2-Clause")

    version("0.10.4", sha256="5033ceb974d6452cf8716c2ff5059074b77e546df5c849fb44a53f98dfe0d82c")

    depends_on("py-setuptools", type="build")
