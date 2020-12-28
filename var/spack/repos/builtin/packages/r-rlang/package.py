# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRlang(RPackage):
    """A toolbox for working with base types, core R features like the
       condition system, and core 'Tidyverse' features like tidy evaluation."""

    homepage = "https://cloud.r-project.org/package=rlang"
    url      = "https://cloud.r-project.org/src/contrib/rlang_0.2.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rlang"

    version('0.4.6', sha256='3a81b107765fd6ac0ad716c428d01878775ded9208ba125d43c890c73d2533ca')
    version('0.4.0', sha256='9748a4a217548bbe5631c18fd88c94811950446f798ff21fb327703aebaa150d')
    version('0.3.4', sha256='4e467f7b0dcbde91b60c292137d2c69cecaa713a6e4c9b7157ef6fd5453b7ade')
    version('0.3.1', sha256='30427b2be2288e88acd30c4ea348ee06043a649fd73623a63148b1ad96317151')
    version('0.3.0.1', sha256='29451db0a3cabd75761d32df47a5d43ccadbde07ecb693ffdd73f122a0b9f348')
    version('0.3.0',   sha256='9ab10ea3e19b2d60a289602ebbefa83509f430db1c8161e523896c374241b893')
    version('0.2.2', sha256='c9119420ff0caeb6b0fcee8800e2fb1ec072e291e0e53b8acea3c4cf49420d33')
    version('0.1.4', sha256='8d9b6c962ae81b96c96ada9614c6a1ffb9eda12dd407e2aff634f7d335e7b9f4')
    version('0.1.2', sha256='90cfcd88cae6fff044fca64b24a8e6bdc09fc276163b518ff2d90268b0c785f9')
    version('0.1.1', sha256='5901f95d68728a7d9bb1c2373a20ce6e4ad222f66e397e7735e9eff987c73c3f')

    depends_on('r@3.1.0:', when='@:0.3.4', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@0.4.0:', type=('build', 'run'))
