# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.package_test import compare_output_file, compile_c_and_execute


class Atlas(Package):
    """Automatically Tuned Linear Algebra Software, generic shared ATLAS is an
    approach for the automatic generation and optimization of numerical
    software. Currently ATLAS supplies optimized versions for the complete set
    of linear algebra kernels known as the Basic Linear Algebra Subroutines
    (BLAS), and a subset of the linear algebra routines in the LAPACK library.
    """

    homepage = "https://math-atlas.sourceforge.net/"

    license("Apache-2.0")

    # Developer (unstable)
    version("3.11.41", sha256="477d567a8d683e891d786e9e8bb6ad6659daa9ba18e8dd0e2f70b7a54095f8de")
    version("3.11.39", sha256="584bd44572746142bf19348139530c18f4538ce41d94330ff86ede38c36eddc9")
    version("3.11.34", sha256="b6d42af3afd4fe54ef3a04a070fc7e75f6d8ac9f7d4886b636fe27ebfcbdf91f")

    # Stable
    version(
        "3.10.3",
        sha256="2688eb733a6c5f78a18ef32144039adcd62fabce66f2eb51dd59dde806a6d2b7",
        preferred=True,
    )
    version("3.10.2", sha256="3aab139b118bf3fcdb4956fbd71676158d713ab0d3bccb2ae1dc3769db22102f")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # not all packages (e.g. Trilinos@12.6.3) stopped using deprecated in 3.6.0
    # Lapack routines. Stick with 3.5.0 until this is fixed.
    resource(
        name="lapack",
        url="https://www.netlib.org/lapack/lapack-3.5.0.tgz",
        sha256="9ad8f0d3f3fb5521db49f2dd716463b8fb2b6bc9dc386a9956b8c6144f726352",
        destination="spack-resource-lapack",
        when="@3:",
    )

    variant("shared", default=True, description="Builds shared library")

    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("pthreads", "none"),
        multi=False,
    )

    variant(
        "tune_cpu",
        default=-1,
        multi=False,
        description="Number of threads to tune to, " "-1 for autodetect, 0 for no threading",
    )

    conflicts(
        "platform=windows",
        msg="Atlas requires cygwin to build on Windows, which is unsupported by Spack. "
        "See https://math-atlas.sourceforge.net/atlas_install/node55.html",
    )

    provides("blas")
    provides("lapack")
    provides("lapack@3.6.1")

    parallel = False

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/math-atlas/files/"

        if version >= Version("3.11"):
            url += "Developer%20%28unstable%29/{0}/atlas{0}.tar.bz2"
        else:
            url += "Stable/{0}/atlas{0}.tar.bz2"

        return url.format(version)

    def patch(self):
        # Disable thread check.  LLNL's environment does not allow
        # disabling of CPU throttling in a way that ATLAS actually
        # understands.
        filter_file(r"^\s+if \(thrchk\) exit\(1\);", "if (0) exit(1);", "CONFIG/src/config.c")
        # TODO: investigate a better way to add the check back in
        # TODO: using, say, MSRs.  Or move this to a variant.

    def install(self, spec, prefix):
        # reference to other package managers
        # https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/a/atlas.py
        # https://github.com/macports/macports-ports/blob/master/math/atlas/Portfile
        # https://github.com/Homebrew/homebrew-science/pull/3571
        options = []
        if spec.satisfies("+shared"):
            options.extend(["--shared"])
            # TODO: for non GNU add '-Fa', 'alg', '-fPIC' ?

        # configure for 64-bit build
        options.extend(["-b", "64"])

        # set number of cpu's to tune to
        options.extend(["-t", spec.variants["tune_cpu"].value])

        # set compilers:
        options.extend(["-C", "ic", spack_cc, "-C", "if", spack_f77])

        # Workaround for macOS Clang:
        # http://math-atlas.sourceforge.net/atlas_install/node66.html
        if spec.satisfies("@3.10.3: %apple-clang"):
            options.append("--force-clang=" + spack_cc)

        # Lapack resource to provide full lapack build. Note that
        # ATLAS only provides a few LAPACK routines natively.
        options.append(f"--with-netlib-lapack-tarfile={self.stage[1].archive_file}")

        with working_dir("spack-build", create=True):
            configure = Executable("../configure")
            configure(f"--prefix={prefix}", *options)
            make()
            make("check")
            make("ptcheck")
            make("time")
            if spec.satisfies("+shared"):
                with working_dir("lib"):
                    make("shared_all")

            make("install")
            if self.run_tests:
                self.install_test()

    @property
    def libs(self):
        # libsatlas.[so,dylib,dll ] contains all serial APIs (serial lapack,
        # serial BLAS), and all ATLAS symbols needed to support them. Whereas
        # libtatlas.[so,dylib,dll ] is parallel (multithreaded) version.
        is_threaded = self.spec.satisfies("threads=pthreads")
        if self.spec.satisfies("+shared"):
            to_find = ["libtatlas"] if is_threaded else ["libsatlas"]
            shared = True
        else:
            interfaces = (
                ["libptcblas", "libptf77blas"] if is_threaded else ["libcblas", "libf77blas"]
            )
            to_find = ["liblapack"] + interfaces + ["libatlas"]
            shared = False
        return find_libraries(to_find, root=self.prefix, shared=shared, recursive=True)

    def install_test(self):
        source_file = join_path(os.path.dirname(self.module.__file__), "test_cblas_dgemm.c")
        blessed_file = join_path(os.path.dirname(self.module.__file__), "test_cblas_dgemm.output")

        include_flags = [f"-I{self.spec.prefix.include}"]
        link_flags = self.spec["atlas"].libs.ld_flags.split()

        output = compile_c_and_execute(source_file, include_flags, link_flags)
        compare_output_file(output, blessed_file)
