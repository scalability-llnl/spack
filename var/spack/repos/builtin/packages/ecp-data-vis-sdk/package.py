# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# Wrapper around depends_on to propagate dependency variants
def dav_sdk_depends_on(spec, when=None, propagate=None):
    # Do the basic depends_on
    depends_on(spec, when=when)

    # Strip spec string to just the base spec name
    # ie. A +c ~b -> A
    spec = Spec(spec).name

    # If the package is in the spec tree then it must be enabled in the SDK.
    if "+" in when:
        _when_variants = when.strip("+").split("+")
        if any(tok in when for tok in ["~", "="]):
            tty.error("Bad token in when clause, only positive boolean tokens allowed")

        for variant in _when_variants:
            conflicts("~" + variant, when="^" + spec)

    # Skip if there is nothing to propagate
    if not propagate:
        return

    # Map the propagated variants to the dependency variant.  Some packages may need
    # overrides to propagate a dependency as something else, e.g., {"visit": "libsim"}.
    # Most call-sites will just use a list.
    if not type(propagate) is dict:
        propagate = dict([(v, v) for v in propagate])

    # Determine the base variant
    base_variant = ""
    if when:
        base_variant = when

    def is_boolean(variant):
        return "=" not in variant

    # Propagate variants to dependecy
    for v_when, v_then in propagate.items():
        if is_boolean(v_when):
            depends_on(
                "{0} +{1}".format(spec, v_then), when="{0} +{1}".format(base_variant, v_when)
            )
            depends_on(
                "{0} ~{1}".format(spec, v_then), when="{0} ~{1}".format(base_variant, v_when)
            )
        else:
            depends_on("{0} {1}".format(spec, v_then), when="{0} {1}".format(base_variant, v_when))


def exclude_variants(variants, exclude):
    return [variant for variant in variants if variant not in exclude]


