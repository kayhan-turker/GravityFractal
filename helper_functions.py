from pyglet import shapes


def extend_with_rectangle_border(shape_list, x, y, width, height, border, clr, batch):
    shape_list.extend([shapes.Rectangle(x, y, width, border, color=clr, batch=batch)])
    shape_list.extend([shapes.Rectangle(x, y, border, height, color=clr, batch=batch)])
    shape_list.extend([shapes.Rectangle(x, y + height, width, -border, color=clr, batch=batch)])
    shape_list.extend([shapes.Rectangle(x + width, y, -border, height, color=clr, batch=batch)])

def set_rectangle_border_pos(shape_list, index, x, y):
    dx = x - shape_list[index].x
    dy = y - shape_list[index].y

    shape_list[index].x += dx
    shape_list[index + 1].x += dx
    shape_list[index + 2].x += dx
    shape_list[index + 3].x += dx

    shape_list[index].y += dy
    shape_list[index + 1].y += dy
    shape_list[index + 2].y += dy
    shape_list[index + 3].y += dy
