# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys
from copy import deepcopy

from spack.package import *


def xsdk_depends_on_accl(accl_name, accl_var, *args, **kwargs):
    if accl_name == "cuda":
        accl_arch_name = "cuda_arch"
        accl_arch_values = list(deepcopy(CudaPackage.cuda_arch_values))
    elif accl_name == "rocm":
        accl_arch_name = "amdgpu_target"
        accl_arch_values = list(deepcopy(ROCmPackage.amdgpu_targets))
    # require ~cuda when xsdk~cuda (and '?cuda' not used)
    usedep = 1
    args_new = list(deepcopy(args))
    if not isinstance(accl_var, list):
        accl_var = [accl_var]
    for idx, var in enumerate(accl_var):
        # skip variants starting with '?' so that
        # that that they are left unspecified by xsdk
        if not var.startswith("?"):
            args_new[0] += " ~%s" % var
        else:
            accl_var[idx] = var.replace("?", "")
        # if '?cuda' skip adding '~cuda' dep
        if var == "?" + accl_name:
            usedep = 0
    kwargs_new = deepcopy(kwargs)
    if "when" in kwargs_new:
        kwargs_new["when"] += " ~" + accl_name
    else:
        kwargs_new["when"] = "~" + accl_name
    if usedep:
        depends_on(*args_new, **kwargs_new)

    # require +cuda when xsdk+cuda, and match the arch
    for arch in accl_arch_values:
        args_new = list(deepcopy(args))
        kwargs_new = deepcopy(kwargs)
        args_new[0] += "+%s %s=%s" % ("+".join(accl_var), accl_arch_name, str(arch))
        if "when" in kwargs_new:
            kwargs_new["when"] += " +%s %s=%s" % (accl_name, accl_arch_name, str(arch))
        else:
            kwargs_new["when"] = "+%s %s=%s" % (accl_name, accl_arch_name, str(arch))
        depends_on(*args_new, **kwargs_new)


def xsdk_depends_on(spec, cuda_var="", rocm_var="", **kwargs):
    """
    Wrapper for depends_on which can handle propagating cuda and rocm
    variants.

    Currently, it propagates +cuda_var when xsdk+cuda and rocm_var
    when xsdk+rocm. When xsdk~[cuda|rocm], then ~[cuda|rocm]_var is
    selected unless the variant string is prefixed with a '?'
    (see the tasmanian use below). When '?' prefix is used, then
    the variant is left unspecified.

    [cuda|rocm]_var can be an array of variant strings or just a single
    variant string. The spack '+' and '~' symbols should not appear
    in the strings.
    """
    if bool(cuda_var):
        xsdk_depends_on_accl("cuda", cuda_var, spec, **kwargs)
    if bool(rocm_var):
        xsdk_depends_on_accl("rocm", rocm_var, spec, **kwargs)
    if not bool(cuda_var) and not bool(rocm_var):
        depends_on(spec, **kwargs)


