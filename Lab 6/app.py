import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Вершины буквы "M" в 3D
vertices = np.array([
    [1,1,1],  # точка A (0, 0, 0) - нижняя левая   0
    [1,2,1],  # точка B (0, 1, 0) - верхняя левая    1
    [2,2,1],  # точка C (1, 0, 0) - центральная нижняя  2
    [2,1,1],  # точка D (1, 1, 0) - центральная верхняя   3
    [1,1,4],  # точка A (0, 0, 0) - нижняя левая   4
    [1,2,4],  # точка B (0, 1, 0) - верхняя левая   5
    [2,2,4],  # точка C (1, 0, 0) - центральная нижняя   6
    [2,1,4],  # точка D (1, 1, 0) - центральная верхняя    7

    [3,1,3.5],          #8
    [3,2,3.5],           #9
    [3,1,2.8],         #10
    [3,2,2.8],           #11
    [2,2,3.3],          #12
    [2,1,3.3],            #13

    [4,1,1],  # точка A (0, 0, 0) - нижняя левая   14
    [4,2,1],  # точка B (0, 1, 0) - верхняя левая    15
    [5,2,1],  # точка C (1, 0, 0) - центральная нижняя  16
    [5,1,1],  # точка D (1, 1, 0) - центральная верхняя   17
    [4,1,4],  # точка A (0, 0, 0) - нижняя левая   18
    [4,2,4],  # точка B (0, 1, 0) - верхняя левая   19
    [5,2,4],  # точка C (1, 0, 0) - центральная нижняя   20
    [5,1,4],  # точка D (1, 1, 0) - центральная верхняя    21

    [4,1,2.8], #22
    [4,2,2.8], #23
    #[2, 0, 0],  # точка E (2, 0, 0) - нижняя правая
    #[2, 1, 0],  # точка F (2, 1, 0) - верхняя правая
    #[1, 0, 1],  # точка G (1, 0, 1) - нижняя центральная сдвинута по оси Z
    #[1, 1, 1],  # точка H (1, 1, 1) - верхняя центральная сдвинута по оси Z
])

# Рёбра, соединяющие вершины
edges = [
    (0, 1),  # A -> B
    (1, 2),  # E -> F
    (2, 3),  # B -> H
    (0, 3),  # C -> G
    (4,5),
    (5,6),
    (6,7),
    (4,7),
    (0,4),
    (1,5),
    (2,6),
    (3,7),

    (8,9),
    (8,7),
    (9,6),
    (12,13),
    (12,11),
    (13,10),
    (10,11),
    (10,8),
    (11,9),

    (14,15),
    (15,16),
    (16,17),
    (14,17),
    (18,19),
    (19,20),
    (20,21),
    (18,21),
    (14,18),
    (15,19),
    (16,20),
    (17,21),

    (11,23),
    (10,22),
    (8,18),
    (9,19),

    #(3, 6),  # D -> G
    #(2, 7),  # C -> H
    #(3, 5),  # D -> F
]

# Функция вращения
def rotate(vertices, angle, axis):
    """Вращение объекта вокруг оси (x, y, z) на угол angle"""
    angle = np.radians(angle)  # преобразуем угол в радианы
    if axis == 'x':
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ])
    elif axis == 'y':
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
    elif axis == 'z':
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
    return np.dot(vertices, rotation_matrix.T)

# Функция для рисования объекта
def plot_3d_object(vertices, edges, ax):
    """Отображение 3D объекта"""
    ax.clear()  # Очистить текущую ось

    # Рисуем рёбра
    for edge in edges:
        ax.plot([vertices[edge[0]][0], vertices[edge[1]][0]],
                [vertices[edge[0]][1], vertices[edge[1]][1]],
                [vertices[edge[0]][2], vertices[edge[1]][2]], color='r')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Letter M')
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])

# Настройка анимации
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Функция для анимации вращения
def update(frame):
    rotated_vertices = rotate(vertices, frame, axis='y')  # Вращение на угол "frame" вокруг оси Y
    plot_3d_object(rotated_vertices, edges, ax)

# Анимация вращения объекта
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1), interval=50)

plt.show()
