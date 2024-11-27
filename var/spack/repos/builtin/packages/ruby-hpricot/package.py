# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyHpricot(RubyPackage):
    """A swift, liberal HTML parser with a fantastic library.

    NOTE: ruby-hpricot is no longer maintained, consider ruby-nokogiri instead.
    """

    homepage = "https://github.com/hpricot/hpricot"
    url = "https://github.com/hpricot/hpricot/archive/0.8.6.tar.gz"

    license("MIT")

    version("0.8.6", sha256="792f63cebe2f2b02058974755b4c8a3aef52e5daf37f779a34885d5ff2876017")

    depends_on("c", type="build")  # generated
