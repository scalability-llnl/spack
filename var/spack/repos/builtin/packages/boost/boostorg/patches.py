import spack.package as sp


def load():

    #
    # ----- Compilers ---------
    #
    with sp.when("%gcc"):
        with sp.when("%gcc@4.4.7"):
            sp.patch(
                "patches/boost_11856.patch",
                when="@1.60.0",
                sha256="cfd4e6e1e9747def96adeae0075994a03a10e1bfb471900ecb52b7839afa9ca2",
            )

        with sp.when("%gcc@5.0:"):
            sp.patch(
                "patches/call_once_variadic.patch",
                when="@1.54.0:1.55",
                sha256="4f2b06f77ad5e485e9debb769199414b2d6ebc0784aa1a8e28c1144fa971e155",
            )
        with sp.when("%gcc@8.3"):
            # Workaround gcc-8.3 compiler issue https://github.com/boostorg/mpl/issues/44
            sp.patch(
                "patches/boost_gcc83_cpp17_fix.patch",
                when="@1.69:",
                sha256="53e492188ab40abcb01a2d8b3ab1a61e2bf575070fcd4f54e72145f0281bc2b5",
            )

    with sp.when("%fj"):
        # Change the method for version analysis when using Fujitsu compiler.
        sp.patch(
            "patches/fujitsu_version_analysis.patch",
            when="@1.67.0:1.76.0",
            sha256="34233f0a408ce9b1bb49b548086ef7f2caffc1eece52976d47ffb7cab4fee802",
        )

        sp.patch(
            "patches/fujitsu_version_analysis-1.77.patch",
            when="@1.77.0:",
            sha256="f627cd4a5e33680ff1d08f427a526d43b80a35a2204852d82e769ffa916b4e77",
        )

    with sp.when("%xl"):
        # IBM XL C
        sp.patch(
            "patches/xl_1_62_0_le.patch",
            when="@1.62.0",
            sha256="fd64b4f1e9c136549c7b704bd0014283e1515de8b68e54f0dd0cde758866eb69",
        )

    with sp.when("%xl_r"):
        # IBM XL C++
        sp.patch(
            "patches/xl_1_62_0_le.patch",
            when="@1.62.0",
            sha256="fd64b4f1e9c136549c7b704bd0014283e1515de8b68e54f0dd0cde758866eb69",
        )

    with sp.when("%pgi"):
        sp.patch(
            "patches/boost_1.67.0_pgi.patch",
            when="@1.67.0:1.68",
            sha256="6f8119bbbf80a23aecefffe4cb230b8383fb25e21a589eec74275e3efe487d0d",
        )
        sp.patch(
            "patches/boost_1.63.0_pgi.patch",
            when="@1.63.0",
            sha256="a2f8809e36835080bfa9e69ee8260662858b8d5b1c1c10cdf0ab7e0a381ae872",
        )

        with sp.when("%pgi@17.4"):
            sp.patch(
                "patches/boost_1.63.0_pgi_17.4_workaround.patch",
                when="@1.63.0",
                sha256="f59e6ce697fea69256d597ec624f8c47b5e35f743fa6d91207cf8933737911dd",
            )

    with sp.when("%nvhpc"):
        # Override the PGI toolset when using the NVIDIA compilers
        sp.patch(
            "patches/nvhpc-1.74.patch",
            when="@1.74.0:1.75",
            sha256="d56f31f2a3956630e5372b987d39cb79b5d2c71760fa150b8eb4a3f1a07e2658",
        )

        sp.patch(
            "patches/nvhpc-1.76.patch",
            when="@1.76.0:1.76",
            sha256="cba819a80b2e9449e11b43f4ab3c6d6097aa37d42925d4d64d0a9ba8e047d9e8",
        )

        # Workaround compiler bug
        sp.patch(
            "patches/nvhpc-find_address.patch",
            when="@1.75.0:1.76",
            sha256="938811004ff77783a82d59c8ebf2582a40db88de89fb0a078351e52e9e0aa704",
        )

    with sp.when("%cce"):
        with sp.when("%cce@:1.76"):
            # Fix float128 support when building with CUDA and Cray compiler
            sp.patch(
                "patches/config_PR378.patch",
                sha256="666eec8cfb0f71a87443ab27d179a9771bda32bcb8ff5e16afa3767f7b7f1e70",
                level=2,
            )

    with sp.when("%oneapi"):
        # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html
        sp.patch(
            "patches/intel-oneapi-linux-jam.patch",
            when="@1.76:",
            sha256="8e3faa26450312e5ea8db8f32afda109b8559ba496e6a5799ddde271c9a6fc44",
        )

    with sp.when("platform=darwin"):
        # Fix for version comparison on newer Clang on darwin
        # See: https://github.com/boostorg/build/issues/440
        # See: https://github.com/macports/macports-ports/pull/6726
        sp.patch(
            "patches/darwin_clang_version.patch",
            level=0,
            when="@1.56.0:1.72.0",
            sha256="95f5420d8ed34f60e3f88b38a4a5e8a032c94dc57b85cc2ab8243dd0d754a626",
        )

        # Allow building context asm sources with GCC on Darwin
        # See https://github.com/spack/spack/pull/24889
        # and https://github.com/boostorg/context/issues/177
        sp.patch(
            "patches/context-macho-gcc.patch",
            when="@1.65:1.76 +context %gcc",
            sha256="6edc1de3dcb931939a875796207057c00708525d86926b588ba55f65c18dc611",
        )

    #
    # ----- Python ---------
    #
    with sp.when("^python@3:"):
        sp.patch(
            "patches/python_jam-1_77.patch",
            when="@1.77:",
            sha256="b8569d7d4c3ef0501a39857126a2b0a88519bf256c29f3252a6958916ce82255",
        )
        sp.patch(
            "patches/python_jam.patch",
            when="@1.56:1.76",
            sha256="2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199",
        )
        sp.patch(
            "patches/python_jam_pre156.patch",
            when="@:1.55.0",
            sha256="f994ac84634f2f833a7a4d3179c5bf9a06f14349ef67aacba39d08837ffab004",
        )

    #
    # ----- Generic Fixes ---------
    #

    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372
    sp.patch(
        "patches/glibc_gentoo_v1.53.0.patch",
        when="@1.53.0:1.54",
        sha256="b6f6ce68282159d46c716a1e6c819c815914bdb096cddc516fa48134209659f2",
    )

    # Add option to C/C++ compile commands in clang-linux.jam
    sp.patch(
        "patches/clang-linux_add_option.patch",
        when="@1.56.0:1.63.0",
        sha256="d1cd178ea5348fafbba797113fc5a92cc822f3606dc2fe65c14cc2275334001b",
    )

    sp.patch(
        "patches/clang-linux_add_option2.patch",
        when="@1.47.0:1.55.0",
        sha256="4f0f7c0c0711e330aa077e2a1a989f68cbdcf7a3d20f85db872f3c34fce278e1",
    )

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154
    sp.patch(
        "patches/build_PR154.patch",
        when="@1.56.0:1.63",
        sha256="fb7d84358c36309062fa4aaaa187343eb16871bd95893f0270e0941955c488ab",
    )

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218
    sp.patch(
        "patches/python_PR218.patch",
        when="@1.63.0:1.67",
        sha256="7f95f95be9645eb7f10a7222173c8549501aebbe1db12b955442a7554dc59f3e",
    )

    # Fix: "Unable to compile code using boost/process.hpp"
    # See: https://github.com/boostorg/process/issues/116
    sp.patch(
        "patches/process_PR116.patch",
        level=2,
        when="@1.72.0",
        sha256="e13cca1cfad7dcce9ed3d4ef989c14e464c4ea00caaf335f762e3677b35cab61",
    )

    # Patch fix for warnings from commits 2d37749, af1dc84, c705bab, and
    # 0134441 on https://github.com/boostorg/system.
    sp.patch(
        "patches/system-non-virtual-dtor-include.patch",
        when="@1.69.0",
        level=2,
        sha256="3a83d907043708218325c35ffc318fd6d6cfd78ba89a78f2c70013c72603e5b8",
    )

    sp.patch(
        "patches/system-non-virtual-dtor-test.patch",
        when="@1.69.0",
        working_dir="libs/system",
        level=1,
        sha256="607b0772dec1287c9084ae3b36ee32bff945a2fe5e608823ed47a1ea765c84cd",
    )

    # Fix issues with PTHREAD_STACK_MIN not being a DEFINED constant in newer glibc
    # See https://github.com/spack/spack/issues/28273
    sp.patch(
        "patches/pthread-stack-min-fix.patch",
        when="@1.69.0:1.72.0",
        sha256="5da7ad24de07adc1e99b2bab8b5aeefa0059d0f0ace932788c7746f9117d9917",
    )

    # C++20 concepts fix for Beast
    # See https://github.com/boostorg/beast/pull/1927 for details
    sp.patch(
        "patches/beast_PR1927.patch",
        sha256="4dd507e1f5a29e3b87b15321a4d8c74afdc8331433edabf7aeab89b3c405d556",
        when="@1.73.0",
    )

    # Cloning a status_code with indirecting_domain leads to segmentation fault
    # See https://github.com/ned14/outcome/issues/223 for details
    sp.patch(
        "patches/outcome_PR223.patch",
        sha256="246508e052c44b6f4e8c2542a71c06cacaa72cd1447ab8d2a542b987bc35ace9",
        when="@1.73.0",
    )

    # Fix B2 bootstrap toolset during installation
    # See https://github.com/spack/spack/issues/20757
    # and https://github.com/spack/spack/pull/21408
    sp.patch(
        "patches/bootstrap-toolset.patch",
        when="@1.75",
        sha256="f2409bfa0e69e44817a5f8799e25c2e9e5ee50876a5aaacefd32fa647b80472f",
    )

    # Fix compiler used for building bjam during bootstrap
    sp.patch(
        "patches/bootstrap-compiler.patch",
        when="@1.76:",
        sha256="a440f9696d3bbb77e7eab1516c004730f622e59c71d39960b472026ef92f88e8",
    )

    # Fix building with Intel compilers
    sp.patch(
        "patches/b2_PR79.patch",
        sha256="4849671f9df4b8f3c962130d7f6d44eba3b20d113e84f9faade75e6469e90310",
        when="@1.77.0",
        working_dir="tools/build",
    )

    with sp.when("@1.78.0"):
        # https://github.com/bfgroup/b2/pull/113
        sp.patch(
            "patches/build_PR113.patch",
            sha256="0e1b19e91e0fef2906b3e1bed1ba06b277ff84942bb8ac9e645dd93ad3532b4e",
        )

        # UWP support for atomic
        sp.patch(
            "patches/atomic_PR54.patch",
            when="+atomic",
            sha256="1be9f01f238d54ce311c2a8a5ddbdd3f97268c0c011460e41033443d70280a18",
        )

    # https://github.com/boostorg/json/issues/692
    sp.patch(
        "patches/json_PR695.patch",
        when="@1.79.0 +json",
        sha256="0edcb348b9c6f6ab8c67735881dccd9759af852830ffe651ae51248e24ff11ac",
    )

    with sp.when("@1.80.0"):
        # libcpp@15 removes std::unary{binary}_function
        sp.patch(
            "patches/config_libcpp15.patch",
            when="+clanglibcpp %clang@15",
            sha256="dc43a069c55c0fbea0bc2bd78924835cb3c915b75ec30692f4748147d104ee8a",
        )

        with sp.when("+filesystem"):
            # Compilation failure on POSIX systems that don't support *at APIs
            sp.patch(
                "patches/filesystem_PR250.patch",
                sha256="3bc4efd085d25e0e32abbf2b652412c80281247c8e8ba0a99cd28011d6986826",
            )

            with sp.when("platform=windows"):
                # Directory iterators for a network share on Windows
                sp.patch(
                    "patches/filesystem_PR246.patch",
                    sha256="938e19f55238e168a2170bb68c3b4544fc5db1ba6bc2c03e5eedff89a987f018",
                )

                # Allow weakly_canonical to be used with Windows long paths
                sp.patch(
                    "patches/filesystem_PR247.patch",
                    sha256="f1b2add065611700def7ae727ebb01790f5ac52ab7a04e197d4714e416558303",
                )

        with sp.when("+unordered"):
            # Containers are not in a valid state after moving
            sp.patch(
                "patches/unordered_PR139.patch",
                sha256="6aff29ac5cbded7e5b8c629c6a8cdda2039ff691a7ebebb8c25c3121781a8837",
            )

            with sp.when("platform=windows"):
                # MSVC /RTCc build runtime failures
                sp.patch(
                    "patches/unordered_PR165.patch",
                    sha256="db93780fdcf95275f90094ea8fb7901bb790a030055d6e9354357a130c5bd8cb",
                )

    # https://github.com/boostorg/phoenix/issues/111
    sp.patch(
        "patches/phoenix_PR111.patch",
        level=2,
        when="@1.81.0:1.83.0",
        sha256="a7c807fcd855aa70ba839c0bdfcf5877dc9a37f8026211ccda9c676b42431b17",
    )

    with sp.when("@1.82.0"):
        with sp.when("+filesystem"):
            # OpenBSD has broken support for -Wl,--no-undefined for shared libraries
            sp.patch(
                "patches/filesystem_PR283.patch",
                when="platform=freebsd",
                sha256="53a37c8673b20ee697b48bbee0370334958775d7824d43f533672b2c22f523c0",
            )

            # Directory iterators for Windows SMBv1 shares may fail
            sp.patch(
                "patches/filesystem_PR284.patch",
                when="platform=windows",
                sha256="738ba8e0d7b5cdcf5fae4998f9450b51577bbde1bb0d220a0721551609714ca4",
            )

    with sp.when("@1.83.0"):
        with sp.when("+json"):
            # Compilation on Windows ARM platforms may fail for missing intrinsics
            sp.patch(
                "patches/json_PR926.patch",
                when="platform=windows",
                sha256="af68f8be3fedcbc2eca8fff625c7bd3cfeb0f0611e1579ba9901bd5282da5909",
            )

        with sp.when("+unordered"):
            # Fix erroneous copy assigment operator that would destroy non-existent elements
            sp.patch(
                "patches/unordered_PR205.patch",
                sha256="c6e04429fbf1629f10f456d47d9cfda1a89c4b1f242665cb4c091cd84b0d4626",
            )

    with sp.when("@1.85.0"):
        with sp.when("+container"):
            # flat_map/multimap containers can crash due to UB
            sp.patch(
                "patches/container_PR273.patch",
                level=0,
                sha256="28118307582c3ce716d010fc89c3cd749066b333f3859c6b533613f59394df81",
            )
