# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Itstool(AutotoolsPackage):
    """ITS Tool allows you to translate your XML documents with PO files, using
    rules from the W3C Internationalization Tag Set (ITS) to determine what
    to translate and how to separate it into PO file messages."""

    homepage = "https://itstool.org/"
    url = "https://files.itstool.org/itstool/itstool-2.0.2.tar.bz2"

    maintainers("agoodLANL")

    license("GPL-3.0-or-later")

    version("2.0.7", sha256="6b9a7cd29a12bb95598f5750e8763cee78836a1a207f85b74d8b3275b27e87ca")

    depends_on("libxml2+python", type=("build", "run"))
