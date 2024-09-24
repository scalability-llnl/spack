import spack.package as sp

library_names = dict()


def _boost_variant(name, default=None, buildable=None, conflicts=[], requires=[], **kwargs):
    """
    Create a spack.Variant with extra logic to handle the cases a library
    should be compiled (i.e., passed to b2 via --with-libraries)

    Args:
     name (str): name of the variant

     default (str,bool,None):  The default value for the variant

                                By default, each variant is enabled. A value of
                                'None' is converted to 'True'. This is done so
                                that each _boost_variant can omit a default
                                value. The inversion is done because
                                spack.Variant assumes a default value of
                                'False'.

     buildable (str): The version string indicating which versions
                      for which the library should be compiled or `None`

     conflicts (list): The variant's conflicts

                       Each conflict is a dict with keys 'when' and 'msg'
                       that are identical to the values for the spack
                       'conflicts' directive.

     requires (list): The variant's requires

                       Each requirement is a dict with keys 'spec', 'when', and
                       'msg' that are identical to the values for the spack
                       'requires' directive.

     kwargs (dict): The rest of the arguments forwarded on to the
                    spack.Variant constructor

                    This should include 'when' which indicates the version
                    range for which the variant is valid. This is distinct
                    from 'buildable' as the latter only indicates when the
                    library should be compiled.

                    For example, the coroutine2 library was introduced in
                    version 1.59.0, but was converted to header-only in version
                    1.64.0. In this case, when="@1.59.0:" and
                    buildable="@1.59.0:1.64.0".

                    Conversely, the exception library was introduced in 1.36.0
                    as header-only, but required compilation after 1.47.0. In
                    this case, when="@1.36.0:" and buildable="@1.47.0:".
    """

    if default is None:
        kwargs["sticky"] = True
        default = True

    sp.variant(name, default=default, **kwargs)

    for c in conflicts:
        sp.conflicts(f"+{name}", when=c["when"], msg=c["msg"])

    for r in requires:
        when = f"+{name}"
        if "when" in r:
            when += " " + r["when"]
        sp.requires(r["spec"], when=when, msg=r["msg"])

    if buildable is not None:
        library_names[name] = buildable


