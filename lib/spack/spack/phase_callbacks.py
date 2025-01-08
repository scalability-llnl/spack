# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections

import llnl.util.lang as lang

#: An object of this kind is a shared global state used to collect callbacks during
#: class definition time, and is flushed when the class object is created at the end
#: of the class definition
#:
#: Args:
#:    attribute_name (str): name of the attribute that will be attached to the builder
#:    callbacks (list): container used to temporarily aggregate the callbacks
CallbackTemporaryStage = collections.namedtuple(
    "CallbackTemporaryStage", ["attribute_name", "callbacks"]
)

#: Shared global state to aggregate "@run_before" callbacks
_RUN_BEFORE = CallbackTemporaryStage(attribute_name="run_before_callbacks", callbacks=[])
#: Shared global state to aggregate "@run_after" callbacks
_RUN_AFTER = CallbackTemporaryStage(attribute_name="run_after_callbacks", callbacks=[])


class PhaseCallbacksMeta(type):
    """Permit to register arbitrary functions during class definition and run them
    later, before or after a given install phase.

    Each method decorated with ``run_before`` or ``run_after`` gets temporarily
    stored in a global shared state when a class being defined is parsed by the Python
    interpreter. At class definition time that temporary storage gets flushed and a list
    of callbacks is attached to the class being defined.
    """

    def __new__(mcs, name, bases, attr_dict):
        for temporary_stage in (_RUN_BEFORE, _RUN_AFTER):
            staged_callbacks = temporary_stage.callbacks

            # Here we have an adapter from an old-style package. This means there is no
            # hierarchy of builders, and every callback that had to be combined between
            # *Package and *Builder has been combined already by _PackageAdapterMeta
            if name == "Adapter":
                continue

            # If we are here we have callbacks. To get a complete list, we accumulate all the
            # callbacks from base classes, we deduplicate them, then prepend what we have
            # registered here.
            #
            # The order should be:
            # 1. Callbacks are registered in order within the same class
            # 2. Callbacks defined in derived classes precede those defined in base
            #    classes
            callbacks_from_base = []
            for base in bases:
                current_callbacks = getattr(base, temporary_stage.attribute_name, None)
                if not current_callbacks:
                    continue
                callbacks_from_base.extend(current_callbacks)
            callbacks_from_base = list(lang.dedupe(callbacks_from_base))
            # Set the callbacks in this class and flush the temporary stage
            attr_dict[temporary_stage.attribute_name] = staged_callbacks[:] + callbacks_from_base
            del temporary_stage.callbacks[:]

        return super(PhaseCallbacksMeta, mcs).__new__(mcs, name, bases, attr_dict)

    @staticmethod
    def run_after(phase, when=None):
        """Decorator to register a function for running after a given phase.

        Args:
            phase (str): phase after which the function must run.
            when (str): condition under which the function is run (if None, it is always run).
        """

        def _decorator(fn):
            key = (phase, when)
            item = (key, fn)
            _RUN_AFTER.callbacks.append(item)
            return fn

        return _decorator

    @staticmethod
    def run_before(phase, when=None):
        """Decorator to register a function for running before a given phase.

        Args:
           phase (str): phase before which the function must run.
           when (str): condition under which the function is run (if None, it is always run).
        """

        def _decorator(fn):
            key = (phase, when)
            item = (key, fn)
            _RUN_BEFORE.callbacks.append(item)
            return fn

        return _decorator


# Export these names as standalone to be used in packages
run_after = PhaseCallbacksMeta.run_after
run_before = PhaseCallbacksMeta.run_before
