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
            sp.conditional("98", when="@:1.84.0"),
            sp.conditional("03", when="@:1.84.0"),
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
        description="Enable Unicode support via ICU",
    )
    # fmt: off
    _boost_variant(
        "pic",
        description="Generate binaries with position-independent code (PIC)",
    )
    _boost_variant(
        "shared",
        requires=[
            {"spec": "+pic", "msg": "Cannot build non-PIC shared libraries."},
        ],
        description="Generate shared libraries (DSO, DLL, etc.)",
    )
    _boost_variant(
        "multithreaded",
        description="Enable use of multiple threads",
    )
    _boost_variant(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads",
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
    # fmt: off
    _boost_variant(
        "numpy",
        when="@1.63.0:",
        default=False,
        requires=[
            {"spec": "+python", "msg": "Numpy requires python support"}
        ],
        description="Enable numpy support in Boost.Python",
    )
    # fmt: on

    # ----------------------------------------------------------------------
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------
    # fmt: off
    _boost_variant(
        "integer",
        when="@1.9.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.integer requires cxxstd >= 03"},
        ],
        description="Type traits and math functions for integral values",
    )
    # fmt: on
    _boost_variant(
        "operators",
        when="@1.9.0:",
        conflicts=[
            {"when": "cxxstd=2a", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=20", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=23", "msg": "Boost.Operators requires cxxstd <= 17"},
            {"when": "cxxstd=26", "msg": "Boost.Operators requires cxxstd <= 17"},
        ],
        description="CRTP helpers to define arithmetic operators for a class",
    )
    _boost_variant(
        "timer",
        when="@1.9.0:",
        buildable="@1.48.0:",
        description="Timers for measuring wallclock and CPU times",
    )
    _boost_variant(
        "random",
        when="@1.15.0:",
        buildable="@1.43.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.random requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.random requires cxxstd >= 11"},
        ],
        description="A complete system for random number generation.",
    )
    # fmt: off
    _boost_variant(
        "regex",
        when="@1.18.0:",
        buildable="@1.18.0:",
        conflicts=[
            {"when": "cxxstd=03", "msg": "Boost.regex requires cxxstd >= 11"},
        ],
        description="Perl and POSIX regular expressions",
    )
    # fmt: on
    _boost_variant(
        "graph",
        when="@1.18.0:",
        buildable="@1.18.0:",
        description=(
            "Generic components for mathematical graphs (collections of nodes and edges)."
        ),
    )
    # fmt: off
    _boost_variant(
        "property_map",
        when="@1.19.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PropertyMap requires at least c++03"},
        ],
        description="Concepts defining interfaces which map key objects to value objects.",
    )
    _boost_variant(
        "python",
        default=False,
        sticky=False,
        when="@1.19.0:",
        buildable="@1.19.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.python requires cxxstd >= 03"},
        ],
        description="C++ wrapper for interacting with Python.",
    )
    # fmt: off
    _boost_variant(
        "conversion",
        when="@1.20.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.conversion requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.conversion requires cxxstd >= 11"},
        ],
        description="Extensions to standard casting operators",
    )
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
        description="Type-safe text <-> value conversions",
    )
    _boost_variant(
        "test",
        when="@1.21.0:",
        buildable="@1.21.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.test requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.test requires cxxstd >= 11"},
        ],
        description=(
            "Simple program testing, full unit testing, and program execution monitoring"
        ),
    )
    _boost_variant(
        "crc",
        when="@1.22.0:",
        conflicts=[
            {"when": "@1.86.0: cxxstd=98", "msg": "Boost.CRC requires cxxstd >= 11"},
            {"when": "@1.86.0: cxxstd=03", "msg": "Boost.CRC requires cxxstd >= 11"},
        ],
        description=("Cyclic Redundancy Code generation for confirming data integrity"),
    )
    _boost_variant(
        "any",
        when="@1.23.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.any requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.any requires cxxstd >= 11"},
        ],
        description="Safe, generic container for single values of different value types",
    )
    _boost_variant(
        "function",
        when="@1.23.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.function requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.function requires cxxstd >= 11"},
        ],
        description="Function object wrappers for deferred calls or callbacks",
    )
    _boost_variant(
        "math",
        when="@1.23.0:",
        buildable="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Math requires at least c++11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Math requires at least c++11"},
            {"when": "@1.82.0: cxxstd=11", "msg": "Boost.Math requires at least c++14"},
        ],
        requires=[
            {"spec": "+octonions", "msg": "Boost.Math requires Boost.Octonions"},
            {"spec": "+quaternions", "msg": "Boost.Math requires Boost.Quaternions"},
        ],
        description=(
            "Extensive collection of integer, real, and complex mathematical operations"
        ),
    )
    # fmt: off
    _boost_variant(
        "octonions",
        when="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.math_octonion requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.math_octonion requires cxxstd >= 11"},
            {"when": "@1.82.0: cxxstd=11", "msg": "Boost.math_octonion requires cxxstd >= 14"},
        ],
        description="Octonions",
    )
    _boost_variant(
        "quaternions",
        when="@1.23.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.math_quaternion requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.math_quaternion requires cxxstd >= 11"},
            {"when": "@1.82.0: cxxstd=11", "msg": "Boost.math_quaternion requires cxxstd >= 14"},
        ],
        description="Quaternions",
    )
    _boost_variant(
        "smart_ptr",
        when="@1.23.0:",
        conflicts=[
            {"when": "@1.87.0: cxxstd=98", "msg": "Boost.SmartPtr requires cxxstd >= 11"},
            {"when": "@1.87.0: cxxstd=03", "msg": "Boost.SmartPtr requires cxxstd >= 11"},
        ],
        description="Smart pointers.",
    )
    _boost_variant(
        "bind",
        when="@1.25.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.bind requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.bind requires cxxstd >= 11"},
        ],
        description="Generalizations of the std::bind and std::mem_fn family",
    )
    _boost_variant(
        "thread",
        when="@1.25.0:",
        buildable="@1.25.0:",
        description="Portable C++ multi-threading",
    )
    _boost_variant(
        "math_common_factor",
        when="@1.26.0:1.65.0",
        conflicts=[
            {"when": "@1.65.0:", "msg": "Boost.Math/CommonFactor moved to Boost.Integer"},
        ],
        description="Greatest common divisor and least common multiple",
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
        description="Calculate, format, and convert dates and times",
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
        "variant",
        when="@1.31.0:",
        conflicts=[
            {"when": "@1.84.0: cxxstd=98", "msg": "Boost.variant requires cxxstd >= 11"},
            {"when": "@1.84.0: cxxstd=03", "msg": "Boost.variant requires cxxstd >= 11"},
        ],
        description="Safe, generic, stack-based discriminated union container.",
    )
    _boost_variant(
        "program_options",
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
        "container_hash",
        when="@1.33.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.container_hash requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.container_hash requires cxxstd >= 11"},
        ],
        description="Hash function objects for user-defined types",
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
        conflicts=[
            {"when": "@1.80.0: cxxstd=98", "msg": "Boost.asio requires cxxstd >= 11"},
            {"when": "@1.80.0: cxxstd=03", "msg": "Boost.asio requires cxxstd >= 11"},
        ],
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
        "typeof",
        when="@1.34.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.typeof requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.typeof requires cxxstd >= 11"},
        ],
        description="Typeof operator emulation",
    )
    # fmt: off
    _boost_variant(
        "asio",
        when="@1.35.0:",
        conflicts=[
            {"when": "@1.80.0: cxxstd=98", "msg": "Boost.asio requires cxxstd >= 11"},
            {"when": "@1.80.0: cxxstd=03", "msg": "Boost.asio requires cxxstd >= 11"},
        ],
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
            # 1.64 uses out-dated APIs (https://github.com/spack/spack/issues/3963)
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
    _boost_variant(
        "exception",
        when="@1.36.0:",
        buildable="@1.47.0:",
        description=(
            "Transport arbitrary data in exceptions, and exceptions between threads"
        ),
    )
    # fmt: on
    _boost_variant(
        "unordered",
        when="@1.36.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.unordered requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.unordered requires cxxstd >= 11"},
        ],
        description="Unordered associative containers",
    )
    _boost_variant(
        "signals2",
        when="@1.39.0:",
        description="Thread-safe managed signals & slots callback implementation",
    )
    # fmt: on
    _boost_variant(
        "graph_parallel",
        default=False,
        when="@1.40.0:",
        buildable="@1.40.0:",
        requires=[
            {"spec": "+mpi", "msg": "Boost.GraphParallel requires Boost.MPI"},
            {"spec": "+graph", "msg": "Boost.GraphParallel requires Boost.Graph"},
        ],
        description="Scalable parallel version of Boost.Graph using MPI multiprocessing",
    )
    # fmt: off
    _boost_variant(
        "property_tree",
        when="@1.41.0:",
        description="Structured storage of configuration data",
    )
    # fmt: on
    _boost_variant(
        "uuid",
        when="@1.42.0:",
        conflicts=[
            {"when": "@1.86.0: cxxstd=98", "msg": "Boost.uuid requires cxxstd >= 11"},
            {"when": "@1.86.0: cxxstd=03", "msg": "Boost.uuid requires cxxstd >= 11"},
        ],
        description="Universally unique identifier",
    )
    _boost_variant(
        "functional_factory",
        when="@1.43.0:",
        description="Dynamic and static creation of function objects",
    )
    _boost_variant(
        "functional_forward",
        when="@1.43.0:",
        description="Allow arbitrary arguments in function objects",
    )
    # fmt: off
    _boost_variant(
        "meta_state_machine",
        when="@1.44.0:",
        description="Expressive UML2 finite state machines",
    )
    _boost_variant(
        "polygon",
        when="@1.44.0:",
        description="Voronoi diagram manipulations for planar polygons",
    )
    _boost_variant(
        "icl",
        when="@1.46.0:",
        description="Interval sets and maps",
    )
    # fmt: on
    _boost_variant(
        "chrono",
        when="@1.47.0:",
        buildable="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.chrono requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.chrono requires cxxstd >= 11"},
        ],
        description="Extended version of C++11 time utilities",
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
    # fmt: off
    _boost_variant(
        "phoenix",
        when="@1.47.0:",
        description="Functional programming for C++",
    )
    # fmt: off
    _boost_variant(
        "ratio",
        when="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Ratio requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Ratio requires cxxstd >= 11"},
        ],
        description="Compile-time rational arithmetic",
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
        conflicts=[
            {"when": "@1.81.0: cxxstd=98", "msg": "Boost.Locale requires cxxstd >= 11"},
            {"when": "@1.81.0: cxxstd=03", "msg": "Boost.Locale requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+icu", "msg": "Boost.Locale requires Unicode support"}
        ],
        description="Localization and Unicode facilities",
    )
    _boost_variant(
        "move",
        when="@1.48.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Move requires cxxstd >= 03"},
        ],
        description="Portable move semantics for C++03",
    )
    _boost_variant(
        "heap",
        when="@1.49.0:",
        description="Priority queue data structures",
    )
    _boost_variant(
        "algorithm",
        when="@1.50.0:",
        description="A collection of useful generic algorithms",
    )
    _boost_variant(
        "functional_overloaded_function",
        when="@1.50.0:",
        description="Overload different functions into a single function object",
    )
    _boost_variant(
        "identity_type",
        when="@1.50.0:",
        description="Safely pass user-defined types as macro parameters",
    )
    _boost_variant(
        "local_function",
        when="@1.50.0:",
        description="Declare and use functions in a local scope",
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
        description="Cooperative multitasking on a single thread",
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
        description="DEPRECATED use coroutine2",
    )
    _boost_variant(
        "lockfree",
        when="@1.53.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.LockFree requires cxxstd >= 03"}
        ],
        description="Lockfree queue, stack, and SP/SC queue",
    )
    # fmt: on
    _boost_variant(
        "multiprecision",
        when="@1.53.0:",
        conflicts=[
            {"when": "@1.76.0: cxxstd=98", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
            {"when": "@1.76.0: cxxstd=03", "msg": "Boost.Multiprecision requires cxxstd >= 11"},
            {"when": "@1.82.0: cxxstd=11", "msg": "Boost.Multiprecision requires cxxstd >= 14"},
        ],
        description=(
            "Extended precision arithmetic for floating point, integer, and rational types"
        ),
    )
    # fmt: off
    _boost_variant(
        "odeint",
        when="@1.53.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Odeint requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Odeint requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+math", "msg": "Boost.Odeint requires Boost.Math"}
        ],
        description="Solver for ordinary differential equations",
    )
    _boost_variant(
        "log",
        when="@1.54.0:",
        buildable="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Log requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Log requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+regex", "when": "@1.84.0:", "msg": "Boost.Log requires Boost.Regex"},
        ],
        description="Simple, extensible, and fast logging",
    )
    _boost_variant(
        "tti",
        when="@1.54.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.tti requires cxxstd >= 03"}
        ],
        description="Type Traits Introspection",
    )
    _boost_variant(
        "type_erasure",
        when="@1.54.0:",
        buildable="@1.60.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.TypeErasure requires cxxstd >= 03"}
        ],
        description="Runtime polymorphism based on concepts.",
    )
    _boost_variant(
        "predef",
        when="@1.55.0:",
        description="Macros to identify compilers and their versions",
    )
    # fmt: off
    _boost_variant(
        "align",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Align requires cxxstd >= 03"}
        ],
        description="Memory alignment facilities",
    )
    _boost_variant(
        "core",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.core requires cxxstd >= 03"},
        ],
        description="Simple core utilities with minimal dependencies",
    )
    _boost_variant(
        "throw_exception",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.ThrowException requires cxxstd >= 03"}
        ],
        description="Enhanced exception handling, including source locations",
    )
    # fmt: on
    _boost_variant(
        "type_index",
        when="@1.56.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.TypeIndex requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.TypeIndex requires cxxstd >= 11"},
        ],
        description="Runtime/compile-time copyable type info",
    )
    # fmt: off
    _boost_variant(
        "endian",
        when="@1.58.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Endian requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Endian requires cxxstd >= 11"},
        ],
        description="Manipulate the endianness of integers and user-defined types"
    )
    _boost_variant(
        "sort",
        when="@1.58.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Sort requires cxxstd >= 03"}
        ],
        description="High-performance sorting routines",
    )
    _boost_variant(
        "convert",
        when="@1.59.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Convert requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Convert requires cxxstd >= 11"},
        ],
        description="An extendible and configurable type-conversion framework.",
    )
    _boost_variant(
        "coroutine2",
        when="@1.59.0:",
        buildable="@1.59.0:1.64.0",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+context", "msg": "Boost.Coroutine2 requires Boost.Context"}
        ],
        description=(
            "Subroutines that allow suspending and resuming execution at certain locations"
        ),
    )
    _boost_variant(
        "vmd",
        when="@1.60.0:",
        requires=[
            {"spec": "+preprocessor", "msg": "Boost.VMD requires Boost.Preprocessor"}
        ],
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.VMD requires cxxstd >= 03"}
        ],
        description="Variadic macros for Boost.Preprocessor",
    )
    _boost_variant(
        "compute",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Compute requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Compute requires cxxstd >= 11"},
        ],
        description="Multi-core CPU and GPGPU computing based on OpenCL",
    )
    _boost_variant(
        "dll",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.dll requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.dll requires cxxstd >= 11"},
        ],
        description="Load plugins from DLLs or DSOs",
    )
    # fmt: on
    _boost_variant(
        "hana",
        when="@1.61.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Hana requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Hana requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Hana requires cxxstd >= 14"},
        ],
        description="Modern metaprogramming suited for computations on both types and values",
    )
    # fmt: off
    _boost_variant(
        "metaparse",
        when="@1.61.0:1.65.1",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.MetaParse requires cxxstd >= 03"}
        ],
        description="Generate compile-time parsers for embedded DSL code",
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
        description="Lightweight userland threads",
    )
    # fmt: off
    _boost_variant(
        "qvm",
        when="@1.62.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.QVM requires cxxstd >= 03"},
        ],
        description="Generic operations for Quaternions, Vectors, and Matrices",
    )
    _boost_variant(
        "process",
        when="@1.64.0:",
        buildable="@1.64.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Process requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Process requires cxxstd >= 11"},
        ],
        description="Portable process creation and management",
    )
    _boost_variant(
        "context-impl",
        when="@1.65.0:",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="The backend for Boost.Context",
    )
    # fmt: off
    _boost_variant(
        "poly_collection",
        when="@1.65.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PolyCollection requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.PolyCollection requires cxxstd >= 11"},
        ],
        description="Fast containers of polymorphic objects",
    )
    # fmt: on
    _boost_variant(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy, and print backtraces",
    )
    # fmt: off
    _boost_variant(
        "beast",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Beast requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Beast requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+asio", "msg": "Boost.Beast requires Boost.Asio"}
        ],
        description="Portable HTTP, WebSocket, and network operations using Boost.Asio",
    )
    # fmt: on
    _boost_variant(
        "callable_traits",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
        ],
        description="Compile-time inspection and manipulation of callable types",
    )
    # fmt: off
    _boost_variant(
        "mp11",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.MP11 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.MP11 requires cxxstd >= 11"},
        ],
        description="C++11 metaprogramming",
    )
    # fmt: on
    _boost_variant(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Contract requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Contract requires cxxstd >= 11"},
        ],
        description=(
            "Contract programming with subcontracting, class invariants, and pre/postconditions."
        ),
    )
    # fmt: off
    _boost_variant(
        "hof",
        when="@1.67.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.HoF requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.HoF requires cxxstd >= 11"},
        ],
        description="Higher-order functions",
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
    # fmt: off
    _boost_variant(
        "parameter_python",
        default=False,
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Parameter python bindings require cxxstd >= 03"}
        ],
        requires=[
            {"spec": "+python", "msg": "Parameter Python bindings require python support"},
            {"spec": "+parameter", "msg": "Parameter Python bindings require Boost.Parameter"}
        ],
        description="Python bindings for Boost.Parameter",
    )
    _boost_variant(
        "safe_numerics",
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.SafeNumerics requires cxxstd >= 14"},
        ],
        description="Guaranteed correct integer arithmetic",
    )
    _boost_variant(
        "spirit_repository",
        when="@1.69.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.SpiritRepository requires cxxstd >= 03"}
        ],
        description="Reusable components for Qi parsers and Karma generators",
    )
    _boost_variant(
        "histogram",
        when="@1.70.0:",
        requires=[
            {
                "spec": "+variant2",
                "when": "@1.71.0:",
                "msg": "Boost.Histogram requires Boost.Variant2"
            },
        ],
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Histogram requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Histogram requires cxxstd >= 14"},
        ],
        description="Fast multi-dimensional histogram",
    )
    _boost_variant(
        "outcome",
        when="@1.70.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Outcome requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.Outcome requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.Outcome requires cxxstd >= 14"},
        ],
        description=(
            "Deterministic failure handling, partially simulating lightweight exceptions."
        ),
    )
    # fmt: off
    _boost_variant(
        "string_ref",
        when="@1.71.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.StringRef requires cxxstd >= 03"},
        ],
        description="Non-owning reference to a string",
    )
    _boost_variant(
        "variant2",
        when="@1.71.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Variant2 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Variant2 requires cxxstd >= 11"},
        ],
        description="A never-valueless, strong-guarantee tagged union",
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
        description="Standard library functions with UTF-8 API on Windows",
    )
    # fmt: off
    _boost_variant(
        "static_string",
        when="@1.73.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.StaticString requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.StaticString requires cxxstd >= 11"},
        ],
        description="A fixed-capacity, dynamically-sized string",
    )
    # fmt: on
    _boost_variant(
        "stl_interfaces",
        when="@1.74.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.STLInterfaces requires cxxstd >= 14"},
        ],
        description="Simplifies writing STL-compliant containers and ranges",
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
        description="Basic reflection for user-defined types",
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
        description="Advanced reflection for user-defined types",
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
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.PropertyMapParallel requires cxxstd >= 03"}
        ],
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
        description="Parallel extensions to Property Map for use with Parallel Graph",
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
        description="Portable model for parsing URLs and URIs",
    )
    _boost_variant(
        "mysql",
        when="@1.82.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.mysql requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.mysql requires cxxstd >= 11"},
        ],
        requires=[
            {"spec": "+describe", "msg": "Boost.mysql requires Boost.describe"},
            {"spec": "+pfr", "msg": "Boost.mysql requires Boost.pfr"},
            {"spec": "+variant2", "msg": "Boost.mysql requires Boost.variant2"},
            {"spec": "+asio", "msg": "Boost.mysql requires Boost.Asio"},
        ],
        description="MySQL client library built on top of Boost.Asio.",
    )
    _boost_variant(
        "compat",
        when="@1.83.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.compat requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.compat requires cxxstd >= 11"},
        ],
        description="C++11 implementations of standard components added in later C++ standards.",
    )
    _boost_variant(
        "redis",
        when="@1.84.0:",
        default=False,
        conflicts=[
            {"when": "cxxstd=11", "msg": "Boost.Redis requires cxxstd >= 17"},
            {"when": "cxxstd=14", "msg": "Boost.Redis requires cxxstd >= 17"},
        ],
        # fmt: off
        requires=[
            {"spec": "+asio", "msg": "Boost.Redis requires Boost.Asio"},
        ],
        # fmt: on
        description="Redis async client library built on top of Boost.Asio.",
    )
    _boost_variant(
        "cobalt",
        default=False,
        when="@1.84.0:",
        buildable="@1.84.0:",
        conflicts=[
            {"when": "cxxstd=11", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=14", "msg": "Boost.cobalt requires cxxstd >= 20"},
            {"when": "cxxstd=17", "msg": "Boost.cobalt requires cxxstd >= 20"},
        ],
        requires=[
            {"spec": "+leaf", "msg": "Boost.cobalt requires Boost.leaf"},
            {"spec": "+variant2", "msg": "Boost.cobalt requires Boost.variant2"},
        ],
        description=(
            "Simple single-threaded asynchronicity akin to node.js and asyncio in python"
        ),
    )
    _boost_variant(
        "charconv",
        when="@1.85.0:",
        buildable="@1.85.0:",
        description="An implementation of C++20's <charconv> in C++11.",
    )

    return library_names
