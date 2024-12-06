# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Debug signal handler: prints a stack trace and enters interpreter.

``register_interrupt_handler()`` enables a ctrl-C handler that prints
a stack trace and drops the user into an interpreter.

"""
import collections
import sys
import time
from contextlib import contextmanager
from typing import Callable, Dict, List

from llnl.util.lang import pretty_seconds_formatter

import spack.util.spack_json as sjson

TimerEvent = collections.namedtuple("TimerEvent", ("time", "running", "label"))
TimeTracker = collections.namedtuple("TimeTracker", ("total", "start", "count", "path"))

#: name for the global timer (used in start(), stop(), duration() without arguments)
global_timer_name = "_global"


class BaseTimer:
    def start(self, name=None):
        pass

    def stop(self, name=None):
        pass

    def duration(self, name=None):
        return 0.0

    @contextmanager
    def measure(self, name):
        yield self

    @property
    def phases(self):
        return []

    def write_json(self, out=sys.stdout):
        pass

    def write_tty(self, out=sys.stdout):
        pass


class NullTimer(BaseTimer):
    """Timer interface that does nothing, useful in for "tell
    don't ask" style code when timers are optional."""

    pass


class Timer(BaseTimer):
    """Simple interval timer"""

    def __init__(self, now: Callable[[], float] = time.time):
        """
        Arguments:
            now: function that gives the seconds since e.g. epoch
        """
        self._now = now
        self._timers: Dict[str, TimeTracker] = {}
        self._timer_stack: List[str] = []

        self._events: List[TimerEvent] = []
        # Push start event
        self._events.append(TimerEvent(self._now(), True, global_timer_name))

    def start(self, name=global_timer_name):
        """
        Start or restart a named timer, or the global timer when no name is given.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, the
                global timer is started.
        """
        self._events.append(TimerEvent(self._now(), True, name))

    def stop(self, name=global_timer_name):
        """
        Stop a named timer, or all timers when no name is given. Stopping a
        timer that has not started has no effect.

        Arguments:
            name (str): Optional name of the timer. When no name is passed, all
                timers are stopped.
        """
        self._events.append(TimerEvent(self._now(), False, name))

    def duration(self, name=global_timer_name):
        """
        Get the time in seconds of a named timer, or the total time if no
        name is passed. The duration is always 0 for timers that have not been
        started, no error is raised.

        Arguments:
            name (str): (Optional) name of the timer

        Returns:
            float: duration of timer.
        """
        self._flatten()
        if name in self._timers:
            if name in self._timer_stack:
                return self._timers[name].total + (self._now() - self._timers[name].start)
            return self._timers[name].total
        else:
            return 0.0

    @contextmanager
    def measure(self, name):
        """
        Context manager that allows you to time a block of code.

        Arguments:
            name (str): Name of the timer
        """
        self.start(name)
        yield self
        self.stop(name)

    @property
    def phases(self):
        """Get all named timers (excluding the global/total timer)"""
        self._flatten()
        return [k for k in self._timers.keys() if not k == global_timer_name]

    def _flatten(self):
        for event in self._events:
            if event.running:
                if event.label not in self._timer_stack:
                    self._timer_stack.append(event.label)
                # Only start the timer if it is on top of the stack
                # restart doesn't work after a subtimer is started
                if event.label == self._timer_stack[-1]:
                    timer_path = "/".join(self._timer_stack[1:])
                    tracker = self._timers.get(
                        event.label, TimeTracker(0.0, event.time, 0, timer_path)
                    )
                    assert tracker.path == timer_path
                    self._timers[event.label] = TimeTracker(
                        tracker.total, event.time, tracker.count, tracker.path
                    )
            else:  # if not event.running:
                if event.label in self._timer_stack:
                    index = self._timer_stack.index(event.label)
                    for label in self._timer_stack[index:]:
                        tracker = self._timers[label]
                        self._timers[label] = TimeTracker(
                            tracker.total + (event.time - tracker.start),
                            None,
                            tracker.count + 1,
                            tracker.path,
                        )
                    self._timer_stack = self._timer_stack[: max(0, index)]
        # clear events
        self._events = []

    def write_json(self, out=sys.stdout, extra_attributes={}):
        """Write a json object with times to file"""
        self._flatten()
        data = {
            "total": self._timers[global_timer_name].total,
            "phases": [
                {
                    "name": phase,
                    "path": self._timers[phase].path,
                    "seconds": self._timers[phase].total,
                    "count": self._timers[phase].count,
                }
                for phase in self.phases
            ],
        }
        if extra_attributes:
            data.update(extra_attributes)
        if out:
            out.write(sjson.dump(data))
        else:
            return data

    def write_tty(self, out=sys.stdout):
        """Write a human-readable summary of timings (depth is 1)"""
        self._flatten()

        times = [self.duration(p) for p in self.phases]

        # Get a consistent unit for the time
        pretty_seconds = pretty_seconds_formatter(max(times))

        # Tuples of (phase, time) including total.
        formatted = list(zip(self.phases, times))
        formatted.append(("total", self.duration()))

        # Write to out
        for name, duration in formatted:
            out.write(f"    {name:10s} {pretty_seconds(duration):>10s}\n")


#: instance of a do-nothing timer
NULL_TIMER = NullTimer()
