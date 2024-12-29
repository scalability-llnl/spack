# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Converge(Package):
    """CONVERGE is a revolutionary computational fluid dynamics (CFD) program
    that eliminates the grid generation bottleneck from the simulation process.
    CONVERGE was developed by engine simulation experts and is straightforward
    to use for both engine and non-engine simulations. Unlike many CFD
    programs, CONVERGE automatically generates a perfectly orthogonal,
    structured grid at runtime based on simple, user-defined grid control
    parameters. This grid generation method completely eliminates the need to
    manually generate a grid. In addition, CONVERGE offers many other features
    to expedite the setup process and to ensure that your simulations are as
    computationally efficient as possible."""

    homepage = "https://www.convergecfd.com/"
    url = "https://download.convergecfd.com/download/CONVERGE_2.4/Full_Solver_Packages/converge_install_2.4.10.tar.gz"

    # In order to view available versions, you need to register for an account:
    # https://download.convergecfd.com/wp-login.php?action=register

    version("2.4.10", sha256="5d3c39894598d2395149cfcc653af13b8b1091177290edd62fcf22c7e830d410")
    version("2.3.23", sha256="1217d16eaf9d263f917ee468778508bad9dacb7e4397a293cfa6467f39fb4c52")
    version(
        "2.2.0",
        sha256="3885acbaf352c718ea69f0206c858a01be02f0928ffee738e4aceb1dd939a77a",
        url="https://download.convergecfd.com/download/CONVERGE_2.2/Full_Solver_Packages/converge_install_2.2.0_042916.tar.gz",
    )
    version(
        "2.1.0",
        sha256="6b8896d42cf7b9013cae5456f4dc118306a5bd271d4a15945ceb7dae913e825a",
        url="https://download.convergecfd.com/download/CONVERGE_2.1/Full_Solver_Packages/converge_install_2.1.0_111615.tar.gz",
    )
    version(
        "2.0.0",
        sha256="f32c4824eb33724d85e283481d67ebd0630b1406011c528d775028bb2546f34e",
        url="https://download.convergecfd.com/download/CONVERGE_2.0/Full_Solver_Packages/converge_install_2.0.0_090214.tar.gz",
    )

    variant("mpi", default=True, description="Build with MPI support")

    # The following MPI libraries are compatible with CONVERGE:
    #
    # +--------------+---------+---------+---------+---------+---------+
    # | MPI Packages |  v2.0   |  v2.1   |  v2.2   |  v2.3   |  v2.4   |
    # +--------------+---------+---------+---------+---------+---------+
    # | HP-MPI       | 2.0.3+  | 2.0.3+  | 2.0.3+  | 2.0.3+  |         |
    # | Intel MPI    |         |         |         |         | 17.0.98 |
    # | MPICH        | ?.?.?   | ?.?.?   | 1.2.1   | 3.1.4   | ?.?.?   |
    # | MVAPICH2     | ?.?.?   |         |         |         |         |
    # | Open MPI     | 1.0-1.4 | 1.0-1.4 | 1.5-1.8 | 1.5-1.8 | 1.10    |
    # | Platform MPI |         |         | 9.1.2   | 9.1.2   | 9.1.2   |
    # +--------------+---------+---------+---------+---------+---------+
    #
    # NOTE: HP-MPI was bought out by Platform MPI
    #
    # These version requirements are more strict than for most packages.
    # Since the tarball comes with pre-compiled executables,
    # the version of libmpi.so must match exactly, or else
    # you will end up with missing libraries and symbols.

    depends_on("mpi", when="+mpi")

    # TODO: Add version ranges for other MPI libraries
    depends_on("openmpi@1.10.0:1.10", when="@2.4.0:2.4+mpi^[virtuals=mpi] openmpi")
    depends_on("openmpi@1.5:1.8", when="@2.2:2.3+mpi^[virtuals=mpi] openmpi")
    depends_on("openmpi@:1.4", when="@:2.1+mpi^[virtuals=mpi] openmpi")

    conflicts("^intel-mpi", when="@:2.3")
    conflicts("^intel-parallel-studio+mpi", when="@:2.3")
    conflicts("^spectrum-mpi")

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["license/license.lic"]
    license_vars = ["RLM_LICENSE"]
    license_url = "https://www.reprisesoftware.com/RLM_License_Administration.pdf"

    def url_for_version(self, version):
        url = "https://download.convergecfd.com/download/CONVERGE_{0}/Full_Solver_Packages/converge_install_{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def install(self, spec, prefix):
        # 2.0.0
        # converge                      -> converge-2.0.0-hpmpi-090214
        # converge-2.0.0-hpmpi-090214   -> libmpi.so.1, libmpio.so.1
        # converge-2.0.0-mpich2-090214  -> libmpich.so.1.2
        # converge-2.0.0-mvapich-090214 -> libibumad.so.1
        # converge-2.0.0-openmpi-090214 -> libmpi.so.0
        # converge-2.0.0-serial-090214
        # make_surface
        # post_convert

        # 2.1.0
        # converge                      -> converge-2.1.0-hpmpi-111615
        # converge-2.1.0-hpmpi-111615   -> libmpi.so.1, libmpio.so.1
        # converge-2.1.0-mpich2-111615  -> libmpich.so.1.2
        # converge-2.1.0-openmpi-111615 -> libmpi.so.0
        # converge-2.1.0-serial-111615
        # make_surface
        # post_convert

        # 2.2.0
        # converge                      -> converge-2.2.0-hpmpi-042916
        # converge-2.2.0-hpmpi-042916   -> libmpi.so.1, libmpio.so.1
        # converge-2.2.0-mpich2-042916
        # converge-2.2.0-openmpi-042916 -> libmpi.so.1
        # converge-2.2.0-pmpi-042916    -> libmpi.so.1, libmpio.so.1
        # converge-2.2.0-serial-042916
        # make_surface
        # post_convert

        # 2.3.23
        # converge-2.3.23-hpmpi-linux-64    -> libmpi.so.1, libmpio.so.1
        # converge-2.3.23-mpich2-linux-64   -> libmpi.so.12
        # converge-2.3.23-openmpi-linux-64  -> libmpi.so.1
        # converge-2.3.23-pmpi-linux-64     -> libmpi.so.1, libmpio.so.1
        # converge-2.3.23-serial-linux-64
        # make_surface_64
        # post_convert_mpich_64             -> libmpi.so.12
        # post_convert_ompi_64              -> libmpi.so.1
        # post_convert_pmpi_64              -> libmpi.so.1, libmpio.so.1
        # post_convert_serial_64

        # 2.4.10
        # converge-2.4.10-intel     -> libmpi.so.12, libmpifort.so.12
        # converge-2.4.10-mpich     -> libmpi.so.12
        # converge-2.4.10-ompi      -> libmpi.so.12
        # converge-2.4.10-pmpi      -> libmpi.so.1, libmpio.so.1
        # converge-2.4.10-serial
        # make_surface_64
        # post_convert_mpich_64     -> libmpi.so.12
        # post_convert_ompi_64      -> libmpi.so.1
        # post_convert_pmpi_64      -> libmpi.so.1
        # post_convert_serial_64

        # The CONVERGE tarball comes with binaries for several MPI libraries.
        # Only install the binary that matches the MPI we are building with.
        with working_dir("l_x86_64/bin"):
            if spec.satisfies("~mpi"):
                converge = glob.glob("converge-*-serial*")
                post_convert = glob.glob("post_convert_serial*")
            elif spec.satisfies("^hp-mpi"):
                converge = glob.glob("converge-*-hpmpi*")
                # No HP-MPI version of post_convert
                post_convert = glob.glob("post_convert_serial*")
            elif spec.satisfies("intel-mpi") or spec.satisfies("intel-parallel-studio+mpi"):
                converge = glob.glob("converge-*-intel*")
                # No Intel MPI version of post_convert
                post_convert = glob.glob("post_convert_serial*")
            elif spec.satisfies("^mpich"):
                converge = glob.glob("converge-*-mpich*")
                post_convert = glob.glob("post_convert_mpich*")
            elif spec.satisfies("^mvapich2"):
                converge = glob.glob("converge-*-mvapich*")
                # MVAPICH2 hasn't been supported since CONVERGE
                # came with a single serial post_convert
                post_convert = glob.glob("post_convert")
            elif spec.satisfies("^openmpi"):
                converge = glob.glob("converge-*-o*mpi*")
                post_convert = glob.glob("post_convert_o*mpi*")
            elif spec.satisfies("^platform-mpi"):
                converge = glob.glob("converge-*-pmpi*")
                post_convert = glob.glob("post_convert_pmpi*")
            else:
                raise InstallError("Unsupported MPI provider")

            make_surface = glob.glob("make_surface*")

            # Old versions of CONVERGE come with a single serial post_convert
            if not post_convert:
                post_convert = glob.glob("post_convert")

            # Make sure glob actually found something
            if not converge:
                raise InstallError("converge executable not found")
            if not post_convert:
                raise InstallError("post_convert executable not found")
            if not make_surface:
                raise InstallError("make_surface executable not found")

            # Make sure glob didn't find multiple matches
            if len(converge) > 1:
                raise InstallError("multiple converge executables found")
            if len(post_convert) > 1:
                raise InstallError("multiple post_convert executables found")
            if len(make_surface) > 1:
                raise InstallError("multiple make_surface executables found")

            converge = converge[0]
            post_convert = post_convert[0]
            make_surface = make_surface[0]

            mkdir(prefix.bin)

            # Install the executables
            install(converge, join_path(prefix.bin, converge))
            install(post_convert, join_path(prefix.bin, post_convert))
            install(make_surface, join_path(prefix.bin, make_surface))

        with working_dir(prefix.bin):
            # Create generic symlinks to all executables
            if not os.path.exists("converge"):
                os.symlink(converge, "converge")
            if not os.path.exists("post_convert"):
                os.symlink(post_convert, "post_convert")
            if not os.path.exists("make_surface"):
                os.symlink(make_surface, "make_surface")

    def setup_run_environment(self, env):
        # CONVERGE searches for a valid license file in:
        #     $CONVERGE_ROOT/license/license.lic
        env.set("CONVERGE_ROOT", self.prefix)
