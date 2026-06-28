"""
Moment of Inertia — Complete Visual Treatment
3Blue1Brown-Quality Manim Educational Video

Render individual scenes:
    .venv/bin/manim -pqh main.py SpinnerIntuition
    .venv/bin/manim -pqh main.py RotationalNewton
    .venv/bin/manim -pqh main.py MomentDefinition
    .venv/bin/manim -pqh main.py ParallelAxisTheorem
    .venv/bin/manim -pqh main.py PerpendicularAxisTheorem
    .venv/bin/manim -pqh main.py RingCentralAxis
    .venv/bin/manim -pqh main.py RingAllAxes
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────────────────────
config.background_color = "#0F0F1A"
config.pixel_height = 1080
config.pixel_width  = 1920
config.frame_rate   = 60

# ─────────────────────────────────────────────────────────────
#  COLOR PALETTE
# ─────────────────────────────────────────────────────────────
BACKGROUND_COLOR   = "#0F0F1A"
PRIMARY_BLUE       = "#58C4DD"
GOLD               = "#F4D03F"
GREEN              = "#83C167"
RED_ORANGE         = "#FC6255"
PURPLE             = "#9B59B6"
LIGHT_GRAY         = "#BBBBCC"
DIM_GRAY           = "#555577"
RING_COLOR         = "#4A90D9"
MASS_ELEMENT_COLOR = "#F4D03F"
AXIS_COLOR         = "#FC6255"
VECTOR_COLOR       = "#83C167"


# ─────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def theorem_box(title: str, equation: str, title_color=PRIMARY_BLUE) -> VGroup:
    """Returns a rounded-rectangle theorem box containing a title and equation."""
    title_mob = Tex(title, font_size=28, color=title_color)
    eq_mob    = MathTex(equation, font_size=36)
    group     = VGroup(title_mob, eq_mob).arrange(DOWN, buff=0.3)
    box       = SurroundingRectangle(
        group, color=title_color, buff=0.3, corner_radius=0.1
    )
    return VGroup(box, group)


def chapter_card(scene, title: str, subtitle: str = ""):
    """Animated chapter transition card."""
    t = Tex(title, font_size=52, color=GOLD)
    s = Tex(subtitle, font_size=28, color=LIGHT_GRAY) if subtitle else None
    grp = VGroup(t, s).arrange(DOWN, buff=0.4).center() if s else t.center()
    scene.play(FadeIn(grp, shift=UP * 0.3), run_time=0.9)
    scene.wait(1.5)
    scene.play(FadeOut(grp, shift=UP * 0.3), run_time=0.6)



FORCE_COLOR   = GREEN_C
 
class SpinnerIntuition(MovingCameraScene):
    """Hook → Mass Distribution → Moment of Inertia definition."""
 
    def construct(self):
        # ════════════════════════════════════════════════════
        # PART 1 — Experimental Setup
        # ════════════════════════════════════════════════════
        exp_title = Tex("Experiment", font_size=64, color=GOLD).center()
        exp_sub   = VGroup(
            Tex("Two wheels.",       font_size=30, color=LIGHT_GRAY),
            Tex("Same mass.",        font_size=30, color=LIGHT_GRAY),
            Tex("Different radius.", font_size=30, color=LIGHT_GRAY),
        ).arrange(DOWN, buff=0.15).next_to(exp_title, DOWN, buff=0.45)
 
        self.play(Write(exp_title), run_time=1.0)
        self.play(LaggedStart(
            *[FadeIn(ln, shift=UP * 0.15) for ln in exp_sub],
            lag_ratio=0.35, run_time=1.2
        ))
        self.wait(1.2)
        self.play(FadeOut(VGroup(exp_title, exp_sub)), run_time=0.6)
 
        small_r = 0.85
        large_r = 1.70
 
        small_disc = Circle(radius=small_r, color=PRIMARY_BLUE)
        small_disc.set_fill(PRIMARY_BLUE, opacity=0.28)
        small_disc.set_stroke(PRIMARY_BLUE, width=4)
        small_disc.move_to(LEFT * 3.5)
 
        large_disc = Circle(radius=large_r, color=RING_COLOR)
        large_disc.set_fill(RING_COLOR, opacity=0.20)
        large_disc.set_stroke(RING_COLOR, width=4)
        large_disc.move_to(RIGHT * 3.5)
 
        small_dot = Dot(small_disc.get_center(), color=WHITE, radius=0.07)
        large_dot = Dot(large_disc.get_center(), color=WHITE, radius=0.07)
 
        small_r_lbl = MathTex(r"\text{Radius} = 1.0\text{ m}", font_size=26, color=PRIMARY_BLUE).next_to(small_disc, UP, buff=0.3)
        large_r_lbl = MathTex(r"\text{Radius} = 2.0\text{ m}", font_size=26, color=RING_COLOR  ).next_to(large_disc, UP, buff=0.3)
        small_meq   = MathTex(r"\text{Mass} = 2.0\text{ kg}",  font_size=24, color=LIGHT_GRAY  ).next_to(small_disc, DOWN, buff=0.55)
        large_meq   = MathTex(r"\text{Mass} = 2.0\text{ kg}",  font_size=24, color=LIGHT_GRAY  ).next_to(large_disc, DOWN, buff=0.55)
        lbl_A       = Tex("Wheel A", font_size=22, color=DIM_GRAY).next_to(small_meq, DOWN, buff=0.2)
        lbl_B       = Tex("Wheel B", font_size=22, color=DIM_GRAY).next_to(large_meq, DOWN, buff=0.2)
 
        wheel_a_group = VGroup(small_disc, small_dot, small_r_lbl, small_meq, lbl_A)
        wheel_b_group = VGroup(large_disc, large_dot, large_r_lbl, large_meq, lbl_B)
 
        self.play(FadeIn(wheel_a_group), FadeIn(wheel_b_group), run_time=1.5, rate_func=smooth)
        self.wait(0.8)
 
        # ════════════════════════════════════════════════════
        # PART 2 — Applied Tangential Force
        # ════════════════════════════════════════════════════
        def tangential_force(disc, color=FORCE_COLOR):
            ctr    = disc.get_center()
            r      = disc.radius
            rim_pt = ctr + np.array([r, 0, 0])
            tip_pt = rim_pt + np.array([0, 1.6, 0])
            arrow  = Arrow(rim_pt, tip_pt, buff=0, color=color,
                           stroke_width=8, max_tip_length_to_length_ratio=0.2)
            lbl    = MathTex(r"10.0\text{ N}", font_size=36, color=color).next_to(tip_pt, RIGHT, buff=0.15)
            return VGroup(arrow, lbl)
 
        force_small    = tangential_force(small_disc)
        force_large    = tangential_force(large_disc)
        same_force_lbl = Tex("Same tangential force", font_size=26, color=FORCE_COLOR).to_edge(DOWN, buff=1.6)
 
        self.play(
            GrowArrow(force_small[0]), FadeIn(force_small[1]),
            GrowArrow(force_large[0]), FadeIn(force_large[1]),
            run_time=1.2
        )
        self.play(FadeIn(same_force_lbl, shift=UP * 0.1), run_time=0.7)
        self.wait(0.9)
 
        # Torque seed — r lines from center to rim
        r_line_small = DashedLine(small_disc.get_center(), force_small[0].get_start(),
                                  color=VECTOR_COLOR, dash_length=0.1)
        r_lbl_small  = MathTex("r", font_size=28, color=VECTOR_COLOR).next_to(r_line_small, UP, buff=0.1)
        r_line_large = DashedLine(large_disc.get_center(), force_large[0].get_start(),
                                  color=VECTOR_COLOR, dash_length=0.1)
        r_lbl_large  = MathTex("r", font_size=28, color=VECTOR_COLOR).next_to(r_line_large, UP, buff=0.1)
        r_seed_group = VGroup(r_line_small, r_lbl_small, r_line_large, r_lbl_large)
 
        self.play(Create(r_line_small), Write(r_lbl_small),
                  Create(r_line_large), Write(r_lbl_large), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(r_seed_group), run_time=0.5)
 
        # ════════════════════════════════════════════════════
        # PART 3 — Spin Experiment
        # ════════════════════════════════════════════════════
        self.play(
            force_small[0].animate.scale(1.15).set_color(WHITE),
            force_large[0].animate.scale(1.15).set_color(WHITE),
            run_time=0.25, rate_func=there_and_back
        )
        self.play(FadeOut(force_small), FadeOut(force_large), FadeOut(same_force_lbl), run_time=0.4)
 
        self.play(
            Rotate(small_disc, angle=4 * TAU, about_point=small_disc.get_center(),
                   rate_func=linear, run_time=5),
            Rotate(large_disc, angle=2 * TAU, about_point=large_disc.get_center(),
                   rate_func=linear, run_time=5),
            run_time=5
        )
        self.wait(0.5)
 
        # ════════════════════════════════════════════════════
        # PART 4 — Results Table
        # ════════════════════════════════════════════════════
        self.play(
            wheel_a_group.animate.scale(0.5).move_to(LEFT  * 3.5 + UP * 1.8),
            wheel_b_group.animate.scale(0.5).move_to(RIGHT * 3.5 + UP * 1.8),
            run_time=1.2, rate_func=smooth
        )
 
        table_y_start = 0.6
        x_col0, x_col1, x_col2 = -3.5, 0.0, 3.5
 
        h0  = Tex(r"Property",          color=DIM_GRAY,      font_size=26).move_to([x_col0, table_y_start, 0])
        h1  = Tex(r"\textbf{Wheel A}",  color=PRIMARY_BLUE,  font_size=28).move_to([x_col1, table_y_start, 0])
        h2  = Tex(r"\textbf{Wheel B}",  color=RING_COLOR,    font_size=28).move_to([x_col2, table_y_start, 0])
        h0.align_to(LEFT * 4.0, LEFT)
        header = VGroup(h0, h1, h2)
        sep    = Line(LEFT * 4.5, RIGHT * 4.5, color=DIM_GRAY, stroke_width=1.5).next_to(header, DOWN, buff=0.15)
 
        row_data = [
            ("Mass",          r"2.0\text{ kg}",    r"2.0\text{ kg}",    PRIMARY_BLUE, RING_COLOR),
            ("Radius",        r"1.0\text{ m}",     r"2.0\text{ m}",     PRIMARY_BLUE, RING_COLOR),
            ("Applied Force", r"10.0\text{ N}",    r"10.0\text{ N}",    FORCE_COLOR,  FORCE_COLOR),
            ("Final Velocity",r"5.0\text{ rad/s}", r"2.5\text{ rad/s}", GOLD,         RED_ORANGE),
        ]
 
        row_groups = []
        y_cursor   = sep.get_y() - 0.4
        for lbl, va, vb, ca, cb in row_data:
            c0 = Tex(lbl, font_size=26, color=LIGHT_GRAY).move_to([x_col0, y_cursor, 0])
            c0.align_to(h0, LEFT)
            c1 = MathTex(va, font_size=32, color=ca).move_to([x_col1, y_cursor, 0])
            c2 = MathTex(vb, font_size=32, color=cb).move_to([x_col2, y_cursor, 0])
            row_groups.append(VGroup(c0, c1, c2))
            y_cursor -= 0.60
 
        self.play(FadeIn(header, shift=UP * 0.1), Create(sep), run_time=0.6)
        self.wait(0.2)
 
        for ridx, row in enumerate(row_groups):
            if ridx < 3:
                self.play(FadeIn(row, shift=UP * 0.08), run_time=0.4)
            else:
                self.wait(0.3)
                self.play(FadeIn(row, shift=UP * 0.12, rate_func=rush_from), run_time=0.8)
                self.play(
                    Indicate(row[1], color=GOLD,       scale_factor=1.3, run_time=0.7),
                    Indicate(row[2], color=RED_ORANGE, scale_factor=1.3, run_time=0.7),
                )
                row[2].set_color(RED_ORANGE)
 
        self.wait(3.0)
 
        # ════════════════════════════════════════════════════
        # PART 5 — Narrative Bridge & Rim Zoom
        # ════════════════════════════════════════════════════
        bridge_text = VGroup(
            Tex("Same force. More radius. Less spin.", font_size=28, color=GOLD),
            Tex("Why does the larger wheel resist spinning more?", font_size=32, color=LIGHT_GRAY),
            Tex("Something in the wheel's geometry is resisting rotation.", font_size=26, color=DIM_GRAY),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
 
        self.play(FadeIn(bridge_text[0], shift=UP * 0.1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(bridge_text[1], shift=UP * 0.1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(bridge_text[2], shift=UP * 0.1), run_time=0.8)
        self.wait(1.5)
 
        target_pt = wheel_b_group[0].get_right()
        rim_label = Tex(r"Mass at large $r$", font_size=24, color=RING_COLOR).next_to(target_pt, RIGHT, buff=0.2)
 
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(target_pt + LEFT * 0.5),
            FadeIn(rim_label, shift=LEFT * 0.1),
            run_time=2.0, rate_func=smooth
        )
        self.wait(1.5)
 
        fade_group = VGroup(
            wheel_a_group, wheel_b_group, header, sep, *row_groups,
            bridge_text, rim_label
        )
        self.play(FadeOut(fade_group), run_time=1.0)
 
        # ════════════════════════════════════════════════════
        # PART 6 — Mass Distribution Controls Spin
        # ════════════════════════════════════════════════════
 
        # Reset camera from rim zoom
        self.play(
            self.camera.frame.animate.scale(1 / 0.4).move_to(ORIGIN),
            run_time=1.2, rate_func=smooth
        )
 
        dist_title = Tex("Why does distribution matter?", font_size=38, color=GOLD).to_edge(UP, buff=0.45)
        self.play(Write(dist_title), run_time=1.0)
 
        # ── Visual A — axis + particles at different radii ──
        axis_v   = DashedLine(UP * 2.8, DOWN * 2.8, color=AXIS_COLOR, stroke_width=3)
        axis_lbl = Tex("Axis", font_size=20, color=AXIS_COLOR).next_to(axis_v, UP, buff=0.1)
        self.play(Create(axis_v), Write(axis_lbl))
 
        particle_specs = [
            (0.9, PRIMARY_BLUE, "m"),
            (1.8, RING_COLOR,   "m"),
            (2.8, RED_ORANGE,   "m"),
        ]
        particle_dots  = VGroup()
        orbit_circles  = VGroup()
        r_arrows       = VGroup()
        r_labels       = VGroup()
 
        for r, col, mass_str in particle_specs:
            orbit  = Circle(radius=r, color=col, stroke_width=1.5, stroke_opacity=0.35)
            dot    = Dot(RIGHT * r, color=col, radius=0.16)
            m_lbl  = MathTex(mass_str, font_size=24, color=col).next_to(dot, UP, buff=0.08)
            r_arr  = DashedLine(ORIGIN, RIGHT * r, color=col, stroke_width=2, dash_length=0.12)
            r_lbl  = MathTex("r", font_size=22, color=col).next_to(r_arr.get_center(), DOWN, buff=0.08)
            orbit_circles.add(orbit)
            particle_dots.add(VGroup(dot, m_lbl))
            r_arrows.add(r_arr)
            r_labels.add(r_lbl)
 
        for i in range(3):
            self.play(
                Create(orbit_circles[i]), FadeIn(particle_dots[i], scale=1.4),
                Create(r_arrows[i]),      Write(r_labels[i]),
                run_time=0.6
            )
 
        resistance_lbl = Tex(
            r"Farther from axis $\Rightarrow$ harder to spin",
            font_size=26, color=LIGHT_GRAY
        ).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(resistance_lbl, shift=UP * 0.1), run_time=0.6)
 
        self.play(
            Rotate(particle_dots[0], angle=3.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_arrows[0],      angle=3.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_labels[0],      angle=3.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(particle_dots[1], angle=1.5 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_arrows[1],      angle=1.5 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_labels[1],      angle=1.5 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(particle_dots[2], angle=1.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_arrows[2],      angle=1.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            Rotate(r_labels[2],      angle=1.0 * TAU, about_point=ORIGIN, rate_func=linear, run_time=5),
            run_time=5
        )
        self.wait(0.5)
 
        self.play(FadeOut(VGroup(
            axis_v, axis_lbl, orbit_circles, particle_dots,
            r_arrows, r_labels, resistance_lbl
        )), run_time=0.7)
 
        # ── Visual B — compact disc vs. ring ──
        compare_lbl = Tex("Same total mass — different distribution",
                          font_size=28, color=LIGHT_GRAY).next_to(dist_title, DOWN, buff=0.3)
        self.play(FadeIn(compare_lbl, shift=UP * 0.1), run_time=0.7)
 
        compact_disc = Circle(radius=1.0, color=PRIMARY_BLUE)
        compact_disc.set_fill(PRIMARY_BLUE, opacity=0.55).set_stroke(PRIMARY_BLUE, width=3)
        compact_disc.move_to(LEFT * 3.2)
        compact_center = Dot(compact_disc.get_center(), color=WHITE, radius=0.07)
 
        ring_outer = Circle(radius=1.55, color=RING_COLOR)
        ring_outer.set_stroke(RING_COLOR, width=18).set_fill(opacity=0)
        ring_outer.move_to(RIGHT * 3.2)
        ring_center = Dot(ring_outer.get_center(), color=WHITE, radius=0.07)
 
        compact_lbl = Tex("Compact disc", font_size=24, color=PRIMARY_BLUE).next_to(compact_disc, DOWN, buff=0.5)
        ring_lbl    = Tex("Ring",         font_size=24, color=RING_COLOR  ).next_to(ring_outer,   DOWN, buff=0.5)
        mass_lbl_c  = MathTex(r"M = 2\text{ kg}", font_size=22, color=LIGHT_GRAY).next_to(compact_lbl, DOWN, buff=0.1)
        mass_lbl_r  = MathTex(r"M = 2\text{ kg}", font_size=22, color=LIGHT_GRAY).next_to(ring_lbl,    DOWN, buff=0.1)
 
        self.play(
            FadeIn(compact_disc), FadeIn(compact_center),
            FadeIn(ring_outer),   FadeIn(ring_center),
            FadeIn(compact_lbl),  FadeIn(ring_lbl),
            FadeIn(mass_lbl_c),   FadeIn(mass_lbl_r),
            run_time=1.2
        )
        self.wait(0.5)
 
        def torque_arrow(obj, radius_val, col=FORCE_COLOR):
            ctr    = obj.get_center()
            rim_pt = ctr + np.array([radius_val, 0, 0])
            tip_pt = rim_pt + np.array([0, 1.4, 0])
            arr    = Arrow(rim_pt, tip_pt, buff=0, color=col,
                           stroke_width=7, max_tip_length_to_length_ratio=0.22)
            lbl    = MathTex(r"\tau", font_size=28, color=col).next_to(tip_pt, RIGHT, buff=0.1)
            return VGroup(arr, lbl)
 
        torque_c = torque_arrow(compact_disc, 1.0)
        torque_r = torque_arrow(ring_outer,   1.55)
        same_tau = Tex("Same torque applied to both", font_size=24, color=FORCE_COLOR).to_edge(DOWN, buff=1.2)
 
        self.play(
            GrowArrow(torque_c[0]), FadeIn(torque_c[1]),
            GrowArrow(torque_r[0]), FadeIn(torque_r[1]),
            FadeIn(same_tau),
            run_time=1.0
        )
        self.wait(0.6)
        self.play(FadeOut(torque_c), FadeOut(torque_r), FadeOut(same_tau), run_time=0.4)
 
        self.play(
            Rotate(compact_disc, angle=3 * TAU, about_point=compact_disc.get_center(),
                   rate_func=linear, run_time=5),
            Rotate(ring_outer,   angle=1 * TAU, about_point=ring_outer.get_center(),
                   rate_func=linear, run_time=5),
            run_time=5
        )
        self.wait(0.5)
 
        alpha_c = MathTex(r"\alpha_{\text{compact}} \gg \alpha_{\text{ring}}",
                          font_size=32, color=GOLD).to_edge(DOWN, buff=1.0)
        reason  = Tex("Mass spread farther out resists rotation more strongly",
                      font_size=24, color=LIGHT_GRAY).next_to(alpha_c, DOWN, buff=0.2)
        self.play(Write(alpha_c), run_time=0.8)
        self.play(FadeIn(reason, shift=UP * 0.1), run_time=0.6)
        self.wait(2.0)
 
        self.play(FadeOut(VGroup(
            compact_disc, compact_center, ring_outer, ring_center,
            compact_lbl, ring_lbl, mass_lbl_c, mass_lbl_r,
            alpha_c, reason
        )), run_time=0.7)
 
        # ── Visual C — r² effect ──
        # Layout: axis anchored at LEFT*4.0, particles stay left of centre.
        # Equations panel on the RIGHT half (x≈3.0), zero overlap with particles.
        r2_title = Tex(r"The radius-squared effect", font_size=30, color=LIGHT_GRAY)
        r2_title.next_to(compare_lbl, DOWN, buff=0.2)
        self.play(ReplacementTransform(compare_lbl, r2_title), run_time=0.5)
 
        # Axis lives at x = -4.0  (left quarter)
        AX = -4.0
        axis_c2 = DashedLine(UP * 2.2, DOWN * 2.2, color=AXIS_COLOR, stroke_width=3).shift(LEFT * 4.0)
        self.play(Create(axis_c2))
 
        # r1 = 1.2  →  particle at x = -4.0 + 1.2 = -2.8  (safe left side)
        r1_val    = 1.2
        p1_pos    = np.array([AX + r1_val, 0, 0])
        p1_dot    = Dot(p1_pos, color=GOLD, radius=0.18)
        p1_lbl    = MathTex("m", font_size=26, color=GOLD).next_to(p1_dot, UP, buff=0.08)
        p1_orbit  = Circle(radius=r1_val, color=GOLD, stroke_width=1.5,
                           stroke_opacity=0.4).move_to(np.array([AX, 0, 0]))
        p1_r_line = DashedLine(np.array([AX, 0, 0]), p1_pos,
                               color=GOLD, stroke_width=2, dash_length=0.12)
        p1_r_lbl  = MathTex("r", font_size=24, color=GOLD).next_to(p1_r_line.get_center(), DOWN, buff=0.1)
 
        self.play(
            Create(p1_orbit), FadeIn(p1_dot, scale=1.4), Write(p1_lbl),
            Create(p1_r_line), Write(p1_r_lbl),
            run_time=0.9
        )
 
        # Equations on the RIGHT side, completely clear of the orbit circles
        # Right panel centre: x = 3.0
        EQ_X = 3.0
        i1_eq = MathTex(r"I_1 = mr^2", font_size=30, color=GOLD)
        i1_eq.move_to(np.array([EQ_X, 0.55, 0]))
        self.play(Write(i1_eq), run_time=0.8)
        self.wait(0.5)
 
        # r2 = 2.4  →  particle at x = -4.0 + 2.4 = -1.6  (still left of centre)
        r2_val    = 2.4
        p2_pos    = np.array([AX + r2_val, 0, 0])
        p2_dot    = Dot(p2_pos, color=RED_ORANGE, radius=0.18)
        p2_lbl    = MathTex("m", font_size=26, color=RED_ORANGE).next_to(p2_dot, UP, buff=0.08)
        p2_orbit  = Circle(radius=r2_val, color=RED_ORANGE, stroke_width=1.5,
                           stroke_opacity=0.4).move_to(np.array([AX, 0, 0]))
        p2_r_line = DashedLine(np.array([AX, 0, 0]), p2_pos,
                               color=RED_ORANGE, stroke_width=2, dash_length=0.12)
        p2_r_lbl  = MathTex("2r", font_size=24, color=RED_ORANGE).next_to(p2_r_line.get_center(), DOWN, buff=0.1)
 
        double_lbl = Tex("Double the radius...", font_size=26, color=LIGHT_GRAY).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(double_lbl, shift=UP * 0.1), run_time=0.5)
        self.play(
            Create(p2_orbit), FadeIn(p2_dot, scale=1.4), Write(p2_lbl),
            Create(p2_r_line), Write(p2_r_lbl),
            run_time=0.9
        )
 
        i2_eq = MathTex(r"I_2 = m(2r)^2 = 4mr^2", font_size=26, color=RED_ORANGE)
        i2_eq.move_to(np.array([EQ_X, -0.10, 0]))
        self.play(Write(i2_eq), run_time=1.0)
        self.wait(0.5)
 
        four_x_lbl = Tex("...4\texttimes{} the rotational resistance!", font_size=26, color=RED_ORANGE)
        four_x_lbl.to_edge(DOWN, buff=1.4)
        self.play(
            FadeOut(double_lbl),
            FadeIn(four_x_lbl, shift=UP * 0.1),
            Indicate(i2_eq, color=RED_ORANGE, scale_factor=1.15),
            run_time=1.0
        )
        self.wait(1.5)
 
        # Box ONLY around the key insight: I ∝ r²
        rsq_note = MathTex(r"I \propto r^2", font_size=40, color=GOLD)
        rsq_note.move_to(np.array([EQ_X, -0.85, 0]))
        r_sq_box = SurroundingRectangle(rsq_note, color=GOLD, buff=0.22, corner_radius=0.1)
        self.play(Write(rsq_note), run_time=0.8)
        self.play(Create(r_sq_box), run_time=0.6)
        self.wait(2.0)
 
        self.play(FadeOut(VGroup(
            axis_c2,
            p1_dot, p1_lbl, p1_orbit, p1_r_line, p1_r_lbl,
            p2_dot, p2_lbl, p2_orbit, p2_r_line, p2_r_lbl,
            i1_eq, i2_eq, r_sq_box, rsq_note, four_x_lbl,
            dist_title, r2_title
        )), run_time=0.8)
 
        # ════════════════════════════════════════════════════
        # PART 7 — Defining Moment of Inertia
        # ════════════════════════════════════════════════════
        moi_title = Tex("Moment of Inertia", font_size=52, color=GOLD).shift(UP * 2.8)
        moi_sub   = Tex("The rotational analog of mass", font_size=28, color=LIGHT_GRAY).next_to(moi_title, DOWN, buff=0.2)
        self.play(Write(moi_title), run_time=1.0)
        self.play(FadeIn(moi_sub, shift=UP * 0.1), run_time=0.7)
        self.wait(0.6)
 
        # ── Translational ↔ Rotational analogy columns ──
        col_l_x = -3.0
        col_r_x =  3.0
        row_ys  = [1.4, 0.55, -0.25, -1.05, -1.85]
 
        hdr_trans = Tex("Translational", font_size=26, color=PRIMARY_BLUE).move_to([col_l_x, row_ys[0], 0])
        hdr_rot   = Tex("Rotational",    font_size=26, color=RING_COLOR  ).move_to([col_r_x, row_ys[0], 0])
        divider   = DashedLine(UP * 2.1, DOWN * 2.4, color=DIM_GRAY, stroke_width=1.5)
        hdr_line  = Line(LEFT * 5.5, RIGHT * 5.5, color=DIM_GRAY, stroke_width=1.0).move_to([0, row_ys[0] - 0.32, 0])
 
        self.play(FadeIn(hdr_trans), FadeIn(hdr_rot), Create(divider), Create(hdr_line), run_time=0.8)
 
        analogy_rows = [
            (r"F = ma",                        r"\tau = I\alpha",                     PRIMARY_BLUE, RING_COLOR  ),
            (r"\text{Force } (F)",             r"\text{Torque } (\tau)",              LIGHT_GRAY,   LIGHT_GRAY  ),
            (r"\text{Mass } (m)",              r"\text{Moment of Inertia } (I)",      GOLD,         GOLD        ),
            (r"\text{Linear accel. } (a)",     r"\text{Angular accel. } (\alpha)",    LIGHT_GRAY,   LIGHT_GRAY  ),
        ]
 
        row_mobs = []
        for i, (ltex, rtex, lc, rc) in enumerate(analogy_rows):
            lm = MathTex(ltex, font_size=28, color=lc).move_to([col_l_x, row_ys[i + 1], 0])
            rm = MathTex(rtex, font_size=28, color=rc).move_to([col_r_x, row_ys[i + 1], 0])
            row_mobs.append((lm, rm))
 
        for i, (lm, rm) in enumerate(row_mobs):
            self.play(FadeIn(lm, shift=RIGHT * 0.12), FadeIn(rm, shift=LEFT * 0.12), run_time=0.45)
            if i == 0:
                self.play(
                    Indicate(lm, color=PRIMARY_BLUE, scale_factor=1.2, run_time=0.6),
                    Indicate(rm, color=RING_COLOR,   scale_factor=1.2, run_time=0.6),
                )
            elif i == 2:
                box_l = SurroundingRectangle(lm, color=GOLD, buff=0.1, corner_radius=0.06)
                box_r = SurroundingRectangle(rm, color=GOLD, buff=0.1, corner_radius=0.06)
                self.play(Create(box_l), Create(box_r), run_time=0.5)
                self.wait(0.5)
                self.play(FadeOut(box_l), FadeOut(box_r), run_time=0.3)
 
        self.wait(1.0)
 
        all_table = VGroup(hdr_trans, hdr_rot, divider, hdr_line,
                           *[mob for pair in row_mobs for mob in pair])
        self.play(FadeOut(all_table), run_time=0.7)
 
        # ── Three-line insight reveal ──
        insight_lines = VGroup(
            Tex(r"Mass tells you how hard it is to push something.",
                font_size=26, color=LIGHT_GRAY),
            Tex(r"Moment of Inertia tells you how hard it is to \textit{spin} something.",
                font_size=26, color=LIGHT_GRAY),
            Tex(r"But $I$ depends on the \textbf{axis of rotation} --- not just how much mass,",
                font_size=26, color=LIGHT_GRAY),
            Tex(r"but \textbf{where} that mass sits relative to the axis.",
                font_size=26, color=GOLD),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).center().shift(DOWN * 0.2)
 
        for line in insight_lines:
            self.play(FadeIn(line, shift=UP * 0.1), run_time=0.65)
            self.wait(0.35)
        self.wait(1.0)
 
        self.play(FadeOut(insight_lines), run_time=0.7)
 
        # Fade out moi_title and moi_sub before rod demo to prevent overlap
        self.play(FadeOut(VGroup(moi_title, moi_sub)), run_time=0.6)
 
        # ── Axis-dependence rod demo — top of screen now clear ──
        axis_demo_lbl = Tex(r"Same object, different axis $\rightarrow$ different $I$",
                            font_size=30, color=LIGHT_GRAY).to_edge(UP, buff=0.45)
        self.play(FadeIn(axis_demo_lbl, shift=UP * 0.1))
 
        rod_ctr_pos = LEFT * 3.2 + DOWN * 0.3
        rod_center  = Rectangle(width=3.6, height=0.28, color=PRIMARY_BLUE)
        rod_center.set_fill(PRIMARY_BLUE, opacity=0.55).move_to(rod_ctr_pos)
 
        axis_center = DashedLine(rod_ctr_pos + DOWN * 1.6, rod_ctr_pos + UP * 1.6,
                                 color=AXIS_COLOR, stroke_width=3)
        axis_c_lbl  = Tex("Axis", font_size=18, color=AXIS_COLOR).next_to(axis_center, UP, buff=0.06)
        ctr_lbl     = Tex("Center axis", font_size=22, color=PRIMARY_BLUE).next_to(rod_center,  DOWN, buff=0.6)
        i_ctr_eq    = MathTex(r"I = \tfrac{1}{12}ML^2", font_size=28, color=GOLD).next_to(ctr_lbl,    DOWN, buff=0.12)
        i_ctr_sub   = Tex("(smaller $I$)", font_size=20, color=LIGHT_GRAY).next_to(i_ctr_eq,  DOWN, buff=0.1)
 
        rod_end_pos = RIGHT * 3.2 + DOWN * 0.3
        rod_end     = Rectangle(width=3.6, height=0.28, color=RING_COLOR)
        rod_end.set_fill(RING_COLOR, opacity=0.45).move_to(rod_end_pos)
        rod_end.align_to(rod_end_pos + LEFT * 1.8, LEFT)
 
        axis_end_x  = rod_end_pos[0] - 1.8
        axis_end    = DashedLine(
            np.array([axis_end_x, rod_end_pos[1] - 1.6, 0]),
            np.array([axis_end_x, rod_end_pos[1] + 1.6, 0]),
            color=AXIS_COLOR, stroke_width=3
        )
        axis_e_lbl  = Tex("Axis", font_size=18, color=AXIS_COLOR).next_to(axis_end, UP, buff=0.06)
        end_lbl     = Tex("End axis", font_size=22, color=RING_COLOR).next_to(rod_end,     DOWN, buff=0.6)
        i_end_eq    = MathTex(r"I = \tfrac{1}{3}ML^2", font_size=28, color=GOLD).next_to(end_lbl,     DOWN, buff=0.12)
        i_end_sub   = Tex(r"(4$\times$ larger $I$!)", font_size=20, color=RED_ORANGE).next_to(i_end_eq, DOWN, buff=0.1)
 
        self.play(
            FadeIn(rod_center), Create(axis_center), Write(axis_c_lbl),
            FadeIn(rod_end),    Create(axis_end),    Write(axis_e_lbl),
            run_time=1.0
        )
        self.play(
            FadeIn(ctr_lbl), Write(i_ctr_eq), FadeIn(i_ctr_sub),
            FadeIn(end_lbl), Write(i_end_eq), FadeIn(i_end_sub),
            run_time=0.9
        )
        self.wait(0.4)
 
        self.play(
            Rotate(rod_center, angle=2.0 * TAU,
                   about_point=rod_ctr_pos,
                   rate_func=linear, run_time=4.5),
            Rotate(rod_end,    angle=0.8 * TAU,
                   about_point=np.array([axis_end_x, rod_end_pos[1], 0]),
                   rate_func=linear, run_time=4.5),
            run_time=4.5
        )
        self.wait(0.5)
 
        four_x = Tex(r"Same rod, same mass --- $I$ is 4$\times$ bigger at the end!",
                     font_size=24, color=RED_ORANGE).to_edge(DOWN, buff=0.8)
        self.play(
            Indicate(i_end_sub, color=RED_ORANGE, scale_factor=1.3),
            FadeIn(four_x, shift=UP * 0.1),
            run_time=0.9
        )
        self.wait(2.0)
 
        self.play(FadeOut(VGroup(
            rod_center, axis_center, axis_c_lbl, ctr_lbl, i_ctr_eq, i_ctr_sub,
            rod_end,    axis_end,    axis_e_lbl, end_lbl,  i_end_eq, i_end_sub,
            four_x, axis_demo_lbl
        )), run_time=0.8)
 
        # ── Final definition + formula teaser ──
        definition_group = VGroup(
            Tex("Moment of Inertia $(I)$", font_size=40, color=GOLD),
            Tex(r"is the measure of how strongly a body", font_size=28, color=LIGHT_GRAY),
            Tex(r"resists angular acceleration,", font_size=28, color=LIGHT_GRAY),
            Tex(r"determined by both its \textbf{mass} and how that mass", font_size=28, color=LIGHT_GRAY),
            Tex(r"is \textbf{distributed around the axis of rotation}.", font_size=28, color=GOLD),
        ).arrange(DOWN, buff=0.28).center()
 
        for line in definition_group:
            self.play(FadeIn(line, shift=UP * 0.1), run_time=0.55)
            self.wait(0.2)
        self.wait(1.2)
 
        formula_hint = VGroup(
            Tex("Mathematically:", font_size=26, color=DIM_GRAY),
            MathTex(r"I = \sum_i m_i r_i^2", font_size=44, color=GOLD),
            Tex("(derived in the next scene)", font_size=22, color=DIM_GRAY),
        ).arrange(DOWN, buff=0.2)
        formula_hint.next_to(definition_group, DOWN, buff=0.55)
 
        hint_box = SurroundingRectangle(formula_hint[1], color=GOLD, buff=0.18, corner_radius=0.1)
 
        self.play(FadeIn(formula_hint[0], shift=UP * 0.1), run_time=0.5)
        self.play(Write(formula_hint[1]), run_time=1.2)
        self.play(Create(hint_box), FadeIn(formula_hint[2], shift=UP * 0.1), run_time=0.7)
        self.wait(3.0)
 
        # ── Scene-end clean-up ──
        self.play(FadeOut(VGroup(
            # moi_title, moi_sub already faded out before rod demo
            definition_group,
            formula_hint, hint_box
        )), run_time=1.2)
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1.0), run_time=0.5)


# ─────────────────────────────────────────────────────────────
#  SCENE 2 — RotationalNewton
# ─────────────────────────────────────────────────────────────
class RotationalNewton(MovingCameraScene):
    """Derive I as the rotational analog of mass — F=ma → τ=Iα from first principles."""

    def construct(self):
        chapter_card(self, "Rotational Newton's Law",
                     r"Why does $I$ play the role of mass?")

        # ── F = ma ──
        fma = MathTex(r"F", r"=", r"m", r"a", font_size=72)
        fma[0].set_color(RED_ORANGE)
        fma[2].set_color(GOLD)
        fma[3].set_color(PRIMARY_BLUE)
        self.play(Write(fma), run_time=1.5)

        flbl = Tex("Force",        font_size=22, color=RED_ORANGE).next_to(fma[0], DOWN, buff=0.3)
        mlbl = Tex("Mass",         font_size=22, color=GOLD).next_to(fma[2], DOWN, buff=0.3)
        albl = Tex("Acceleration", font_size=22, color=PRIMARY_BLUE).next_to(fma[3], DOWN, buff=0.3)
        self.play(FadeIn(flbl), FadeIn(mlbl), FadeIn(albl))
        self.wait(1.0)
        self.play(FadeOut(VGroup(flbl, mlbl, albl)))

        # ── Transform → τ = Iα ──
        tia = MathTex(r"\tau", r"=", r"I", r"\alpha", font_size=72)
        tia[0].set_color(RED_ORANGE)
        tia[2].set_color(GOLD)
        tia[3].set_color(PRIMARY_BLUE)
        self.play(TransformMatchingTex(fma, tia), run_time=2.0)

        t2lbl = Tex("Torque",              font_size=22, color=RED_ORANGE).next_to(tia[0], DOWN, buff=0.3)
        i2lbl = Tex("Moment of Inertia",   font_size=22, color=GOLD).next_to(tia[2], DOWN, buff=0.3)
        a2lbl = Tex("Angular Accel.",      font_size=22, color=PRIMARY_BLUE).next_to(tia[3], DOWN, buff=0.3)
        self.play(FadeIn(t2lbl), FadeIn(i2lbl), FadeIn(a2lbl))
        self.wait(1.5)
        self.play(FadeOut(VGroup(t2lbl, i2lbl, a2lbl)))
        self.play(tia.animate.to_edge(UP, buff=0.4).scale(0.65), run_time=0.8)

        # ── Single-particle derivation ──
        sec = Tex("Single Particle Derivation", font_size=30, color=LIGHT_GRAY).to_edge(UP, buff=1.5)
        self.play(Write(sec))

        axis_l = DashedLine(UP * 2.5, DOWN * 2.5, color=AXIS_COLOR, stroke_width=3).shift(LEFT * 4.5)
        axis_t = Tex("Axis", font_size=22, color=AXIS_COLOR).next_to(axis_l, UP, buff=0.05)
        self.play(Create(axis_l), Write(axis_t))

        r_val   = 2.8
        mpos    = LEFT * 4.5 + RIGHT * r_val          # = RIGHT*(r_val-4.5)
        mdot    = Dot(mpos, color=GOLD, radius=0.18)
        mlbl2   = MathTex("m", font_size=28, color=GOLD).next_to(mdot, UP, buff=0.1)
        rline   = DashedLine(LEFT * 4.5, mpos, color=VECTOR_COLOR, stroke_width=3)
        rlbl    = MathTex("r", font_size=28, color=VECTOR_COLOR).next_to(rline.get_center(), UP, buff=0.15)

        self.play(FadeIn(mdot, scale=1.5), Write(mlbl2),
                  Create(rline), Write(rlbl))

        ft_arr  = Arrow(mpos, mpos + UP * 1.3, buff=0, color=GREEN, stroke_width=5,
                        max_tip_length_to_length_ratio=0.3)
        ft_lbl  = MathTex(r"F_t", font_size=28, color=GREEN).next_to(ft_arr, RIGHT, buff=0.1)
        self.play(GrowArrow(ft_arr), Write(ft_lbl))
        self.wait(0.4)

        steps_deriv = VGroup(
            MathTex(r"F_t = m a_t",              font_size=34),
            MathTex(r"a_t = r \alpha",            font_size=34),
            MathTex(r"F_t = m r \alpha",          font_size=34),
            MathTex(r"\tau = r F_t = mr^2\alpha", font_size=34),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)

        for step in steps_deriv:
            self.play(Write(step), run_time=0.9)
            self.wait(0.35)

        box_last = SurroundingRectangle(steps_deriv[-1], color=GOLD, buff=0.12, corner_radius=0.07)
        self.play(Create(box_last))

        highlight = MathTex(r"\underbrace{mr^2}_{I}", font_size=36, color=GOLD)
        highlight.next_to(steps_deriv[-1], DOWN, buff=0.45).align_to(steps_deriv, LEFT)
        self.play(Write(highlight))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            axis_l, axis_t, mdot, mlbl2, rline, rlbl,
            ft_arr, ft_lbl, steps_deriv, box_last, highlight, sec, tia
        )))
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1.0), run_time=1.0)

        # ── Multi-particle extension ──
        axis2 = DashedLine(UP * 2.5, DOWN * 2.5, color=AXIS_COLOR, stroke_width=3).shift(LEFT * 5.5)
        self.play(Create(axis2))

        particle_data = [(0.9, 0.5), (1.6, -0.3), (2.2, 0.7), (2.9, -0.1), (3.5, 0.3)]
        dots_grp  = VGroup()
        arrows_grp = VGroup()
        term_mobs  = []

        for idx, (ri, dy) in enumerate(particle_data):
            pos = LEFT * 5.5 + RIGHT * ri + UP * dy
            dot = Dot(pos, color=GOLD, radius=0.13)
            arr = Arrow(
                LEFT * 5.5 + UP * dy, pos, buff=0, color=VECTOR_COLOR,
                stroke_width=3, max_tip_length_to_length_ratio=0.25
            )
            ri_lbl = MathTex(f"r_{idx+1}", font_size=22, color=VECTOR_COLOR)
            ri_lbl.next_to(arr.get_center(), UP, buff=0.05)
            dots_grp.add(dot)
            arrows_grp.add(VGroup(arr, ri_lbl))

            term = MathTex(
                f"m_{idx+1}r_{idx+1}^2" + (" + " if idx < len(particle_data)-1 else ""),
                font_size=26, color=LIGHT_GRAY
            )
            term_mobs.append(term)

        terms_row = VGroup(*term_mobs).arrange(RIGHT, buff=0.05)
        terms_row.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.8)

        for idx in range(len(particle_data)):
            self.play(
                FadeIn(dots_grp[idx], scale=1.5),
                GrowArrow(arrows_grp[idx][0]),
                Write(arrows_grp[idx][1]),
                FadeIn(term_mobs[idx]),
                run_time=0.55
            )

        sum_eq = MathTex(r"I_{\text{total}}", r"=", r"\sum_i", r"m_i", r"r_i^2", font_size=40)
        sum_eq.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(Write(sum_eq))
        self.wait(1.0)

        # ── Σ → ∫ ──
        limit_note = Tex(r"Particles become infinitesimal\ldots", font_size=26, color=LIGHT_GRAY)
        limit_note.next_to(sum_eq, DOWN, buff=0.4)
        self.play(Write(limit_note))
        self.wait(0.8)

        self.play(FadeOut(arrows_grp), FadeOut(terms_row))
        dense_dots = VGroup(*[
            Dot(LEFT * 5.5 + RIGHT * (0.9 + 2.6 * np.random.random()) + UP * (np.random.random() * 1.5 - 0.75), color=GOLD, radius=0.06)
            for _ in range(60)
        ])
        self.play(FadeIn(dense_dots))
        self.wait(0.5)

        continuous_body = RoundedRectangle(corner_radius=0.4, width=3.2, height=1.8, color=PRIMARY_BLUE)
        continuous_body.set_fill(PRIMARY_BLUE, opacity=0.3).move_to(LEFT * 5.5 + RIGHT * 2.2)
        self.play(ReplacementTransform(VGroup(dots_grp, dense_dots), continuous_body))
        self.wait(0.5)

        int_eq = MathTex(r"I", r"=", r"\int", r"r^2", r"\, dm", font_size=54)
        int_eq[3].set_color(GOLD)
        int_eq[4].set_color(PRIMARY_BLUE)
        int_eq.center().shift(DOWN * 0.2)

        int_box = SurroundingRectangle(int_eq, color=GOLD, buff=0.3, corner_radius=0.1)

        self.play(FadeOut(axis2), FadeOut(limit_note))
        self.play(TransformMatchingTex(sum_eq, int_eq), run_time=2.0)
        self.play(Create(int_box))

        master_lbl = Tex("The Master Formula", font_size=28, color=GOLD)
        master_lbl.next_to(int_box, UP, buff=0.4)
        self.play(FadeIn(master_lbl, shift=DOWN * 0.2))
        
        self.play(self.camera.frame.animate.scale(0.7).move_to(int_eq), run_time=1.5)
        self.wait(3.0)
        
        self.play(FadeOut(VGroup(int_eq, int_box, master_lbl, continuous_body)))
        self.camera.frame.scale(1/0.7).move_to(ORIGIN)


# ─────────────────────────────────────────────────────────────
#  SCENE 3 — MomentDefinition
# ─────────────────────────────────────────────────────────────
class MomentDefinition(MovingCameraScene):
    """Deep geometric understanding: what does r² mean physically?"""

    def construct(self):
        chapter_card(self, "Understanding $r^2$", "Why the quadratic dependence?")

        master = MathTex(r"I = \int", r"r^2", r"\, dm", font_size=46)
        master[1].set_color(GOLD)
        master[2].set_color(PRIMARY_BLUE)
        master.to_edge(UP, buff=0.5)
        self.play(Write(master))
        self.wait(0.5)

        # ── Quadratic sensitivity: dynamic visualization ──
        axis_l  = DashedLine(UP * 2.5, DOWN * 2.5, color=AXIS_COLOR, stroke_width=3).shift(LEFT * 4)
        axis_t  = Tex("axis", font_size=20, color=AXIS_COLOR).next_to(axis_l, UP, buff=0.05)
        self.play(Create(axis_l), Write(axis_t))

        r_val = ValueTracker(1.0)

        dm_dot = always_redraw(lambda: Dot(LEFT * 4 + RIGHT * r_val.get_value(), color=GOLD, radius=0.15))
        r_arr = always_redraw(lambda: Arrow(LEFT * 4, LEFT * 4 + RIGHT * r_val.get_value(), buff=0, color=VECTOR_COLOR, stroke_width=4))
        r_lbl = always_redraw(lambda: MathTex("r", font_size=26, color=VECTOR_COLOR).next_to(r_arr, UP, buff=0.06))
        
        contrib_lbl = Tex("Current contribution ($r^2$):", font_size=28, color=LIGHT_GRAY).to_edge(RIGHT, buff=2.0).shift(UP * 1.0)
        contrib_val = always_redraw(lambda: DecimalNumber(r_val.get_value()**2, num_decimal_places=2, font_size=36, color=GOLD).next_to(contrib_lbl, DOWN, buff=0.3))
        
        contrib_arrow = always_redraw(lambda: Arrow(
            contrib_val.get_bottom() + DOWN * 0.2, 
            contrib_val.get_bottom() + DOWN * (0.2 + r_val.get_value()**2 * 0.4), 
            buff=0, color=RED_ORANGE, stroke_width=6, max_tip_length_to_length_ratio=0.2
        ))

        self.play(FadeIn(dm_dot), GrowArrow(r_arr), Write(r_lbl))
        self.play(Write(contrib_lbl), FadeIn(contrib_val), GrowArrow(contrib_arrow))
        
        self.play(r_val.animate.set_value(3.0), run_time=4.0, rate_func=smooth)
        self.wait(1.5)

        self.play(FadeOut(VGroup(axis_l, axis_t, dm_dot, r_arr, r_lbl, contrib_lbl, contrib_val, contrib_arrow)))

        # ── Parabola plot ──
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 9, 3],
                  x_length=4.5, y_length=3.5,
                  axis_config={"color": LIGHT_GRAY, "stroke_width": 2},
                  tips=True).shift(LEFT * 1.5 + DOWN * 0.5)

        ax_xl = ax.get_x_axis_label(MathTex("r", font_size=28, color=VECTOR_COLOR))
        ax_yl = ax.get_y_axis_label(MathTex(r"r^2", font_size=28, color=GOLD),
                                     edge=LEFT, direction=LEFT)

        parabola = ax.plot(lambda t: t ** 2, x_range=[0, 3],
                           color=GOLD, stroke_width=4)
        p_lbl = MathTex(r"r^2", font_size=28, color=GOLD).move_to(ax.c2p(2.7, 8.0))

        self.play(Create(ax), Write(ax_xl), Write(ax_yl))
        self.play(Create(parabola, rate_func=smooth), run_time=1.5)
        self.play(Write(p_lbl))
        self.wait(0.8)

        # ── Physical interpretation ──
        interp_t = Tex("Physical Meaning", font_size=30, color=PRIMARY_BLUE)
        interp_t.to_edge(RIGHT, buff=2.8).shift(UP * 2.0)
        self.play(Write(interp_t))

        def make_panel(text_lines, color, shift_y):
            box = RoundedRectangle(corner_radius=0.12, width=3.6, height=2.4, color=color)
            box.set_fill(color, opacity=0.1)
            content = VGroup(*[Tex(t, font_size=21, color=color) for t in text_lines])
            content.arrange(DOWN, buff=0.22).move_to(box)
            grp = VGroup(box, content)
            grp.to_edge(RIGHT, buff=0.4).shift(UP * shift_y)
            return grp

        panel1 = make_panel(
            ["Dense, small $r$", "Easy to spin / stop", r"$\Rightarrow$ Low $I$"],
            PRIMARY_BLUE, 0.6
        )
        panel2 = make_panel(
            ["Spread out, large $r$", "Hard to spin / stop", r"$\Rightarrow$ High $I$"],
            GOLD, -2.2
        )

        self.play(Create(panel1[0]), FadeIn(panel1[1]))
        self.wait(0.4)
        self.play(Create(panel2[0]), FadeIn(panel2[1]))
        self.wait(0.5)

        def_txt = Tex(
            r"Moment of inertia $=$ rotational inertia\\$=$ resistance to change in rotation",
            font_size=24, color=LIGHT_GRAY
        ).next_to(panel2, DOWN, buff=0.35)
        self.play(Write(def_txt))
        self.wait(1.5)

        # ── Unit analysis ──
        unit = MathTex(
            r"[I] = \text{kg}\cdot\text{m}^2",
            r"\;\leftarrow\;",
            r"[\tau]=\text{N}\cdot\text{m},\;\;[\alpha]=\text{rad/s}^2",
            font_size=28, color=LIGHT_GRAY
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(unit))
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            master, ax, ax_xl, ax_yl, parabola, p_lbl,
            interp_t, panel1, panel2, def_txt, unit
        )))


# ─────────────────────────────────────────────────────────────
#  SCENE 4 — ParallelAxisTheorem
# ─────────────────────────────────────────────────────────────
class ParallelAxisTheorem(MovingCameraScene):
    """Derive and visually prove I = I_cm + Md²."""

    def construct(self):
        chapter_card(self, "Parallel Axis Theorem",
                     r"$I = I_{\text{cm}} + Md^2$")

        # ── Setup: irregular shape ──
        shape = Polygon(
            [-1.1, 0.8, 0], [-0.3, 1.2, 0], [0.5, 0.9, 0],
            [0.9, 0.2, 0], [0.6, -0.7, 0], [-0.1, -1.0, 0],
            [-0.8, -0.6, 0], [-1.2, 0.1, 0],
            color=PRIMARY_BLUE
        ).set_fill(PRIMARY_BLUE, opacity=0.22).set_stroke(PRIMARY_BLUE, width=3)
        shape.shift(LEFT * 1.2)
        cm_pos = shape.get_center()

        cm_dot = Dot(cm_pos, color=WHITE, radius=0.1)
        cm_lbl = Tex("CM", font_size=22, color=WHITE).next_to(cm_dot, RIGHT, buff=0.1)
        cm_axis = Line(cm_pos + UP * 2.8, cm_pos + DOWN * 2.8,
                       color=PRIMARY_BLUE, stroke_width=3)
        cm_axis_lbl = MathTex(r"I_{\text{cm}}", font_size=26, color=PRIMARY_BLUE).next_to(cm_axis, UP, buff=0.1)

        self.play(Create(shape), run_time=1.4, rate_func=smooth)
        self.play(FadeIn(cm_dot, scale=1.5), Write(cm_lbl), Create(cm_axis), Write(cm_axis_lbl))
        self.wait(0.7)

        # ── Parallel axis with dynamic d ──
        d_tr = ValueTracker(2.4)

        par_axis = always_redraw(lambda: DashedLine(
            cm_pos + RIGHT * d_tr.get_value() + UP * 2.8,
            cm_pos + RIGHT * d_tr.get_value() + DOWN * 2.8,
            color=GOLD, stroke_width=3, dash_length=0.14
        ))
        d_brace = always_redraw(lambda: BraceBetweenPoints(
            cm_pos + DOWN * 1.8,
            cm_pos + RIGHT * d_tr.get_value() + DOWN * 1.8,
            direction=DOWN, color=GOLD
        ))
        d_lbl = always_redraw(lambda: MathTex("d", font_size=28, color=GOLD).next_to(d_brace, DOWN, buff=0.08))

        self.play(Create(par_axis))
        self.play(FadeIn(d_brace), Write(d_lbl))
        self.wait(0.6)

        # ── Theorem statement ──
        thm = MathTex(
            r"I_{\text{par}} = ", r"I_{\text{cm}}", r" + ", r"Md^2",
            font_size=42
        )
        thm[1].set_color(PRIMARY_BLUE)
        thm[3].set_color(GOLD)
        thm.to_edge(RIGHT, buff=0.4).shift(UP * 2.8)
        thm_box = SurroundingRectangle(thm, color=LIGHT_GRAY, buff=0.18, corner_radius=0.07)
        self.play(Write(thm), Create(thm_box))
        self.wait(0.8)

        # ── Geometric vectors ──
        d_vec = always_redraw(lambda: Arrow(cm_pos + RIGHT * d_tr.get_value(), cm_pos, buff=0, color=GOLD, stroke_width=4))
        d_vec_lbl = always_redraw(lambda: MathTex(r"\vec{d}", font_size=24, color=GOLD).next_to(d_vec.get_center(), UP, buff=0.1))

        theta_dm = ValueTracker(2.55)
        dm_pos_func = lambda: cm_pos + np.array([0.72 * np.cos(theta_dm.get_value()), 0.72 * np.sin(theta_dm.get_value()), 0])
        dm_dot = always_redraw(lambda: Dot(dm_pos_func(), color=RED_ORANGE, radius=0.08))
        r_prime = always_redraw(lambda: Arrow(cm_pos, dm_pos_func(), buff=0, color=VECTOR_COLOR, stroke_width=3))
        r_prime_lbl = always_redraw(lambda: MathTex(r"\vec{r}'", font_size=20, color=VECTOR_COLOR).next_to(r_prime.get_center(), UP, buff=0.05))
        r_vec = always_redraw(lambda: Arrow(cm_pos + RIGHT * d_tr.get_value(), dm_pos_func(), buff=0, color=PRIMARY_BLUE, stroke_width=3))
        r_vec_lbl = always_redraw(lambda: MathTex(r"\vec{r} = \vec{r}' + \vec{d}", font_size=20, color=PRIMARY_BLUE).next_to(r_vec.get_center(), RIGHT, buff=0.05))

        self.play(GrowArrow(d_vec), Write(d_vec_lbl))
        self.play(FadeIn(dm_dot), GrowArrow(r_prime), Write(r_prime_lbl))
        self.play(GrowArrow(r_vec), Write(r_vec_lbl))
        
        self.play(theta_dm.animate.set_value(2.55 + 0.5), run_time=1.5, rate_func=there_and_back)

        # ── Derivation ──
        lines = [
            MathTex(r"I = \int |\vec{r}' + \vec{d}|^2\,dm",             font_size=30),
            MathTex(r"= \int (r'^2 + 2\vec{r}'\cdot\vec{d} + d^2)\,dm", font_size=28),
            MathTex(r"= \int r'^2\,dm + 2\vec{d}\cdot\underbrace{\int\vec{r}'\,dm}_{=\,0} + d^2\!\int dm",
                    font_size=26, color=WHITE),
            MathTex(r"\Rightarrow\; I = I_{\text{cm}} + Md^2", font_size=36, color=GOLD),
        ]
        deriv = VGroup(*lines).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        deriv.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)

        zero_note = Tex(r"Zero because this is the Center of Mass!", font_size=20, color=GOLD)

        for i, line in enumerate(lines):
            if i == 0:
                self.play(Write(line), Indicate(r_vec), run_time=1.0)
            elif i == 1:
                self.play(Write(line), Indicate(r_prime), Indicate(d_vec), run_time=1.0)
            else:
                self.play(Write(line), run_time=1.0)
            
            if i == 2:
                zero_note.next_to(line, DOWN, buff=0.12).align_to(line, LEFT)
                self.play(Write(zero_note), Flash(cm_dot, color=GOLD, flash_radius=0.5), run_time=0.7)
            if i > 0:
                self.play(lines[i-1].animate.set_color(DIM_GRAY), run_time=0.25)
            self.wait(0.4)

        final_box = SurroundingRectangle(lines[-1], color=GOLD, buff=0.14, corner_radius=0.07)
        self.play(Create(final_box))
        
        self.play(self.camera.frame.animate.scale(0.85).move_to(deriv), run_time=1.5)
        self.wait(2.0)
        self.play(self.camera.frame.animate.scale(1/0.85).move_to(ORIGIN), run_time=1.0)

        # ── Dynamic d animation: bar shows Md² growing ──
        self.play(FadeOut(VGroup(deriv, zero_note, final_box, thm, thm_box, d_vec, d_vec_lbl, dm_dot, r_prime, r_prime_lbl, r_vec, r_vec_lbl)))

        bar_title = Tex("Total $I$ increases as $d$ grows:", font_size=26, color=LIGHT_GRAY)
        bar_title.to_edge(RIGHT, buff=1.8).shift(UP * 2.2)
        self.play(Write(bar_title))

        I_CM_FIXED = 0.45

        def make_bars(d_val):
            md2 = d_val ** 2 * 0.28
            scale = 2.8 / (2.4 ** 2 * 0.28 + I_CM_FIXED)
            b1 = Rectangle(width=0.65, height=I_CM_FIXED * scale,
                            color=PRIMARY_BLUE, fill_color=PRIMARY_BLUE, fill_opacity=0.85)
            b2 = Rectangle(width=0.65, height=max(md2 * scale, 0.01),
                            color=GOLD, fill_color=GOLD, fill_opacity=0.85)
            stack = VGroup(b1, b2).arrange(UP, buff=0)
            stack.to_edge(RIGHT, buff=1.8).shift(DOWN * 0.6)

            lbl_cm  = Tex(r"$I_{\text{cm}}$", font_size=20, color=PRIMARY_BLUE).next_to(b1, LEFT, buff=0.1)
            lbl_md2 = Tex(r"$Md^2$",          font_size=20, color=GOLD).next_to(b2, LEFT, buff=0.1) if md2 * scale > 0.05 else VMobject()
            return VGroup(stack, lbl_cm, lbl_md2)

        bars = always_redraw(lambda: make_bars(d_tr.get_value()))
        d_val_lbl = always_redraw(lambda: MathTex(
            r"d = " + f"{d_tr.get_value():.1f}",
            font_size=26, color=GOLD
        ).to_edge(RIGHT, buff=3.5).shift(DOWN * 0.1))

        self.add(bars, d_val_lbl)
        self.play(d_tr.animate.set_value(0.2), run_time=1.5, rate_func=smooth)
        self.wait(0.3)
        self.play(d_tr.animate.set_value(2.6), run_time=3.0, rate_func=smooth)
        self.wait(1.0)
        
        rot_grp = VGroup(shape, cm_dot, cm_lbl, cm_axis, cm_axis_lbl)
        
        # First CM rotation
        self.play(Rotate(rot_grp, angle=TAU, about_point=cm_pos, run_time=1.5, rate_func=smooth))
        self.wait(0.5)
        
        # Second offset rotation
        path = TracedPath(cm_dot.get_center, stroke_color=LIGHT_GRAY, stroke_width=2, stroke_opacity=0.5)
        self.add(path)
        self.play(Rotate(rot_grp, angle=TAU, about_point=cm_pos + RIGHT * d_tr.get_value(), run_time=3.5, rate_func=smooth))
        self.wait(1.0)

        # ── Key insight ──
        self.play(FadeOut(VGroup(
            rot_grp, par_axis, d_brace, d_lbl, bars, d_val_lbl, bar_title, path
        )))
        insight_lines = VGroup(
            Tex("The CM axis always gives the", font_size=28, color=WHITE),
            Tex(r"\textbf{MINIMUM} moment of inertia", font_size=32, color=GOLD),
            Tex("for any given axis direction.", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.3).center()
        ins_box = SurroundingRectangle(insight_lines, color=GOLD, buff=0.35, corner_radius=0.12)
        self.play(Write(insight_lines), Create(ins_box), run_time=1.5)
        
        self.play(self.camera.frame.animate.scale(0.85).move_to(insight_lines), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(insight_lines, ins_box)))
        self.camera.frame.scale(1/0.85).move_to(ORIGIN)


# ─────────────────────────────────────────────────────────────
#  SCENE 5 — PerpendicularAxisTheorem
# ─────────────────────────────────────────────────────────────
class PerpendicularAxisTheorem(ThreeDScene):
    """Derive I_x + I_y = I_z — it's secretly Pythagoras. Planar objects only."""

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2)

        # ── Chapter card (fixed frame) ──
        ch = VGroup(
            Tex("Perpendicular Axis Theorem", font_size=50, color=GOLD),
            MathTex(r"I_x + I_y = I_z",       font_size=36, color=LIGHT_GRAY)
        ).arrange(DOWN, buff=0.4).center()
        self.add_fixed_in_frame_mobjects(ch)
        self.play(FadeIn(ch, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(ch))
        self.remove(ch)

        # ── Caveat ──
        caveat = Tex(r"\textbf{Valid ONLY for planar (flat) objects!}",
                     font_size=36, color=RED_ORANGE).center()
        self.add_fixed_in_frame_mobjects(caveat)
        self.play(Write(caveat))
        self.wait(2.0)
        self.play(FadeOut(caveat))
        self.remove(caveat)

        # ── 3D setup ──
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2.0)

        lamina = Square(side_length=3.6, color=PRIMARY_BLUE)
        lamina.set_fill(PRIMARY_BLUE, opacity=0.18)
        lamina.set_stroke(PRIMARY_BLUE, width=2)

        x_ax = Arrow3D([-3, 0, 0], [3.5, 0, 0], color=RED_ORANGE, thickness=0.03)
        y_ax = Arrow3D([0, -3, 0], [0, 3.5, 0], color=GREEN,      thickness=0.03)
        z_ax = Arrow3D([0, 0, -0.5], [0, 0, 3.5], color=PRIMARY_BLUE, thickness=0.03)

        xl = MathTex("x", font_size=28, color=RED_ORANGE).move_to([3.9, 0, 0])
        yl = MathTex("y", font_size=28, color=GREEN).move_to([0, 3.9, 0])
        zl = MathTex("z", font_size=28, color=PRIMARY_BLUE).move_to([0, 0, 3.9])

        self.play(Create(lamina))
        self.play(Create(x_ax), Create(y_ax), Create(z_ax))
        self.add_fixed_in_frame_mobjects(xl, yl, zl)
        self.play(Write(xl), Write(yl), Write(zl))
        self.begin_ambient_camera_rotation(rate=0.04)
        self.wait(2.0)
        self.stop_ambient_camera_rotation()

        # ── Formal statement ──
        formal = MathTex(
            r"I_x", r"+", r"I_y", r"=", r"I_z",
            font_size=42
        )
        formal[0].set_color(RED_ORANGE)   # I_x
        formal[2].set_color(GREEN)         # I_y
        formal[4].set_color(PRIMARY_BLUE)  # I_z
        formal.to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(formal)
        self.play(Write(formal))
        self.wait(0.7)

        # ── Derivation ──
        deriv = VGroup(
            MathTex(r"I_z = \int (x^2+y^2)\,dm", font_size=28),
            MathTex(r"I_x = \int y^2\,dm",        font_size=28, color=RED_ORANGE),
            MathTex(r"I_y = \int x^2\,dm",        font_size=28, color=GREEN),
            MathTex(r"I_z = I_y + I_x",           font_size=32, color=GOLD),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(deriv)
        for line in deriv:
            self.play(Write(line), run_time=0.9)
            self.wait(0.35)

        concl = MathTex(r"\boxed{I_x + I_y = I_z}", font_size=38, color=GOLD)
        concl.next_to(deriv, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(concl)
        self.play(Write(concl))
        self.wait(2.0)

        self.play(FadeOut(deriv), FadeOut(concl))
        self.remove(deriv, concl)

        # ── Pythagorean visual ──
        pt = np.array([1.2, 0.9, 0])
        pdot = Dot3D(pt, color=GOLD, radius=0.12)
        xline = Line3D([0, pt[1], 0], pt, color=GREEN,        thickness=0.04)
        yline = Line3D([pt[0], 0, 0], pt, color=RED_ORANGE,   thickness=0.04)
        rline = Line3D([0, 0, 0],     pt, color=PRIMARY_BLUE,  thickness=0.04)

        self.play(FadeIn(pdot, scale=1.5))
        self.play(Create(xline), Create(yline), Create(rline))

        pyth = MathTex(r"r^2 = x^2 + y^2", font_size=34, color=GOLD).to_corner(DR, buff=0.5)
        pyth_sub = Tex("It's secretly Pythagoras!", font_size=26, color=LIGHT_GRAY).next_to(pyth, UP, buff=0.25)
        self.add_fixed_in_frame_mobjects(pyth, pyth_sub)
        self.play(Write(pyth), Write(pyth_sub))

        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()

        # ── Counterexample (Cube) ──
        self.play(FadeOut(VGroup(lamina, pdot, xline, yline, rline)),
                  FadeOut(formal), FadeOut(pyth), FadeOut(pyth_sub))
        self.remove(formal, pyth, pyth_sub)
        
        cube = Cube(side_length=2.5, color=RED_ORANGE)
        cube.set_fill(RED_ORANGE, opacity=0.15)
        cube.set_stroke(RED_ORANGE, width=2)
        
        c_pdot = Dot3D([1.25, 1.25, 1.25], color=GOLD, radius=0.15)
        c_xline = Line3D([0, 1.25, 1.25], [1.25, 1.25, 1.25], color=GREEN, thickness=0.04)
        c_yline = Line3D([1.25, 0, 1.25], [1.25, 1.25, 1.25], color=RED_ORANGE, thickness=0.04)
        c_zline = Line3D([1.25, 1.25, 0], [1.25, 1.25, 1.25], color=PRIMARY_BLUE, thickness=0.04)
        
        self.play(Create(cube))
        
        ce_text = Tex(r"This theorem no longer applies.", font_size=36, color=RED_ORANGE).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(ce_text)
        self.play(Write(ce_text))
        
        self.play(FadeIn(c_pdot, scale=1.5))
        self.play(Create(c_xline), Create(c_yline), Create(c_zline))
        
        ce_eq = MathTex(r"r^2 = x^2 + y^2", r"+ z^2", font_size=34, color=GOLD).to_corner(DR, buff=0.5)
        ce_eq[1].set_color(RED_ORANGE)
        self.add_fixed_in_frame_mobjects(ce_eq)
        self.play(Write(ce_eq))
        
        self.play(Indicate(ce_eq[1], color=RED_ORANGE, scale_factor=1.5), Indicate(c_zline, color=RED_ORANGE, scale_factor=1.5))
        
        cross = Tex(r"$\times$", font_size=150, color=RED_ORANGE).center()
        self.add_fixed_in_frame_mobjects(cross)
        self.play(FadeIn(cross, scale=0.5))
        self.wait(2.0)
        
        self.play(FadeOut(VGroup(cube, c_pdot, c_xline, c_yline, c_zline)))
        self.play(FadeOut(ce_text), FadeOut(ce_eq), FadeOut(cross))
        self.remove(ce_text, ce_eq, cross)

        # ── Symmetry foreshadow ──
        ring_prev = Circle(radius=1.5, color=RING_COLOR, stroke_width=7)
        ring_prev.set_stroke(opacity=0.65)

        sym = VGroup(
            Tex(r"Ring has rotational symmetry about $z$:", font_size=24, color=LIGHT_GRAY),
            MathTex(r"I_x = I_y\;\Rightarrow\;2I_x = I_z\;\Rightarrow\;I_x = \frac{I_z}{2}",
                    font_size=30, color=GOLD),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(sym)

        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=1.5)
        self.play(Create(ring_prev))
        self.play(Write(sym))
        self.wait(2.0)

        self.play(FadeOut(ring_prev), FadeOut(sym),
                  FadeOut(x_ax), FadeOut(y_ax), FadeOut(z_ax),
                  FadeOut(xl), FadeOut(yl), FadeOut(zl))
        self.remove(sym, xl, yl, zl)


# ─────────────────────────────────────────────────────────────
#  SCENE 6 — RingCentralAxis
# ─────────────────────────────────────────────────────────────
class RingCentralAxis(ThreeDScene):
    """Derive I_z = MR² — the most elegant derivation in rotational mechanics."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)

        # ── Chapter card ──
        ch = VGroup(
            Tex("The Ring — Central Axis", font_size=48, color=GOLD),
            MathTex(r"I_z = ?", font_size=34, color=LIGHT_GRAY)
        ).arrange(DOWN, buff=0.4).center()
        self.add_fixed_in_frame_mobjects(ch)
        self.play(FadeIn(ch, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(ch))
        self.remove(ch)

        R = 2.0

        # ── Ring + z-axis ──
        ring = Circle(radius=R, color=RING_COLOR)
        ring.set_stroke(RING_COLOR, width=10)
        z_ax = Line3D([0, 0, -3], [0, 0, 3], color=AXIS_COLOR, thickness=0.04)
        z_lbl = MathTex("z", font_size=30, color=AXIS_COLOR).move_to([0, 0, 3.5])
        self.add_fixed_in_frame_mobjects(z_lbl)

        self.play(Create(ring), run_time=1.5, rate_func=smooth)
        self.play(Create(z_ax), Write(z_lbl))

        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()

        # ── Sweeping dm element ──
        theta = ValueTracker(0.0)

        dm_dot = always_redraw(lambda: Dot3D(
            [R * np.cos(theta.get_value()), R * np.sin(theta.get_value()), 0],
            color=MASS_ELEMENT_COLOR, radius=0.15
        ))
        r_seg = always_redraw(lambda: Line3D(
            [0, 0, 0],
            [R * np.cos(theta.get_value()), R * np.sin(theta.get_value()), 0],
            color=VECTOR_COLOR, thickness=0.03
        ))
        r_lbl_fix = MathTex("R", font_size=30, color=VECTOR_COLOR).move_to([0.7, 0.7, 0.3])
        self.add_fixed_in_frame_mobjects(r_lbl_fix)

        self.add(dm_dot, r_seg)
        self.play(theta.animate.set_value(TAU), run_time=3.0, rate_func=linear)

        obs = Tex(r"Every $dm$ is at constant distance $R$ from the $z$-axis",
                  font_size=26, color=GOLD).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(obs)
        self.play(Write(obs))
        self.wait(1.5)

        # ── Integral setup ──
        self.play(theta.animate.set_value(PI / 4), run_time=0.4)

        eq1 = MathTex(r"I_z", r"=", r"\int", r"r^2", r"\,dm", font_size=42)
        eq1.to_edge(RIGHT, buff=0.5).shift(UP * 2.5)
        self.add_fixed_in_frame_mobjects(eq1)
        self.play(Write(eq1))

        const_note = MathTex(r"r = R = \text{const for this ring}", font_size=28, color=GOLD)
        const_note.next_to(eq1, DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(const_note)
        self.play(Write(const_note))
        self.wait(0.7)

        # ── 3-step simplification ──
        eq2 = MathTex(r"I_z", r"=", r"\int", r"R^2", r"\,dm", font_size=42)
        eq2.move_to(eq1)
        self.add_fixed_in_frame_mobjects(eq2)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.0)
        self.wait(0.5)
        
        eq3 = MathTex(r"I_z", r"=", r"R^2", r"\int", r"\,dm", font_size=42)
        eq3.move_to(eq2)
        self.add_fixed_in_frame_mobjects(eq3)
        self.play(
            TransformMatchingTex(eq2, eq3),
            Indicate(eq3[2], color=GOLD, scale_factor=1.5),
            run_time=1.5
        )
        self.wait(0.5)
        
        eq4 = MathTex(r"I_z", r"=", r"R^2", r"M", font_size=42)
        eq4.move_to(eq3)
        self.add_fixed_in_frame_mobjects(eq4)
        self.play(TransformMatchingTex(eq3, eq4), run_time=1.0)
        self.wait(0.5)

        # ── Result box ──
        result = MathTex(r"I_z = MR^2", font_size=58, color=GOLD)
        res_box = SurroundingRectangle(result, color=GOLD, buff=0.3, corner_radius=0.12)
        res_grp = VGroup(res_box, result).center().shift(LEFT * 1.5)

        self.play(FadeOut(VGroup(eq4, const_note, obs, r_lbl_fix, dm_dot, r_seg)))
        self.remove(eq4, const_note, obs, r_lbl_fix)

        self.add_fixed_in_frame_mobjects(res_grp)
        self.play(Write(result), Create(res_box), run_time=1.5)
        self.wait(2.5)

        # ── Aha moment: ghost single particle ──
        aha = Tex(
            r"All mass already at $R$ — behaves like one particle $M$ at radius $R$.",
            font_size=25, color=LIGHT_GRAY
        ).to_edge(DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(aha)
        self.play(Write(aha))

        ghost = Dot3D([R, 0, 0], color=GOLD, radius=0.25)
        ghost_line = DashedLine([0,0,0], [R,0,0], color=GOLD, stroke_width=3, dash_length=0.12)
        g_lbl = MathTex(r"M\text{ at }R", font_size=24, color=GOLD).move_to([R+0.6, 0.5, 0])
        self.add_fixed_in_frame_mobjects(g_lbl)
        self.play(FadeIn(ghost, scale=2.0), Create(ghost_line), Write(g_lbl))
        self.wait(1.5)

        # ── R doubling → I quadrupling ──
        r_tr = ValueTracker(R)
        r_readout = always_redraw(lambda: Tex(
            f"$R={r_tr.get_value():.1f}$ → $I={r_tr.get_value()**2:.1f}M$",
            font_size=26, color=LIGHT_GRAY
        ).to_corner(DL, buff=0.5))
        self.add_fixed_in_frame_mobjects(r_readout)
        self.add(r_readout)
        self.play(r_tr.animate.set_value(2 * R), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(r_tr.animate.set_value(R), run_time=1.5, rate_func=smooth)
        self.wait(1.0)

        self.play(FadeOut(VGroup(
            res_grp, aha, ghost, ghost_line, g_lbl, r_readout,
            ring, z_ax, z_lbl
        )))
        self.remove(res_grp, aha, g_lbl, r_readout, z_lbl)


# ─────────────────────────────────────────────────────────────
#  SCENE 7 — RingAllAxes
# ─────────────────────────────────────────────────────────────
class RingAllAxes(ThreeDScene):
    """Synthesis: all four axes of a ring. Theorems as tools. Grand summary."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        R = 2.0

        # ── Chapter card ──
        ch = VGroup(
            Tex("One Ring, Four Axes", font_size=52, color=GOLD),
            Tex("Using our theorems as tools", font_size=28, color=LIGHT_GRAY)
        ).arrange(DOWN, buff=0.4).center()
        self.add_fixed_in_frame_mobjects(ch)
        self.play(FadeIn(ch, shift=UP * 0.3))
        self.wait(1.8)
        self.play(FadeOut(ch))
        self.remove(ch)

        # ── Part A: Ring + 4 axes ──
        ring = Circle(radius=R, color=RING_COLOR, stroke_width=10)
        z_ax   = Line3D([0, 0, -3],  [0, 0, 3],  color=RED_ORANGE,   thickness=0.04)
        x_ax   = Line3D([-3.5,0, 0], [3.5,0, 0], color=GREEN,        thickness=0.04)
        y_ax   = Line3D([0,-3.5, 0], [0,3.5, 0], color=PRIMARY_BLUE, thickness=0.04)
        t_ax   = Line3D([R, 0, -3],  [R, 0,  3], color=PURPLE,       thickness=0.04)

        zl = MathTex("z",        font_size=26, color=RED_ORANGE).move_to([0,   0,   3.5])
        xl = MathTex("x",        font_size=26, color=GREEN).move_to([3.8,  0,   0])
        yl = MathTex("y",        font_size=26, color=PRIMARY_BLUE).move_to([0,   3.8, 0])
        tl = Tex("tangent",      font_size=20, color=PURPLE).move_to([R+0.3, 0, 3.4])

        self.play(Create(ring))
        self.play(Create(z_ax), Create(x_ax), Create(y_ax), Create(t_ax))
        self.add_fixed_in_frame_mobjects(zl, xl, yl, tl)
        self.play(Write(zl), Write(xl), Write(yl), Write(tl))

        self.begin_ambient_camera_rotation(rate=0.04)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()

        # ────────────────────────────────────────────────────────
        # PART B — Axis 1: I_z = MR²
        # ────────────────────────────────────────────────────────
        b_ttl = Tex("Axis 1: Central $(z)$", font_size=28, color=RED_ORANGE).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(b_ttl)
        self.play(Write(b_ttl),
                  x_ax.animate.set_opacity(0.2), y_ax.animate.set_opacity(0.2),
                  t_ax.animate.set_opacity(0.2))

        iz = MathTex(r"I_z = MR^2", font_size=44, color=RED_ORANGE)
        iz_box = SurroundingRectangle(iz, color=RED_ORANGE, buff=0.2, corner_radius=0.08)
        iz_grp = VGroup(iz_box, iz).to_corner(UR, buff=0.4)
        self.add_fixed_in_frame_mobjects(iz_grp)
        self.play(
            Flash(iz.get_center(), color=RED_ORANGE, flash_radius=0.9, line_length=0.3),
            Write(iz), Create(iz_box)
        )
        self.wait(0.4)
        self.play(Rotate(ring, angle=TAU, axis=OUT, about_point=ORIGIN,
                         run_time=2.5, rate_func=linear))
        self.wait(0.4)
        self.play(x_ax.animate.set_opacity(1.0), y_ax.animate.set_opacity(1.0),
                  t_ax.animate.set_opacity(1.0),
                  FadeOut(b_ttl))
        self.remove(b_ttl)

        # ────────────────────────────────────────────────────────
        # PART C — Axis 2: I_x = MR²/2 via Perpendicular Axis Theorem
        # ────────────────────────────────────────────────────────
        c_ttl = Tex("Axis 2: Diameter $(x)$", font_size=28, color=GREEN).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(c_ttl)
        self.play(Write(c_ttl),
                  z_ax.animate.set_opacity(0.2), y_ax.animate.set_opacity(0.2),
                  t_ax.animate.set_opacity(0.2))

        qx = MathTex(r"I_x = ?", font_size=38, color=GREEN).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        self.add_fixed_in_frame_mobjects(qx)
        self.play(Write(qx))

        # Perpendicular Axis Theorem tool (slides in from left)
        pat = theorem_box("Perpendicular Axis Theorem", r"I_x + I_y = I_z",
                          title_color=PRIMARY_BLUE)
        pat.to_edge(LEFT, buff=0.3).shift(UP * 0.6 + LEFT * 6)
        self.add_fixed_in_frame_mobjects(pat)
        self.play(pat.animate.shift(RIGHT * 6), run_time=1.0, rate_func=smooth)
        self.wait(0.4)

        # Symmetry argument
        sym = VGroup(
            Tex(r"Ring is rotationally symmetric:", font_size=24, color=LIGHT_GRAY),
            MathTex(r"I_x = I_y\quad\text{(by symmetry)}", font_size=28, color=GOLD),
        ).arrange(DOWN, buff=0.28).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        self.add_fixed_in_frame_mobjects(sym)
        self.play(
            Rotate(ring, angle=PI / 2, axis=OUT, about_point=ORIGIN, run_time=1.0),
            Write(sym[0])
        )
        self.play(Write(sym[1]))
        self.wait(0.4)

        # Algebra
        alg_c = VGroup(
            MathTex(r"I_x + I_x = MR^2",    font_size=30),
            MathTex(r"2I_x = MR^2",          font_size=30),
            MathTex(r"I_x = \frac{MR^2}{2}", font_size=36, color=GREEN),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).next_to(sym, DOWN, buff=0.45)
        self.add_fixed_in_frame_mobjects(alg_c)
        for line in alg_c:
            self.play(Write(line), run_time=0.85)
            self.wait(0.25)

        ix_box2 = SurroundingRectangle(alg_c[-1], color=GREEN, buff=0.14, corner_radius=0.07)
        self.add_fixed_in_frame_mobjects(ix_box2)
        self.play(Create(ix_box2))
        self.wait(1.5)

        # Spin about x
        self.play(Rotate(ring, angle=TAU, axis=RIGHT, about_point=ORIGIN,
                         run_time=2.5, rate_func=linear))
        self.wait(0.6)

        # ── Intuition for I_x = MR^2 / 2 ──
        int_ttl = Tex("Intuition:", font_size=28, color=LIGHT_GRAY).to_edge(RIGHT, buff=2.0).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(int_ttl)
        self.play(Write(int_ttl))
        
        near_arcs = VGroup(
            Arc(radius=R, start_angle=-PI/4, angle=PI/2, color=PRIMARY_BLUE, stroke_width=10).set_z_index(1),
            Arc(radius=R, start_angle=3*PI/4, angle=PI/2, color=PRIMARY_BLUE, stroke_width=10).set_z_index(1)
        )
        far_arcs = VGroup(
            Arc(radius=R, start_angle=PI/4, angle=PI/2, color=GOLD, stroke_width=10).set_z_index(1),
            Arc(radius=R, start_angle=5*PI/4, angle=PI/2, color=GOLD, stroke_width=10).set_z_index(1)
        )
        self.play(Create(near_arcs), Create(far_arcs))
        
        lines_near = VGroup(*[Line3D([R*np.cos(th), R*np.sin(th), 0], [R*np.cos(th), 0, 0], color=PRIMARY_BLUE, thickness=0.02) for th in np.concatenate((np.linspace(-PI/4+0.1, PI/4-0.1, 8), np.linspace(3*PI/4+0.1, 5*PI/4-0.1, 8)))])
        lines_far = VGroup(*[Line3D([R*np.cos(th), R*np.sin(th), 0], [R*np.cos(th), 0, 0], color=GOLD, thickness=0.02) for th in np.concatenate((np.linspace(PI/4+0.1, 3*PI/4-0.1, 8), np.linspace(5*PI/4+0.1, 7*PI/4-0.1, 8)))])
        
        self.play(Create(lines_near), Create(lines_far))
        
        near_lbl = Tex("Small contribution", font_size=24, color=PRIMARY_BLUE).next_to(int_ttl, DOWN, buff=0.3).align_to(int_ttl, LEFT)
        far_lbl = Tex("Large contribution", font_size=24, color=GOLD).next_to(near_lbl, DOWN, buff=0.15).align_to(near_lbl, LEFT)
        
        self.add_fixed_in_frame_mobjects(near_lbl, far_lbl)
        self.play(Write(near_lbl), Write(far_lbl))
        self.wait(1.5)
        
        avg_lbl = Tex(r"Average $\rightarrow \frac{1}{2}MR^2$", font_size=26, color=WHITE).next_to(far_lbl, DOWN, buff=0.4).align_to(far_lbl, LEFT)
        self.add_fixed_in_frame_mobjects(avg_lbl)
        self.play(Write(avg_lbl))
        self.wait(2.0)
        
        self.play(FadeOut(VGroup(near_arcs, far_arcs, lines_near, lines_far, int_ttl, near_lbl, far_lbl, avg_lbl)))
        self.remove(int_ttl, near_lbl, far_lbl, avg_lbl)

        self.play(FadeOut(VGroup(pat, sym, alg_c, ix_box2, qx, c_ttl)),
                  z_ax.animate.set_opacity(1.0), y_ax.animate.set_opacity(1.0),
                  t_ax.animate.set_opacity(1.0))
        self.remove(pat, sym, alg_c, ix_box2, qx, c_ttl)

        # ────────────────────────────────────────────────────────
        # PART D — Axis 3: I_tangent = 2MR² via Parallel Axis Theorem
        # ────────────────────────────────────────────────────────
        d_ttl = Tex("Axis 3: Tangent (rim, $\\parallel z$)", font_size=28, color=PURPLE).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(d_ttl)
        self.play(Write(d_ttl),
                  z_ax.animate.set_opacity(0.2), x_ax.animate.set_opacity(0.2),
                  y_ax.animate.set_opacity(0.2))

        qt = MathTex(r"I_{\text{tan}} = ?", font_size=38, color=PURPLE).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        self.add_fixed_in_frame_mobjects(qt)
        self.play(Write(qt))

        # Parallel Axis Theorem tool (slides from right)
        pat2 = theorem_box("Parallel Axis Theorem", r"I = I_{\text{cm}} + Md^2",
                           title_color=GOLD)
        pat2.to_edge(RIGHT, buff=0.3).shift(UP * 0.4 + RIGHT * 8)
        self.add_fixed_in_frame_mobjects(pat2)
        self.play(pat2.animate.shift(LEFT * 8), run_time=1.0, rate_func=smooth)
        self.wait(0.4)

        # Identify terms
        id_lines = VGroup(
            MathTex(r"I_{\text{cm}} = I_z = MR^2", font_size=28, color=RED_ORANGE),
            MathTex(r"d = R\;\text{(tangent axis distance)}", font_size=26, color=GOLD),
        ).arrange(DOWN, buff=0.28).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
        self.add_fixed_in_frame_mobjects(id_lines)

        d_arrow3d = Arrow3D([0, 0, 1.5], [R, 0, 1.5], color=GOLD, thickness=0.04)
        d_lbl3d   = MathTex("d=R", font_size=24, color=GOLD).move_to([R/2, 0.4, 1.8])
        self.add_fixed_in_frame_mobjects(d_lbl3d)
        self.play(Create(d_arrow3d), Write(d_lbl3d), Write(id_lines))
        self.wait(0.5)

        alg_d = VGroup(
            MathTex(r"I_{\text{tan}} = MR^2 + M(R)^2", font_size=30),
            MathTex(r"= MR^2 + MR^2",                   font_size=30),
            MathTex(r"= 2MR^2",                          font_size=36, color=PURPLE),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).next_to(id_lines, DOWN, buff=0.45)
        self.add_fixed_in_frame_mobjects(alg_d)
        for line in alg_d:
            self.play(Write(line), run_time=0.85)
            self.wait(0.25)

        it_box2 = SurroundingRectangle(alg_d[-1], color=PURPLE, buff=0.14, corner_radius=0.07)
        self.add_fixed_in_frame_mobjects(it_box2)
        self.play(Create(it_box2))
        self.wait(1.5)

        # Three traced points rotating about tangent axis
        near_d = Dot3D([R, 0, 0], color=GREEN, radius=0.13)
        mid_d  = Dot3D([0, 0, 0], color=PRIMARY_BLUE, radius=0.13)
        far_d  = Dot3D([-R, 0, 0], color=RED_ORANGE, radius=0.13)
        
        lbl_0R = MathTex("0R", font_size=28, color=GREEN).next_to([R, 0.2, 0], UP)
        lbl_1R = MathTex("1R", font_size=28, color=PRIMARY_BLUE).next_to([0, 0.2, 0], UP)
        lbl_2R = MathTex("2R", font_size=28, color=RED_ORANGE).next_to([-R, 0.2, 0], UP)
        lbl_0R.rotate(PI/2, axis=RIGHT)
        lbl_1R.rotate(PI/2, axis=RIGHT)
        lbl_2R.rotate(PI/2, axis=RIGHT)
        # Using simple Text attached to the dots in 3D

        self.play(FadeIn(near_d, scale=1.5), FadeIn(mid_d, scale=1.5), FadeIn(far_d, scale=1.5))
        self.play(FadeIn(lbl_0R), FadeIn(lbl_1R), FadeIn(lbl_2R))

        near_tr = TracedPath(near_d.get_center, stroke_color=GREEN,        stroke_width=2, stroke_opacity=0.7)
        mid_tr  = TracedPath(mid_d.get_center,  stroke_color=PRIMARY_BLUE, stroke_width=2, stroke_opacity=0.7)
        far_tr  = TracedPath(far_d.get_center,  stroke_color=RED_ORANGE,   stroke_width=2, stroke_opacity=0.7)
        self.add(near_tr, mid_tr, far_tr)

        self.play(
            Rotate(VGroup(ring, near_d, mid_d, far_d, lbl_0R, lbl_1R, lbl_2R),
                   angle=TAU, axis=UP, about_point=[R, 0, 0],
                   run_time=3.5, rate_func=linear)
        )
        self.wait(0.5)

        self.play(FadeOut(VGroup(
            pat2, id_lines, alg_d, it_box2, d_arrow3d, d_lbl3d, qt, d_ttl,
            near_d, mid_d, far_d, near_tr, mid_tr, far_tr, lbl_0R, lbl_1R, lbl_2R
        )),
        z_ax.animate.set_opacity(1.0), x_ax.animate.set_opacity(1.0),
        y_ax.animate.set_opacity(1.0))
        self.remove(pat2, id_lines, alg_d, it_box2, d_lbl3d, qt, d_ttl)

        # ────────────────────────────────────────────────────────
        # PART E — Grand Summary Panel
        # ────────────────────────────────────────────────────────
        self.play(FadeOut(VGroup(ring, z_ax, x_ax, y_ax, t_ax, zl, xl, yl, tl, iz_grp)))
        self.remove(zl, xl, yl, tl, iz_grp)

        self.move_camera(phi=0, theta=-PI / 2, run_time=2.0)

        table = MobjectTable(
            [
                [Tex("Central"), MathTex(r"MR^2")],
                [Tex("Diameter"), MathTex(r"MR^2/2")],
                [Tex("Tangent"), MathTex(r"2MR^2")]
            ],
            col_labels=[Tex("Axis"), Tex("Formula")],
            line_config={"stroke_width": 1, "color": LIGHT_GRAY},
            arrange_in_grid_config={"cell_alignment": LEFT}
        ).scale(0.8).to_edge(UP, buff=0.6)
        
        self.add_fixed_in_frame_mobjects(table)
        
        self.play(Create(table.get_horizontal_lines()), Create(table.get_vertical_lines()))
        self.play(Write(table.get_rows()[0]))
        self.wait(0.5)
        
        for i in range(1, 4):
            self.play(FadeIn(table.get_rows()[i], shift=RIGHT * 0.2), run_time=0.8)
            self.wait(0.3)
            
        bars_grp = VGroup()
        bar_data = [("Central", 1.0, RED_ORANGE), ("Diameter", 0.5, GREEN), ("Tangent", 2.0, PURPLE)]
        
        for lbl, h, col in bar_data:
            b = Rectangle(width=0.8, height=h * 1.8, color=col, fill_opacity=0.8)
            l = Tex(lbl, font_size=28, color=col).next_to(b, DOWN, buff=0.2)
            bars_grp.add(VGroup(b, l))
            
        bars_grp.arrange(RIGHT, buff=2.0, aligned_edge=DOWN).to_edge(DOWN, buff=1.0)
        self.add_fixed_in_frame_mobjects(bars_grp)
        
        for bg in bars_grp:
            self.play(GrowFromEdge(bg[0], DOWN), FadeIn(bg[1]), run_time=0.6)
        self.wait(2.0)
        
        self.play(FadeOut(table), FadeOut(bars_grp))
        self.remove(table, bars_grp)
        
        quote = VGroup(
            Tex("The ring knows its own geometry.", font_size=36, color=WHITE),
            Tex("Change the axis.", font_size=36, color=GOLD),
            Tex("Change the physics.", font_size=36, color=GOLD),
            Tex("The mathematics is simply listening.", font_size=36, color=WHITE)
        ).arrange(DOWN, buff=0.5).center()
        self.add_fixed_in_frame_mobjects(quote)
        
        for line in quote:
            self.play(Write(line), run_time=1.2)
        self.wait(2.5)
        
        self.play(FadeOut(quote))
        self.remove(quote)
        
        final = MathTex(r"I = \int r^2\,dm", font_size=72)
        final[0].set_color(WHITE)
        self.add_fixed_in_frame_mobjects(final)
        self.play(Write(final), run_time=2.0)
        self.wait(3.0)
        self.play(FadeOut(final), run_time=2.0)
        self.remove(final)
