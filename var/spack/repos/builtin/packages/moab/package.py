# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Moab(AutotoolsPackage):
    """MOAB is a component for representing and evaluating mesh
    data. MOAB can store structured and unstructured mesh, consisting
    of elements in the finite element 'zoo.' The functional interface
    to MOAB is simple yet powerful, allowing the representation of
    many types of metadata commonly found on the mesh. MOAB is
    optimized for efficiency in space and time, based on access to
    mesh in chunks rather than through individual entities, while also
    versatile enough to support individual entity access."""

    homepage = "https://sigma.mcs.anl.gov/moab-library"
    git = "https://bitbucket.org/fathomteam/moab.git"
    url = "https://web.cels.anl.gov/projects/sigma/downloads/moab/moab-5.5.1.tar.gz"

    maintainers("vijaysm", "iulian787")

    license("LGPL-3.0-only")

    version("develop", branch="develop")
    version("master", branch="master")
    version("5.5.1", sha256="67b6ed3a13c235cec16f60f8f46f9bf0371fd321cf36dea113d0e09f09d0d438")
    version("5.5.0", sha256="58969f8a1b209ec9036c08c53a6b7078b368eb3bf99d0368a4de5a2f2a8db678")
    version("5.4.1", sha256="3625e25321bf37f88d98438f5d56c280b2774172602d8b6eb6c34eedf37686fc")
    version("5.4.0", sha256="a30d2a1911fbf214ae0175b0856e0475c0077dc51ea5914c850d631155a72952")
    version("5.3.1", sha256="2404fab2d84f87be72b57cfef5ea237bfa444aaca059e66a158f22134956fe54")
    version("5.3.0", sha256="51c31ccbcaa76d9658a44452b9a39f076b795b27a1c9f408fc3d0eea97e032ef")
    version("5.2.1", sha256="60d31762be3f0e5c89416c764e844ec88dac294169b59a5ead3c316b50f85c29")
    version("5.2.0", sha256="805ed3546deff39e076be4d1f68aba1cf0dda8c34ce43e1fc179d1aff57c5d5d")
    version("5.1.0", sha256="0371fc25d2594589e95700739f01614f097b6157fb6023ed8995e582726ca658")
    version("5.0.0", sha256="df5d5eb8c0d0dbb046de2e60aa611f276cbf007c9226c44a24ed19c570244e64")
    version("4.9.2", sha256="26611b8cc24f6b7df52eb4ecbd31523d61523da0524b5a2d066a7656e2e82ac5")
    version("4.9.1", sha256="b26cee46c096157323cafe047ad58616e16ebdb1e06caf6878673817cb4410cf")
    version("4.9.0", sha256="267a7c05da847e4ea856db2c649a5484fb7bdc132ab56721ca50ee69a7389f4d")
    version("4.8.2", sha256="b105cff42930058dc14eabb9a25e979df7289b175732fe319d2494e83e09e968")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallelism support")
    variant("hdf5", default=True, description="Enable the HDF5 (default I/O) format")
    variant("netcdf", default=False, description="Enable the ExodusII reader/writer support")
    variant("pnetcdf", default=False, description="Enable parallel-Netcdf library support")
    variant("zoltan", default=True, description="Enable Zoltan partitioner support")
    variant("eigen", default=True, description="Enable Eigen template library for linear algebra")
    variant("cgm", default=False, description="Enable the Common Geometry Module")
    variant("metis", default=False, description="Enable Metis partitioner")
    variant("parmetis", default=False, description="Enable Parmetis partitioner")
    variant("irel", default=False, description="Enable iRel interface")
    variant("fbigeom", default=False, description="Enable FBiGeom interface")
    variant("coupler", default=False, description="Enable mbcoupler tool")
    variant("dagmc", default=False, description="Enable DagMC tool")

    variant("debug", default=False, description="Enable debug symbols in libraries")
    variant("shared", default=False, description="Enables the build of shared libraries")
    variant("fortran", default=False, description="Enable Fortran support")

    conflicts("+irel", when="~cgm")
    conflicts("+pnetcdf", when="~mpi")
    conflicts("+parmetis", when="~mpi")
    conflicts("+coupler", when="~mpi")

    # There are many possible variants for MOAB. Here are examples for
    # two of them:
    #
    # variant('vtk', default=False, description='Enable VTK support')
    # variant('cgns', default=False, description='Enable CGNS support')
    # depends_on('cgns', when='+cgns')
    # depends_on('vtk', when='+vtk')

    depends_on("autoconf", type="build", when="@master,5.0.1:")
    depends_on("automake", type="build", when="@master,5.0.1:")
    depends_on("libtool", type="build", when="@master,5.0.1:")
    depends_on("m4", type="build", when="@master,5.0.1:")
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("parallel-netcdf", when="+pnetcdf")
    depends_on("cgm", when="+cgm")
    depends_on("metis", when="+metis")
    depends_on("parmetis", when="+parmetis")
    depends_on("eigen", when="+eigen")
    # FIXME it seems that zoltan needs to be built without fortran
    depends_on("zoltan~fortran", when="+zoltan")

    patch("tools-492.patch", when="@4.9.2")

    @run_before("configure")
    def remove_march_native(self):
        filter_file("-march=native", "", "configure", string=True)

    def configure_args(self):
        spec = self.spec

        options = [
            "--enable-optimize",
            "--disable-vtkMOABReader",
            "--disable-mbtagprop",
            "--disable-mbmem",
            "--disable-spheredecomp",
            "--disable-mbsurfplot",
            "--disable-gsets",
            "--disable-mcnpmit",
            "--disable-refiner",
            "--disable-h5mtools",
            "--disable-mbcslam",
            "--with-pic",
            "--without-vtk",
        ]
        if "+mpi" in spec:
            options.extend(
                [
                    "--with-mpi=%s" % spec["mpi"].prefix,
                    "CXX=%s" % spec["mpi"].mpicxx,
                    "CC=%s" % spec["mpi"].mpicc,
                    "FC=%s" % spec["mpi"].mpifc,
                ]
            )
            if "+parmetis" in spec:
                options.append("--with-parmetis=%s" % spec["parmetis"].prefix)
            else:
                options.append("--without-parmetis")

        options.append("--with-blas=%s" % spec["blas"].libs.ld_flags)
        options.append("--with-lapack=%s" % spec["lapack"].libs.ld_flags)
        if "+eigen" in spec:
            options.append("--with-eigen3=%s" % spec["eigen"].prefix.include.eigen3)

        if "+hdf5" in spec:
            options.append("--with-hdf5=%s" % spec["hdf5"].prefix)
        else:
            options.append("--without-hdf5")

        if "+netcdf" in spec:
            options.append("--with-netcdf=%s" % spec["netcdf-c"].prefix)
        else:
            options.append("--without-netcdf")

        if "+pnetcdf" in spec:
            options.append("--with-pnetcdf=%s" % spec["parallel-netcdf"].prefix)
        else:
            options.append("--without-pnetcdf")

        if "+cgm" in spec:
            options.append("--with-cgm=%s" % spec["cgm"].prefix)
            if "+irel" in spec:
                options.append("--enable-irel")
            else:
                options.append("--disable-irel")
        else:
            options.append("--without-cgm")
        if "+fbigeom" in spec:
            options.append("--enable-fbigeom")
        else:
            options.append("--disable-fbigeom")

        if "+coupler" in spec:
            options.append("--enable-mbcoupler")
        else:
            options.append("--disable-mbcoupler")

        if "+dagmc" in spec:
            options.append("--enable-dagmc")
        else:
            options.append("--disable-dagmc")

        if "+metis" in spec:
            options.append("--with-metis=%s" % spec["metis"].prefix)
        else:
            options.append("--without-metis")

        if "+parmetis" in spec:
            options.append("--with-parmetis=%s" % spec["parmetis"].prefix)
        else:
            options.append("--without-parmetis")

        if "+zoltan" in spec:
            options.append("--with-zoltan=%s" % spec["zoltan"].prefix)
        else:
            options.append("--without-zoltan")

        if "+debug" in spec:
            options.append("--enable-debug")
        else:
            options.append("--disable-debug")

        # FIXME it seems that with cgm and shared, we have a link
        #   issue  in tools/geometry
        if "+shared" in spec:
            options.append("--enable-shared")
        else:
            options.append("--disable-shared")

        if "~fortran" in spec:
            options.append("--disable-fortran")
        else:
            options.append("--enable-fortran")

        return options

    # Run the install phase in parallel
    def install(self, spec, prefix):
        make("install", parallel=True)
