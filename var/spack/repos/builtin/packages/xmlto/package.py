# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmlto(AutotoolsPackage):
    """Utility xmlto is a simple shell script for converting XML files to various
    formats. It serves as easy to use command line frontend to make fine output
    without remembering many long options and searching for the syntax of the
    backends."""

    homepage = "https://pagure.io/xmlto"
    url = "https://releases.pagure.org/xmlto/xmlto-0.0.28.tar.gz"

    license("GPL-2.0-or-later")

    version("0.0.28", sha256="2f986b7c9a0e9ac6728147668e776d405465284e13c74d4146c9cbc51fd8aad3")

    depends_on("c", type="build")  # generated

    # FIXME: missing a lot of dependencies
    depends_on("flex", type=("build"))
    depends_on("docbook-xsl", type=("build", "run"))
    depends_on("libxml2", type=("build", "run"))  # xmllint
    depends_on("libxslt", type=("build", "run"))  # xsltconf
    depends_on("util-linux", type=("build", "run"))  # getopt with support for longopts

    depends_on("docbook-xml", type="run")

    patch(
        "https://src.fedoraproject.org/rpms/xmlto/raw/571fc033c0ff5d6cf448e2ca20d8ae8ac61a7cb8/f/xmlto-c99-1.patch",
        sha256="056c8bebc25d8d1488cc6a3724e2bcafc0e5e0df5c50080559cdef99bd377839",
    )
    patch(
        "https://src.fedoraproject.org/rpms/xmlto/raw/571fc033c0ff5d6cf448e2ca20d8ae8ac61a7cb8/f/xmlto-c99-2.patch",
        sha256="50e39b1810bbf22a1d67944086c5681bcd58b8c325dfb251d56ac15d088fc17a",
    )
