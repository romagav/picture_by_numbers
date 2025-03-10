from PIL import Image
import numpy as np


BASIC_COLORS = {
    (0, 0, 0): '1',       # Черный - 1
    (255, 255, 255): '2',  # Белый - 2
    (255, 0, 0): '3',     # Красный - 3
    (0, 255, 0): '4',     # Зеленый - 4
    (0, 0, 255): '5',     # Синий - 5
    (255, 255, 0): '6',   # Желтый - 6
    (0, 255, 255): '7',   # Голубой - 7
    (255, 0, 255): '8',   # Пурпурный - 8
    (128, 0, 0): '9',     # Темно-красный - 9
    (0, 128, 0): '10',     # Темно-зеленый - 10
    (0, 0, 128): '11',     # Темно-синий - 11
    (128, 128, 0): '12',   # Оливковый - 12
    (128, 0, 128): '13',   # Фиолетовый - 13
    (0, 128, 128): '14',   # Темно-голубой - 14
    (192, 192, 192): '15',  # Серебряный - 15
    (128, 128, 128): '16'  # Серый - 16
}


def split_image(image_path, rows, cols):
    # Открываем изображение
    image = Image.open(image_path)
    width, height = image.size

    # Вычисляем размер каждой части
    part_width = width // cols
    part_height = height // rows

    # Список для хранения частей изображения
    parts = []

    # Разделяем изображение на части
    for i in range(rows):
        for j in range(cols):
            left = j * part_width
            upper = i * part_height
            right = (j + 1) * part_width
            lower = (i + 1) * part_height

            # Обрезаем изображение
            part = image.crop((left, upper, right, lower))
            parts.append(part)

    return parts


def get_average_color(image_part):
    # Преобразуем изображение в массив numpy
    np_image = np.array(image_part)

    # Вычисляем среднее значение по каждому каналу (R, G, B)
    average_color = np.mean(np_image, axis=(0, 1)).astype(int)
    return tuple(average_color)


def find_closest_color(color):
    # Находим ближайший цвет из списка BASIC_COLORS
    min_distance = float('inf')
    closest_color = None

    for basic_color in BASIC_COLORS:
        # Вычисляем евклидово расстояние между цветами
        distance = np.sqrt(
            (color[0] - basic_color[0]) ** 2 +
            (color[1] - basic_color[1]) ** 2 +
            (color[2] - basic_color[2]) ** 2
        )

        # Если расстояние меньше минимального, обновляем ближайший цвет
        if distance < min_distance:
            min_distance = distance
            closest_color = basic_color
    return BASIC_COLORS[closest_color]


def get_average_colors(image_path, rows, cols):
    parts = split_image(image_path, rows, cols)

    average_colors = []

    for part in parts:
        avg_color = get_average_color(part)
        closest_color = find_closest_color(avg_color)
        average_colors.append(closest_color)

    return average_colors


def result(image_path, colors, number_of_parts):
    image = Image.open(image_path)
    width, height = image.size
    new_image = Image.new('RGB', (width, height), (0, 0, 0))
    for i in range(number_of_parts):
        img = Image.open(f"kartinka_po_nomeram/{colors[i]}.jpg")
        n = int(number_of_parts ** 0.5)
        w = width // n
        h = height // n

        new_image.paste(img.resize((w, h)), (((i % n) * w, (i // n) * h)))
    new_image.save("kartinka_po_nomeram/result.jpg")
    return new_image


image_path = ('kartinka_po_nomeram/test.jpg')
rows = 15
cols = 15
result(image_path, get_average_colors(image_path, rows, cols), rows * cols)
#  for i in split_image(image_path, rows, cols):
#      i.show()
#  print(get_average_colors(image_path, rows, cols))
