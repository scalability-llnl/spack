# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graphite2(CMakePackage):
    """Graphite is a system that can be used to create "smart fonts" capable of
    displaying writing systems with various complex behaviors. A smart font
    contains not only letter shapes but also additional instructions indicating
    how to combine and position the letters in complex ways."""

    homepage = "https://scripts.sil.org/cms/scripts/page.php?site_id=projects&item_id=graphite_home"
    url      = "https://github.com/silnrsi/graphite/releases/download/1.3.13/graphite2-1.3.13.tgz"

    version('1.3.13', sha256='dd63e169b0d3cf954b397c122551ab9343e0696fb2045e1b326db0202d875f06')

    patch('regparm.patch')
