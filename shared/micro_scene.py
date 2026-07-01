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
    SHORTAGE_COLOR = ORANGE
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

        h_line = self.drop_to_axis(axes, x_val, y_val, axis="y", color=color)
        v_line = self.drop_to_axis(axes, x_val, y_val, axis="x", color=color)

        return VGroup(dot, dot_label, h_line, v_line)

    def drop_to_axis(self, axes, x_val, y_val, axis="x", label=None, color=None, label_direction=None, buff=0.15):
        """
        Dashed line from a point (x_val, y_val) straight down to the quantity
        axis (axis="x") or across to the price axis (axis="y") — used to mark
        where a price line meets a curve, e.g. Qd/Qs at a given price.
        """
        color = color or self.AXIS_COLOR
        point = axes.coords_to_point(x_val, y_val)
        if axis == "x":
            end = axes.coords_to_point(x_val, 0)
            label_direction = label_direction or DOWN
        else:
            end = axes.coords_to_point(0, y_val)
            label_direction = label_direction or LEFT

        line = DashedLine(point, end, color=color)
        group = VGroup(line)
        if label:
            text = Text(label, font_size=24, color=color).next_to(end, label_direction, buff=buff)
            group.add(text)
        return group

    def price_line(self, axes, price, x_max=None, color=None, label=None, label_direction=LEFT):
        """
        Horizontal dashed line at a given price, spanning the plot width —
        e.g. showing P = 40 to read off quantity demanded/supplied.
        """
        color = color or self.AXIS_COLOR
        x_max = x_max if x_max is not None else axes.x_range[1]
        start = axes.coords_to_point(0, price)
        end = axes.coords_to_point(x_max, price)

        line = DashedLine(start, end, color=color)
        group = VGroup(line)
        if label:
            text = Text(label, font_size=24, color=color).next_to(start, label_direction, buff=0.15)
            group.add(text)
        return group

    def label_axis_value(self, axes, axis, value, text, color=None, buff=0.2):
        """
        Text label at a specific value along an axis, e.g. marking
        P* = 30 on the price axis or Q* = 40 on the quantity axis.
        axis: "x" or "y".
        """
        color = color or self.AXIS_COLOR
        if axis == "x":
            point = axes.coords_to_point(value, 0)
            direction = DOWN
        else:
            point = axes.coords_to_point(0, value)
            direction = LEFT
        return Text(text, font_size=24, color=color).next_to(point, direction, buff=buff)

    def mark_gap(self, axes, x1, x2, y=0, label=None, color=None, label_direction=DOWN, buff=0.3):
        """
        Double-headed arrow along the quantity axis between two x-values,
        used to show the size of a surplus or shortage gap.
        """
        color = color or self.SURPLUS_COLOR
        p1 = axes.coords_to_point(x1, y)
        p2 = axes.coords_to_point(x2, y)

        arrow = DoubleArrow(p1, p2, color=color, buff=0)
        group = VGroup(arrow)
        if label:
            text = Text(label, font_size=24, color=color).next_to(arrow, label_direction, buff=buff)
            group.add(text)
        return group

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