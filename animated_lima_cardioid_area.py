from manim import *
import numpy as np

class CardioidLimaconIntersection(Scene):
    def construct(self):
        axes = Axes(x_range=[-8, 8, 1], y_range=[-6, 6, 1],
                    x_length=9, y_length=6).shift(DOWN)
        self.add(axes)

        r_card = lambda t: 3 * (1 + np.cos(t))
        r_lima = lambda t: 2 + 4 * np.cos(t)
        to_xy = lambda r, t: axes.c2p(r*np.cos(t), r*np.sin(t))

        t_vals = np.linspace(0, 2*np.pi, 500)
        card_curve = VMobject().set_points_smoothly([to_xy(r_card(t), t) for t in t_vals]).set_color(BLUE).set_stroke(width=3)
        lima_curve = VMobject().set_points_smoothly([to_xy(r_lima(t), t) for t in t_vals]).set_color(RED).set_stroke(width=3)

        title = Text("Cardioid & Limacon Intersections", font_size=30, color=YELLOW).to_edge(UP, buff=0.3)
        labels = VGroup(
            MathTex("r = 3(1 + \\cos\\theta)", color=BLUE, font_size=24),
            MathTex("r = 2 + 4\\cos\\theta", color=RED, font_size=24)
        ).arrange(RIGHT, buff=0.5).next_to(title, DOWN, buff=0.2)

        self.play(Write(title), Write(labels))
        self.play(Create(card_curve), Create(lima_curve), run_time=2)

        intersections = [
            (0, GREEN, "0", RIGHT),
            (2*np.pi/3, YELLOW, "2\\pi/3", UL),
            (np.pi, ORANGE, "\\pi", LEFT),
            (4*np.pi/3, PINK, "4\\pi/3", DL)
        ]

        dots = VGroup()
        texts = VGroup()

        for θ, col, lbl, direction in intersections:
            r = r_card(θ) if θ != np.pi else 0
            pt = to_xy(r, θ)
            dot = Dot(pt, color=col, radius=0.12)
            label = MathTex(f"\\theta = {lbl}", color=col, font_size=22).next_to(pt, direction, buff=0.2)

            if lbl == "0":     label.shift(UP*0.35 + RIGHT*0.35)
            if lbl == "\\pi":  label.shift(DOWN*0.35 + LEFT*0.35)

            dots.add(dot)
            texts.add(label)

        self.play(FadeIn(dots), Write(texts), run_time=2)
        self.wait(2)
