from manim import *
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from shared.micro_scene import MicroScene

class TestScene(MicroScene):
    def construct(self):
        axes, x_label, y_label = self.make_axes()
        self.play(Create(axes), Write(x_label), Write(y_label))

        demand, d_label = self.make_curve(
            axes, lambda x: 10 - x, x_range=[0, 10],
            color=self.DEMAND_COLOR, label="D"
        )
        supply, s_label = self.make_curve(
            axes, lambda x: x, x_range=[0, 10],
            color=self.SUPPLY_COLOR, label="S"
        )
        self.play(Create(demand), Write(d_label), Create(supply), Write(s_label))

        eq = self.mark_equilibrium(axes, 5, 5, label_direction=UP)
        self.play(Create(eq))
        self.wait(1)