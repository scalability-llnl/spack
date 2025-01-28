# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import copy
import functools
from typing import Dict, List, Optional, Tuple, Type

import spack.error
import spack.multimethod
import spack.package_base
import spack.phase_callbacks
import spack.repo
import spack.spec
import spack.util.environment

#: Builder classes, as registered by the "builder" decorator
BUILDER_CLS: Dict[str, Type["Builder"]] = {}

#: Map id(pkg) to a builder, to avoid creating multiple
#: builders for the same package object.
_BUILDERS: Dict[int, "Builder"] = {}


def builder(build_system_name: str):
    """Class decorator used to register the default builder
    for a given build-system.

    Args:
        build_system_name: name of the build-system
    """

    def _decorator(cls):
        cls.build_system = build_system_name
        BUILDER_CLS[build_system_name] = cls
        return cls

    return _decorator


def create(pkg: spack.package_base.PackageBase) -> "Builder":
    """Given a package object with an associated concrete spec, return the builder object that can
    install it."""
    if id(pkg) not in _BUILDERS:
        _BUILDERS[id(pkg)] = _create(pkg)
    return _BUILDERS[id(pkg)]


class _PhaseAdapter:
    def __init__(self, builder, phase_fn):
        self.builder = builder
        self.phase_fn = phase_fn

    def __call__(self, spec, prefix):
        return self.phase_fn(self.builder.pkg, spec, prefix)


def get_builder_class(pkg, name: str) -> Optional[Type["Builder"]]:
    """Return the builder class if a package module defines it."""
    cls = getattr(pkg.module, name, None)
    if cls and cls.__module__.startswith(spack.repo.ROOT_PYTHON_NAMESPACE):
        return cls
    return None


def _create(pkg: spack.package_base.PackageBase) -> "Builder":
    """Return a new builder object for the package object being passed as argument.

    The function inspects the build-system used by the package object and try to:

    1. Return a custom builder, if any is defined in the same ``package.py`` file.
    2. Return a customization of more generic builders, if any is defined in the
       class hierarchy (look at AspellDictPackage for an example of that)
    3. Return a run-time generated adapter builder otherwise

    The run-time generated adapter builder is capable of adapting an old-style package
    to the new architecture, where the installation procedure has been extracted from
    the ``*Package`` hierarchy into a ``*Builder`` hierarchy. This means that the
    adapter looks for attribute or method overrides preferably in the ``*Package``
    before using the default builder implementation.

    Note that in case a builder is explicitly coded in ``package.py``, no attempt is made
    to look for build-related methods in the ``*Package``.

    Args:
        pkg: package object for which we need a builder
    """
    package_buildsystem = buildsystem_name(pkg)
    default_builder_cls = BUILDER_CLS[package_buildsystem]
    builder_cls_name = default_builder_cls.__name__
    builder_class = get_builder_class(pkg, builder_cls_name)

    if builder_class:
        return builder_class(pkg)

    # Specialized version of a given buildsystem can subclass some
    # base classes and specialize certain phases or methods or attributes.
    # In that case they can store their builder class as a class level attribute.
    # See e.g. AspellDictPackage as an example.
    base_cls = getattr(pkg, builder_cls_name, default_builder_cls)

    # From here on we define classes to construct a special builder that adapts to the
    # old, single class, package format. The adapter forwards any call or access to an
    # attribute related to the installation procedure to a package object wrapped in
    # a class that falls-back on calling the base builder if no override is found on the
    # package. The semantic should be the same as the method in the base builder were still
    # present in the base class of the package.

    class _ForwardToBaseBuilder:
        def __init__(self, wrapped_pkg_object, root_builder):
            self.wrapped_package_object = wrapped_pkg_object
            self.root_builder = root_builder

            package_cls = type(wrapped_pkg_object)
            wrapper_cls = type(self)
            bases = (package_cls, wrapper_cls)
            new_cls_name = package_cls.__name__ + "Wrapper"
            # Forward attributes that might be monkey patched later
            new_cls = type(
                new_cls_name,
                bases,
                {
                    "run_tests": property(lambda x: x.wrapped_package_object.run_tests),
                    "test_requires_compiler": property(
                        lambda x: x.wrapped_package_object.test_requires_compiler
                    ),
                    "test_suite": property(lambda x: x.wrapped_package_object.test_suite),
                    "tester": property(lambda x: x.wrapped_package_object.tester),
                },
            )
            new_cls.__module__ = package_cls.__module__
            self.__class__ = new_cls
            self.__dict__.update(wrapped_pkg_object.__dict__)

        def __getattr__(self, item):
            result = getattr(super(type(self.root_builder), self.root_builder), item)
            if item in super(type(self.root_builder), self.root_builder).phases:
                result = _PhaseAdapter(self.root_builder, result)
            return result

    def forward_method_to_getattr(fn_name):
        def __forward(self, *args, **kwargs):
            return self.__getattr__(fn_name)(*args, **kwargs)

        return __forward

    # Add fallback methods for the Package object to refer to the builder. If a method
    # with the same name is defined in the Package, it will override this definition
    # (when _ForwardToBaseBuilder is initialized)
    for method_name in (
        base_cls.phases  # type: ignore
        + base_cls.legacy_methods  # type: ignore
        + getattr(base_cls, "legacy_long_methods", tuple())
        + ("setup_build_environment", "setup_dependent_build_environment")
    ):
        setattr(_ForwardToBaseBuilder, method_name, forward_method_to_getattr(method_name))

    def forward_property_to_getattr(property_name):
        def __forward(self):
            return self.__getattr__(property_name)

        return __forward

    for attribute_name in base_cls.legacy_attributes:  # type: ignore
        setattr(
            _ForwardToBaseBuilder,
            attribute_name,
            property(forward_property_to_getattr(attribute_name)),
        )

    class Adapter(base_cls, metaclass=_PackageAdapterMeta):  # type: ignore
        def __init__(self, pkg):
            # Deal with custom phases in packages here
            if hasattr(pkg, "phases"):
                self.phases = pkg.phases
                for phase in self.phases:
                    setattr(Adapter, phase, _PackageAdapterMeta.phase_method_adapter(phase))

            # Attribute containing the package wrapped in dispatcher with a `__getattr__`
            # method that will forward certain calls to the default builder.
            self.pkg_with_dispatcher = _ForwardToBaseBuilder(pkg, root_builder=self)
            super().__init__(pkg)

        # These two methods don't follow the (self, spec, prefix) signature of phases nor
        # the (self) signature of methods, so they are added explicitly to avoid using a
        # catch-all (*args, **kwargs)
        def setup_build_environment(self, env):
            return self.pkg_with_dispatcher.setup_build_environment(env)

        def setup_dependent_build_environment(self, env, dependent_spec):
            return self.pkg_with_dispatcher.setup_dependent_build_environment(env, dependent_spec)

    return Adapter(pkg)


