import math

import numpy as np
from matplotlib import pyplot as plt


def initial_velocity_from_angle(speed_kmh: float, i_angle: float):
    initial_velocity_ms = speed_kmh / 3.6
    angle_radians = math.radians(i_angle)
    i_v_x = initial_velocity_ms * math.cos(angle_radians)
    i_v_y = initial_velocity_ms * math.sin(angle_radians)

    return i_v_x, i_v_y


def calculate_angle(i_v_x, i_v_y):
    angle_radians = math.atan2(i_v_y, i_v_x)  # Calculate the angle in radians
    angle_degrees = math.degrees(angle_radians)  # Convert the angle to degrees
    return angle_degrees


def plot_trajectory(plots: list):
    court_length = 23.77
    net_height = 0.914
    net_distance = court_length / 2

    plt.figure(figsize=(8, 6))

    for x, y, label in plots:
        plt.plot(x, y, label=label)

    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Tennis Ball Trajectory')
    plt.ylim(0, 10)
    plt.xlim(0, 30)
    plt.legend()
    plt.grid(True)

    # Plot net
    plt.plot([net_distance, net_distance], [0, net_height], 'k-', linewidth=2)

    # Plot out
    plt.plot([court_length, court_length], [0, 0.1], 'k-', linewidth=2)

    plt.show()


def create_sensor_to_ms_func(sensor_value_max: int, kmh_value_max: float):
    ms_value_max = kmh_value_max / 3.6

    def sensor_to_ms(sensor_value: int) -> float:
        return sensor_value / sensor_value_max * ms_value_max

    return sensor_to_ms


def initial_velocity_from_sensors(x_sensor: int, y_sensor: int):
    return x_sensor_to_ms(x_sensor), y_sensor_to_ms(y_sensor)


def rpm_to_rads_s(rpm: float):
    return rpm * 2 * np.pi / 60


def calculate_trajectory(i_v_x: float, i_v_y: float, h_0: float = 0.0, rads_s: float = 0.0):
    g = 9.81
    rho = 1.225  # air density, kg/m^3
    radius = 0.0335  # tennis ball radius, m
    A = np.pi * radius ** 2  # cross-sectional area of the ball, m^2
    C_l = 0.2  # lift coefficient

    initial_speed_kmh = np.sqrt(i_v_x ** 2 + i_v_y ** 2) * 3.6
    angle_deg = calculate_angle(i_v_x, i_v_y)
    rpm = rads_s * 60 / (2 * np.pi)

    t = np.linspace(0, 5, 1000)

    # Initial conditions
    omega_z = rads_s  # angular velocity, rad/s

    # Calculate positions
    x = i_v_x * t

    # Incorporate Magnus effect
    # Define velocity at each time step
    v_x = i_v_x * np.ones_like(t)
    v_y = i_v_y - g * t

    # Calculate Magnus force per unit mass at each timestamp
    # Magnus force F_m = rho * A * C_l * |v| * omega
    v_mag = np.sqrt(v_x ** 2 + v_y ** 2)
    F_m_y = rho * A * C_l * v_mag * omega_z

    # New acceleration in y due to Magnus effect
    a_y = g + F_m_y

    # Integrate to find new y position
    y = h_0 + i_v_y * t - 0.5 * a_y * t ** 2

    ground_index = np.argmax(y < 0)

    x = x[:ground_index]
    y = y[:ground_index]

    label = f'{initial_speed_kmh:.2f} km/h, ({i_v_x:.2f}, {i_v_y:.2f}) m/s, {angle_deg:.2f}°, {rpm:.2f} rpm'

    return x, y, label


y_sensor_to_ms = create_sensor_to_ms_func(10000, 30)
x_sensor_to_ms = create_sensor_to_ms_func(10000, 144)


def main():
    """
    This application calculates and plots a trajectory of a tennis ball.
    It is possible to create multiple trajectories with different initial conditions.
    All the trajectories can be plotted on the same graph.

    The initial velocities could be calculated from sensors readings. The x-axis is the z-axis in Unity.
    To calculate the initial velocity from sensors, the following function is used:
    initial_velocity_from_sensors. This method returns the initial velocity in x and y directions in m/s.

    It is also possible to calculate the trajectory with a given initial velocity in km/h and angle.
    The function initial_velocity_from_angle is used for this purpose.
    It returns the initial velocity in x and y directions in m/s.

    h_0 is the initial height of the ball in meters.

    rads_s is the angular velocity of the ball in radians per second.
    The rpm_to_rads_s function is used to convert rpm to radians per second.
    """
    plots = [
        calculate_trajectory(
            *initial_velocity_from_sensors(4534, 4678),
            h_0=1.0, rads_s=rpm_to_rads_s(1085)),
        calculate_trajectory(
            *initial_velocity_from_sensors(4534, 4678),
            h_0=1.0, rads_s=rpm_to_rads_s(0))
    ]

    plot_trajectory(plots)


if __name__ == '__main__':
    main()
