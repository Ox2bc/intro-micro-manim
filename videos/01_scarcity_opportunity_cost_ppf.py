from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.micro_scene import MicroScene


class ScarcityOpportunityCostPPF(MicroScene):
    """
    Video 01 — Scarcity, Opportunity Cost & the PPF
    Island economy: Coconuts (C) vs. Fish (F)
    Simple PPF: F = 100 - 2C
    Realistic (bowed-out) PPF: F = 100 * sqrt(1 - (C/50)^2)
    """

    PPF_COLOR = GOLD

    # Simple, constant-opportunity-cost PPF (straight line)
    @staticmethod
    def simple_ppf(c):
        return 100 - 2 * c

    def construct(self):
        # ---- Beat 1: Hook ----
        title = Text("Scarcity, Opportunity Cost & the PPF", font_size=40)

        credit = VGroup(
            Text("Episode 01", font_size=20),
            Text("Michael Frid", font_size=20),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        credit.to_corner(DR, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(credit))
        self.wait(30)
        self.play(FadeOut(title), FadeOut(credit))

        # ---- Beat 2: Scarcity ----
        time_word = Text("Time", font_size=34, weight=BOLD, color=PURPLE_B, font="Helvetica")
        money_word = Text("Money", font_size=34, weight=BOLD, color=PURPLE_B, font="Helvetica")
        resources_word = Text("Resources", font_size=34, weight=BOLD, color=PURPLE_B, font="Helvetica")
        concept_words = VGroup(time_word, money_word, resources_word).arrange(
            RIGHT, buff=1.2, aligned_edge=UP
        )
        concept_words.shift(UP * 1.8)

        self.play(FadeIn(time_word))
        self.wait(1)
        self.play(FadeIn(money_word))
        self.wait(1)
        self.play(FadeIn(resources_word))
        self.wait(2)

        scarcity_card = self.make_concept_card(
            title="Scarcity",
            description="Unlimited wants, limited resources.",
            color=PURPLE_B
        )
        scarcity_card.shift(DOWN * 0.5)
        self.play(FadeIn(scarcity_card))
        self.wait(24)

        self.play(FadeOut(concept_words), FadeOut(scarcity_card))

        # ---- Beat 3: Opportunity Cost ----
        oc_card = self.make_concept_card(
            title="Opportunity Cost",
            description="The value of the next best alternative given up.",
            color=TEAL, width=7.5
        )
        oc_card.move_to(UP * 0.8)
        self.play(FadeIn(oc_card))
        self.wait(14)

        study_word = Text("Study", font_size=30, weight=BOLD, color=TEAL, font="Helvetica")
        vs_word = Text("vs.", font_size=30, font="Helvetica", color=GRAY)
        beach_word = Text("Beach", font_size=30, weight=BOLD, color=TEAL, font="Helvetica")
        example = VGroup(study_word, vs_word, beach_word).arrange(
            RIGHT, buff=0.5, aligned_edge=UP
        )
        example.move_to(DOWN * 1.6)

        self.play(FadeIn(example))
        self.wait(10)
        self.play(FadeOut(example))
        self.wait(6)

        self.play(FadeOut(oc_card))

        # ---- Beat 4: Build the PPF (simple line) ----
        axes, x_label, y_label = self.make_axes(
            x_range=(0, 70, 10), y_range=(0, 140, 20),
            x_label="Coconuts", y_label="Fish"
        )
        axes.add_coordinates()
        x_label.shift(DOWN * 0.35)
        self.play(Create(axes), Write(x_label), Write(y_label))

        ppf_line, ppf_label = self.make_curve(
            axes, self.simple_ppf, x_range=[0, 50],
            color=self.PPF_COLOR, label="PPF", label_direction=UR, label_x_val=40
        )
        self.play(Create(ppf_line, run_time=3), Write(ppf_label))
        self.wait(40)

        # ---- Beat 5: Constant opportunity cost ----
        point1 = (10, 80)
        point2 = (30, 40)

        dot1 = Dot(axes.coords_to_point(*point1), color=self.PPF_COLOR)
        dot2 = Dot(axes.coords_to_point(*point2), color=self.PPF_COLOR)
        guide1 = self.drop_to_axis(axes, x_val=point1[0], y_val=point1[1], axis="x", color=GRAY)
        guide2 = self.drop_to_axis(axes, x_val=point2[0], y_val=point2[1], axis="x", color=GRAY)

        self.play(Create(dot1), Create(guide1))
        self.wait(2)
        self.play(Create(dot2), Create(guide2))
        self.wait(2)

        slope_label = Text("-2 fish per coconut", font_size=26, color=self.PPF_COLOR, font="Helvetica")
        slope_label.move_to(axes.coords_to_point(20, 15))
        self.play(Write(slope_label))
        self.wait(25)

        self.play(
            FadeOut(dot1), FadeOut(dot2), FadeOut(guide1), FadeOut(guide2), FadeOut(slope_label)
        )
