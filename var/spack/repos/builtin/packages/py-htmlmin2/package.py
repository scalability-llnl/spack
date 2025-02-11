# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtmlmin2(PythonPackage):
    """(Warning: This is a fork of htmlmin) A configurable HTML Minifier with safety features."""

    homepage = "https://github.com/wilhelmer/htmlmin"
    version(
        "0.1.13",
        url="https://files.pythonhosted.org/packages/be/31/a76f4bfa885f93b8167cb4c85cf32b54d1f64384d0b897d45bc6d19b7b45/htmlmin2-0.1.13-py3-none-any.whl",
    )

    license("BSD", checked_by="lizzyd710")

    version(
        "0.1.13",
        sha256="75609f2a42e64f7ce57dbff28a39890363bde9e7e5885db633317efbdf8c79a2",
        expand=False,
    )
