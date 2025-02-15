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
        default = True

    if "sticky" not in kwargs:
        kwargs["sticky"] = True

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
    # ----------------------------------------------------------------------
    #  Boost-level configurations
    #
    #    These variants affect every library.
    # ----------------------------------------------------------------------
    _boost_variant(
        "clanglibcpp",
        default=False,
        when="@1.73.0:",
        conflicts=[
            # Boost 1.85.0 stacktrace added a hard compilation error that has to
            # explicitly be suppressed on some platforms:
            # https://github.com/boostorg/stacktrace/issues/163
            {"when": "@1.85: +stacktrace", "msg": "Stacktrace cannot be used with libc++"},
            # gcc doesn't support libc++
            {"when": "%gcc", "msg": "gcc doesn't support libc++"},
        ],
        description="Compile with clang's libc++ instead of libstdc++",
    )
    _boost_variant(
        "cxxstd",
        default="14",
        values=(
            "98",
            "03",
            "11",
            "14",
            sp.conditional("17", when="@1.63.0:"),
            sp.conditional("2a", when="@1.73.0:"),
            sp.conditional("20", when="@1.77.0:"),
            sp.conditional("23", when="@1.79.0:"),
            sp.conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="C++ standard",
    )
    # fmt: off
    _boost_variant(
        "debug",
        default=False,
        description="Build in debug mode",
    )
    # fmt: on
    _boost_variant(
        "icu",
        default=False,
        conflicts=[
            {"when": "cxxstd=98", "msg": "ICU requires at least c++11"},
            {"when": "cxxstd=03", "msg": "ICU requires at least c++11"},
        ],
        description="Build with Unicode and ICU suport",
    )
    # fmt: off
    _boost_variant(
        "pic",
        description="Build Boost libraries with position-independent code (PIC)",
    )
    _boost_variant(
        "shared",
        requires=[
            {"spec": "+pic", "msg": "Cannot build non-PIC shared libraries."},
        ],
        description="Build Boost libraries as shared libraries (DSO, DLL, etc.)",
    )
    _boost_variant(
        "multithreaded",
        description="Enable use of multiple threads in the Boost libraries",
    )
    # fmt: on
    _boost_variant(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads in the Boost libraries",
    )
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
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------
    _boost_variant(
        "timer",
        when="@1.9.0:",
        buildable="@1.48.0:",
        description="Event timer, progress timer, and progress display classes.",
    )
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
        "graph",
        when="@1.18.0:",
        buildable="@1.39.0:",
        description=(
            "Generic components for mathematical graphs (collections of nodes and edges)."
        ),
    )
    # fmt: off
    _boost_variant(
        "property_map",
        when="@1.19.0:",
        description="Concepts defining interfaces which map key objects to value objects.",
    )
    _boost_variant(
        "python",
        default=False,
        sticky=False,
        when="@1.19.0:",
        buildable="@1.19.0:",
        description="C++ wrapper for interacting with Python.",
    )
    # fmt: off
    _boost_variant(
        "lexical_cast",
        when="@1.20.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LexicalCast requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.LexicalCast requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+math", "when": "@:1.76.0", "msg": "Boost.LexicalCast requires Boost.Math"}
        ],
        description=(
            "General literal text conversions, such as an int represented a string, or vice-versa."
        ),
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
    _boost_variant(
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Math requires at least c++11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Math requires at least c++11"},
        ],
        requires=[
            {"spec": "+octonions", "msg": "Boost.Math requires Math.Octonions (+octonions)"},
            {"spec": "+quaternions", "msg": "Boost.Math requires Math.Quaternions (+quaternions)"},
        ],
        description=(
            "Common integer mathematical operations (gcd, lcd, etc.), special functions, "
            "complex numbers, quaternions, and octonions."
        ),
    )
    # fmt: off
    _boost_variant(
        "octonions",
        when="@1.23.0:",
        description="Octonions.",
    )
    _boost_variant(
        "quaternions",
        when="@1.23.0:",
        description="Quaternions.",
    )
    # fmt: on
    _boost_variant(
        "thread",
        when="@1.25.0:",
        buildable="@1.25.0:",
        description="Portable C++ multi-threading. C++03, C++11, C++14, C++17.",
    )
    _boost_variant(
        "preprocessor",
        when="@1.26.0:",
        conflicts=[
            {"when": "@1.75.0: cxxstd=98", "msg": "Boost.Preprocessor requires cxxstd >= 11"},
            {"when": "@1.75.0: cxxstd=03", "msg": "Boost.Preprocessor requires cxxstd >= 11"},
        ],
        description="Preprocessor metaprogramming tools including repetition and recursion.",
    )
    _boost_variant(
        "date_time",
        when="@1.29.0:",
        buildable="@1.29.0:",
        description="A set of date-time libraries based on generic programming concepts.",
    )
    # fmt: off
    _boost_variant(
        "signals",
        default=False,
        when="@1.29.0:1.68.0",
        buildable="@1.29.0:1.68.0",
        conflicts=[
            {"when": "@1.69.0:", "msg": "Boost.signals was removed in 1.68.0"}
        ],
        description="Managed signals & slots callback implementation",
    )
    # fmt: on
    _boost_variant(
        "filesystem",
        when="@1.30.0:",
        buildable="@1.30.0:",
        description="Portable facilities to query and manipulate paths, files, and directories.",
    )
    _boost_variant(
        "spirit",
        when="@1.30.0:",
        conflicts=[{"when": "cxxstd=98", "msg": "Boost.Spirit requires cxxstd >= 03"}],
        description=(
            "LL parser framework represents parsers directly as EBNF grammars in inlined C++."
        ),
    )
    _boost_variant(
        "program_options",
        default=False,
        when="@1.32.0:",
        buildable="@1.32.0:",
        description="Parse command-line options similar to POSIX getops or from config files.",
    )
    _boost_variant(
        "serialization",
        when="@1.32.0:",
        buildable="@1.32.0:",
        description="Serialization for persistence and marshalling.",
    )
    _boost_variant(
        "iostreams",
        when="@1.33.0:",
        buildable="@1.33.0:",
        description=("Streams, stream buffers, and i/o filters"),
    )
    # fmt: off
    _boost_variant(
        "parameter",
        when="@1.33.0:",
        buildable="@1.33.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Parameter requires at least c++03"},
        ],
        description="Write functions that accept arguments by name.",
    )
    # fmt: on
    _boost_variant(
        "wave",
        when="@1.33.0:",
        buildable="@1.33.0:",
        conflicts=[
            {"when": "@1.79.0: cxxstd=98", "msg": "Boost.Wave requires cxxstd >= 11"},
            {"when": "@1.79.0: cxxstd=03", "msg": "Boost.Wave requires cxxstd >= 11"},
        ],
        description="Highly configurable implementation of the mandatory C99/C++ preprocessor.",
    )
    # fmt: off
    _boost_variant(
        "asio",
        when="@1.35.0:",
        requires=[
            {"spec": "+context", "when": "@1.80.0:", "msg": "Boost.Asio requires Boost.Context"},
        ],
        description="Portable networking and other low-level I/O.",
    )
    # fmt: on
    _boost_variant(
        "gil",
        when="@1.35.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.GIL requires at least c++11"},
            {"when": "cxxstd=03", "msg": "Boost.GIL requires at least c++11"},
            {"when": "cxxstd=11 @1.80.0:", "msg": "Boost.GIL requires at least c++14"},
            {"when": "%gcc@:6 @1.80.0:", "msg": "Boost.GIL requires gcc-6 or newer"},
        ],
        description="Generic Image Library",
    )
    _boost_variant(
        "mpi",
        default=False,
        sticky=False,
        when="@1.35.0:",
        buildable="@1.35.0:",
        conflicts=[
            # NOTE: 1.64.0 seems fine for *most* applications, but if you need
            #       +python and +mpi, there seem to be errors with out-of-date
            #       API calls from mpi/python.
            #       See: https://github.com/spack/spack/issues/3963
            {"when": "@1.64.0 +python", "msg": "Boost.MPI@1.64.0 does not support python"},
            {"when": "@1.72.0 cxxstd=98", "msg": "Boost.MPI@1.72.0 does not support C++98"},
        ],
        requires=[
            {"spec": "+python", "when": "@1.87.0:", "msg": "Boost.MPI requires Boost.Numpy"}
        ],
        description=(
            "C++ wrapper to the Message Passing Interface for distributed-memory parallelism."
        ),
    )
    # fmt: off
    _boost_variant(
        "system",
        when="@1.35.0:",
        buildable="@1.35.0:",
        description="Extensible error reporting.",
    )
    # fmt: on
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
        "signals2",
        when="@1.39.0:",
        description="Thread-safe managed signals & slots callback implementation",
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
        "geometry",
        when="@1.47.0:",
        conflicts=[
            {"when": "@1.75.0: cxxstd=98", "msg": "Boost.Geometry requires cxxstd >= 14"},
            {"when": "@1.75.0: cxxstd=03", "msg": "Boost.Geometry requires cxxstd >= 14"},
            {"when": "@1.75.0: cxxstd=11", "msg": "Boost.Geometry requires cxxstd >= 14"},
        ],
        description="Geometric algorithms, primitives, and spatial indices.",
    )
    _boost_variant(
        "phoenix",
        when="@1.47.0:",
        description="Define small unnamed function objects at the actual call site, and more.",
    )
    # fmt: off
    _boost_variant(
        "ratio",
        when="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Ratio requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Ratio requires cxxstd >= 11"},
        ],
        description="Compile-time rational arithmetic.",
    )
    # fmt: on
    _boost_variant(
        "container",
        # Can be both header-only and compiled. '+container' indicates the
        # compiled version which requires Extended Allocator support. The
        # header-only library is installed when no variant is given.
        when="@1.48.0:",
        buildable="@1.56.0:",  # Extended Allocators need to be compiled
        description="Standard library containers and extensions.",
    )
    # fmt: off
    _boost_variant(
        "locale",
        default=False,
        when="@1.48.0:",
        buildable="@1.48.0:",
        requires=[
            {"spec": "+icu", "msg": "Boost.Locale requires Unicode support (+icu)"}
        ],
        description="Provide localization and Unicode handling tools for C++.",
    )
    # fmt: on
    _boost_variant(
        "context",
        when="@1.51.0:",
        buildable="@1.51.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="Context-switching library",
    )
    # fmt: off
    _boost_variant(
        "atomic",
        when="@1.53.0:",
        buildable="@1.53.0:",
        description="C++11-style atomic<>.",
    )
    _boost_variant(
        "coroutine",
        when="@1.53.0:",
        buildable="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+context", "msg": "Boost.Coroutine requires Boost.Context"}
        ],
        description="Coroutine library.",
    )
    _boost_variant(
        "lockfree",
        when="@1.53.0:",
        description="Lockfree queue, stack, and SP/SC queue.",
    )
    # fmt: on
    _boost_variant(
        "multiprecision",
        when="@1.53.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
        ],
        description=(
            "Extended precision arithmetic for floating point, integer, and rational types."
        ),
    )
    # fmt: off
    _boost_variant(
        "odeint",
        when="@1.53.0:",
        description="Solver for ordinary differential equations.",
    )
    _boost_variant(
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        description="Logging library.",
    )
    _boost_variant(
        "type_erasure",
        when="@1.54.0:",
        buildable="@1.60.0:",
        description="Runtime polymorphism based on concepts.",
    )
    _boost_variant(
        "fiber",
        when="@1.62.0:",
        buildable="@1.62.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Fiber requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Fiber requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+context", "msg": "Boost.Fiber requires Boost.Context"}
        ],
        description="Userland threads",
    )
    _boost_variant(
        "numpy",
        when="@1.63.0:",
        default=False,
        requires=[
            {"spec": "+python", "msg": "Numpy requires python support"}
        ],
        description="Build the Boost NumPy library",
    )
    # fmt: on
    _boost_variant(
        "context-impl",
        when="@1.65.0:",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="The backend for Boost.Context",
    )
    _boost_variant(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy and print backtraces.",
    )
    _boost_variant(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        description=(
            "Contract programming with subcontracting, class invariants, and pre/postconditions."
        ),
    )
    # fmt: off
    _boost_variant(
        "hof",
        when="@1.67.0:",
        description="Higher-order functions for C++",
    )
    # fmt: on
    _boost_variant(
        "yap",
        when="@1.68.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.YAP requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.YAP requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.YAP requires cxxstd >= 14"},
        ],
        description="An expression template library for C++14 and later.",
    )
    _boost_variant(
        "parameter_python",
        default=False,
        when="@1.69.0:",
        # fmt: off
        requires=[
            {"spec": "+python", "msg": "Parameter Python bindings requires python support"},
            {"spec": "+parameter", "msg": "Parameter Python bindings requires Boost.Parameter"}
        ],
        # fmt: on
        description="Python bindings for Boost.Parameter.",
    )
    # fmt: off
    _boost_variant(
        "safe_numerics",
        when="@1.69.0:",
        description="Guaranteed Correct Integer Arithmetic",
    )
    # fmt: on
    _boost_variant(
        "spirit_repository",
        when="@1.69.0:",
        description="A collection of reusable components for Qi parsers and Karma generators.",
    )
    _boost_variant(
        "histogram",
        when="@1.70.0:",
        # fmt: off
        requires=[
            {
                "spec": "+variant2",
                "when": "@1.71.0:",
                "msg": "Boost.Histogram requires Boost.Variant2"
            },
        ],
        # fmt: on
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Histogram requires cxxstd >= 14"},
        ],
        description="Fast multi-dimensional histogram with convenient interface.",
    )
    _boost_variant(
        "outcome",
        when="@1.70.0:",
        description=(
            "Deterministic failure handling, partially simulating lightweight exceptions."
        ),
    )
    # fmt: off
    _boost_variant(
        "string_ref",
        when="@1.71.0:",
        description="String view templates.",
    )
    _boost_variant(
        "variant2",
        when="@1.71.0:",
        description="A never-valueless, strong guarantee implementation of std::variant.",
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
        "leaf",
        when="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LEAF requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.LEAF requires cxxstd >= 11"},
        ],
        description="Lightweight error-handling",
    )
    # fmt: off
    _boost_variant(
        "pfr",
        when="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PFR requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.PFR requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.PFR requires cxxstd >= 14"},
        ],
        description="Basic reflection for user defined types.",
    )
    # fmt: on
    _boost_variant(
        "describe",
        when="@1.77.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Describe requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Describe requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Describe requires cxxstd >= 14"},
        ],
        description="A C++14 reflection library.",
    )
    _boost_variant(
        "lambda2",
        when="@1.77.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.lambda2 requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.lambda2 requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.lambda2 requires cxxstd >= 14"},
        ],
        description="A C++14 lambda library.",
    )
    _boost_variant(
        "property_map_parallel",
        default=False,
        when="@1.77.0:",
        # fmt: off
        requires=[
            {
                "spec": "+graph_parallel",
                "msg": "Boost.PropertyMap (Parallel) requires Boost.GraphParallel"
            },
            {
                "spec": "+property_map",
                "msg": "Boost.PropertyMap (Parallel) requires Boost.PropertyMap"
            }
        ],
        # fmt: on
        description="Parallel extensions to Property Map for use with Parallel Graph.",
    )
    _boost_variant(
        "url",
        when="@1.81.0:",
        buildable="@1.81.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.URL requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.URL requires cxxstd >= 11"},
        ],
        # fmt: off
        requires=[
            {"spec": "+variant2", "msg": "Boost.url requires Boost.variant2"},
        ],
        # fmt: on
        description="URL parsing in C++11",
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
            {"spec": "+leaf", "msg": "Boost.cobalt requires Boost.leaf"},
            {"spec": "+variant2", "msg": "Boost.cobalt requires Boost.variant2"},
        ],
        description="Coroutines. Basic Algorithms & Types",
    )
    _boost_variant(
        "charconv",
        when="@1.85.0:",
        buildable="@1.85.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="An implementation of C++20's <charconv> in C++11.",
    )

    return library_names
