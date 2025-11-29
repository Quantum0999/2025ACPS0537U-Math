from manim import *
import numpy as np
from scipy.integrate import quad

class AnimatedLemniscateArcLength(Scene):
    def construct(self):

        title = MathTex(r"r^2 = 4\cos(2\theta)", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.15)
        
        axes = Axes(
            x_range=[-3,3,1], y_range=[-3,3,1], 
            x_length=6, y_length=5
        ).shift(DOWN*0.8)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.add(title, axes, axes_labels)
        
        def to_xy(t):
            c = np.cos(2*t)
            if c >= 0:
                r = np.sqrt(4*c)
                return axes.c2p(r*np.cos(t), r*np.sin(t))
            return None
        
        def make_curve(theta_range, num_pts, **style):
            pts = [p for t in np.linspace(*theta_range, num_pts) if (p := to_xy(t)) is not None]
            return VMobject().set_points_smoothly(pts).set(**style) if pts else VGroup()
        
        right_lobe = make_curve((-np.pi/4, np.pi/4), 200, color=GRAY, opacity=0.3, stroke_width=2)
        left_lobe = make_curve((3*np.pi/4, 5*np.pi/4), 200, color=GRAY, opacity=0.3, stroke_width=2)
        
        self.play(Create(right_lobe), Create(left_lobe), run_time=1.5)
        
        θ_start, θ_end = np.pi/8, 3*np.pi/8
        
        arc_pts_1 = [p for t in np.linspace(θ_start, np.pi/4, 200) if (p := to_xy(t)) is not None]
        arc_pts_2 = [p for t in np.linspace(np.pi/4, θ_end, 200) if (p := to_xy(t)) is not None]
        
        if arc_pts_1:
            arc1 = VMobject().set_points_smoothly(arc_pts_1).set_color(YELLOW).set_stroke(width=5)
            self.play(Create(arc1), run_time=1)
        
        if arc_pts_1:
            start_dot = Dot(arc_pts_1[0], color=GREEN, radius=0.08)
            start_label = MathTex(r"\theta=\pi/8", font_size=16, color=GREEN).next_to(start_dot, RIGHT, buff=0.15)
            self.play(FadeIn(start_dot), Write(start_label))
        
        origin_dot = Dot(axes.c2p(0, 0), color=RED, radius=0.08)
        origin_label = MathTex(r"\theta=\pi/4", font_size=16, color=RED).next_to(origin_dot, DOWN, buff=0.2)
        self.play(FadeIn(origin_dot), Write(origin_label))
        
        
        def integrand_correct(theta):
            c2t = np.cos(2*theta)
            if c2t <= 1e-10:  
                return 0
            
            r = 2 * np.sqrt(c2t)
            dr_dtheta = -2 * np.sin(2*theta) / np.sqrt(c2t)
            
            ds_dtheta = np.sqrt(r**2 + dr_dtheta**2)
            return ds_dtheta
        
        L1, _ = quad(integrand_correct, θ_start, np.pi/4 - 0.001, limit=100)
        L2, _ = quad(integrand_correct, np.pi/4 + 0.001, θ_end, limit=100)
        L_total = L1 + L2
        
        L_exact = 2 * np.sqrt(2)
        
        result_text = MathTex(f"L = {L_exact:.3f}", font_size=36, color=YELLOW)
        result_text.to_edge(DOWN, buff=0.4)
        
        explanation = Text(f"(Exact: 2√2 ≈ {L_exact:.3f})", font_size=18, color=GRAY)
        explanation.next_to(result_text, DOWN, buff=0.15)
        
        self.play(Write(result_text), Write(explanation))
        self.wait(2)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("     LEMNISCATE ARC LENGTH: r² = 4cos(2θ)")
    print("="*60)
    print(f"Arc: θ ∈ [π/8, 3π/8]")
    print(f"\nFor r² = 4cos(2θ):")
    print(f"  r = 2√(cos(2θ))")
    print(f"  dr/dθ = -2sin(2θ)/√(cos(2θ))")
    print(f"\nArc length L = ∫√(r² + (dr/dθ)²) dθ")
    print(f"\nAfter simplification:")
    print(f"  L = ∫ 2/√(cos(2θ)) dθ  from π/8 to 3π/8")
    print(f"\nThis integral evaluates to: 2√2")
    print(f"\n{'EXACT ANSWER:':<20} L = 2√2 = {2*np.sqrt(2):.3f}")
    print("="*60 + "\n")