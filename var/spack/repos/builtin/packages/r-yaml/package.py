# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYaml(RPackage):
    """This package implements the libyaml YAML 1.1 parser and emitter
    (http://pyyaml.org/wiki/LibYAML) for R."""

    homepage = "https://cloud.r-project.org/package=yaml"
    url      = "https://cloud.r-project.org/src/contrib/yaml_2.1.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/yaml"

    version('2.2.0', sha256='55bcac87eca360ab5904914fcff473a6981a1f5e6d2215d2634344d0ac30c546')
    version('2.1.19', sha256='e5db035693ac765e4b5fe1fc2e9711f8ca73e398e3f2bf27cc60def59ccd7f11')
    version('2.1.14', sha256='41a559846f6d44cc2dbcb3fc0becbc50d2766d3dc2aad7cfb97c1f9759ec0875')
    version('2.1.13', sha256='26f69aa2008bcacf3b2f95ef82a4667eaec2f2da8487646f71f1e2635d2d7fa2')