def buildsystem_name(pkg: spack.package_base.PackageBase) -> str:
    """Given a package object with an associated concrete spec,
    return the name of its build system."""
    try:
        return pkg.spec.variants["build_system"].value
    except KeyError:
        # We are reading an old spec without the build_system variant
        return pkg.legacy_buildsystem  # type: ignore


class BuilderMeta(
    spack.phase_callbacks.PhaseCallbacksMeta,
    spack.multimethod.MultiMethodMeta,
    type(collections.abc.Sequence),  # type: ignore
):
    pass


class _PackageAdapterMeta(BuilderMeta):
    """Metaclass to adapt old-style packages to the new architecture based on builders
    for the installation phase.

    This class does the necessary mangling to function argument so that a call to a
    builder object can delegate to a package object.
    """

    @staticmethod
    def phase_method_adapter(phase_name):
        def _adapter(self, pkg, spec, prefix):
            phase_fn = getattr(self.pkg_with_dispatcher, phase_name)
            return phase_fn(spec, prefix)

        return _adapter

    @staticmethod
    def legacy_long_method_adapter(method_name):
        def _adapter(self, spec, prefix):
            bind_method = getattr(self.pkg_with_dispatcher, method_name)
            return bind_method(spec, prefix)

        return _adapter

    @staticmethod
    def legacy_method_adapter(method_name):
        def _adapter(self):
            bind_method = getattr(self.pkg_with_dispatcher, method_name)
            return bind_method()

        return _adapter

    @staticmethod
    def legacy_attribute_adapter(attribute_name):
        def _adapter(self):
            return getattr(self.pkg_with_dispatcher, attribute_name)

        return property(_adapter)

    @staticmethod
    def combine_callbacks(pipeline_attribute_name):
        """This function combines callbacks from old-style packages with callbacks that might
        be registered for the default builder.

        It works by:
        1. Extracting the callbacks from the old-style package
        2. Transforming those callbacks by adding an adapter that receives a builder as argument
           and calls the wrapped function with ``builder.pkg``
        3. Combining the list of transformed callbacks with those that might be present in the
           default builder
        """

        def _adapter(self):
            def unwrap_pkg(fn):
                @functools.wraps(fn)
                def _wrapped(builder):
                    return fn(builder.pkg_with_dispatcher)

                return _wrapped

            # Concatenate the current list with the one from package
            callbacks_from_package = getattr(self.pkg, pipeline_attribute_name, [])
            callbacks_from_package = [(key, unwrap_pkg(x)) for key, x in callbacks_from_package]
            callbacks_from_builder = getattr(super(type(self), self), pipeline_attribute_name, [])
            return callbacks_from_package + callbacks_from_builder

        return property(_adapter)

    def __new__(mcs, name, bases, attr_dict):
        # Add ways to intercept methods and attribute calls and dispatch
        # them first to a package object
        default_builder_cls = bases[0]
        for phase_name in default_builder_cls.phases:
            attr_dict[phase_name] = _PackageAdapterMeta.phase_method_adapter(phase_name)

        for method_name in default_builder_cls.legacy_methods:
            attr_dict[method_name] = _PackageAdapterMeta.legacy_method_adapter(method_name)

        # These exist e.g. for Python, see discussion in https://github.com/spack/spack/pull/32068
        for method_name in getattr(default_builder_cls, "legacy_long_methods", []):
            attr_dict[method_name] = _PackageAdapterMeta.legacy_long_method_adapter(method_name)

        for attribute_name in default_builder_cls.legacy_attributes:
            attr_dict[attribute_name] = _PackageAdapterMeta.legacy_attribute_adapter(
                attribute_name
            )

        combine_callbacks = _PackageAdapterMeta.combine_callbacks
        attr_dict[spack.phase_callbacks._RUN_BEFORE.attribute_name] = combine_callbacks(
            spack.phase_callbacks._RUN_BEFORE.attribute_name
        )
        attr_dict[spack.phase_callbacks._RUN_AFTER.attribute_name] = combine_callbacks(
            spack.phase_callbacks._RUN_AFTER.attribute_name
        )

        return super(_PackageAdapterMeta, mcs).__new__(mcs, name, bases, attr_dict)


