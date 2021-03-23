# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Acts(CMakePackage, CudaPackage):
    """
    A Common Tracking Software (Acts)

    This project contains an experiment-independent set of track reconstruction
    tools. The main philosophy is to provide high-level track reconstruction
    modules that can be used for any tracking detector. The description of the
    tracking detector's geometry is optimized for efficient navigation and
    quick extrapolation of tracks. Converters for several common geometry
    description languages exist. Having a highly performant, yet largely
    customizable implementation of track reconstruction algorithms was a
    primary objective for the design of this toolset. Additionally, the
    applicability to real-life HEP experiments plays major role in the
    development process. Apart from algorithmic code, this project also
    provides an event data model for the description of track parameters and
    measurements.

    Key features of this project include: tracking geometry description which
    can be constructed from TGeo, DD4Hep, or GDML input, simple and efficient
    event data model, performant and highly flexible algorithms for track
    propagation and fitting, basic seed finding algorithms.
    """

    homepage = "http://acts.web.cern.ch/ACTS/"
    git      = "https://github.com/acts-project/acts.git"
    maintainers = ['HadrienG2']

    tags = ['hep']

    # Supported Acts versions
    version('master', branch='master')
    version('6.00.0', commit='a5cf04acd4b1a2c625e0826189109472a3392558')
    version('5.00.0', commit='df77b91a7d37b8db6ed028a4d737014b5ad86bb7')
    version('4.01.0', commit='c383bf434ef69939b47e840e0eac0ba632e6af9f')
    version('4.00.0', commit='ed64b4b88d366b63adc4a8d1afe5bc97aa5751eb')
    version('3.00.0', commit='e20260fccb469f4253519d3f0ddb3191b7046db3')
    version('2.00.0', commit='8708eae2b2ccdf57ab7b451cfbba413daa1fc43c')
    version('1.02.1', commit='f6ebeb9a28297ba8c54fd08b700057dd4ff2a311')
    version('1.02.0', commit='e69b95acc9a264e63aded7d1714632066e090542')
    version('1.01.0', commit='836fddd02c3eff33825833ff97d6abda5b5c20a0')
    version('1.00.0', commit='ec9ce0bcdc837f568d42a12ddf3fc9c80db62f5d')
    version('0.32.0', commit='a4cedab7e727e1327f2835db29d147cc86b21054')
    version('0.31.0', commit='cfbd901555579a2f32f4efe2b76a7048442b42c3')
    version('0.30.0', commit='a71ef0a9c742731611645214079884585a92b15e')
    version('0.29.0', commit='33aa3e701728112e8908223c4a7fd521907c8ea4')
    version('0.28.0', commit='55626b7401eeb93fc562e79bcf385f0ad0ac48bf')
    version('0.27.1', commit='8ba3010a532137bc0ab6cf83a38b483cef646a01')
    version('0.27.0', commit='f7b1a1c27d5a95d08bb67236ad0e117fcd1c679f')
    version('0.26.0', commit='cf542b108b31fcc349fc18fb0466f889e4e42aa6')
    version('0.25.2', commit='76bf1f3e4be51d4d27126b473a2caa8d8a72b320')
    version('0.25.1', commit='6e8a1ea6d2c7385a78e3e190efb2a8a0c1fa957f')
    version('0.25.0', commit='0aca171951a214299e8ff573682b1c5ecec63d42')
    version('0.24.0', commit='ef4699c8500bfea59a5fe88bed67fde2f00f0adf')
    version('0.23.0', commit='dc443dd7e663bc4d7fb3c1e3f1f75aaf57ffd4e4')
    version('0.22.1', commit='ca1b8b1645db6b552f44c48d2ff34c8c29618f3a')
    version('0.22.0', commit='2c8228f5843685fc0ae69a8b95dd8fc001139efb')
    version('0.21.0', commit='10b719e68ddaca15b28ac25b3daddce8c0d3368d')
    version('0.20.0', commit='1d37a849a9c318e8ca4fa541ef8433c1f004637b')
    version('0.19.0', commit='408335636486c421c6222a64372250ef12544df6')
    version('0.18.0', commit='d58a68cf75b52a5e0f563bc237f09250aa9da80c')
    version('0.17.0', commit='0789f654ff484b013fd27e5023cf342785ea8d97')
    version('0.16.0', commit='b3d965fe0b8ae335909d79114ef261c6b996773a')
    version('0.15.0', commit='267c28f69c561e64369661a6235b03b5a610d6da')
    version('0.14.0', commit='38d678fcb205b77d60326eae913fbb1b054acea1')
    version('0.13.0', commit='b33f7270ddbbb33050b7ec60b4fa255dc2bfdc88')
    version('0.12.1', commit='a8b3d36e7c6cb86487637589e0eff7bbe626054a')
    version('0.12.0', commit='f9cda77299606d78c889fb1db2576c1971a271c4')
    version('0.11.1', commit='c21196cd6c3ecc6da0f14d0a9ef227a274be584b')
    version('0.11.0', commit='22bcea1f19adb0021ca61b843b95cfd2462dd31d')
    version('0.10.5', commit='b6f7234ca8f18ee11e57709d019c14bf41cf9b19')
    version('0.10.4', commit='42cbc359c209f5cf386e620b5a497192c024655e')
    version('0.10.3', commit='a3bb86b79a65b3d2ceb962b60411fd0df4cf274c')
    version('0.10.2', commit='64cbf28c862d8b0f95232b00c0e8c38949d5015d')
    version('0.10.1', commit='0692dcf7824efbc504fb16f7aa00a50df395adbc')
    version('0.10.0', commit='30ef843cb00427f9959b7de4d1b9843413a13f02')
    version('0.09.5', commit='12b11fe8b0d428ccb8e92dda7dc809198f828672')
    version('0.09.4', commit='e5dd9fbe179201e70347d1a3b9fa1899c226798f')
    version('0.09.3', commit='a8f31303ee8720ed2946bfe2d59e81d0f70e307e')
    version('0.09.2', commit='4e1f7fa73ffe07457080d787e206bf6466fe1680')
    version('0.09.1', commit='69c451035516cb683b8f7bc0bab1a25893e9113d')
    version('0.09.0', commit='004888b0a412f5bbaeef2ffaaeaf2aa182511494')
    version('0.08.2', commit='c5d7568714e69e7344582b93b8d24e45d6b81bf9')
    version('0.08.1', commit='289bdcc320f0b3ff1d792e29e462ec2d3ea15df6')
    version('0.08.0', commit='99eedb38f305e3a1cd99d9b4473241b7cd641fa9')

    # Variants that affect the core Acts library
    variant('benchmarks', default=False, description='Build the performance benchmarks')
    variant('examples', default=False, description='Build the examples')
    variant('integration_tests', default=False, description='Build the integration tests')
    variant('unit_tests', default=False, description='Build the unit tests')
    variant('log_failure_threshold', default='MAX', description='Log level above which examples should auto-crash')

    # Variants that enable / disable Acts plugins
    variant('autodiff', default=False, description='Build the auto-differentiation plugin')
    variant('dd4hep', default=False, description='Build the DD4hep plugin')
    variant('digitization', default=False, description='Build the geometric digitization plugin')
    variant('fatras', default=False, description='Build the FAst TRAcking Simulation package')
    variant('fatras_geant4', default=False, description='Build Geant4 Fatras package')
    variant('identification', default=False, description='Build the Identification plugin')
    variant('json', default=False, description='Build the Json plugin')
    variant('legacy', default=False, description='Build the Legacy package')
    # FIXME: Cannot build ONNX plugin as Spack doesn't have an ONNX runtime
    # FIXME: Cannot build SyCL plugin yet as Spack doesn't have SyCL support
    variant('tgeo', default=False, description='Build the TGeo plugin')

    # Variants that only affect Acts examples for now
    variant('geant4', default=False, description='Build the Geant4-based examples')
    variant('hepmc3', default=False, description='Build the HepMC3-based examples')
    variant('pythia8', default=False, description='Build the Pythia8-based examples')

    # Build dependencies
    # FIXME: Use spack's autodiff package once there is one
    depends_on('boost @1.62:1.69.99 +program_options +test', when='@:0.10.3')
    depends_on('boost @1.71: +filesystem +program_options +test', when='@0.10.4:')
    depends_on('cmake @3.14:', type='build')
    depends_on('dd4hep @1.11:', when='+dd4hep')
    depends_on('dd4hep @1.11: +geant4', when='+dd4hep +geant4')
    depends_on('eigen @3.3.7:', type='build')
    depends_on('geant4', when='+fatras_geant4')
    depends_on('geant4', when='+geant4')
    depends_on('hepmc3 @3.2.1:', when='+hepmc3')
    depends_on('heppdt', when='+hepmc3 @:4.0')
    depends_on('intel-tbb @2020.1:', when='+examples')
    depends_on('nlohmann-json @3.9.1:', when='@0.14: +json')
    depends_on('pythia8', when='+pythia8')
    depends_on('root @6.10: cxxstd=14', when='+tgeo @:0.8.0')
    depends_on('root @6.20: cxxstd=17', when='+tgeo @0.8.1:')

    # Some variant combinations do not make sense
    conflicts('+autodiff', when='@:1.01')
    conflicts('+benchmarks', when='@:0.15')
    conflicts('+dd4hep', when='-tgeo')
    conflicts('+examples', when='@:0.22')
    conflicts('+examples', when='-digitization')
    conflicts('+examples', when='-fatras')
    conflicts('+examples', when='-identification')
    conflicts('+examples', when='-json')
    conflicts('+examples', when='-tgeo')
    conflicts('+fatras', when='@:0.15')
    conflicts('+geant4', when='@:0.22')
    conflicts('+geant4', when='-examples')
    conflicts('+hepmc3', when='@:0.22')
    conflicts('+hepmc3', when='-examples')
    conflicts('+pythia8', when='@:0.22')
    conflicts('+pythia8', when='-examples')
    conflicts('+tgeo', when='-identification')
    conflicts('%gcc@:7', when='@0.23:')

    def cmake_args(self):
        spec = self.spec

        def cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies('+' + spack_variant)
            return "-DACTS_BUILD_{0}={1}".format(cmake_label, enabled)

        def example_cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies('+examples +' + spack_variant)
            return "-DACTS_BUILD_EXAMPLES_{0}={1}".format(cmake_label, enabled)

        def plugin_label(plugin_name):
            if spec.satisfies('@0.33:'):
                return "PLUGIN_" + plugin_name
            else:
                return plugin_name + "_PLUGIN"

        def plugin_cmake_variant(plugin_name, spack_variant):
            return cmake_variant(plugin_label(plugin_name), spack_variant)

        integration_tests_label = "INTEGRATIONTESTS"
        unit_tests_label = "UNITTESTS"
        legacy_plugin_label = "LEGACY_PLUGIN"
        if spec.satisfies('@:0.15'):
            integration_tests_label = "INTEGRATION_TESTS"
            unit_tests_label = "TESTS"
        if spec.satisfies('@:0.32'):
            legacy_plugin_label = "LEGACY"

        args = [
            plugin_cmake_variant("AUTODIFF", "autodiff"),
            cmake_variant("BENCHMARKS", "benchmarks"),
            plugin_cmake_variant("CUDA", "cuda"),
            plugin_cmake_variant("DD4HEP", "dd4hep"),
            plugin_cmake_variant("DIGITIZATION", "digitization"),
            cmake_variant("EXAMPLES", "examples"),
            example_cmake_variant("DD4HEP", "dd4hep"),
            example_cmake_variant("GEANT4", "geant4"),
            example_cmake_variant("HEPMC3", "hepmc3"),
            example_cmake_variant("PYTHIA8", "pythia8"),
            cmake_variant("FATRAS", "fatras"),
            cmake_variant("FATRAS_GEANT4", "fatras_geant4"),
            plugin_cmake_variant("IDENTIFICATION", "identification"),
            cmake_variant(integration_tests_label, "integration_tests"),
            plugin_cmake_variant("JSON", "json"),
            cmake_variant(unit_tests_label, "unit_tests"),
            cmake_variant(legacy_plugin_label, "legacy"),
            plugin_cmake_variant("TGEO", "tgeo")
        ]

        log_failure_threshold = spec.variants['log_failure_threshold'].value
        args.append("-DACTS_LOG_FAILURE_THRESHOLD={0}".format(log_failure_threshold))

        cuda_arch = spec.variants['cuda_arch'].value
        if cuda_arch != 'none':
            args.append('-DCUDA_FLAGS=-arch=sm_{0}'.format(cuda_arch[0]))

        if 'root' in spec:
            cxxstd = spec['root'].variants['cxxstd'].value
            args.append("-DCMAKE_CXX_STANDARD={0}".format(cxxstd))

        # FIXME: Once we can use spack's autodiff package, set
        #        ACTS_USE_SYSTEM_AUTODIFF too.
        if spec.satisfies('@0.33: +json'):
            args.append("-DACTS_USE_SYSTEM_NLOHMANN_JSON=ON")
        elif spec.satisfies('@0.14.0: +json'):
            args.append("-DACTS_USE_BUNDLED_NLOHMANN_JSON=OFF")

        return args
