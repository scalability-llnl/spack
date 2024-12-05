# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMistune(PythonPackage):
    """A sane Markdown parser with useful plugins and renderers."""

    homepage = "https://github.com/lepture/mistune"
    pypi = "mistune/mistune-2.0.2.tar.gz"

    license("BSD-3-Clause")

    version("2.0.5", sha256="0246113cb2492db875c6be56974a7c893333bf26cd92891c85f63151cee09d34")
    version("2.0.4", sha256="9ee0a66053e2267aba772c71e06891fa8f1af6d4b01d5e84e267b4570d4d9808")
    version("2.0.2", sha256="6fc88c3cb49dba8b16687b41725e661cf85784c12e8974a29b9d336dd596c3a1")
    version("0.8.4", sha256="59a3429db53c50b5c6bcc8a07f8848cb00d7dc8bdb431a4ab41920d201d4756e")
    version("0.8.3", sha256="bc10c33bfdcaa4e749b779f62f60d6e12f8215c46a292d05e486b869ae306619")
    version("0.8.2", sha256="c50f2fb3a058120c5696f08af9d57877a9c76e879f19af5835fb2c6a4e56a67b")
    version("0.8.1", sha256="4c0f66924ce28f03b95b210ea57e57bd0b59f479edd91c2fa4fe59331eae4a82")
    version("0.8", sha256="dc3f43e7cf0abb95cdfecbf82d85c419108d5f13e1844b2a8a2fc0abf24c7a47")
    version("0.7.4", sha256="8517af9f5cd1857bb83f9a23da75aa516d7538c32a2c5d5c56f3789a9e4cd22f")
    version("0.7.3", sha256="21d0e869df3b9189f248e022f1c9763cf9069e1a2f00676f1f1852bd7f98b713")
    version("0.7.2", sha256="626f2516adcde4af608eaf83635ff20ff7e577c1898ad4d0f0fcd8c094399840")
    version("0.7.1", sha256="6076dedf768348927d991f4371e5a799c6a0158b16091df08ee85ee231d929a7")
    version("0.7", sha256="1daa2e55f5de63ecde7c446c4677c0447006752f78ad2c9c1c3c3452d395f89f")
    version("0.6", sha256="d54a69365d01bc97412a39c11674a8aae3f333586e91f38895cc1ad818e13dc5")
    version("0.5.1", sha256="cc66489a28845c0e1848ae290af5b555074eb76185136ca058e8eed1faa89692")
    version("0.5", sha256="d53d868cfd10cf757160e88adb5760fce95f7026a243f15a02b7c604238e5869")

    depends_on("py-setuptools", type="build")