class InstallationPhase:
    """Manages a single phase of the installation.

    This descriptor stores at creation time the name of the method it should
    search for execution. The method is retrieved at __get__ time, so that
    it can be overridden by subclasses of whatever class declared the phases.

    It also provides hooks to execute arbitrary callbacks before and after
    the phase.
    """

    def __init__(self, name, builder):
        self.name = name
        self.builder = builder
        self.phase_fn = self._select_phase_fn()
        self.run_before = self._make_callbacks(spack.phase_callbacks._RUN_BEFORE.attribute_name)
        self.run_after = self._make_callbacks(spack.phase_callbacks._RUN_AFTER.attribute_name)

    def _make_callbacks(self, callbacks_attribute):
        result = []
        callbacks = getattr(self.builder, callbacks_attribute, [])
        for (phase, condition), fn in callbacks:
            # Same if it is for another phase
            if phase != self.name:
                continue

            # If we have no condition or the callback satisfies a condition, register it
            if condition is None or self.builder.pkg.spec.satisfies(condition):
                result.append(fn)
        return result

    def __str__(self):
        msg = '{0}: executing "{1}" phase'
        return msg.format(self.builder, self.name)

    def execute(self):
        pkg = self.builder.pkg
        self._on_phase_start(pkg)

        for callback in self.run_before:
            callback(self.builder)

        self.phase_fn(pkg, pkg.spec, pkg.prefix)

        for callback in self.run_after:
            callback(self.builder)

        self._on_phase_exit(pkg)

    def _select_phase_fn(self):
        phase_fn = getattr(self.builder, self.name, None)

        if not phase_fn:
            msg = (
                'unexpected error: package "{0.fullname}" must implement an '
                '"{1}" phase for the "{2}" build system'
            )
            raise RuntimeError(msg.format(self.builder.pkg, self.name, self.builder.build_system))

        return phase_fn

    def _on_phase_start(self, instance):
        # If a phase has a matching stop_before_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "stop_before_phase", None) == self.name:
            raise spack.error.StopPhase("Stopping before '{0}' phase".format(self.name))

    def _on_phase_exit(self, instance):
        # If a phase has a matching last_phase attribute,
        # stop the installation process raising a StopPhase
        if getattr(instance, "last_phase", None) == self.name:
            raise spack.error.StopPhase("Stopping at '{0}' phase".format(self.name))

    def copy(self):
        return copy.deepcopy(self)


