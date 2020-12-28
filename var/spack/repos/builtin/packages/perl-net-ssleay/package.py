# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack.package import *


class PerlNetSsleay(PerlPackage):
    """Perl extension for using OpenSSL"""

    homepage = "http://search.cpan.org/~mikem/Net-SSLeay-1.82/lib/Net/SSLeay.pod"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/Net-SSLeay-1.82.tar.gz"

    version('1.85', sha256='9d8188b9fb1cae3bd791979c20554925d5e94a138d00414f1a6814549927b0c8')
    version('1.82', sha256='5895c519c9986a5e5af88e3b8884bbdc70e709ee829dc6abb9f53155c347c7e5')

    depends_on('openssl')

    def configure(self, spec, prefix):
        self.build_method = 'Makefile.PL'
        self.build_executable = inspect.getmodule(self).make
        # Do you want to run external tests?
        config_answers = ['\n']
        config_answers_filename = 'spack-config.in'

        with open(config_answers_filename, 'w') as f:
            f.writelines(config_answers)

        with open(config_answers_filename, 'r') as f:
            env['OPENSSL_PREFIX'] = self.spec['openssl'].prefix
            inspect.getmodule(self).perl('Makefile.PL', 'INSTALL_BASE={0}'.
                                         format(prefix), input=f)
