# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Whizard(AutotoolsPackage):
    """WHIZARD is a program system designed for the efficient calculation
      of multi-particle scattering cross sections
      and simulated event samples."""

    homepage = "whizard.hepforge.org"
    url      = "https://whizard.hepforge.org/downloads/?f=whizard-2.8.3.tar.gz"
    git      = "https://gitlab.tp.nt.uni-siegen.de/whizard/public.git"

    tags = ['hep']

    maintainers = ['vvolkl']

    version('master', branch="master")
    version('3.0.0_alpha', sha256='4636e5a10350bb67ccc98cd105bc891ea04f3393c2420f81be3d21240be20009')
    version('2.8.5', sha256='0f633e5620aa7dd50336b492e8a76bfae15b15943ea842010346ad7610818ecd', preferred=True)
    version('2.8.4', sha256='49893f077484470934a9d6e1545bbda7d398076568bceda00880d58132f26432')
    version('2.8.3', sha256='96a9046682d4b992b477eb96d561c3db789207e1049b60c9bd140db40eb1e5d7')
    version('2.8.2', sha256='32c9be342d01b3fc6f947fddce74bf2d81ece37fb39bca1f37778fb0c07e2568')
    version('2.8.1', sha256='0c759ce0598e25f38e04659f745c5963d238c4b5c12209f16449b6c0bc6dc64e')
    version('2.8.0', sha256='3b5175eafa879d1baca20237d18fb2b18bee89631e73ada499de9c082d009696')

    variant(
        'hepmc',
        default='3',
        description='builds with hepmc 2/3',
        values=('off', '2', '3'),
        multi=False
    )

    variant('pythia8', default=True,
            description="builds with pythia8")

    variant('fastjet', default=False,
            description="builds with fastjet")

    variant('lcio', default=False,
            description="builds with lcio")

    variant('lhapdf', default=False,
            description="builds with fastjet")

    variant('openmp', default=False,
            description="builds with openmp")

    variant('openloops', default=False,
            description="builds with openloops")

    variant('latex', default=False,
            description="data visualization with latex")

    depends_on('ocaml@4.02.3:', type='build', when="@3:")
    depends_on('ocaml@4.02.3:~force-safe-string', type='build', when="@:2.99.99")
    depends_on('hepmc', when="hepmc=2")
    depends_on('hepmc3', when="hepmc=3")
    depends_on('lcio', when="+lcio")
    depends_on('pythia8', when="+pythia8")
    depends_on('lhapdf', when="+lhapdf")
    depends_on('fastjet', when="+fastjet")
    depends_on('openloops@2.0.0: +compile_extra num_jobs=1 '
               'processes=eett,eevvjj,ppllj,tbw',
               when="+openloops")
    depends_on('texlive', when="+latex")
    depends_on('zlib')

    conflicts('%gcc@:5.0.99',
              msg='gfortran needs to support Fortran 2008. For more detailed information see https://whizard.hepforge.org/compilers.html')
    conflicts('%gcc@6.5.0',
              msg='Due to severe regressions, gfortran 6.5.0 can not be used. See https://whizard.hepforge.org/compilers.html')

    conflicts('%intel@:17',
              msg='The fortran compiler needs to support Fortran 2008. For more detailed information see https://whizard.hepforge.org/compilers.html')

    # Trying to build in parallel leads to a race condition at the build step.
    # See: https://github.com/key4hep/k4-spack/issues/71
    parallel = False

    def setup_build_environment(self, env):
        # whizard uses the compiler during runtime,
        # and seems incompatible with
        # filter_compiler_wrappers, thus the
        # actual compilers need to be used to build
        env.set('CC', self.compiler.cc)
        env.set('CXX', self.compiler.cxx)
        env.set('FC', self.compiler.fc)
        env.set('F77', self.compiler.fc)

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-hepmc=%s' % ("no" if "hepmc=off" in spec else "yes"),
            '--enable-fastjet=%s' % ("yes" if "+fastjet" in spec else "no"),
            '--enable-pythia8=%s' % ("yes" if "+pythia8" in spec else "no"),
            '--enable-lcio=%s' % ("yes" if "+lcio" in spec else "no"),
            '--enable-lhapdf=%s' % ("yes" if "+lhapdf" in spec else "no"),
            '--enable-openloops=%s' % ("yes" if "+openloops" in spec
                                       else "no"),
            # todo: hoppet
            # todo: recola
            # todo: looptools
            # todo: gosam
            # todo: pythia6
        ]

        if "+openloops" in spec:
            args.append('--with-openloops=%s' % spec['openloops'].prefix)
        if "+lcio" in spec:
            args.append('--with-lcio=%s' % spec['lcio'].prefix)
        if "hepmc=3" in spec:
            args.append('--with-hepmc=%s' % spec['hepmc3'].prefix)
        if "hepmc=2" in spec:
            args.append('--with-hepmc=%s' % spec['hepmc'].prefix)
        if "+openmp" not in spec:
            args.append('--disable-openmp')
        return args

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        patch = str(version[2])
        if len(version) == 4:
            url = "https://whizard.hepforge.org/downloads/?f=whizard-%s.%s.%s_%s.tar.gz" % (major, minor, patch, version[3])
        else:
            url = "https://whizard.hepforge.org/downloads/?f=whizard-%s.%s.%s.tar.gz" % (major, minor, patch)
        return url
