from spack import *
import os

class Mvapich2(Package):
    """MVAPICH2 is an MPI implementation for Infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"
    url = "http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2b.tar.gz"

    version('2.2b', '5651e8b7a72d7c77ca68da48f3a5d108')
    version('2.2a', 'b8ceb4fc5f5a97add9b3ff1b9cbe39d2')
    version('2.0',  '9fbb68a4111a8b6338e476dc657388b4')
    version('1.9',  '5dc58ed08fd3142c260b70fe297e127c')

    patch('ad_lustre_rwcontig_open_source.patch', when='@1.9')

    provides('mpi@:2.2', when='@1.9')  # MVAPICH2-1.9 supports MPI 2.2
    provides('mpi@:3.0', when='@2.0:')  # MVAPICH2-2.0 supports MPI 3.0

    variant('debug', default=False, description='Enables debug information and error messages at run-time')

    ##########
    # TODO : Process managers should be grouped into the same variant, as soon as variant capabilities will be extended
    # See https://groups.google.com/forum/#!topic/spack/F8-f8B4_0so
    SLURM = 'slurm'
    HYDRA = 'hydra'
    GFORKER = 'gforker'
    REMSHELL = 'remshell'
    SLURM_INCOMPATIBLE_PMS = (HYDRA, GFORKER, REMSHELL)
    variant(SLURM, default=False, description='Sets slurm as the only process manager')
    variant(HYDRA, default=False, description='Sets hydra as one of the process managers')
    variant(GFORKER, default=False, description='Sets gforker as one of the process managers')
    variant(REMSHELL, default=False, description='Sets remshell as one of the process managers')
    ##########

    ##########
    # TODO : Network types should be grouped into the same variant, as soon as variant capabilities will be extended
    PSM = 'psm'
    SOCK = 'sock'
    NEMESISIBTCP = 'nemesisibtcp'
    NEMESISIB = 'nemesisib'
    NEMESIS = 'nemesis'
    MRAIL = 'mrail'
    SUPPORTED_NETWORKS = (PSM, SOCK, NEMESIS, NEMESISIB, NEMESISIBTCP)
    variant(PSM, default=False, description='Configures a build for QLogic PSM-CH3')
    variant(SOCK, default=False, description='Configures a build for TCP/IP-CH3')
    variant(NEMESISIBTCP, default=False, description='Configures a build for both OFA-IB-Nemesis and TCP/IP-Nemesis')
    variant(NEMESISIB, default=False, description='Configures a build for OFA-IB-Nemesis')
    variant(NEMESIS, default=False, description='Configures a build for TCP/IP-Nemesis')
    variant(MRAIL, default=False, description='Configures a build for OFA-IB-CH3')
    ##########

    # FIXME : CUDA support is missing

    def url_for_version(self, version):
        base_url = "http://mvapich.cse.ohio-state.edu/download"
        if version < Version('2.0'):
            return "%s/mvapich2/mv2/mvapich2-%s.tar.gz" % (base_url, version)
        else:
            return "%s/mvapich/mv2/mvapich2-%s.tar.gz"  % (base_url, version)

    @staticmethod
    def enabled(x):
        """
        Given a variant name returns the string that means the variant is enabled

        :param x: variant name
        :return:
        """
        return '+' + x

    def set_build_type(self, spec, configure_args):
        """
        Appends to configure_args the flags that depends only on the build type (i.e. release or debug)

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        if '+debug' in spec:
            build_type_options = [
                "--disable-fast",
                "--enable-error-checking=runtime",
                "--enable-error-messages=all",
                "--enable-g=dbg", "--enable-debuginfo"  # Permits debugging with TotalView
            ]
        else:
            build_type_options = ["--enable-fast=all"]

        configure_args.extend(build_type_options)

    def set_process_manager(self, spec, configure_args):
        """
        Appends to configure_args the flags that will enable the appropriate process managers

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        # Check that slurm variant is not activated together with other pm variants
        has_slurm_incompatible_variants = any(self.enabled(x) in spec for x in Mvapich2.SLURM_INCOMPATIBLE_PMS)
        if self.enabled(Mvapich2.SLURM) in spec and has_slurm_incompatible_variants:
            raise RuntimeError(" %s : 'slurm' cannot be activated together with other process managers" % self.name)

        process_manager_options = []
        if self.enabled(Mvapich2.SLURM) in spec:
            process_manager_options = [
                "--with-pm=slurm"
            ]
        elif has_slurm_incompatible_variants:
            pms = []
            # The variant name is equal to the process manager name in the configuration options
            for x in Mvapich2.SLURM_INCOMPATIBLE_PMS:
                if self.enabled(x) in spec:
                    pms.append(x)
            process_manager_options = [
                "--with-pm=%s" % ':'.join(pms)
            ]
        configure_args.extend(process_manager_options)

    def set_network_type(self, spec, configure_args):
        # Check that at most one variant has been activated
        count = 0
        for x in Mvapich2.SUPPORTED_NETWORKS:
            if self.enabled(x) in spec:
                count += 1
        if count > 1:
            raise RuntimeError('network variants are mutually exclusive (only one can be selected at a time)')
        network_options = []
        # From here on I can suppose that only one variant has been selected
        if self.enabled(Mvapich2.PSM) in spec:
            network_options = ["--with-device=ch3:psm"]
        elif self.enabled(Mvapich2.SOCK) in spec:
            network_options = ["--with-device=ch3:sock"]
        elif self.enabled(Mvapich2.NEMESISIBTCP) in spec:
            network_options = ["--with-device=ch3:nemesis:ib,tcp"]
        elif self.enabled(Mvapich2.NEMESISIB) in spec:
            network_options = ["--with-device=ch3:nemesis:ib"]
        elif self.enabled(Mvapich2.NEMESIS) in spec:
            network_options = ["--with-device=ch3:nemesis"]
        elif self.enabled(Mvapich2.MRAIL) in spec:
            network_options = ["--with-device=ch3:mrail", "--with-rdma=gen2"]

        configure_args.extend(network_options)

    def install(self, spec, prefix):
        # we'll set different configure flags depending on our environment
        configure_args = [
            "--prefix=%s" % prefix,
            "--enable-shared",
            "--enable-romio",
            "--disable-silent-rules",
        ]

        if self.compiler.f77 and self.compiler.fc:
            configure_args.append("--enable-fortran=all")
        elif self.compiler.f77:
            configure_args.append("--enable-fortran=f77")
        elif self.compiler.fc:
            configure_args.append("--enable-fortran=fc")
        else:
            configure_args.append("--enable-fortran=none")

        # Set the type of the build (debug, release)
        self.set_build_type(spec, configure_args)
        # Set the process manager
        self.set_process_manager(spec, configure_args)
        # Determine network type by variant
        self.set_network_type(spec, configure_args)

        configure(*configure_args)
        make()
        make("install")

        self.filter_compilers()


    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX, F77, and FC set
           to Spack's generic cc, c++, f77, and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        bin = self.prefix.bin
        mpicc  = os.path.join(bin, 'mpicc')
        mpicxx = os.path.join(bin, 'mpicxx')
        mpif77 = os.path.join(bin, 'mpif77')
        mpif90 = os.path.join(bin, 'mpif90')

        spack_cc  = os.environ['CC']
        spack_cxx = os.environ['CXX']
        spack_f77 = os.environ['F77']
        spack_fc  = os.environ['FC']

        kwargs = { 'ignore_absent' : True, 'backup' : False, 'string' : True }
        filter_file('CC="%s"' % spack_cc , 'CC="%s"'  % self.compiler.cc,  mpicc,  **kwargs)
        filter_file('CXX="%s"'% spack_cxx, 'CXX="%s"' % self.compiler.cxx, mpicxx, **kwargs)
        filter_file('F77="%s"'% spack_f77, 'F77="%s"' % self.compiler.f77, mpif77, **kwargs)
        filter_file('FC="%s"' % spack_fc , 'FC="%s"'  % self.compiler.fc,  mpif90, **kwargs)