class Xsdk(BundlePackage, CudaPackage, ROCmPackage):
    """Xsdk is a suite of Department of Energy (DOE) packages for numerical
    simulation. This is a Spack bundle package that installs the xSDK
    packages
    """

    homepage = "https://xsdk.info"
    maintainers("balay", "luszczek", "balos1", "shuds13", "v-dobrev")

    version("1.0.0")
    version("0.8.0", deprecated=True)

    variant("sycl", default=False, sticky=True, description="Enable sycl variant of xsdk packages")
    variant("trilinos", default=True, sticky=True, description="Enable trilinos package build")
    variant("datatransferkit", default=True, description="Enable datatransferkit package build")
    variant("amrex", default=True, description="Enable amrex package build")
    variant("omega-h", default=True, description="Enable omega-h package build")
    variant("strumpack", default=True, description="Enable strumpack package build")
    variant("dealii", default=True, description="Enable dealii package build")
    variant("alquimia", default=True, description="Enable alquimia package build")
    variant("phist", default=True, description="Enable phist package build")
    variant("ginkgo", default=True, description="Enable ginkgo package build")
    variant("libensemble", default=True, description="Enable py-libensemble package build")
    variant(
        "precice", default=(sys.platform != "darwin"), description="Enable precice package build"
    )
    variant("butterflypack", default=True, description="Enable butterflypack package build")
    variant("heffte", default=True, description="Enable heffte package build")
    variant("slate", default=(sys.platform != "darwin"), description="Enable slate package build")
    variant("arborx", default=True, description="Enable ArborX build")
    variant("exago", default=True, description="Enable exago build")
    variant("hiop", default=True, description="Enable hiop build")
    variant("raja", default=(sys.platform != "darwin"), description="Enable raja for hiop, exago")
    variant("pflotran", default=True, description="Enable pflotran package build")

    xsdk_depends_on(
        "hypre@2.30.0+superlu-dist+shared", when="@1.0.0", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on("hypre@2.26.0+superlu-dist+shared", when="@0.8.0", cuda_var="cuda")

    xsdk_depends_on(
        "mfem@4.6.0+shared+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@1.0.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "mfem@4.5.0+shared+mpi+superlu-dist+petsc+sundials+examples+miniapps",
        when="@0.8.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )

    xsdk_depends_on("superlu-dist@8.2.1", when="@1.0.0", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("superlu-dist@8.1.2", when="@0.8.0")

    xsdk_depends_on("trilinos +superlu-dist", when="@1.0.0: +trilinos ~cuda ~rocm")
    xsdk_depends_on(
        "trilinos@14.4.0+hypre+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards+stratimikos gotype=int"
        + " cxxstd=17",
        when="@1.0.0 +trilinos",
    )
    xsdk_depends_on(
        "trilinos@13.4.1+hypre+superlu-dist+hdf5~mumps+boost"
        + "~suite-sparse+tpetra+nox+ifpack2+zoltan+zoltan2+amesos2"
        + "~exodus~dtk+intrepid2+shards+stratimikos gotype=int"
        + " cxxstd=14",
        when="@0.8.0 +trilinos",
    )

    xsdk_depends_on("datatransferkit@3.1.1", when="@1.0.0 +trilinos +datatransferkit")
    dtk7ver = "3.1-rc2" if sys.platform == "darwin" else "3.1-rc3"
    xsdk_depends_on("datatransferkit@" + dtk7ver, when="@0.8.0 +trilinos +datatransferkit")

    xsdk_depends_on("petsc +batch", when="^cray-mpich")
    xsdk_depends_on("petsc +sycl +kokkos", when="@1.0.0: +sycl")
    xsdk_depends_on(
        "petsc@3.20.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@1.0.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )
    xsdk_depends_on(
        "petsc@3.18.1+mpi+hypre+superlu-dist+metis+hdf5~mumps+double~int64",
        when="@0.8.0",
        cuda_var="cuda",
        rocm_var="rocm",
    )

    xsdk_depends_on("dealii +trilinos~adol-c", when="+trilinos +dealii")
    xsdk_depends_on("dealii ~trilinos", when="~trilinos +dealii")
    xsdk_depends_on(
        "dealii@9.5.1~assimp~python~doc~gmsh+petsc+slepc+mpi~int64"
        + "~netcdf+metis+sundials~ginkgo~symengine~simplex~arborx~cgal~oce",
        when="@1.0.0 +dealii",
    )
    xsdk_depends_on(
        "dealii@9.4.0~assimp~python~doc~gmsh+petsc+slepc+mpi~int64"
        + "~netcdf+metis+sundials~ginkgo~symengine~simplex~arborx~cgal",
        when="@0.8.0 +dealii",
    )

    xsdk_depends_on("pflotran@5.0.0", when="@1.0.0 +pflotran")
    xsdk_depends_on("pflotran@4.0.1", when="@0.8.0 +pflotran")

    xsdk_depends_on("alquimia@1.1.0", when="@1.0.0 +alquimia")
    xsdk_depends_on("alquimia@1.0.10", when="@0.8.0 +alquimia")

    xsdk_depends_on("sundials +trilinos", when="+trilinos")
    xsdk_depends_on("sundials +ginkgo", when="+ginkgo @0.8.0:")
    xsdk_depends_on("sundials +sycl cxxstd=17", when="@1.0.0: +sycl")
    xsdk_depends_on(
        "sundials@6.6.2~int64+hypre+petsc+superlu-dist",
        when="@1.0.0",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "sundials@6.4.1~int64+hypre+petsc+superlu-dist",
        when="@0.8.0",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )

    xsdk_depends_on("plasma@23.8.2:", when="@1.0.0 %gcc@6.0:")
    xsdk_depends_on("plasma@22.9.29:", when="@0.8.0 %gcc@6.0:")

    xsdk_depends_on("magma@2.7.1", when="@1.0.0", cuda_var="?cuda", rocm_var="?rocm")
    xsdk_depends_on("magma@2.7.0", when="@0.8.0", cuda_var="?cuda", rocm_var="?rocm")

    xsdk_depends_on("amrex +sycl", when="@1.0.0: +sycl")
    xsdk_depends_on("amrex@23.08+sundials", when="@1.0.0 +amrex", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("amrex@22.09+sundials", when="@0.8.0 +amrex", cuda_var="cuda", rocm_var="rocm")

    xsdk_depends_on("slepc@3.20.0", when="@1.0.0", cuda_var="cuda", rocm_var="rocm")
    xsdk_depends_on("slepc@3.18.1", when="@0.8.0", cuda_var="cuda", rocm_var="rocm")

    xsdk_depends_on("omega-h +trilinos", when="+trilinos +omega-h")
    xsdk_depends_on("omega-h ~trilinos", when="~trilinos +omega-h")
    xsdk_depends_on("omega-h@scorec.10.6.0", when="@1.0.0 +omega-h")
    xsdk_depends_on("omega-h@9.34.13", when="@0.8.0 +omega-h")

    xsdk_depends_on("strumpack ~cuda", when="~cuda +strumpack")
    xsdk_depends_on("strumpack ~slate~openmp", when="~slate @0.8.0: +strumpack")
    xsdk_depends_on("strumpack@7.2.0", when="@1.0.0 +strumpack", cuda_var=["cuda"])
    xsdk_depends_on("strumpack@7.0.1", when="@0.8.0 +strumpack", cuda_var=["cuda"])

    xsdk_depends_on("pumi@2.2.8+shared", when="@1.0.0")
    xsdk_depends_on("pumi@2.2.7+shared", when="@0.8.0")

    tasmanian_openmp = "~openmp" if sys.platform == "darwin" else "+openmp"
    xsdk_depends_on(
        "tasmanian@8.0+mpi+blas" + tasmanian_openmp, when="@1.0.0", cuda_var=["cuda", "?magma"]
    )
    xsdk_depends_on(
        "tasmanian@7.9+xsdkflags+mpi+blas" + tasmanian_openmp,
        when="@0.8.0",
        cuda_var=["cuda", "?magma"],
    )

    xsdk_depends_on("arborx+sycl", when="@1.0.0: +arborx +sycl")
    xsdk_depends_on("arborx@1.4.1", when="@1.0.0 +arborx")
    xsdk_depends_on("arborx@1.2", when="@0.8.0 +arborx")

    # the Fortran 2003 bindings of phist require python@3:, but this
    # creates a conflict with other packages like petsc@main. Actually
    # these are type='build' dependencies, but spack reports a conflict anyway.
    # This will be fixed once the new concretizer becomes available
    # (says @adamjstewart)

    xsdk_depends_on("phist kernel_lib=tpetra", when="+trilinos +phist")
    xsdk_depends_on("phist kernel_lib=petsc", when="~trilinos +phist")
    xsdk_depends_on("phist@1.12.0 ~fortran ~scamac ~openmp ~host ~int64", when="@1.0.0 +phist")
    xsdk_depends_on("phist@1.11.2 ~fortran ~scamac ~openmp ~host ~int64", when="@0.8.0 +phist")

    xsdk_depends_on("ginkgo+sycl", when="@1.0.0: +ginkgo +sycl")
    xsdk_depends_on(
        "ginkgo@1.7.0 +mpi ~openmp", when="@1.0.0 +ginkgo", cuda_var="cuda", rocm_var="rocm"
    )
    xsdk_depends_on(
        "ginkgo@1.5.0 +mpi ~openmp", when="@0.8.0 +ginkgo", cuda_var="cuda", rocm_var="rocm"
    )

    xsdk_depends_on("py-libensemble@1.0.0+petsc4py", when="@1.0.0 +libensemble")
    xsdk_depends_on("py-petsc4py@3.20.1", when="@1.0.0 +libensemble")
    xsdk_depends_on("py-libensemble@0.9.3+petsc4py", when="@0.8.0 +libensemble")
    xsdk_depends_on("py-petsc4py@3.18.1", when="@0.8.0 +libensemble")

    xsdk_depends_on("precice ~petsc", when="+precice ^cray-mpich")
    xsdk_depends_on("precice@2.5.0", when="@1.0.0 +precice")
    xsdk_depends_on("precice@2.5.0", when="@0.8.0 +precice")

    bfpk_openmp = "~openmp" if sys.platform == "darwin" else "+openmp"
    xsdk_depends_on("butterflypack@2.4.0" + bfpk_openmp, when="@1.0.0 +butterflypack")
    xsdk_depends_on("butterflypack@2.2.2" + bfpk_openmp, when="@0.8.0 +butterflypack")

    xsdk_depends_on(
        "heffte@2.4.0+fftw",
        when="@1.0.0 +heffte",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )
    xsdk_depends_on(
        "heffte@2.3.0+fftw",
        when="@0.8.0 +heffte",
        cuda_var=["cuda", "?magma"],
        rocm_var=["rocm", "?magma"],
    )

    xsdk_depends_on("slate@2023.08.25", when="@1.0.0 +slate", cuda_var="cuda")
    xsdk_depends_on("slate@2022.07.00", when="@0.8.0 +slate", cuda_var="cuda")

    xsdk_depends_on("exago@1.6.0~ipopt~hiop~python", when="@1.0.0 +exago ~raja")
    xsdk_depends_on("exago@1.6.0~ipopt+hiop+raja", when="@1.0.0 +exago +raja", cuda_var="cuda")
    xsdk_depends_on("exago@1.5.0~ipopt~hiop~python", when="@0.8.0 +exago ~raja")
    xsdk_depends_on("exago@1.5.0~ipopt+hiop+raja", when="@0.8.0 +exago +raja", cuda_var="cuda")

    xsdk_depends_on("hiop@1.0.0", when="@1.0.0 +hiop ~raja")
    xsdk_depends_on("hiop@1.0.0+raja", when="@1.0.0 +hiop +raja", cuda_var="cuda")
    xsdk_depends_on("hiop@0.7.1", when="@0.8.0 +hiop ~raja")
    xsdk_depends_on("hiop@0.7.1+raja", when="@0.8.0 +hiop +raja", cuda_var="cuda")
