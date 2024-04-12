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


def plot_trajectory(i_v_x: float, i_v_y: float, h_0: float = 0.0, rads_s: float = 0.0):
    g = 9.81
    court_length = 23.77
    net_height = 0.914
    net_distance = court_length / 2
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


def create_sensor_to_ms_func(sensor_value_max: int, kmh_value_max: float):
    ms_value_max = kmh_value_max / 3.6

    def sensor_to_ms(sensor_value: int) -> float:
        return sensor_value / sensor_value_max * ms_value_max

    return sensor_to_ms


y_sensor_to_ms = create_sensor_to_ms_func(10000, 30)
x_sensor_to_ms = create_sensor_to_ms_func(10000, 144)


def initial_velocity_from_sensors(x_sensor: int, y_sensor: int):
    return x_sensor_to_ms(x_sensor), y_sensor_to_ms(y_sensor)


def rpm_to_rads_s(rpm: float):
    return rpm * 2 * np.pi / 60


def main():
    angle = 45
    velocity_kmh = 30
    v_x, v_y = initial_velocity_from_angle(velocity_kmh, angle)
    v_x, v_y = initial_velocity_from_sensors(4534, 4678)
    rads_s = rpm_to_rads_s(100)
    plot_trajectory(v_x, v_y, 1.0, rads_s)
    # plot_trajectory(16.3, 16.3, 1.0)


if __name__ == '__main__':
    main()
