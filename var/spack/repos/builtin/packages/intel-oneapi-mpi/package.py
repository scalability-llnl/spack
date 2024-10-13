# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel MPI Library is a multifabric message-passing library that
    implements the open-source MPICH specification. Use the library
    to create, maintain, and test advanced, complex applications
    that perform better on high-performance computing (HPC)
    clusters based on Intel processors.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html"

    version(
        "2021.13.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/364c798c-4cad-4c01-82b5-e1edd1b476af/l_mpi_oneapi_p_2021.13.1.769_offline.sh",
        sha256="be61c4792d25bd4a1b5f7b808c06a9f4676f1b247d7605ac6d3c6cffdb8f19b7",
        expand=False,
    )
    version(
        "2021.13.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/9f84e1e8-11b2-4bd1-8512-3e3343585956/l_mpi_oneapi_p_2021.13.0.719_offline.sh",
        sha256="5e23cf495c919e17032577e3059438f632297ee63f2cdb906a2547298823cc64",
        expand=False,
    )
    version(
        "2021.12.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/56b2dd0e-954d-4330-b0a7-b22992f7e6b7/l_mpi_oneapi_p_2021.12.1.8_offline.sh",
        sha256="6a4cd82ff1c64eac2a7ac3784ea2dc3a0e32740fb7e7bc6a1aa48740d5011b2f",
        expand=False,
    )
    version(
        "2021.12.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/749f02a5-acb8-4bbb-91db-501ff80d3f56/l_mpi_oneapi_p_2021.12.0.538_offline.sh",
        sha256="6ccfc35784ec86d898f4c1cedf82c4f71926123a12db64111f67e7d0286bbb2d",
        expand=False,
    )
    version(
        "2021.11.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/2c45ede0-623c-4c8e-9e09-bed27d70fa33/l_mpi_oneapi_p_2021.11.0.49513_offline.sh",
        sha256="9a96caeb7abcf5aa08426216db38a2c7936462008b9825036266bc79cb0e30d8",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4f5871da-0533-4f62-b563-905edfb2e9b7/l_mpi_oneapi_p_2021.10.0.49374_offline.sh",
        sha256="ab2e97d87b139201a2e7dab9a61ac6e8927b7783b459358c4ad69a1b1c064f40",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/718d6f8f-2546-4b36-b97b-bc58d5482ebf/l_mpi_oneapi_p_2021.9.0.43482_offline.sh",
        sha256="5c170cdf26901311408809ced28498b630a494428703685203ceef6e62735ef8",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19131/l_mpi_oneapi_p_2021.8.0.25329_offline.sh",
        sha256="0fcb1171fc42fd4b2d863ae474c0b0f656b0fa1fdc1df435aa851ccd6d1eaaf7",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19010/l_mpi_oneapi_p_2021.7.1.16815_offline.sh",
        sha256="90e7804f2367d457cd4cbf7aa29f1c5676287aa9b34f93e7c9a19e4b8583fff7",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18926/l_mpi_oneapi_p_2021.7.0.8711_offline.sh",
        sha256="4eb1e1487b67b98857bc9b7b37bcac4998e0aa6d1b892b2c87b003bf84fb38e9",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18714/l_mpi_oneapi_p_2021.6.0.602_offline.sh",
        sha256="e85db63788c434d43c1378e5e2bf7927a75d11aee8e6b78ee0d933da920977a6",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18471/l_mpi_oneapi_p_2021.5.1.515_offline.sh",
        sha256="b992573959e39752e503e691564a0d876b099547c38b322d5775c5b06ec07a7f",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18370/l_mpi_oneapi_p_2021.5.0.495_offline.sh",
        sha256="3aae53fe77f7c6aac7a32b299c25d6ca9a00ba4e2d512a26edd90811e59e7471",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18186/l_mpi_oneapi_p_2021.4.0.441_offline.sh",
        sha256="cc4b7072c61d0bd02b1c431b22d2ea3b84b967b59d2e587e77a9e7b2c24f2a29",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17947/l_mpi_oneapi_p_2021.3.0.294_offline.sh",
        sha256="04c48f864ee4c723b1b4ca62f2bea8c04d5d7e3de19171fd62b17868bc79bc36",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17729/l_mpi_oneapi_p_2021.2.0.215_offline.sh",
        sha256="d0d4cdd11edaff2e7285e38f537defccff38e37a3067c02f4af43a3629ad4aa3",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17397/l_mpi_oneapi_p_2021.1.1.76_offline.sh",
        sha256="8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe",
        expand=False,
    )

    variant("ilp64", default=False, description="Build with ILP64 support")
    variant(
        "generic-names",
        default=False,
        description="Use generic names, e.g mpicc instead of mpiicx",
    )
    variant(
        "classic-names",
        default=False,
        description="Use classic compiler names, e.g mpiicc instead of mpiicx",
    )
    variant(
        "external-libfabric", default=False, description="Enable external libfabric dependency"
    )
    depends_on("libfabric", when="+external-libfabric", type=("link", "run"))

    provides("mpi@:3.1")
    conflicts("+generic-names +classic-names")

    @property
    def mpiexec(self):
        return self.component_prefix.bin.mpiexec

    @property
    def v2_layout_versions(self):
        return "@2021.11:"

    @property
    def component_dir(self):
        return "mpi"

    @property
    def env_script_args(self):
        if self.spec.satisfies("+external-libfabric"):
            return ("-i_mpi_ofi_internal=0",)
        else:
            return ()

    def wrapper_names(self):
        if self.spec.satisfies("+generic-names"):
            return ["mpicc", "mpicxx", "mpif77", "mpif90", "mpifc"]
        elif self.spec.satisfies("+classic-names"):
            return ["mpiicc", "mpiicpc", "mpiifort", "mpiifort", "mpiifort"]
        else:
            return ["mpiicx", "mpiicpx", "mpiifx", "mpiifx", "mpiifx"]

    def wrapper_paths(self):
        return [self.component_prefix.bin.join(name) for name in self.wrapper_names()]

    def setup_dependent_package(self, module, dep_spec):
        wrappers = self.wrapper_paths()
        self.spec.mpicc = wrappers[0]
        self.spec.mpicxx = wrappers[1]
        self.spec.mpif77 = wrappers[2]
        # no self.spec.mpif90
        self.spec.mpifc = wrappers[4]

    def setup_dependent_build_environment(self, env, dependent_spec):
        dependent_module = dependent_spec.package.module
        env.set("I_MPI_CC", dependent_module.spack_cc)
        env.set("I_MPI_CXX", dependent_module.spack_cxx)
        env.set("I_MPI_F77", dependent_module.spack_f77)
        env.set("I_MPI_F90", dependent_module.spack_fc)
        env.set("I_MPI_FC", dependent_module.spack_fc)

        # Set compiler wrappers for dependent build stage
        wrappers = self.wrapper_paths()
        env.set("MPICC", wrappers[0])
        env.set("MPICXX", wrappers[1])
        env.set("MPIF77", wrappers[2])
        env.set("MPIF90", wrappers[3])
        env.set("MPIFC", wrappers[4])

        env.set("I_MPI_ROOT", self.component_prefix)

    @property
    def libs(self):
        libs = []
        if self.spec.satisfies("+ilp64"):
            libs += find_libraries("libmpi_ilp64", self.component_prefix.lib.release)
        libs += find_libraries(["libmpicxx", "libmpifort"], self.component_prefix.lib)
        libs += find_libraries("libmpi", self.component_prefix.lib.release)
        libs += find_system_libraries(["libdl", "librt", "libpthread"])

        # Find libfabric for libmpi.so
        if self.spec.satisfies("+external-libfabric"):
            libs += self.spec["libfabric"].libs
        else:
            libs += find_libraries(["libfabric"], self.component_prefix.libfabric.lib)

        return libs

    @run_after("install")
    def fix_wrappers(self):
        # When spack builds from source
        # fix I_MPI_SUBSTITUTE_INSTALLDIR and
        #   __EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__
        for wrapper in ["mpif77", "mpif90", "mpigcc", "mpigxx", "mpiicc", "mpiicpc", "mpiifort"]:
            filter_file(
                r"I_MPI_SUBSTITUTE_INSTALLDIR|" r"__EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__",
                self.component_prefix,
                self.component_prefix.bin.join(wrapper),
                backup=False,
            )

    @run_after("install")
    def fixup_prefix(self):
        # The motivation was to provide a more standard layout so impi
        # would be more likely to work as a virtual dependence.  It
        # does not work for v2_layout because of a library conflict. I
        # am not sure if this mechanism is useful so disabling for
        # v2_layout rather than try to make it work.
        if self.v2_layout:
            return
        self.symlink_dir(self.component_prefix.include, self.prefix.include)
        self.symlink_dir(self.component_prefix.lib, self.prefix.lib)
        self.symlink_dir(self.component_prefix.lib.release, self.prefix.lib)
        self.symlink_dir(self.component_prefix.bin, self.prefix.bin)
