# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Viennarna(AutotoolsPackage):
    """The ViennaRNA Package consists of a C code library and several
    stand-alone programs for the prediction and comparison of RNA secondary
    structures.
    """

    homepage = "https://www.tbi.univie.ac.at/RNA/"
    url      = "https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_4_x/ViennaRNA-2.4.3.tar.gz"

    version('2.4.3', sha256='4cda6e22029b34bb9f5375181562f69e4a780a89ead50fe952891835e9933ac0')
    version('2.3.5', sha256='26b62a00da21bc5597b580ab8fef4e624234ec446d7d3cb0ce22803a5d7074ca')

    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('perl', default=True, description='Build ViennaRNA with Perl interface')
    variant('python', default=True, description='Build ViennaRNA with Python interface')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('libsvm')
    depends_on('gsl')

    def url_for_version(self, version):
        url = 'https://www.tbi.univie.ac.at/RNA/download/sourcecode/{0}_x/ViennaRNA-{1}.tar.gz'
        return url.format(version.up_to(2).underscored, version)

    def configure_args(self):

        args = self.enable_or_disable('sse')
        args += self.with_or_without('python')
        args += self.with_or_without('perl')
        if self.spec.satisfies('@2.4.3:'):
            args.append('--without-swig')

        if 'python@3:' in self.spec:
            args.append('--with-python3')

        return args
