# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Enchant(AutotoolsPackage):
    """Enchant is a library (and command-line program) that wraps a
    number of different spelling libraries and programs with a
    consistent interface."""

    homepage = "https://abiword.github.io/enchant/"
    url      = "https://github.com/AbiWord/enchant/releases/download/v2.2.5/enchant-2.2.5.tar.gz"

    version('2.2.7', sha256='1b22976135812b35cb5b8d21a53ad11d5e7c1426c93f51e7a314a2a42cab3a09')
    version('2.2.6', sha256='8048c5bd26190b21279745cfecd05808c635bc14912e630340cd44a49b87d46d')
    version('2.2.5', sha256='ffce4ea00dbda1478d91c3e1538cadfe5761d9d6c0ceb27bc3dba51882fe1c47')
    version('2.2.4', sha256='f5d6b689d23c0d488671f34b02d07b84e408544b2f9f6e74fb7221982b1ecadc')
    version('2.2.3', sha256='abd8e915675cff54c0d4da5029d95c528362266557c61c7149d53fa069b8076d')
    version('2.2.2', sha256='661e0bd6e82deceb97fc94bea8c6cdbcd8ff631cfa9b7a8196de2e2aca13f54b')
    version('2.2.1', sha256='97f2e617b34c66a645b9cfebe33700456c31ca2f4677eb827b364c0d9a7f4e5e')
    version('2.2.0', sha256='2f91ea06992c923ac9b72c9c6d0a7c855aef1e9a4991350d83236723c8412467')
    version('2.1.3', sha256='086f37cdecd42eacd0e1dc291f5410d9ca2c5ed2cd9cd9367729e3d2d18a8550')
    version('2.1.2', sha256='039563bbb7340f320bd9237dac92303b3e7768152b08fc0d554d6957ae7183d8')
    version('2.1.1', sha256='5fad0a1e82ddfed91647e93da5955fc76249760fd51865648a36074dc97d526c')
    version('2.1.0', sha256='2cdda2d9edb62ad895c34be35c598d56ac5b9b9298f3dfdaa2b40a1914d1db7e')

    variant('hunspell', default=True, description='Enables hunspell backend')

    depends_on('glib')
    depends_on('aspell')
    depends_on('hunspell', when='+hunspell')

    def configure_args(self):
        spec = self.spec
        args = ['--with-aspell',
                '--with-aspell-dir={0}'.format(spec['aspell'].prefix)]

        args += self.with_or_without('hunspell')
        if spec.satisfies('+hunspell'):
            args.append(
                '--with-hunspell-dir={0}'.format(spec['hunspell'].prefix))

        return args
