# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
from io import StringIO

import spack.util.timer as timer


class Tick:
    """Timer that increments the seconds passed by 1
    everytime tick is called."""

    def __init__(self):
        self.time = 0.0

    def tick(self):
        self.time += 1
        return self.time


def test_timer():
    # 0
    t = timer.Timer(now=Tick().tick)

    # 1 (restart)
    t.start()

    # 2
    t.start("wrapped")

    # 3
    t.start("first")

    # 4
    t.stop("first")
    assert t.duration("first") == 1.0

    # 5
    t.start("second")

    # 6
    t.stop("second")
    assert t.duration("second") == 1.0

    # 7-8
    with t.measure("third"):
        pass
    assert t.duration("third") == 1.0

    # 9
    t.stop("wrapped")
    assert t.duration("wrapped") == 7.0

    # tick 10-13
    t.start("not-stopped")
    assert t.duration("not-stopped") == 1.0
    assert t.duration("not-stopped") == 2.0
    assert t.duration("not-stopped") == 3.0

    # 14
    assert t.duration() == 13.0

    # 15
    t.stop()
    assert t.duration() == 14.0


def test_timer_stop_stops_all():
    # Ensure that timer.stop() effectively stops all timers.

    # 0
    t = timer.Timer(now=Tick().tick)

    # 1
    t.start("first")

    # 2
    t.start("second")

    # 3
    t.start("third")

    # 4
    t.stop()

    assert t.duration("first") == 3.0
    assert t.duration("second") == 2.0
    assert t.duration("third") == 1.0
    assert t.duration() == 4.0


def test_stopping_unstarted_timer_is_no_error():
    t = timer.Timer(now=Tick().tick)
    assert t.duration("hello") == 0.0
    t.stop("hello")
    assert t.duration("hello") == 0.0


def test_timer_write():
    text_buffer = StringIO()
    json_buffer = StringIO()

    # 0
    t = timer.Timer(now=Tick().tick)

    # 1
    t.start("timer")

    # 2
    t.stop("timer")

    # 3
    t.stop()

    t.write_tty(text_buffer)
    t.write_json(json_buffer)

    output = text_buffer.getvalue().splitlines()
    assert "timer" in output[0]
    assert "1.000s" in output[0]
    assert "total" in output[1]
    assert "3.000s" in output[1]

    deserialized = json.loads(json_buffer.getvalue())
    assert deserialized == {
        "phases": [{"name": "timer", "path": "timer", "seconds": 1.0, "count": 1}],
        "total": 3.0,
    }


def test_null_timer():
    # Just ensure that the interface of the noop-timer doesn't break at some point
    buffer = StringIO()
    t = timer.NullTimer()
    t.start()
    t.start("first")
    t.stop("first")
    with t.measure("second"):
        pass
    t.stop()
    assert t.duration("first") == 0.0
    assert t.duration() == 0.0
    assert not t.phases
    t.write_json(buffer)
    t.write_tty(buffer)
    assert not buffer.getvalue()
