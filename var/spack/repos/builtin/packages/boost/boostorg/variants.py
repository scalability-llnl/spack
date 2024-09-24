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
    # fmt: off
    _boost_variant(
        "asio",
        description="Portable networking and other low-level I/O.",
    )
    # fmt: on
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
    _boost_variant(
        "date_time",
        buildable="@1.29.0:",
        description="A set of date-time libraries based on generic programming concepts.",
    )
    # fmt: off
    _boost_variant(
        "debug",
        default=False,
        description="Switch to the debug version of Boost",
    )
    # fmt: on
    _boost_variant(
        "exception",
        buildable="@1.47.0:",
        description=(
            "Transport arbitrary data in exception objects and exceptions between threads."
        ),
    )
    _boost_variant(
        "filesystem",
        buildable="@1.30.0:",
        description="Portable facilities to query and manipulate paths, files, and directories.",
    )

    _boost_variant(
        "gil",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.GIL requires at least c++11"},
            {"when": "cxxstd=03", "msg": "Boost.GIL requires at least c++11"},
        ],
        description="Generic Image Library",
    )
    _boost_variant(
        "graph",
        buildable="@1.18.0:",
        description=(
            "Generic components for mathematical graphs (collections of nodes and edges)."
        ),
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
        "iostreams",
        buildable="@1.33.0:",
        description="A framework for defining streams, stream buffers and i/o filters.",
    )
    _boost_variant(
        "math",
        buildable="@1.23.0:",
        requires=[
            {"spec": "+octonions", "msg": "Boost.Math requires Math.Octonions (+octonions)"},
            {"spec": "+quaternions", "msg": "Boost.Math requires Math.Quaternions (+quaternions)"},
        ],
        description=(
            "Common integer mathematical operations (gcd, lcd, etc.), special functions, "
            "complex numbers, quaternions, and octonions."
        ),
    )
    _boost_variant(
        "mpi",
        default=False,
        buildable="@1.35.0:",
        description=(
            "C++ wrapper to the Message Passing Interface for distributed-memory parallelism."
        ),
    )
    # fmt: off
    _boost_variant(
        "multithreaded",
        description="Enable use of multiple threads in the Boost libraries",
    )
    # fmt: on
    _boost_variant(
        "numpy",
        default=False,
        # fmt: off
        requires=[
            {"spec": "+python", "msg": "Numpy requires python support"}
        ],
        # fmt: on
        description="C++ wrapper for the python NumPy library.",
    )
    # fmt: off
    _boost_variant(
        "octonions",
        description="Octonions.",
    )
    _boost_variant(
        "parameter",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Parameter requires at least c++03"},
        ],
        description="Write functions that accept arguments by name.",
    )
    # fmt: on
    _boost_variant(
        "program_options",
        buildable="@1.32.0:",
        description="Parse command-line options similar to POSIX getops or from config files.",
    )
    _boost_variant(
        "python",
        default=False,
        buildable="@1.19.0:",
        description="C++ wrapper for interacting with Python.",
    )
    # fmt: off
    _boost_variant(
        "pic",
        description="Build Boost libraries with position-independent code (PIC)",
    )
    _boost_variant(
        "quaternions",
        description="Quaternions.",
    )
    _boost_variant(
        "random",
        buildable="@1.43.0:",
        description="A complete system for random number generation.",
    )
    _boost_variant(
        "regex",
        buildable="@1.18.0:",
        description="Regular expressions.",
    )
    _boost_variant(
        "serialization",
        buildable="@1.32.0:",
        description="Serialization for persistence and marshalling.",
    )
    _boost_variant(
        "shared",
        description="Build Boost libraries as shared libraries (DSO, DLL, etc.)",
    )
    _boost_variant(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads in the Boost libraries",
    )
    _boost_variant(
        "system",
        buildable="@1.35.0:",
        description="Extensible error reporting.",
    )
    # fmt: on
    _boost_variant(
        "test",
        buildable="@1.21.0:",
        description="Simple program testing, unit testing, and program execution monitoring.",
    )
    # fmt: off
    _boost_variant(
        "thread",
        buildable="@1.25.0:",
        description="Portable multi-threading",
    )
    # fmt: on
    _boost_variant(
        "timer",
        buildable="@1.48.0:",
        description="Event timer, progress timer, and progress display classes.",
    )
    _boost_variant(
        "versionedlayout",
        default=False,
        conflicts=[
            {"when": "+taggedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Add version number to Boost installation directory names.",
    )
    _boost_variant(
        "wave",
        buildable="@1.33.0:",
        description="Highly configurable implementation of the mandatory C99/C++ preprocessor.",
    )

    # ----------------------------------------------------------------------
    #
    # mpi and python are not enabled by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    #
    # ----------------------------------------------------------------------
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
        description="Thread-safe managed signals & slots callback implementation.",
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
        description="Scalable parallel version of Boost.Graph using MPI multiprocessing.",
    )
    _boost_variant(
        "taggedlayout",
        default=False,
        when="@1.40.0:",
        conflicts=[
            {"when": "+versionedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Add build options to Boost installation directory names.",
    )
    _boost_variant(
        "property_tree",
        when="@1.41.0:",
        description="A tree data structure especially suited to storing configuration data.",
    )
    # fmt: off
    _boost_variant(
        "uuid",
        when="@1.42.0:",
        description="A universally unique identifier.",
    )
    # fmt: on
    _boost_variant(
        "functional_factory",
        when="@1.43.0:",
        description="Function object templates for dynamic and static object creation",
    )
    _boost_variant(
        "functional_forward",
        when="@1.43.0:",
        description="Adapters to allow generic function objects to accept arbitrary arguments",
    )
    _boost_variant(
        "meta_state_machine",
        when="@1.44.0:",
        description="A very high-performance library for expressive UML2 finite state machines.",
    )
    _boost_variant(
        "polygon",
        when="@1.44.0:",
        description=(
            "Voronoi diagram manipulations for planar polygons with integral coordinates."
        ),
    )
    _boost_variant(
        "icl",
        when="@1.46.0:",
        description="Interval sets and maps and aggregation of associated values.",
    )
    _boost_variant(
        "chrono",
        when="@1.47.0:",
        buildable="@1.47.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="Time utilities.",
    )
    _boost_variant(
        "geometry",
        when="@1.47.0:",
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
    _boost_variant(
        "locale",
        default=False,
        when="@1.48.0:",
        buildable="@1.48.0:",
        # fmt: off
        requires=[
            {"spec": "+icu", "msg": "Boost.Locale requires Unicode support (+icu)"}
        ],
        # fmt: on
        description="Localization and Unicode tools.",
    )
    _boost_variant(
        "move",
        when="@1.48.0:",
        # fmt: off
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Move requires cxxstd >= 03"},
        ],
        # fmt: on
        description="Portable move semantics for C++03 and C++11 compilers.",
    )
    # fmt: off
    _boost_variant(
        "heap",
        when="@1.49.0:",
        description="Priority queue data structures.",
    )
    _boost_variant(
        "algorithm",
        when="@1.50.0:",
        description="A collection of useful generic algorithms.",
    )
    # fmt: on
    _boost_variant(
        "functional_overloaded_function",
        when="@1.50.0:",
        description="Overload different functions into a single function object.",
    )
    _boost_variant(
        "identity_type",
        when="@1.50.0:",
        description="Safely express types so they can always be passed as macro parameters.",
    )
    _boost_variant(
        "local_function",
        when="@1.50.0:",
        description=(
            "Write functions locally, within other functions, directly within the "
            "scope where they are needed."
        ),
    )
    _boost_variant(
        "context",
        when="@1.51.0:",
        buildable="@1.51.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Context requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Context requires cxxstd >= 11"},
        ],
        description="Cooperative multitasking on a single thread.",
    )
    # fmt: off
    _boost_variant(
        "atomic",
        when="@1.53.0:",
        buildable="@1.53.0:",
        description="Portable C++11-style atomic<>.",
    )
    # fmt: on
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
        description="DEPRECATED use coroutine2.",
    )
    # fmt: off
    _boost_variant(
        "lockfree",
        when="@1.53.0:",
        description="Lockfree queue, stack, and SP/SC queue.",
    )
    # fmt: on
    _boost_variant(
        "multiprecision",
        when="@1.53.0:",
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
        "tti",
        when="@1.54.0:",
        description="Type Traits Introspection library.",
    )
    # fmt: on
    _boost_variant(
        "type_erasure",
        when="@1.54.0:",
        buildable="@1.60.0:",
        description="Runtime polymorphism based on concepts.",
    )
    _boost_variant(
        "predef",
        when="@1.55.0:",
        description=(
            "A set of macros to identify compilers and consistently represent their versions."
        ),
    )
    # fmt: off
    _boost_variant(
        "align",
        when="@1.56.0:",
        description="Memory alignment functions, allocators, traits.",
    )
    _boost_variant(
        "core",
        when="@1.56.0:",
        description="A collection of simple core utilities with minimal dependencies.",
    )
    _boost_variant(
        "throw_exception",
        when="@1.56.0:",
        description="A common infrastructure for throwing exceptions from Boost libraries.",
    )
    _boost_variant(
        "type_index",
        when="@1.56.0:",
        description="Runtime/Compile time copyable type info.",
    )
    # fmt: on
    _boost_variant(
        "endian",
        when="@1.58.0:",
        description=(
            "Types and conversion functions for correct byte ordering, regardless of endianness."
        ),
    )
    # fmt: off
    _boost_variant(
        "sort",
        when="@1.58.0:",
        description="High-performance templated sort functions.",
    )
    # fmt: on
    _boost_variant(
        "convert",
        when="@1.59.0:",
        description="An extendible and configurable type-conversion framework.",
    )
    _boost_variant(
        "coroutine2",
        when="@1.59.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Coroutine2 requires cxxstd >= 11"},
        ],
        description="Generalized subroutines that allow suspending and resuming execution.",
    )
    # fmt: off
    _boost_variant(
        "vmd",
        when="@1.60.0:",
        description=(
            "Variadic macros that provide enhancements to the Boost preprocessor library."
        ),
    )
    _boost_variant(
        "compute",
        when="@1.61.0:",
        description="Multi-core CPU and GPGPU computing based on OpenCL.",
    )
    _boost_variant(
        "dll",
        when="@1.61.0:",
        description="Library for comfortable work with DLL and DSO.",
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
        description="Modern metaprogramming suited for computations on both types and values.",
    )
    _boost_variant(
        "metaparse",
        when="@1.61.0:",
        description="Generate compile-time parsers for embedded DSL code.",
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
        description="Lightweight userland threads.",
    )
    _boost_variant(
        "qvm",
        when="@1.62.0:",
        # fmt: off
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Fiber requires cxxstd >= 03"},
        ],
        # fmt: on
        description="Generic library for working with Quaternions, Vectors, and Matrices.",
    )
    # fmt: off
    _boost_variant(
        "process",
        when="@1.64.0:",
        description="Library to create processes in a portable way.",
    )
    # fmt: on
    _boost_variant(
        "context-impl",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        when="@1.65.0:",
        description="The backend for Boost.Context",
    )
    # fmt: off
    _boost_variant(
        "poly_collection",
        when="@1.65.0:",
        description="Fast containers of polymorphic objects.",
    )
    # fmt: on
    _boost_variant(
        "stacktrace",
        when="@1.65.0:",
        buildable="@1.65.0:",
        description="Gather, store, copy and print backtraces.",
    )
    _boost_variant(
        "beast",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.Beast requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.Beast requires cxxstd >= 11"},
        ],
        # fmt: off
        requires=[
            {"spec": "+asio", "msg": "Boost.Beast requires Boost.Asio"}
        ],
        # fmt: on
        description="Portable HTTP, WebSocket, and network operations using Boost.Asio",
    )
    _boost_variant(
        "callable_traits",
        when="@1.66.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.CallableTraits requires cxxstd >= 11"},
        ],
        description="Compile-time inspection and manipulation of all 'callable' types.",
    )
    # fmt: off
    _boost_variant(
        "mp11",
        when="@1.66.0:",
        description="C++11 metaprogramming.",
    )
    # fmt: on
    _boost_variant(
        "contract",
        when="@1.67.0:",
        buildable="@1.67.0:",
        description=(
            "Contract programming with subcontracting, class invariants, pre/postconditions, "
            "and customizable actions on assertion failure."
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
        "spirit_classic",
        when="@1.69.0:",
        description=(
            "LL parser framework represents parsers directly as EBNF grammars in inlined C++."
        ),
    )
    _boost_variant(
        "spirit_repository",
        when="@1.69.0:",
        description="A collection of reusable components for Qi parsers and Karma generators.",
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
        "histogram",
        when="@1.70.0:",
        # fmt: off
        requires=[
            {"spec": "+variant2", "msg": "Boost.Histogram requires Boost.Variant2"},
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
    # fmt: off
    _boost_variant(
        "static_string",
        when="@1.73.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.StaticString requires cxxstd >= 14"},
            {"when": "cxxstd=03", "msg": "Boost.StaticString requires cxxstd >= 14"},
            {"when": "cxxstd=11", "msg": "Boost.StaticString requires cxxstd >= 14"},
        ],
        description="A fixed capacity dynamically sized string.",
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
        description="CRTP templates for defining iterators, views, and containers.",
    )
    _boost_variant(
        "json",
        when="@1.75.0:",
        buildable="@1.75.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.filesystem requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.filesystem requires cxxstd >= 11"},
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
        description='Portable model for a "URL" or URI (as described in rfc3986).',
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
        description=(
            "Simple single-threaded asynchronicity akin to node.js and asyncio in python"
        ),
    )
    _boost_variant(
        "charconv",
        when="@1.85.0:",
        buildable="@1.85.0:",
        conflicts=[
            {"when": "cxxstd=98", "msg": "Boost.CharConv requires cxxstd >= 11"},
            {"when": "cxxstd=03", "msg": "Boost.CharConv requires cxxstd >= 11"},
        ],
        description="An implementation of C++20's <charconv> in C++11.",
    )
    return library_names
