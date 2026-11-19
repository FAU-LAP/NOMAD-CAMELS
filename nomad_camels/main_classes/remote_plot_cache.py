"""Plain-Python copies of the live plots for OASIS.

The Qt plot windows can only be read in the GUI thread. ``RemotePlotCache``
keeps a thread-safe copy of the data and of the plot's appearance, which the
API thread and the OASIS remote agent can read at any time.

Data is append-only with a cursor, so a client asks only for the points it has
not seen yet. ``generation`` changes whenever the plot is cleared; a client
with an outdated generation receives the plot from the beginning again.

Every change increases a counter, so the remote agent can tell OASIS that
there is something new without sending the data itself.
"""

from __future__ import annotations

import math
import threading
import uuid

# Upper bound of numbers (x and all y values) in one snapshot of all plots.
# Keeps a reply well below the 1 MiB message limit of the OASIS connection.
MAX_VALUES_PER_SNAPSHOT = 20000

# pyqtgraph symbol -> Plotly marker symbol
PLOTLY_SYMBOLS = {
    "o": "circle",
    "s": "square",
    "t": "triangle-down",
    "t1": "triangle-up",
    "t2": "triangle-right",
    "t3": "triangle-left",
    "d": "diamond",
    "+": "cross-thin",
    "x": "x-thin",
    "p": "pentagon",
    "h": "hexagon",
    "star": "star",
    "arrow_up": "arrow-up",
    "arrow_right": "arrow-right",
    "arrow_down": "arrow-down",
    "arrow_left": "arrow-left",
    "crosshair": "cross-thin",
}

# Name of a Qt pen style -> Plotly dash
PLOTLY_DASHES = {
    "SolidLine": "solid",
    "DashLine": "dash",
    "DotLine": "dot",
    "DashDotLine": "dashdot",
    "DashDotDotLine": "longdashdot",
}


def json_value(value):
    """Return ``value`` as a JSON-compatible number, list or string."""
    if hasattr(value, "tolist"):
        value = value.tolist()
    elif hasattr(value, "item"):
        try:
            value = value.item()
        except (TypeError, ValueError):
            pass
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [json_value(item) for item in value]
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return str(value)


def plotly_style(
    *,
    line_color=None,
    line_width=2,
    pen_style="NoPen",
    symbol=None,
    symbol_size=10,
    symbol_color=None,
    symbol_line_color=None,
    visible=True,
):
    """Translate pyqtgraph's appearance of one curve into Plotly trace fields."""
    dash = PLOTLY_DASHES.get(pen_style)
    plotly_symbol = PLOTLY_SYMBOLS.get(symbol) if symbol else None
    if dash and plotly_symbol:
        mode = "lines+markers"
    elif dash:
        mode = "lines"
    else:
        mode = "markers"
    style = {"mode": mode, "visible": True if visible else "legendonly"}
    if dash:
        style["line"] = {"color": line_color, "width": line_width, "dash": dash}
    if plotly_symbol or not dash:
        color = symbol_color or line_color
        style["marker"] = {
            "symbol": plotly_symbol or "circle",
            "size": symbol_size,
            "color": color,
            "line": {"color": symbol_line_color or color, "width": 1},
        }
    return style