class BaseBuilder(metaclass=BuilderMeta):
    """An interface for builders, without any phases defined. This class is exposed in the package
    API, so that packagers can create a single class to define ``setup_build_environment`` and
    ``@run_before`` and ``@run_after`` callbacks that can be shared among different builders.

    Example:

    .. code-block:: python

       class AnyBuilder(BaseBuilder):
           @run_after("install")
           def fixup_install(self):
                # do something after the package is installed
                pass

           def setup_build_environment(self, env):
                env.set("MY_ENV_VAR", "my_value")

        class CMakeBuilder(cmake.CMakeBuilder, AnyBuilder):
            pass

        class AutotoolsBuilder(autotools.AutotoolsBuilder, AnyBuilder):
            pass
    """

    def __init__(self, pkg: spack.package_base.PackageBase) -> None:
        self.pkg = pkg

    @property
    def spec(self) -> spack.spec.Spec:
        return self.pkg.spec

    @property
    def stage(self):
        return self.pkg.stage

    @property
    def prefix(self):
        return self.pkg.prefix

    def setup_build_environment(
        self, env: spack.util.environment.EnvironmentModifications
    ) -> None:
        """Sets up the build environment for a package.

        This method will be called before the current package prefix exists in
        Spack's store.

        Args:
            env: environment modifications to be applied when the package is built. Package authors
                can call methods on it to alter the build environment.
        """
        if not hasattr(super(), "setup_build_environment"):
            return
        super().setup_build_environment(env)  # type: ignore

    def setup_dependent_build_environment(
        self, env: spack.util.environment.EnvironmentModifications, dependent_spec: spack.spec.Spec
    ) -> None:
        """Sets up the build environment of a package that depends on this one.

        This is similar to ``setup_build_environment``, but it is used to modify the build
        environment of a package that *depends* on this one.

        This gives packages the ability to set environment variables for the build of the
        dependent, which can be useful to provide search hints for headers or libraries if they are
        not in standard locations.

        This method will be called before the dependent package prefix exists in Spack's store.

        Args:
            env: environment modifications to be applied when the dependent package is built.
                Package authors can call methods on it to alter the build environment.

            dependent_spec: the spec of the dependent package about to be built. This allows the
                extendee (self) to query the dependent's state. Note that *this* package's spec is
                available as ``self.spec``
        """
        if not hasattr(super(), "setup_dependent_build_environment"):
            return
        super().setup_dependent_build_environment(env, dependent_spec)  # type: ignore

    def __repr__(self):
        fmt = "{name}{/hash:7}"
        return f"{self.__class__.__name__}({self.spec.format(fmt)})"

    def __str__(self):
        fmt = "{name}{/hash:7}"
        return f'"{self.__class__.__name__}" builder for "{self.spec.format(fmt)}"'


class Builder(BaseBuilder, collections.abc.Sequence):
    """A builder is a class that, given a package object (i.e. associated with concrete spec),
    knows how to install it.

    The builder behaves like a sequence, and when iterated over return the "phases" of the
    installation in the correct order.
    """

    #: Sequence of phases. Must be defined in derived classes
    phases: Tuple[str, ...] = ()
    #: Build system name. Must also be defined in derived classes.
    build_system: Optional[str] = None

    legacy_methods: Tuple[str, ...] = ()
    legacy_attributes: Tuple[str, ...] = ()

    # type hints for some of the legacy methods
    build_time_test_callbacks: List[str]
    install_time_test_callbacks: List[str]

    #: List of glob expressions. Each expression must either be absolute or relative to the package
    #: source path. Matching artifacts found at the end of the build process will be copied in the
    #: same directory tree as _spack_build_logfile and _spack_build_envfile.
    @property
    def archive_files(self) -> List[str]:
        return []

    def __init__(self, pkg: spack.package_base.PackageBase) -> None:
        super().__init__(pkg)
        self.callbacks = {}
        for phase in self.phases:
            self.callbacks[phase] = InstallationPhase(phase, self)

    def __getitem__(self, idx):
        key = self.phases[idx]
        return self.callbacks[key]

    def __len__(self):
        return len(self.phases)
