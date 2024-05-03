from typing import List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import Button
from palettable.cartocolors.qualitative import Bold_10


def arrange_in_circle(n_agents: int, radius: float) -> np.ndarray:
    thetas = np.linspace(0, 2 * np.pi, n_agents, endpoint=False)
    return np.array([np.cos(thetas), np.sin(thetas)]).T


def get_random_partners(n_agents: int) -> np.ndarray:
    partners = []
    for i in range(n_agents):
        possible_partners = np.array([j for j in range(n_agents) if j != i])
        partners.append(np.random.choice(possible_partners, 2, replace=False))
    return np.array(partners)


def isosceles_triangle_agent_offset(
    agent: np.ndarray,
    reference_1: np.ndarray,
    reference_2: np.ndarray,
) -> np.ndarray:
    a_r1 = reference_1 - agent
    r1_r2 = reference_2 - reference_1

    proj = np.dot(a_r1, r1_r2) / np.dot(r1_r2, r1_r2) * r1_r2
    vec = (proj + 0.5) * r1_r2

    return vec


def plot_target_triangle_interactive(
    fixed_vertices: np.ndarray = None,
    initial_movable_vertex: np.ndarray = None,
    x_lim: float = 5,
    y_lim: float = 5,
) -> None:
    fixed_vertices = fixed_vertices or np.array([[0, 0], [1, 0]])
    initial_movable_vertex = initial_movable_vertex or np.array([1, 1])

    fig, ax = plt.subplots()
    ax.set_xlim(-x_lim, x_lim)
    ax.set_ylim(-y_lim, y_lim)

    line_points_current = np.vstack(
        [fixed_vertices, initial_movable_vertex, fixed_vertices[0]]
    )
    ax.plot(line_points_current[:, 0], line_points_current[:, 1], "o-")

    offset_vector = isosceles_triangle_agent_offset(
        initial_movable_vertex,
        fixed_vertices[0],
        fixed_vertices[1],
    )
    line_points_offset = np.vstack(
        [fixed_vertices, initial_movable_vertex + offset_vector, fixed_vertices[0]]
    )
    ax.plot(line_points_offset[:, 0], line_points_offset[:, 1], "o-")

    def on_click(event):
        if event.button == MouseButton.LEFT:
            x = event.xdata
            y = event.ydata
            line_points_current = np.vstack([fixed_vertices, [x, y], fixed_vertices[0]])
            ax.lines[0].set_xdata(line_points_current[:, 0])
            ax.lines[0].set_ydata(line_points_current[:, 1])

            offset_vector = isosceles_triangle_agent_offset(
                np.array([x, y]),
                fixed_vertices[0],
                fixed_vertices[1],
            )
            line_points_offset = np.vstack(
                [fixed_vertices, [x, y] + offset_vector, fixed_vertices[0]]
            )
            ax.lines[1].set_xdata(line_points_offset[:, 0])
            ax.lines[1].set_ydata(line_points_offset[:, 1])

            plt.draw()

    fig.canvas.mpl_connect("button_press_event", on_click)

    plt.show()


def record_agent_positions(
    agents: np.ndarray,
    partners: np.ndarray,
    n_steps: int = 100,
    movement_per_step: float = 0.1,
) -> List[np.ndarray]:

    agents_over_time = [agents.copy()]

    for _ in range(n_steps):
        moved_agents = agents.copy()
        for i, (partner_1, partner_2) in enumerate(partners):
            agent = agents[i]
            partner_1 = agents[partner_1]
            partner_2 = agents[partner_2]
            agent_offset = isosceles_triangle_agent_offset(agent, partner_1, partner_2)
            moved_agents[i] = agent + movement_per_step * agent_offset / np.linalg.norm(
                agent_offset
            )

        agents = moved_agents
        agents_over_time.append(agents.copy())

    return agents_over_time


def plot_iteration(ax, current_agents, partners):
    for i, (partner_1, partner_2) in enumerate(partners):
        agent = current_agents[i]
        partner_1 = current_agents[partner_1]
        partner_2 = current_agents[partner_2]

        color = Bold_10.mpl_colors[i % Bold_10.number]
        ax.scatter(agent[0], agent[1], color=color)
        triangle_line_current = np.vstack([agent, partner_1, partner_2, agent])
        ax.plot(
            triangle_line_current[:, 0],
            triangle_line_current[:, 1],
            color=color,
            linestyle="--",
        )


if __name__ == "__main__":
    N_AGENTS = 10
    RADIUS = 5.0
    N_STEPS = 100
    MOVEMENT_PER_STEP = 0.1

    agents = arrange_in_circle(N_AGENTS, RADIUS)
    partners = get_random_partners(N_AGENTS)

    agents_over_time = record_agent_positions(
        agents, partners, n_steps=N_STEPS, movement_per_step=MOVEMENT_PER_STEP
    )

    print(agents_over_time[15])

    # fig, ax = plt.subplots(figsize=(6, 6))
    # plot_iteration(ax, agents_over_time[0], partners)
    # plt.show()

    # # fig, ax = plt.subplots(figsize=(6, 6))
    # button_prev = Button(plt.axes([0.4, 0.01, 0.09, 0.04]), "Previous")
    # button_next = Button(plt.axes([0.51, 0.01, 0.09, 0.04]), "Next")

    # # ax.set_xlim(-RADIUS, RADIUS)
    # # ax.set_ylim(-RADIUS, RADIUS)

    # # i = 0
    # # ax.plot(agents_over_time[0][:, 0], agents_over_time[0][:, 1], "o")

    # def on_next():
    #     i = min(i + 1, N_STEPS)
    #     ax.lines[0].set_xdata(agents_over_time[i][:, 0])
    #     ax.lines[0].set_ydata(agents_over_time[i][:, 1])
    #     plt.draw()

    # # # def on_click(event):
    # # plt.show()