class RemotePlotCache:
    """Thread-safe data copy and appearance of one 1D live plot."""

    def __init__(self, *, title, x_label, y_label, y_axes=None, y_names=(), maxlen=None):
        self._lock = threading.Lock()
        self._token = uuid.uuid4().hex[:8]
        self._clears = 0
        self._meta = {
            "title": str(title or ""),
            "x_label": str(x_label or ""),
            "y_label": str(y_label or ""),
            "y2_label": "",
            "x_log": False,
            "y_log": False,
            "y2_log": False,
            "background": None,
            "foreground": None,
        }
        self._y_axes = dict(y_axes or {})
        try:
            self._maxlen = int(maxlen) if maxlen is not None and math.isfinite(float(maxlen)) else None
        except (TypeError, ValueError):
            self._maxlen = None
        self._offset = 0
        self._x: list = []
        self._order: list[str] = [str(name) for name in y_names]
        self._y: dict[str, list] = {name: [] for name in self._order}
        self._styles: dict[str, dict] = {}
        self._fits: dict[str, dict] = {}
        self._info: dict = {}
        self._version = 0
        self._changes = 0

    @property
    def changes(self) -> int:
        """Increases with every change of data, appearance or run info."""
        return self._changes

    @property
    def generation(self) -> str:
        return f"{self._token}-{self._clears}"

    def append(self, x, ys: dict) -> None:
        """Add one point; ``ys`` maps curve name to value."""
        with self._lock:
            self._x.append(json_value(x))
            for name in ys:
                name = str(name)
                if name not in self._y:
                    self._order.append(name)
                    self._y[name] = [None] * (len(self._x) - 1)
            values = {str(name): value for name, value in ys.items()}
            for name in self._order:
                self._y[name].append(json_value(values.get(name)))
            if self._maxlen is not None and len(self._x) > self._maxlen:
                drop = len(self._x) - self._maxlen
                del self._x[:drop]
                for values_list in self._y.values():
                    del values_list[:drop]
                self._offset += drop
            self._changes += 1

    def clear(self) -> None:
        with self._lock:
            self._clears += 1
            self._offset = 0
            self._x = []
            self._y = {name: [] for name in self._order}
            self._fits = {}
            self._version += 1
            self._changes += 1

    def set_appearance(self, styles: dict[str, dict], meta: dict) -> None:
        """Store curve styles and axis settings read in the GUI thread."""
        with self._lock:
            new_meta = {**self._meta, **{k: v for k, v in meta.items() if k in self._meta}}
            if styles != self._styles or new_meta != self._meta:
                self._styles = dict(styles)
                self._meta = new_meta
                self._version += 1
                self._changes += 1

    def set_info(self, info: dict) -> None:
        """Store the run this plot belongs to (protocol, times, state,
        variables); the given keys replace the stored ones."""
        with self._lock:
            new_info = {**self._info, **{str(k): json_value(v) if not isinstance(v, dict)
                                          else {str(n): json_value(x) for n, x in v.items()}
                                          for k, v in info.items()}}
            if new_info != self._info:
                self._info = new_info
                self._version += 1
                self._changes += 1

    @property
    def info(self) -> dict:
        with self._lock:
            return dict(self._info)

    def set_fit(self, name: str, x, y, style: dict, axis: str = "y") -> None:
        """Replace the curve of one fit; empty data removes it."""
        with self._lock:
            if len(x) == 0:
                removed = self._fits.pop(str(name), None)
                if removed is not None:
                    self._version += 1
                    self._changes += 1
                return
            self._fits[str(name)] = {
                "name": str(name),
                "x": json_value(list(x)),
                "y": json_value(list(y)),
                "axis": axis,
                **style,
            }
            self._version += 1
            self._changes += 1

    def snapshot(self, since=None, generation=None, version=None, max_values=None) -> dict:
        """Return the points from index ``since`` on.

        Args:
            since: Absolute index of the first point the client does not have.
            generation: Generation the client's points belong to.
            version: Appearance version the client has; fits and styles are
                left out when it is current.
            max_values: Limit of numbers in this reply; the rest follows in
                the next request (``more`` is true).
        """
        with self._lock:
            end = self._offset + len(self._x)
            reset = (
                generation != self.generation
                or not isinstance(since, int)
                or since < self._offset
                or since > end
            )
            start = self._offset if reset else since
            per_point = 1 + len(self._order)
            limit = max(1, (max_values or MAX_VALUES_PER_SNAPSHOT) // per_point)
            stop = min(end, start + limit)
            first, last = start - self._offset, stop - self._offset
            traces = []
            for name in self._order:
                trace = {
                    "name": name,
                    "axis": "y2" if self._y_axes.get(name, 1) == 2 else "y",
                    "y": self._y[name][first:last],
                }
                trace.update(self._styles.get(name) or plotly_style())
                traces.append(trace)
            result = {
                **self._meta,
                "generation": self.generation,
                "version": self._version,
                "reset": reset,
                "start": start,
                "end": stop,
                "more": stop < end,
                "x": self._x[first:last],
                "traces": traces,
            }
            if reset or version != self._version:
                result["fits"] = [dict(fit) for fit in self._fits.values()]
                result["info"] = dict(self._info)
            return result


class PlotCacheRegistry:
    """All open live plots of this CAMELS instance, readable from any thread."""

    def __init__(self):
        self._lock = threading.Lock()
        self._caches: dict[str, RemotePlotCache] = {}
        self._changes = 0

    def register(self, cache_id: str, cache: RemotePlotCache) -> None:
        with self._lock:
            self._caches[str(cache_id)] = cache
            self._changes += 1

    def unregister(self, cache_id: str) -> None:
        with self._lock:
            if self._caches.pop(str(cache_id), None) is not None:
                self._changes += 1

    def ids(self) -> list[str]:
        with self._lock:
            return list(self._caches)

    def change_token(self) -> tuple:
        """Differs from the previous value whenever a plot was opened,
        closed or changed. Cheap; meant to be compared often."""
        with self._lock:
            return (self._changes, tuple((key, cache.changes) for key, cache in self._caches.items()))

    def snapshots(self, cursors: dict | None = None) -> dict:
        """Return the new points of every plot.

        ``cursors`` maps a plot id to ``{"generation", "since", "version"}``
        from the client's previous reply.
        """
        with self._lock:
            caches = list(self._caches.items())
        cursors = cursors if isinstance(cursors, dict) else {}
        budget = MAX_VALUES_PER_SNAPSHOT // max(1, len(caches))
        plots = []
        for cache_id, cache in caches:
            cursor = cursors.get(cache_id)
            cursor = cursor if isinstance(cursor, dict) else {}
            try:
                plots.append(
                    {
                        "id": cache_id,
                        **cache.snapshot(
                            since=cursor.get("since"),
                            generation=cursor.get("generation"),
                            version=cursor.get("version"),
                            max_values=budget,
                        ),
                    }
                )
            except (AttributeError, RuntimeError, TypeError, ValueError):
                continue
        return {"open_plot_count": len(plots), "plots": plots}
