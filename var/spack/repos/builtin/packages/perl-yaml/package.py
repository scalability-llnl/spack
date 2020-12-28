# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYaml(PerlPackage):
    """This module has been released to CPAN as YAML::Old, and soon YAML.pm
       will be changed to just be a frontend interface module for all the
       various Perl YAML implementation modules, including YAML::Old"""

    homepage = "https://metacpan.org/pod/YAML"
    url      = "https://cpan.metacpan.org/authors/id/T/TI/TINITA/YAML-1.27.tar.gz"

    version('1.27', sha256='c992a1e820de0721b62b22521de92cdbf49edc306ab804c485b4b1ec25f682f9')
