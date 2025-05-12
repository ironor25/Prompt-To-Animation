
import numpy as np
from manim import *

class ProjectileMotion(Scene):
    def construct(self):
        g = 9.81
        v0 = 10
        theta = 60 * DEGREES
        t_total = 2 * v0 * np.sin(theta) / g

        axes = Axes(
            x_range=[0, v0 * np.cos(theta) * t_total * 1.1, 1],
            y_range=[0, v0**2 * np.sin(theta)**2 / (2 * g) * 1.1, 1],
            axis_config={"include_tip": False},
        )
        self.add(axes)

        ball = Dot(color=BLUE)
        ball.move_to(axes.c2p(0, 0))
        self.add(ball)

        def get_position(t):
            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2
            return axes.c2p(x, y)

        trajectory = ParametricFunction(
            lambda t: axes.c2p(v0 * np.cos(theta) * t, v0 * np.sin(theta) * t - 0.5 * g * t**2),
            t_range=[0, t_total],
            color=GREEN
        )
        self.add(trajectory)

        v_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([v0 * np.cos(theta)/5, v0 * np.sin(theta)/5, 0]), color=YELLOW)
        v_label = MathTex(r"\vec{v}", color=YELLOW).next_to(v_vector, UP)
        self.add(v_vector, v_label)

        v_x_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([v0 * np.cos(theta)/5, 0, 0]), color=RED)
        v_x_label = MathTex(r"v_x", color=RED).next_to(v_x_vector, DOWN)
        self.add(v_x_vector, v_x_label)

        v_y_vector = Arrow(start=ball.get_center(), end=ball.get_center() + np.array([0, v0 * np.sin(theta)/5, 0]), color=PURPLE)
        v_y_label = MathTex(r"v_y", color=PURPLE).next_to(v_y_vector, LEFT)
        self.add(v_y_vector, v_y_label)

        def update_position(mob, alpha):
            t = alpha * t_total
            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2
            mob.move_to(axes.c2p(x, y))

            v_x = v0 * np.cos(theta)
            v_y = v0 * np.sin(theta) - g * t

            v_vector.become(Arrow(start=axes.c2p(x,y), end=axes.c2p(x,y) + np.array([v_x/5, v_y/5, 0]), color=YELLOW))
            v_x_vector.become(Arrow(start=axes.c2p(x,y), end=axes.c2p(x,y) + np.array([v_x/5, 0, 0]), color=RED))
            v_y_vector.become(Arrow(start=axes.c2p(x,y), end=axes.c2p(x,y) + np.array([0, v_y/5, 0]), color=PURPLE))
            v_label.next_to(v_vector, UP)
            v_x_label.next_to(v_x_vector, DOWN)
            v_y_label.next_to(v_y_vector, LEFT)

        self.play(UpdateFromAlphaFunc(ball, update_position), run_time=5, rate_func=linear)
        self.wait(1)
