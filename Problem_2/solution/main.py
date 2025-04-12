import numpy as np
import matplotlib.pyplot as plt

# Параметры Земли
R_earth = 6371.302 # Радиус Земли в км
mu = 398600.4415 # Гравитационный параметр Земли, км^3/с^2
omega_earth = 2 * np.pi / (24 * 3600)  # Угловая скорость вращения Земли, рад/с

# Параметры орбиты
h = 561.0873263  # Высота орбиты в км
r_orbit = R_earth + h
i = np.radians(98)  # Наклонение орбиты (например, 45°)

# Время
T_orbit = 2 * np.pi * np.sqrt(r_orbit ** 3 / mu) # Период обращения спутника
num_orbits = 5  # Сколько орбит рисовать
num_points_per_orbit = 500  # Точек на одну орбиту
t = np.linspace(0, num_orbits * T_orbit, num_orbits * num_points_per_orbit)

# Угловая скорость спутника
omega_sat = 2 * np.pi / T_orbit


# Вычисляем широту и долготу спутника
def groundtrack(t):
    # Положение спутника в инерциальной системе
    nu = omega_sat * t  # Истинная аномалия (меняется равномерно)

    x = r_orbit * np.cos(nu)
    y = r_orbit * np.sin(nu) * np.cos(i)
    z = r_orbit * np.sin(nu) * np.sin(i)

    # Переход в сферические координаты
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    lat = np.arcsin(z / r)  # Широта

    # Долгота в инерциальной системе
    lon_inertial = np.arctan2(y, x)

    # Исправление долготы на вращение Земли
    lon = lon_inertial - omega_earth * t

    # Приводим долготу в диапазон [-180, 180]
    lon = np.degrees(lon)
    lon = (lon + 180) % 360 - 180
    lat = np.degrees(lat)

    return lon, lat


# Строим граундтрек
lon, lat = groundtrack(t)

plt.figure(figsize=(12, 6))
plt.plot(lon, lat, 'r', linewidth=1)
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.title('Граундтрек спутника')
plt.xlabel('Долгота [°]')
plt.ylabel('Широта [°]')
plt.grid(True)
plt.show()

