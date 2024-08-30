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

    return library_names
