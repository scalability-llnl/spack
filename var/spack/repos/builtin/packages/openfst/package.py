# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openfst(AutotoolsPackage):
    """OpenFst is a library for constructing, combining, optimizing,
        and searching weighted finite-state transducers (FSTs). Weighted
        finite-state transducers are automata where each transition has
        an input label, an output label, and a weight."""

    homepage = "http://www.openfst.org"
    url      = "http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.1.tar.gz"
    list_url = "http://www.openfst.org/twiki/bin/view/FST/FstDownload"

    version('1.7.9',  sha256='9319aeb31d1e2950ae25449884e255cc2bc9dfaf987f601590763e61a10fbdde')
    version('1.6.7',  sha256='e21a486d827cde6a592c8e91721e4540ad01a5ae35a60423cf17be4d716017f7')
    version('1.6.1',  sha256='5245af8ebccb96208eec2dfe3b3a81143d3565a4d41220bff299287fb3333f7d')
    version('1.6.0',  sha256='c03467951631af3f74a6f33ffd50f04285bc4562f79127afd95785120379d293')
    version('1.5.4',  sha256='acc115aaaa33de53de62dae44120ab368fabaea06f52606b77714081ecd32657')
    version('1.5.3',  sha256='9b09e457aeab87f613508b92a0f9f820140c9e18d05584e3f1ae384396b5dcbd')
    version('1.5.2',  sha256='944b9ae654d62345f51b9c2f728eee2751af32f90caeb35283bb7a5262d19cf2')
    version('1.5.1',  sha256='6593edb401d047d942365437be012d974990609b6eb89814d1c6422a4161771e')
    version('1.5.0',  sha256='01c2b810295a942fede5b711bd04bdc9677855c846fedcc999c792604e02177b')
    version('1.4.1-patch',  sha256='e671bf6bd4425a1fed4e7543a024201b74869bfdd029bdf9d10c53a3c2818277',
            url='http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.4.1.tar.gz')
    version('1.4.1',  sha256='e671bf6bd4425a1fed4e7543a024201b74869bfdd029bdf9d10c53a3c2818277')
    version('1.4.0',  sha256='eb557f37560438f03912b4e43335c4c9e72aa486d4f2046127131185eb88f17a')

    conflicts('%intel@16:')
    conflicts('%gcc@6:', when='@:1.6.1')

    variant('far', default=False, description="Enable FAR support")

    # Patch openfst-1.4.1 for kaldi@c024e8
    # See https://github.com/kaldi-asr/kaldi/blob/c024e8aa0a727bf76c91a318f76a1f8b0b59249e/tools/Makefile#L82-L88
    patch('openfst-1.4.1.patch', when='@1.4.1-patch')
    patch('openfst_gcc41up.patch', when='@1.4.1-patch')

    def configure_args(self):
        args = []
        spec = self.spec
        if '+far' in spec:
            args.append('--enable-far')
        else:
            args.append('--disable-far')
        return args
