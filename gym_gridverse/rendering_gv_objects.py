import pygame
import math
import numpy as np

RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180


def create_wall(surface, obj_position, window_scaling):
    # Create brick background
    brick_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(184, 110, 94), points=brick_background_coords
    )

    # Create horizontal lines
    line_width = int(window_scaling / 25)
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + (2 / 3) * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + (2 / 3) * window_scaling,
        ),
        width=line_width,
    )
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + (1 / 3) * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + (1 / 3) * window_scaling,
        ),
        width=line_width,
    )

    # Create vertical lines
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling + (1 / 4) * window_scaling,
            obj_position[1] * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + (1 / 4) * window_scaling,
            obj_position[1] * window_scaling + (1 / 3) * window_scaling,
        ),
        width=line_width,
    )
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling + (3 / 4) * window_scaling,
            obj_position[1] * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + (3 / 4) * window_scaling,
            obj_position[1] * window_scaling + (1 / 3) * window_scaling,
        ),
        width=line_width,
    )
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling + (1 / 4) * window_scaling,
            obj_position[1] * window_scaling + (2 / 3) * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + (1 / 4) * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        width=line_width,
    )
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling + (3 / 4) * window_scaling,
            obj_position[1] * window_scaling + (2 / 3) * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + (3 / 4) * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        width=line_width,
    )
    pygame.draw.line(
        surface=surface,
        color=(0, 0, 0),
        start_pos=(
            obj_position[0] * window_scaling + (0.5) * window_scaling,
            obj_position[1] * window_scaling + (1 / 3) * window_scaling,
        ),
        end_pos=(
            obj_position[0] * window_scaling + (0.5) * window_scaling,
            obj_position[1] * window_scaling + (2 / 3) * window_scaling,
        ),
        width=line_width,
    )


def create_hidden(surface, obj_position, window_scaling):
    # Create hidden object background
    hidden_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=hidden_background_coords
    )


def create_floor(surface, obj_position, window_scaling):
    # Create floor object background
    floor_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=floor_background_coords
    )


def create_key(surface, obj_position, window_scaling):
    # Create floor background
    floor_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=floor_background_coords
    )
    circle_center_coords = (
        obj_position[0] * window_scaling + 0.3 * window_scaling,
        obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
    )
    pygame.draw.circle(
        surface=surface,
        color=(255, 235, 138),
        center=circle_center_coords,
        radius=0.2 * window_scaling,
    )
    stem_filled_coords = [
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.42) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.58) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.58) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.42) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(255, 235, 138), points=stem_filled_coords
    )
    end_filled_coords = [
        (
            obj_position[0] * window_scaling + 0.7 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.7 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.7) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.7) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(255, 235, 138), points=end_filled_coords
    )


def draw_polygon_alpha(surface, color, points):
    # Taken from https://stackoverflow.com/a/64630102/6619979
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(
        shape_surf, color, [(x - min_x, y - min_y) for x, y in points]
    )
    surface.blit(shape_surf, target_rect)


def create_agent(
    surface, obj_position, obj_orientation, obj_scaling, window_scaling
):
    agent_coords = [
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.5 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
    ]

    # Transform vertices for rotation prep
    rotate_around = (
        obj_position[0] * window_scaling + 0.5 * window_scaling,
        obj_position[1] * window_scaling + 0.5 * window_scaling,
    )
    vertices = np.array(agent_coords)
    rotation_point = np.array(rotate_around)
    vertices = vertices - rotation_point

    # Calculate transformation matrices
    scale_matrix = np.array([[obj_scaling[0], 0], [0, obj_scaling[1]]])
    rotation_matrix = np.array(
        [
            [
                math.cos(DEG2RAD * obj_orientation),
                -math.sin(DEG2RAD * obj_orientation),
            ],
            [
                math.sin(DEG2RAD * obj_orientation),
                math.cos(DEG2RAD * obj_orientation),
            ],
        ]
    )

    # Apply transforms
    vertices = scale_matrix @ vertices.T
    vertices = rotation_matrix @ vertices
    vertices = vertices.T + rotation_point
    vertices = list(map(tuple, vertices))

    draw_polygon_alpha(
        surface=surface, color=(51, 85, 119, 200), points=vertices
    )

    # pygame.draw.polygon(
    #     surface=surface,
    #     color=(51, 85, 119),
    #     points=vertices,
    #     width=int(window_scaling / 15),
    # )