def load():
    _boost_variant(
        "clanglibcpp",
        default=False,
        when="@1.73.0:",
        conflicts=[
            # Boost 1.85.0 stacktrace added a hard compilation error that has to
            # explicitly be suppressed on some platforms:
            # https://github.com/boostorg/stacktrace/issues/163
            {"when": "@1.85: +stacktrace", "msg": "Stacktrace cannot be used with libc++"}
        ],
        description="Compile with clang's libc++ instead of libstdc++",
    )
    _boost_variant(
        "cxxstd",
        default="11",
        values=(
            sp.conditional("98", when="@:1.83.0"),
            sp.conditional("03", when="@:1.83.0"),
            "11",
            "14",
            sp.conditional("17", when="@1.63.0:"),
            sp.conditional("2a", when="@1.73.0:"),
            sp.conditional("20", when="@1.77.0:"),
            sp.conditional("23", when="@1.79.0:"),
            sp.conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building",
    )
    # fmt: off
    _boost_variant(
        "debug",
        default=False,
        description="Switch to the debug version of Boost",
    )
    _boost_variant(
        "icu",
        default=False,
        conflicts=[
            {"when": "cxxstd=98", "msg": "ICU requires at least c++11"},
            {"when": "cxxstd=03", "msg": "ICU requires at least c++11"},
        ],
        description="Build with Unicode and ICU suport",
    )
    _boost_variant(
        "multithreaded",
        description="Build multi-threaded versions of libraries",
    )
    _boost_variant(
        "numpy",
        default=False,
        requires=[
            {"spec": "+python", "msg": "Numpy requires python support"}
        ],
        description="Build the Boost NumPy library",
    )
    # fmt: on
    _boost_variant(
        "pic",
        default=False,
        description="Generate position-independent code (PIC), useful for building static"
        " libraries",
    )
    # fmt: off
    _boost_variant(
        "shared",
        description="Additionally build shared libraries",
    )
    _boost_variant(
        "singlethreaded",
        default=False,
        description="Build single-threaded versions of libraries",
    )
    # fmt: on
    _boost_variant(
        "taggedlayout",
        default=False,
        when="@1.40.0:",
        conflicts=[
            {"when": "+versionedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library names with build options",
    )
    _boost_variant(
        "versionedlayout",
        default=False,
        conflicts=[
            {"when": "+taggedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library layout with versioned subdirs",
    )
    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    _boost_variant(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        when="@1.69.0:",
        description="Default symbol visibility in compiled libraries",
    )

    # ----------------------------------------------------------------------
    # fmt: off
    _boost_variant(
        "atomic",
        when="@1.53.0:",
        buildable="@1.53.0:",
        description="C++11-style atomic<>.",
    )
    # fmt: on
    _boost_variant(
        "charconv",
        when="@1.85.0:",
        buildable="@1.85.0:",
        description="An implementation of <charconv> in C++11.",
    )
    _boost_variant(
        "chrono",
        when="@1.47.0:",
        buildable="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="Useful time utilities. C++11.",
    )
    _boost_variant(
        "cobalt",
        default=False,
        when="@1.84.0:",
        buildable="@1.84.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=03", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=11", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=14", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=17", "msg": "Boost.cobalt requires cxxstd >= 20"},
        ],
        requires=[
            # {"spec": "+leaf", "msg": "Boost.cobalt requires Boost.leaf"},
            {"spec": "+variant2", "msg": "Boost.cobalt requires Boost.variant2"}
        ],
        description="Coroutines. Basic Algorithms & Types",
    )
    _boost_variant(
        "container",
        # Can be both header-only and compiled. '+container' indicates the
        # compiled version which requires Extended Allocator support. The
        # header-only library is installed when no variant is given.
        when="@1.48.0:",
        buildable="@1.56.0:",  # Extended Allocators need to be compiled
        description="Standard library containers and extensions.",
    )
    _boost_variant(
        "context",
        when="@1.51.0:",
        buildable="@1.51.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="(C++11) Context switching library.",
    )
    _boost_variant(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        description=(
            "Contract programming with subcontracting, class invariants, and pre/postconditions."
        ),
    )
    _boost_variant(
        "context-impl",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        when="@1.65.0:",
        description="The backend for Boost.Context",
    )
    _boost_variant(
        "coroutine",
        when="@1.53.0:",
        buildable="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine requires cxxstd >= 11"},
        ],
        # fmt: off
        requires=[
            {"spec": "+context", "msg": "Boost.Coroutine requires Boost.Context"}
        ],
        # fmt: on
        description="Coroutine library.",
    )
    _boost_variant(
        "date_time",
        when="@1.29.0:",
        buildable="@1.29.0:",
        description="A set of date-time libraries based on generic programming concepts.",
    )
    _boost_variant(
        "exception",
        when="@1.36.0:",
        buildable="@1.47.0:",
        description=(
            "The Boost Exception library supports transporting of arbitrary data in exception"
            " objects, and transporting of exceptions between threads."
        ),
    )
    _boost_variant(
        "fiber",
        when="@1.62.0:",
        buildable="@1.62.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Fiber requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Fiber requires cxxstd >= 11"},
        ],
        # fmt: off
        requires=[
            {"spec": "+context", "msg": "Boost.Fiber requires Boost.Context"}
        ],
        # fmt: on
        description="(C++11) Userland threads library.",
    )
    _boost_variant(
        "filesystem",
        when="@1.30.0:",
        buildable="@1.30.0:",
        description=(
            "The Boost Filesystem Library provides portable facilities to query and manipulate"
            " paths, files, and directories."
        ),
    )
    _boost_variant(
        "graph",
        when="@1.18.0:",
        buildable="@1.18.0:",
        description=(
            "The BGL graph interface and graph components are generic, in the same sense as"
            " the Standard Template Library (STL)."
        ),
    )
    _boost_variant(
        "graph_parallel",
        default=False,
        when="@1.40.0:",
        buildable="@1.40.0:",
        requires=[
            {"spec": "+mpi", "msg": "Boost.GraphParallel requires Boost.MPI"},
            {"spec": "+graph", "msg": "Boost.GraphParallel requires Boost.Graph"},
        ],
        description=(
            "The PBGL graph interface and graph components are generic, in the same sense as"
            " the Standard Template Library (STL)."
        ),
    )
    _boost_variant(
        "iostreams",
        when="@1.33.0:",
        buildable="@1.33.0:",
        description=(
            "Boost.IOStreams provides a framework for defining streams, stream buffers and i/o"
            " filters."
        ),
    )
    _boost_variant(
        "json",
        when="@1.75.0:",
        buildable="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.JSON requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.JSON requires cxxstd >= 11"},
        ],
        description="JSON parsing, serialization, and DOM in C++11",
    )
    _boost_variant(
        "locale",
        when="@1.48.0:",
        buildable="@1.48.0:",
        # fmt: off
        requires=[
            {"spec": "+icu", "msg": "Boost.Locale requires Unicode support (+icu)"}
        ],
        # fmt: on
        description="Provide localization and Unicode handling tools for C++.",
    )
    # fmt: off
    _boost_variant(
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        description="Logging library.",
    )
    # fmt: on
    _boost_variant(
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        requires=[
            {"spec": "+octonions", "msg": "Boost.Math requires Math.Octonions (+octonions)"},
            {"spec": "+quaternions", "msg": "Boost.Math requires Math.Quaternions (+quaternions)"},
        ],
        description=(
            "Boost.Math includes several contributions in the domain of mathematics: The"
            " Greatest Common Divisor and Least Common Multiple library provides run-time and"
            " compile-time evaluation of the greatest common divisor (GCD) or least common"
            " multiple (LCM) of two integers. The Special Functions library currently provides"
            " eight templated special functions, in namespace boost. The Complex Number"
            " Inverse Trigonometric Functions are the inverses of trigonometric functions"
            " currently present in the C++ standard. Quaternions are a relative of complex"
            " numbers often used to parameterise rotations in three dimentional space."
            " Octonions, like quaternions, are a relative of complex numbers."
        ),
    )
    _boost_variant(
        "mpi",
        default=False,
        when="@1.35.0:",
        buildable="@1.35.0:",
        description=(
            "Message Passing Interface library, for use in distributed-memory parallel"
            " application programming."
        ),
    )
    # fmt: off
    _boost_variant(
        "octonions",
        when="@1.23.0:",
        description="Octonions.",
    )
    # fmt: on
    _boost_variant(
        "nowide",
        default=False,
        when="@1.73.0:",
        buildable="@1.73.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Nowide requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Nowide requires cxxstd >= 11"},
        ],
        requires=[
            # It doesn't require Windows, but it makes no sense to build it anywhere else.
            {"spec": "platform=windows", "msg": "Boost.Nowide can only be built on Windows"}
        ],
        description="Standard library functions with UTF-8 API on Windows.",
    )
    _boost_variant(
        "program_options",
        default=False,
        when="@1.32.0:",
        buildable="@1.32.0:",
        description=(
            "The program_options library allows program developers to obtain program options,"
            " that is (name, value) pairs from the user, via conventional methods such as"
            " command line and config file."
        ),
    )
    _boost_variant(
        "python",
        default=False,
        when="@1.19.0:",
        buildable="@1.19.0:",
        description=(
            "The Boost Python Library is a framework for interfacing Python and C++. It allows"
            " you to quickly and seamlessly expose C++ classes functions and objects to"
            " Python, and vice-versa, using no special tools -- just your C++ compiler."
        ),
    )
    # fmt: off
    _boost_variant(
        "quaternions",
        when="@1.23.0:",
        description="Quaternions.",
    )
    # fmt: on
    _boost_variant(
        "random",
        when="@1.15.0:",
        buildable="@1.43.0:",
        description="A complete system for random number generation.",
    )
    # fmt: off
    _boost_variant(
        "regex",
        when="@1.18.0:",
        buildable="@1.18.0:",
        description="Regular expression library.",
    )
    # fmt: on
    _boost_variant(
        "serialization",
        when="@1.32.0:",
        buildable="@1.32.0:",
        description="Serialization for persistence and marshalling.",
    )
    _boost_variant(
        "signals",
        default=False,
        when="@1.29.0:1.68.0",
        buildable="@1.29.0:1.68.0",
        description="Managed signals & slots callback implementation.",
    )
    _boost_variant(
        "signals2",
        when="@1.39.0:",
        description="Managed signals & slots callback implementation (thread-safe version 2).",
    )
    _boost_variant(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy and print backtraces.",
    )
    _boost_variant(
        "test",
        when="@1.21.0:",
        buildable="@1.21.0:",
        description=(
            "Support for simple program testing, full unit testing, and for program execution"
            " monitoring."
        ),
    )
    return library_names
