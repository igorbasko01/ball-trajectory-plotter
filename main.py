import math
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


def initial_velocity_from_angle(speed_kmh: float, i_angle: float, i_rpm: float) -> Tuple[float, float, float]:
    initial_velocity_ms = speed_kmh / 3.6
    angle_radians = math.radians(i_angle)
    i_v_x = initial_velocity_ms * math.cos(angle_radians)
    i_v_y = initial_velocity_ms * math.sin(angle_radians)

    # Calculate the angular velocity
    a_velocity = i_rpm * 2 * math.pi / 60
    return i_v_x, i_v_y, a_velocity


def plot_trajectory(i_v_x: float, i_v_y: float, h_0: float = 0.0, i_a_velocity: float = 0.0,
                    angle_deg: float = 0.0):
    g = 9.81
    court_length = 23.77
    net_height = 0.914
    net_distance = court_length / 2

    initial_speed_kmh = np.sqrt(i_v_x ** 2 + i_v_y ** 2) * 3.6

    t = np.linspace(0, 5, 1000)

    # Calculate positions
    x = v_x * t
    y = h_0 + v_y * t - 0.5 * g * t ** 2

    ground_index = np.argmax(y < 0)

    x = x[:ground_index]
    y = y[:ground_index]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Tennis Ball Trajectory')
    plt.ylim(0, 10)
    plt.xlim(0, 30)
    plt.grid(True)

    # Plot net
    plt.plot([net_distance, net_distance], [0, net_height], 'k-', linewidth=2)

    # Plot out
    plt.plot([court_length, court_length], [0, 0.1], 'k-', linewidth=2)

    plt.text(0.05, 0.95, f'Initial Speed: {initial_speed_kmh:.2f} km/h, ({i_v_x:.2f}, {i_v_y:.2f}) m/s, {rpm:.2f} RPM',
             transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top')
    plt.text(0.05, 0.90, f'Initial Angle: {angle_deg:.2f}', transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top')
    plt.show()


if __name__ == '__main__':
    angle = 6
    velocity_kmh = 100
    rpm = 0
    v_x, v_y, angular_velocity = initial_velocity_from_angle(velocity_kmh, angle, rpm)
    plot_trajectory(v_x, v_y, 1.0, angular_velocity, angle_deg=angle)