def create_door_open(surface, obj_position, window_scaling):
    outer_door_coords = [
        (obj_position[0] * window_scaling, obj_position[1] * window_scaling),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(255, 235, 138), points=outer_door_coords
    )
    inner_door_coords = [
        (
            obj_position[0] * window_scaling + 0.10 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.10) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.10 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.90) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.90 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.90) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.90 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.10) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=inner_door_coords
    )
    pygame.draw.polygon(
        surface=surface,
        color=(0, 0, 0),
        points=inner_door_coords,
        width=int(window_scaling / 25),
    )


def create_door_closed_locked(surface, obj_position, window_scaling):
    outer_door_coords = [
        (obj_position[0] * window_scaling, obj_position[1] * window_scaling),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(255, 235, 138), points=outer_door_coords
    )

    door_border_coords = [
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface,
        color=(0, 0, 0),
        points=door_border_coords,
        width=int(window_scaling / 25),
    )

    circle_center_coords = (
        obj_position[0] * window_scaling + 0.7 * window_scaling,
        obj_position[1] * window_scaling + (1 - 0.4) * window_scaling,
    )
    pygame.draw.circle(
        surface=surface,
        color=(0, 0, 0),
        center=circle_center_coords,
        radius=0.1 * window_scaling,
    )

    keyhole_triangle_coords = [
        (
            obj_position[0] * window_scaling + 0.6 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.2) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.7 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.4) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.8 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.2) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=keyhole_triangle_coords
    )


def create_door_closed_unlocked(surface, obj_position, window_scaling):
    outer_door_coords = [
        (obj_position[0] * window_scaling, obj_position[1] * window_scaling),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling + 1 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(255, 235, 138), points=outer_door_coords
    )
    door_border_coords = [
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface,
        color=(0, 0, 0),
        points=door_border_coords,
        width=int(window_scaling / 25),
    )
    circle_center_coords = (
        obj_position[0] * window_scaling + 0.7 * window_scaling,
        obj_position[1] * window_scaling + (1 - 0.4) * window_scaling,
    )
    pygame.draw.circle(
        surface=surface,
        color=(0, 0, 0),
        center=circle_center_coords,
        radius=0.1 * window_scaling,
        width=int(window_scaling / 25),
    )


def create_moving_obstacle(surface, obj_position, window_scaling):
    # Create floor background
    floor_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=floor_background_coords
    )

    closed_polygon_coords = [
        (
            obj_position[0] * window_scaling + 0.1 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.5 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.9 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.5 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(204, 78, 92), points=closed_polygon_coords
    )


def create_exit(surface, obj_position, window_scaling, color):
    if color is not None:
        flag_background_coord = [
            (
                obj_position[0] * window_scaling,
                obj_position[1] * window_scaling,
            ),
            (
                obj_position[0] * window_scaling,
                obj_position[1] * window_scaling + 1.0 * window_scaling,
            ),
            (
                obj_position[0] * window_scaling + 1.0 * window_scaling,
                obj_position[1] * window_scaling + 1.0 * window_scaling,
            ),
            (
                obj_position[0] * window_scaling + 1.0 * window_scaling,
                obj_position[1] * window_scaling,
            ),
        ]
        pygame.draw.polygon(
            surface=surface, color=color, points=flag_background_coord
        )
    flag_triangle_coords = [
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.5) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.9) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.8 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.7) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=flag_triangle_coords
    )
    flag_pole_coords = [
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.2 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.7) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.24 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.7) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.24 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.1) * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=flag_pole_coords
    )


def create_beacon(surface, obj_position, window_scaling, color):
    # Create floor background
    floor_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=floor_background_coords
    )
    # Create beacon circle
    circle_center_coords = (
        obj_position[0] * window_scaling + 0.5 * window_scaling,
        obj_position[1] * window_scaling + 0.5 * window_scaling,
    )
    pygame.draw.circle(
        surface=surface,
        color=color,
        center=circle_center_coords,
        radius=0.45 * window_scaling,
    )
    # Create beacon X
    x_left_coords = [
        (
            obj_position[0] * window_scaling + 0.28 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.22) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.22 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.28) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.72 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.78) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.78 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.72) * window_scaling,
        ),
    ]
    pygame.draw.polygon(surface=surface, color=(0, 0, 0), points=x_left_coords)
    x_right_coords = [
        (
            obj_position[0] * window_scaling + 0.22 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.72) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.28 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.78) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.78 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.28) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.72 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.22) * window_scaling,
        ),
    ]
    pygame.draw.polygon(surface=surface, color=(0, 0, 0), points=x_right_coords)


