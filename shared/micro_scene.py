from manim import *

class MicroScene(Scene):
    """
    Base class for all Intro Micro videos.
    Holds shared color palette, axis style, and reusable
    animation helpers so every video looks/behaves consistently.

    Label convention: curve labels (in make_curve) default to sitting on
    the inside of the plot relative to their cutoff endpoint, not sticking
    out toward the nearest axis/arrow. E.g. demand curves end near the
    bottom -> label goes UP; supply curves end near the top -> label goes
    DOWN. Override label_direction per-beat only when this default would
    collide with another mobject.

    Text row alignment: when arranging multiple Text() words in a RIGHT
    row, always pass aligned_edge=UP. Manim centers each word on its own
    glyph bounding box, so a word with a descender (e.g. "Money", "Study")
    sits visibly lower than neighbors without one under the default center
    alignment.
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
        axes.shift(RIGHT * 0.7)
        x_text = axes.get_x_axis_label(x_label, edge=RIGHT, direction=DOWN, buff=0.3)
        y_text = axes.get_y_axis_label(y_label, edge=UP, direction=LEFT, buff=0.3).rotate(PI / 2)
        return axes, x_text, y_text

    def make_curve(self, axes, func, x_range, color, label=None, label_direction=UP, label_x_val=None):
        """
        Returns a styled curve (and optional label) plotted on given axes.
        Label anchors to the curve's own endpoint (x_range[-1] by default)
        instead of manim's default search, so it lines up with wherever
        the curve is cut off rather than drifting toward the full axes range.
        """
        curve = axes.plot(func, x_range=x_range, color=color)
        if label:
            if label_x_val is None:
                label_x_val = x_range[-1]
            curve_label = axes.get_graph_label(
                curve, label=label, direction=label_direction, color=color,
                x_val=label_x_val
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

    def drop_to_axis(self, axes, x_val, y_val, axis="x", label=None, color=None,
                      label_direction=None, buff=0.15, use_tex=False):
        """
        Dashed line from a point (x_val, y_val) straight down to the quantity
        axis (axis="x") or across to the price axis (axis="y") — used to mark
        where a price line meets a curve, e.g. Qd/Qs at a given price.

        Pass use_tex=True to render label with MathTex (e.g. r"Q_d = 20" for
        a proper subscript) instead of plain Text.
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
            if use_tex:
                text = MathTex(label, font_size=32, color=color).next_to(end, label_direction, buff=buff)
            else:
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

    def make_definition_box(self, title, condition, description, color=None,
                             width=4.6, height=2.3):
        """
        Rounded box summarizing a concept: bold title, a MathTex condition
        line (e.g. r"Q_s > Q_d"), and a plain-English description underneath.
        Used for definition-recap beats.
        """
        color = color or self.AXIS_COLOR
        box = RoundedRectangle(width=width, height=height, color=color, corner_radius=0.2)

        title_text = Text(title, font_size=28, color=color, weight=BOLD, font="Helvetica")
        condition_text = MathTex(condition, font_size=32, color=color)
        description_text = Text(description, font_size=18, color=WHITE, font="Helvetica")
        if description_text.width > width - 0.5:
            description_text.scale_to_fit_width(width - 0.5)

        content = VGroup(title_text, condition_text, description_text).arrange(DOWN, buff=0.2)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_concept_card(self, title, description, color=None, width=6.0, height=1.9):
        """
        Rounded box with a bold colored title and a plain-English description
        underneath — like make_definition_box() but without a math condition
        line, for conceptual terms (e.g. Scarcity, Opportunity Cost) that
        aren't naturally an equation.
        """
        color = color or self.AXIS_COLOR
        box = RoundedRectangle(width=width, height=height, color=color, corner_radius=0.2)

        title_text = Text(title, font_size=34, color=color, weight=BOLD, font="Helvetica")
        description_text = Text(description, font_size=24, color=WHITE, font="Helvetica")
        if description_text.width > width - 0.6:
            description_text.scale_to_fit_width(width - 0.6)

        content = VGroup(title_text, description_text).arrange(DOWN, buff=0.3)
        content.move_to(box.get_center())
        return VGroup(box, content)

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