class EcpDataVisSdk(BundlePackage, CudaPackage, ROCmPackage):
    """ECP Data & Vis SDK"""

    homepage = "https://ecp-data-vis-sdk.github.io/"

    tags = ["ecp"]
    maintainers("kwryankrattiger", "svenevs")

    version("1.0")

    ############################################################
    # Variants
    ############################################################

    # I/O
    variant("adios2", default=False, description="Enable ADIOS2")
    variant("darshan", default=False, description="Enable Darshan")
    variant("faodel", default=False, description="Enable FAODEL")
    variant("hdf5", default=False, description="Enable HDF5")
    variant("pnetcdf", default=False, description="Enable PNetCDF")
    variant("unifyfs", default=False, description="Enable UnifyFS")
    variant("veloc", default=False, description="Enable VeloC")

    # Vis
    variant("ascent", default=False, description="Enable Ascent")
    variant("cinema", default=False, description="Enable Cinema")
    variant("paraview", default=False, description="Enable ParaView")
    variant("sensei", default=False, description="Enable Sensei")
    variant("sz", default=False, description="Enable SZ")
    variant("visit", default=False, description="Enable VisIt")
    variant("vtkm", default=False, description="Enable VTK-m")
    variant("zfp", default=False, description="Enable ZFP")

    # Language Options
    variant("fortran", default=True, sticky=True, description="Enable fortran language features.")

    ############################################################
    # Dependencies
    ############################################################
    cuda_arch_variants = ["cuda_arch={0}".format(x) for x in CudaPackage.cuda_arch_values]
    amdgpu_target_variants = ["amdgpu_target={0}".format(x) for x in ROCmPackage.amdgpu_targets]

    dav_sdk_depends_on(
        "adios2+shared+mpi+python+sst+dataman",
        when="+adios2",
        propagate=["cuda", "hdf5", "sz", "zfp", "fortran"] + cuda_arch_variants,
    )

    dav_sdk_depends_on("darshan-runtime+mpi", when="+darshan")
    dav_sdk_depends_on("darshan-util", when="+darshan")

    dav_sdk_depends_on("faodel+shared+mpi network=libfabric", when="+faodel", propagate=["hdf5"])

    # HDF5 1.14 is a soft requirement for the ECP Data and Vis SDK.
    # When building with VisIt and CinemaSci in the same SDK environment there is a conflict
    # in the build dependency of py-setuptools which prevents building a py-h5py that is
    # compatible with 'hdf5@1.14:'. Until there is a version of VisIt with an updated VTK or Spack
    # allows the concretization of multiple versions of the same build only dependency
    # concretization with VisIt and Cinema variants will not allow building VOLs.
    dav_sdk_depends_on("hdf5@1.12: +shared+mpi", when="+hdf5", propagate=["fortran"])

    # HDF5 VOL Adapters require hdf5@1.14:

    # hdf5-vfd-gds needs cuda@11.7.1 or later, only enable when 11.7.1+ available.
    depends_on("hdf5-vfd-gds@1.0.2:", when="+cuda+hdf5 ^cuda@11.7.1: ^hdf5@1.14:")
    for cuda_arch in cuda_arch_variants:
        depends_on(
            "hdf5-vfd-gds@1.0.2: {0}".format(cuda_arch),
            when="+cuda+hdf5 {0} ^cuda@11.7.1: ^hdf5@1.14:".format(cuda_arch),
        )
    conflicts("~cuda", when="^hdf5-vfd-gds@1.0.2:")
    conflicts("~hdf5", when="^hdf5-vfd-gds@1.0.2:")
    conflicts("~hdf5", when="^hdf5-vol-async")
    conflicts("~hdf5", when="^hdf5-vol-cache")
    conflicts("~hdf5", when="^hdf5-vol-log")
    depends_on("hdf5-vol-async", when="+hdf5 ^hdf5@1.14:")
    depends_on("hdf5-vol-cache", when="+hdf5 ^hdf5@1.14:")
    depends_on("hdf5-vol-log", when="+hdf5 ^hdf5@1.14:")

    dav_sdk_depends_on("parallel-netcdf+shared", when="+pnetcdf", propagate=["fortran"])

    dav_sdk_depends_on("unifyfs", when="+unifyfs ")
    conflicts("^unifyfs@develop")

    dav_sdk_depends_on("veloc", when="+veloc")

    # Skipping propagating ascent, catalyst(paraview), and libsim(visit) to sensei
    # due to incomaptiblity between these variants in sensei.
    dav_sdk_depends_on("sensei@4: ~vtkio +python", when="+sensei", propagate=["adios2", "hdf5"])

    # Fortran support with ascent is problematic on some Cray platforms so the
    # SDK is explicitly disabling it until the issues are resolved.
    dav_sdk_depends_on(
        "ascent+mpi~fortran+python+shared+vtkh+dray~test",
        when="+ascent",
        propagate=["adios2", "cuda"] + cuda_arch_variants,
    )
    depends_on("ascent+openmp", when="~rocm+ascent")
    depends_on("ascent~openmp", when="+rocm+ascent")

    # Need to explicitly turn off conduit hdf5_compat in order to build
    # hdf5@1.12 which is required for SDK
    depends_on("conduit ~hdf5_compat", when="+ascent +hdf5")
    # Disable configuring with @develop. This should be removed after ascent
    # releases 0.8 and ascent can build with conduit@0.8: and vtk-m@1.7:
    conflicts("^ascent@develop", when="+ascent")

    depends_on("py-cinemasci", when="+cinema")

    # ParaView needs @5.11: in order to use CUDA/ROCM, therefore it is the minimum
    # required version since GPU capability is desired for ECP
    dav_sdk_depends_on(
        "paraview@5.11:+mpi+openpmd+python+kits+shared+catalyst+libcatalyst" " use_vtkm=on",
        when="+paraview",
        propagate=["adios2", "cuda", "hdf5", "rocm"] + amdgpu_target_variants + cuda_arch_variants,
    )
    dav_sdk_depends_on("libcatalyst@2:+mpi", when="+paraview")
    conflicts("^paraview@master", when="+paraview")

    dav_sdk_depends_on("visit+mpi+python+silo", when="+visit", propagate=["hdf5", "adios2"])

    dav_sdk_depends_on(
        "vtk-m@1.7:+shared+mpi+rendering",
        when="+vtkm",
        propagate=["cuda", "rocm"] + cuda_arch_variants + amdgpu_target_variants,
    )
    # TODO: When Ascent is updated to use VTK-m >= 1.8 move examples to
    # the main spec.
    conflicts("^vtk-m~examples", when="+vtkm ^vtk-m@1.8:")
    depends_on("vtk-m+openmp", when="~rocm+vtkm")
    depends_on("vtk-m~openmp", when="+rocm+vtkm")

    # +python is currently broken in sz
    # dav_sdk_depends_on('sz+shared+python+random_access',
    dav_sdk_depends_on("sz+shared+random_access", when="+sz", propagate=["hdf5", "fortran"])

    dav_sdk_depends_on("zfp", when="+zfp", propagate=["cuda"] + cuda_arch_variants)