def create_portal(surface, obj_position, window_scaling):
    # Create portal object
    portal_background_coords = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    pygame.draw.polygon(
        surface=surface, color=(191, 182, 168), points=portal_background_coords
    )
    circle_center_coords = (
        obj_position[0] * window_scaling + 0.5 * window_scaling,
        obj_position[1] * window_scaling + 0.5 * window_scaling,
    )
    pygame.draw.circle(
        surface=surface,
        color=(180, 160, 200),
        center=circle_center_coords,
        radius=0.45 * window_scaling,
    )

    radius = 0
    center = (
        obj_position[0] * window_scaling + 0.5 * window_scaling,
        obj_position[1] * window_scaling + 0.5 * window_scaling,
    )
    max_radius = 0.4 * window_scaling
    num_segments = 500
    radius_delta = max_radius / num_segments
    spin_rate = 2
    x = center[0]
    y = center[1]
    for i in range(num_segments):
        x1 = x
        y1 = y
        radius += radius_delta
        x = center[0] + radius * math.cos(
            (2 * math.pi * i / num_segments) * spin_rate
        )
        y = center[1] + radius * math.sin(
            (2 * math.pi * i / num_segments) * spin_rate
        )
        pygame.draw.line(
            surface=surface,
            color=(0, 0, 0),
            start_pos=(x, y),
            end_pos=(x1, y1),
            width=int(window_scaling / 15),
        )


def create_unknown(surface, obj_position, window_scaling):
    # Create vertices for pieces of object
    unknown_background_coord = [
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling,
        ),
        (
            obj_position[0] * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling + 1.0 * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 1.0 * window_scaling,
            obj_position[1] * window_scaling,
        ),
    ]
    question_mark_coord_1 = [
        (
            obj_position[0] * window_scaling + 0.15 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.65) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.15 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.25 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.25 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.65) * window_scaling,
        ),
    ]
    question_mark_coord_2 = [
        (
            obj_position[0] * window_scaling + 0.15 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.75) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.15 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.75) * window_scaling,
        ),
    ]
    question_mark_coord_3 = [
        (
            obj_position[0] * window_scaling + 0.75 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.85) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.85 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.45) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.75 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.45) * window_scaling,
        ),
    ]
    question_mark_coord_4 = [
        (
            obj_position[0] * window_scaling + 0.75 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.55) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.75 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.45) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.45) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.55) * window_scaling,
        ),
    ]
    question_mark_coord_5 = [
        (
            obj_position[0] * window_scaling + 0.45 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.55) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.55) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.3) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.45 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.3) * window_scaling,
        ),
    ]
    question_mark_coord_6 = [
        (
            obj_position[0] * window_scaling + 0.45 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.15) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.45 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.25) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.25) * window_scaling,
        ),
        (
            obj_position[0] * window_scaling + 0.55 * window_scaling,
            obj_position[1] * window_scaling + (1 - 0.15) * window_scaling,
        ),
    ]

    # Draw the object
    pygame.draw.polygon(
        surface=surface, color=(255, 179, 102), points=unknown_background_coord
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_1
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_2
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_3
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_4
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_5
    )
    pygame.draw.polygon(
        surface=surface, color=(0, 0, 0), points=question_mark_coord_6
    )


def create_grid(surface, grid_size, window_scaling):
    grid_width = grid_size[0]
    grid_height = grid_size[1]
    line_width = int(window_scaling / 25)

    # Create horizontal lines
    for i in range(grid_height + 1):
        start_pos = (0, i * window_scaling)
        end_pos = (grid_width * window_scaling, i * window_scaling)
        pygame.draw.line(
            surface=surface,
            color=(0, 0, 0),
            start_pos=start_pos,
            end_pos=end_pos,
            width=line_width,
        )

    # Create vertical lines
    for i in range(grid_width + 1):
        start_pos = (i * window_scaling, 0)
        end_pos = (i * window_scaling, grid_height * window_scaling)
        pygame.draw.line(
            surface=surface,
            color=(0, 0, 0),
            start_pos=start_pos,
            end_pos=end_pos,
            width=line_width,
        )
