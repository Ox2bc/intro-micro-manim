from manim import *

class MicroScene(Scene):
    """
    Base class for all Intro Micro videos.
    Holds shared color palette, axis style, and reusable
    animation helpers so every video looks/behaves consistently.
    """

    # ---- Shared color palette ----
    DEMAND_COLOR = BLUE
    SUPPLY_COLOR = RED
    EQUILIBRIUM_COLOR = YELLOW
    SURPLUS_COLOR = GREEN
    DWL_COLOR = GRAY
    AXIS_COLOR = WHITE

    def make_axes(self, x_range=(0, 10, 1), y_range=(0, 10, 1),
                  x_label="Quantity", y_label="Price"):
        """Standard styled axes used across the series."""
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"color": self.AXIS_COLOR, "include_tip": True},
            tips=True,
        )
        x_text = axes.get_x_axis_label(x_label, edge=DOWN, direction=DOWN)
        y_text = axes.get_y_axis_label(y_label, edge=LEFT, direction=LEFT).rotate(PI / 2)
        y_text.next_to(axes.y_axis, LEFT, buff=0.3)
        return axes, x_text, y_text

    def make_curve(self, axes, func, x_range, color, label=None, label_direction=UP):
        """Returns a styled curve (and optional label) plotted on given axes."""
        curve = axes.plot(func, x_range=x_range, color=color)
        if label:
            curve_label = axes.get_graph_label(
                curve, label=label, direction=label_direction, color=color
            )
            return curve, curve_label
        return curve, None

    def shift_curve(self, axes, old_curve, new_func, x_range, run_time=2):
        """
        Animates a curve morphing into a new function — e.g. demand
        shifting right after an income increase. Returns the new curve
        mobject (old_curve is transformed into it).
        """
        new_curve = axes.plot(new_func, x_range=x_range, color=old_curve.color)
        self.play(Transform(old_curve, new_curve), run_time=run_time)
        return old_curve  # old_curve now visually IS the new curve

    def mark_equilibrium(self, axes, x_val, y_val, label="E", color=None, label_direction=UR):
        color = color or self.EQUILIBRIUM_COLOR
        point = axes.coords_to_point(x_val, y_val)
        dot = Dot(point, color=color)
        dot_label = Text(label, font_size=24, color=color).next_to(dot, label_direction, buff=0.1)

        h_line = DashedLine(axes.coords_to_point(0, y_val), point, color=color)
        v_line = DashedLine(axes.coords_to_point(x_val, 0), point, color=color)

        return VGroup(dot, dot_label, h_line, v_line)

    def shade_region(self, axes, func1, func2, x_range, color=None, opacity=0.5):
        """
        Shades the area between two functions over x_range —
        used for surplus, deadweight loss, tax incidence wedges, etc.
        """
        color = color or self.SURPLUS_COLOR
        area = axes.get_area(
            axes.plot(func1, x_range=x_range),
            x_range=x_range,
            bounded_graph=axes.plot(func2, x_range=x_range),
            color=color,
            opacity=opacity,
        )
        return area