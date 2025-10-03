from manim import *
import numpy as np
from scipy.integrate import solve_ivp

def coupled_oscillators(t, y, m, k1, k2):
    x1, v1, x2, v2 = y
    dx1dt = v1
    dx2dt = v2
    dv1dt = -(k1/m)*x1 + (k2/m)*(x2 - x1)
    dv2dt = -(k1/m)*x2 + (k2/m)*(x1 - x2)
    return [dx1dt, dv1dt, dx2dt, dv2dt]

class CoupledOscillatorGraph(Scene):
    def construct(self):
        # Initial conditions
        x1_initial = 1.75
        x2_initial = 0.0
        y0 = [x1_initial, 0.0, x2_initial, 0.0]
        m = 1
        k1 = 10.0
        k2 = 8.0
        t_span = (0,60)
        t_eval = np.linspace(*t_span, 1000)
        sol = solve_ivp(coupled_oscillators, t_span, y0, args=(m, k1, k2), t_eval=t_eval)
        t = sol.t
        x1 = sol.y[0]
        x2 = sol.y[2]

        axes = Axes(
        x_range=[0, 60, 5],
        y_range=[-3, 3, 0.5],
        x_length=10, y_length=5,
        axis_config={"color": "#DDDDDD", "stroke_width": 3, "include_tip": False}
        )
        axes.set(width=config.frame_width)
        axes.add_coordinates()

        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("x")
        self.add(axes, x_label, y_label)

        # Main animated curves
        graph1 = axes.plot(lambda s: np.interp(s, t, x1), color='#0099DD',stroke_width=5, x_range=[0, 60])
        graph2 = axes.plot(lambda s: np.interp(s, t, x2), color='#FF7043',stroke_width=5, x_range=[0, 60])

        # Legend
        legend = VGroup(
            Dot(color='#0099DD').scale(1.1),
            Text("Mass 1", color='#0099DD', font_size=28),
            Dot(color='#FF7043').scale(1.1),
            Text("Mass 2", color='#FF7043', font_size=28)
        ).arrange(RIGHT, buff=0.3).to_corner(UR, buff=0.7)

        # Animated tip dots
        tip_dot1 = Dot(color='#0099DD').scale(1.2)
        tip_dot2 = Dot(color='#FF7043').scale(1.2)
        tip_dot1.move_to(axes.c2p(t[0], x1[0]))
        tip_dot2.move_to(axes.c2p(t[0], x2[0]))

        def update_dot(mob, alpha, arr):
            i = int(alpha * (len(t) - 1))
            mob.move_to(axes.c2p(t[i], arr[i]))

        # Add everything
        self.add(tip_dot1, tip_dot2, legend)
        self.play(
            Create(graph1, rate_func=linear),
            Create(graph2, rate_func=linear),
            UpdateFromAlphaFunc(tip_dot1, lambda mob, alpha: update_dot(mob, alpha, x1), run_time=30, rate_func=linear),
            UpdateFromAlphaFunc(tip_dot2, lambda mob, alpha: update_dot(mob, alpha, x2), run_time=30, rate_func=linear),
            run_time=30
        )
        self.wait(2)
