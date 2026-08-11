from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.micro_scene import MicroScene


class EquilibriumSurplusShortage(MicroScene):
    """
    Video 07 — Surplus, Shortage & Equilibrium
    Market: Cheese (pounds per week)
    Qd = 100 - 2P  ->  inverse: P = 50 - 0.5Q
    Qs = 3P - 50   ->  inverse: P = (Q + 50) / 3
    Equilibrium: P* = 30, Q* = 40
    """

    # Creates Demand Curve
    @staticmethod
    def demand(q):
        return 50 - 0.5 * q

    # Creates Supply Curve
    @staticmethod
    def supply(q):
        return (q + 50) / 3

    def construct(self):
        # ---- Beat 1: Hook ----
        title = Text("Surplus, Shortage & Equilibrium", font_size=40)

        credit = VGroup(
            Text("Episode 07", font_size=20),
            Text("Michael Frid", font_size=20),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        credit.to_corner(DR, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(credit))
        self.wait(30)
        self.play(FadeOut(title), FadeOut(credit))

        # ---- Beat 2: Build axes and curves ----
        axes, x_label, y_label = self.make_axes(
            x_range=(0, 100, 20), y_range=(0, 50, 10)
        )
        self.play(Create(axes), Write(x_label), Write(y_label))

        demand, d_label = self.make_curve(
            axes, self.demand, x_range=[5, 95],
            color=self.DEMAND_COLOR, label="D", label_direction=UP
        )
        self.play(Create(demand, run_time=3), Write(d_label))

        supply, s_label = self.make_curve(
            axes, self.supply, x_range=[5, 95],
            color=self.SUPPLY_COLOR, label="S", label_direction=DOWN
        )
        self.play(Create(supply, run_time=3), Write(s_label))

        self.wait(40)

        # ---- Beat 3: Equilibrium ----
        equilibrium = self.mark_equilibrium(axes, x_val=40, y_val=30, label="E")
        p_star = self.label_axis_value(axes, axis="y", value=30, text="P* = 30")
        q_star = self.label_axis_value(axes, axis="x", value=40, text="Q* = 40")
        self.play(Create(equilibrium))
        self.play(Write(p_star), Write(q_star))
        self.wait(35)

        # ---- Beat 4: Surplus (P = 40) ----
        price_40 = self.price_line(axes, price=40, label="P = 40")
        self.play(Create(price_40))

        qd_40 = self.drop_to_axis(
            axes, x_val=20, y_val=40, axis="x",
            label=r"Q_d = 20", color=self.DEMAND_COLOR, use_tex=True
        )
        qs_40 = self.drop_to_axis(
            axes, x_val=70, y_val=40, axis="x",
            label=r"Q_s = 70", color=self.SUPPLY_COLOR, use_tex=True
        )
        self.play(Create(qd_40), Create(qs_40))

        surplus_gap = self.mark_gap(
            axes, x1=20, x2=70, y=40, label="Surplus = 50", color=self.SURPLUS_COLOR,
            label_direction=UP, buff=0.1
        )
        self.play(Create(surplus_gap))
        self.wait(40)

        self.play(
            FadeOut(price_40), FadeOut(qd_40), FadeOut(qs_40),
            FadeOut(surplus_gap)
        )

        # ---- Beat 5: Shortage (P = 25) ----
        price_25 = self.price_line(axes, price=25, label="P = 25")
        self.play(Create(price_25))

        qd_25 = self.drop_to_axis(
            axes, x_val=50, y_val=25, axis="x",
            label=r"Q_d = 50", color=self.DEMAND_COLOR, use_tex=True
        )
        qs_25 = self.drop_to_axis(
            axes, x_val=25, y_val=25, axis="x",
            label=r"Q_s = 25", color=self.SUPPLY_COLOR, use_tex=True
        )
        self.play(Create(qd_25), Create(qs_25))

        shortage_gap = self.mark_gap(
            axes, x1=25, x2=50, y=25, label="Shortage = 25", color=self.SHORTAGE_COLOR,
            label_direction=DOWN, buff=0.1
        )
        self.play(Create(shortage_gap))
        self.wait(35)

        # ---- Beat 6: Definitions ----
        self.play(
            FadeOut(price_25), FadeOut(qd_25), FadeOut(qs_25),
            FadeOut(shortage_gap)
        )

        graph_group = VGroup(
            axes, x_label, y_label, demand, d_label, supply, s_label,
            equilibrium, p_star, q_star
        )
        graph_original_center = graph_group.get_center()
        self.play(graph_group.animate.scale(0.4).to_corner(DL, buff=0.3))

        surplus_box = self.make_definition_box(
            title="Surplus", condition=r"Q_s > Q_d",
            description="Price too high — too much is being produced",
            color=self.SURPLUS_COLOR
        )
        shortage_box = self.make_definition_box(
            title="Shortage", condition=r"Q_d > Q_s",
            description="Price too low — not enough is being produced",
            color=self.SHORTAGE_COLOR
        )
        definition_boxes = VGroup(surplus_box, shortage_box).arrange(DOWN, buff=0.6)
        definition_boxes.move_to(ORIGIN).shift(RIGHT * 1.5)

        self.play(FadeIn(surplus_box))
        self.play(FadeIn(shortage_box))
        self.wait(40)

        # ---- Beat 7: Example setup ----
        self.play(FadeOut(surplus_box), FadeOut(shortage_box))

        market_line = Text("Market: Cheese (pounds per week)", font_size=28)
        qd_eq = MathTex(r"Q_d = 100 - 2P", font_size=32, color=self.DEMAND_COLOR)
        qs_eq = MathTex(r"Q_s = 3P - 50", font_size=32, color=self.SUPPLY_COLOR)
        given = MathTex(r"P^* = 30, \quad Q^* = 40", font_size=32, color=self.EQUILIBRIUM_COLOR)

        word_problem = VGroup(market_line, qd_eq, qs_eq, given).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        )
        word_problem.move_to(ORIGIN).shift(RIGHT * 1.5)

        self.play(Write(market_line))
        self.play(Write(qd_eq))
        self.play(Write(qs_eq))
        self.play(Write(given))
        self.wait(35)

        # ---- Beat 8: Work the example ----
        self.play(word_problem.animate.scale(0.6).to_corner(UL, buff=0.4))

        p40_heading = Text("At P = $40 (above equilibrium):", font_size=26, font="Helvetica")
        p40_qd = MathTex(r"Q_d = 100 - 2(40) = 20", font_size=30, color=self.DEMAND_COLOR)
        p40_qs = MathTex(r"Q_s = 3(40) - 50 = 70", font_size=30, color=self.SUPPLY_COLOR)
        p40_row = VGroup(p40_qd, p40_qs).arrange(RIGHT, buff=0.8)
        p40_result = MathTex(r"Q_s - Q_d = 70 - 20 = 50", font_size=32, color=self.SURPLUS_COLOR)
        p40_calc = VGroup(p40_heading, p40_row, p40_result).arrange(DOWN, buff=0.35)

        p25_heading = Text("At P = $25 (below equilibrium):", font_size=26, font="Helvetica")
        p25_qd = MathTex(r"Q_d = 100 - 2(25) = 50", font_size=30, color=self.DEMAND_COLOR)
        p25_qs = MathTex(r"Q_s = 3(25) - 50 = 25", font_size=30, color=self.SUPPLY_COLOR)
        p25_row = VGroup(p25_qd, p25_qs).arrange(RIGHT, buff=0.8)
        p25_result = MathTex(r"Q_d - Q_s = 50 - 25 = 25", font_size=32, color=self.SHORTAGE_COLOR)
        p25_calc = VGroup(p25_heading, p25_row, p25_result).arrange(DOWN, buff=0.35)

        calc_stack = VGroup(p40_calc, p25_calc).arrange(DOWN, buff=1.0)
        calc_stack.move_to(RIGHT * 2.9)

        self.play(Write(p40_heading))
        self.play(Write(p40_qd), Write(p40_qs))
        self.wait(5)
        self.play(Write(p40_result))
        self.wait(6)

        self.play(Write(p25_heading))
        self.play(Write(p25_qd), Write(p25_qs))
        self.wait(5)
        self.play(Write(p25_result))
        self.wait(7)

        # ---- Beat 9: Bring axes back, surplus on graph ----
        self.play(
            FadeOut(word_problem),
            FadeOut(p40_calc),
            FadeOut(p25_calc),
        )
        self.play(graph_group.animate.scale(2.5).move_to(graph_original_center))

        price_40 = self.price_line(axes, price=40, label="P = 40")
        self.play(Create(price_40))

        qd_40 = self.drop_to_axis(
            axes, x_val=20, y_val=40, axis="x",
            label=r"Q_d = 20", color=self.DEMAND_COLOR, use_tex=True
        )
        qs_40 = self.drop_to_axis(
            axes, x_val=70, y_val=40, axis="x",
            label=r"Q_s = 70", color=self.SUPPLY_COLOR, use_tex=True
        )
        self.play(Create(qd_40), Create(qs_40))

        surplus_gap = self.mark_gap(
            axes, x1=20, x2=70, y=40, label="Surplus = 50", color=self.SURPLUS_COLOR,
            label_direction=UP, buff=0.1
        )
        self.play(Create(surplus_gap))
        self.wait(45)

        # ---- Beat 10: Shortage on graph ----
        self.play(
            FadeOut(price_40), FadeOut(qd_40), FadeOut(qs_40),
            FadeOut(surplus_gap)
        )

        price_25 = self.price_line(axes, price=25, label="P = 25")
        self.play(Create(price_25))

        qd_25 = self.drop_to_axis(
            axes, x_val=50, y_val=25, axis="x",
            label=r"Q_d = 50", color=self.DEMAND_COLOR, use_tex=True
        )
        qs_25 = self.drop_to_axis(
            axes, x_val=25, y_val=25, axis="x",
            label=r"Q_s = 25", color=self.SUPPLY_COLOR, use_tex=True
        )
        self.play(Create(qd_25), Create(qs_25))

        shortage_gap = self.mark_gap(
            axes, x1=25, x2=50, y=25, label="Shortage = 25", color=self.SHORTAGE_COLOR,
            label_direction=DOWN, buff=0.1
        )
        self.play(Create(shortage_gap))
        self.wait(40)

        # ---- Beat 11: Why prices move toward equilibrium ----
        self.play(
            FadeOut(price_25), FadeOut(qd_25), FadeOut(qs_25), FadeOut(shortage_gap)
        )

        down_arrow = Arrow(
            axes.coords_to_point(0, 40), axes.coords_to_point(0, 30),
            color=self.SURPLUS_COLOR, buff=0.1, stroke_width=6
        )
        up_arrow = Arrow(
            axes.coords_to_point(0, 25), axes.coords_to_point(0, 30),
            color=self.SHORTAGE_COLOR, buff=0.1, stroke_width=6
        )

        self.play(GrowArrow(down_arrow))
        self.play(Indicate(equilibrium[0], color=self.EQUILIBRIUM_COLOR))
        self.wait(3)

        self.play(GrowArrow(up_arrow))
        self.play(Indicate(equilibrium[0], color=self.EQUILIBRIUM_COLOR))
        self.wait(3)

        self.play(FadeOut(down_arrow), FadeOut(up_arrow))
        self.wait(28)

        # ---- Beat 12: Closing beat ----
        self.play(graph_group.animate.set_opacity(0.3))

        summary_surplus = self.make_definition_box(
            title="Surplus", condition=r"Q_s > Q_d",
            description="Price too high — pushes price down",
            color=self.SURPLUS_COLOR
        )
        summary_shortage = self.make_definition_box(
            title="Shortage", condition=r"Q_d > Q_s",
            description="Price too low — pushes price up",
            color=self.SHORTAGE_COLOR
        )
        summary_boxes = VGroup(summary_surplus, summary_shortage).arrange(DOWN, buff=0.6)
        summary_boxes.move_to(ORIGIN)

        self.play(FadeIn(summary_surplus))
        self.wait(8)
        self.play(FadeIn(summary_shortage))
        self.wait(10)

        self.wait(4)
        self.play(FadeOut(*self.mobjects))
        self.wait(1)
