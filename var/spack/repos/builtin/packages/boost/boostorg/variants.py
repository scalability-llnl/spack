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
    _boost_variant(
        "multithreaded",
        description="Enable use of multiple threads",
    )
    _boost_variant(
        "singlethreaded",
        default=False,
        description="Disable use of multiple threads",
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
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------

    return library_names
