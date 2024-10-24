import math

import numpy as np

import shared
from shared import *
from temp import visualize_weight_map
from multiprocessing import Pool


class Node:
    def __init__(self, coords, cost):
        self.coords = np.array(coords)
        self.parent = None
        self.cost = cost

    def get_cost(self):
        return self.cost

    def get_time(self):
        return self.coords[3]

    def set_cost(self, new_cost):
        self.cost = new_cost

    def set_time(self, new_time):
        self.coords[3] = new_time


class RRTStar:
    def __init__(self, start, goal, conn, max_iter):
        self.start = Node(start, 0)
        self.goal = Node(goal, math.inf)
        self.conn = conn
        self.max_iter = max_iter
        self.tree = [self.start]
        self.obstacles = self.fetch_obstacles()

    def distance(self, node1, node2):
        return np.linalg.norm(node1.coords[:3] - node2.coords[:3])

    def distance_2d(self, node1, node2):
        return np.linalg.norm(node1.coords[:2] - node2.coords[:2])

    def fetch_obstacles(self):
        query = "SELECT x_min, x_max, y_min, y_max, z_min, z_max, t_start, t_end, value FROM obstacles;"
        result = query_db(self.conn, query)
        return np.array(result)

    def get_weight(self, coord):
        x, y, z, t = coord
        mask = ((self.obstacles[:, 0] <= x) & (x <= self.obstacles[:, 1]) &
                (self.obstacles[:, 2] <= y) & (y <= self.obstacles[:, 3]) &
                (self.obstacles[:, 4] <= z) & (z <= self.obstacles[:, 5]) &
                (self.obstacles[:, 6] <= t) & (t <= self.obstacles[:, 7]))
        return np.sum(self.obstacles[mask, 8])

    def get_random_node(self):
        # Generate random x, y, z coordinates within their respective maximum values
        x = np.random.rand() * MAX_X - 1
        y = np.random.rand() * MAX_Y - 1
        z = np.random.rand() * (MAX_HEIGHT_FLIGHT - MIN_HEIGHT_FLIGHT - 1) + MIN_HEIGHT_FLIGHT
        t = 0  # in the start we don't know the connection to the node

        coords = np.array([x, y, z, t])
        return Node(coords, math.inf)

    def get_nearest_node(self, node):
        nearest_node = self.tree[0]
        min_dist = self.distance(node, nearest_node)
        for n in self.tree:
            dist = self.distance(node, n)
            if dist < min_dist:
                nearest_node = n
                min_dist = dist
        return nearest_node

    def collision_weight_check(self, node1, node2):
        direction = (node2.coords[:3] - node1.coords[:3]) / SEGMENT_SAMPLING_AMOUNT
        points = node1.coords[:3] + np.outer(np.arange(1, SEGMENT_SAMPLING_AMOUNT + 1), direction)
        times = node1.get_time() + np.linalg.norm(points - node1.coords[:3], axis=1) / FLIGHT_VELOCITY
        coords = np.column_stack((points, times))

        weights = np.zeros(SEGMENT_SAMPLING_AMOUNT)
        is_safe = np.ones(SEGMENT_SAMPLING_AMOUNT, dtype=bool)

        for i, (x, y, z, t) in enumerate(coords):
            # Calculate the distances to the closest points on each obstacle
            dx = np.maximum(np.maximum(self.obstacles[:, 0] - x, x - self.obstacles[:, 1]), 0)
            dy = np.maximum(np.maximum(self.obstacles[:, 2] - y, y - self.obstacles[:, 3]), 0)
            dz = np.maximum(np.maximum(self.obstacles[:, 4] - z, z - self.obstacles[:, 5]), 0)

            distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

            # Check which obstacles are within SAFE_RADIUS
            mask = (distances <= SAFE_RADIUS) & (self.obstacles[:, 6] <= t) & (t <= self.obstacles[:, 7])

            nearby_obstacles = self.obstacles[mask]
            if len(nearby_obstacles) > 0:
                weights[i] = np.sum(nearby_obstacles[:, 8])
                is_safe[i] = not np.any(nearby_obstacles[:, 8] == OBSTACLE_WEIGHT)

        total_weight = np.sum(weights)
        is_collision_free = np.all(is_safe)

        return total_weight, is_collision_free

    def steer(self, from_node, to_node):
        direction = to_node.coords - from_node.coords
        spatial_direction = direction[:3]  # x, y, z dimensions
        spatial_length = np.linalg.norm(spatial_direction)

        # Normalize the spatial direction
        if spatial_length > 0:
            spatial_direction = spatial_direction / spatial_length

        # Calculate the new spatial coordinates
        distance_to_move = min(RRT_MAX_STEP, spatial_length)
        new_spatial_coords = from_node.coords[:3] + distance_to_move * spatial_direction

        # Calculate the corresponding time increment
        time_increment = distance_to_move / FLIGHT_VELOCITY

        # Ensure time does not exceed the max time direction
        new_time_coord = from_node.get_time() + time_increment

        new_coords = np.append(new_spatial_coords, new_time_coord)
        return Node(new_coords, from_node.get_cost() + new_time_coord)

    def rewire(self, new_node, neighbor_nodes):
        for neighbor in neighbor_nodes:
            neighbor_weight, is_collision_free = self.collision_weight_check(new_node, neighbor)
            if is_collision_free:
                additional_time = self.distance(new_node, neighbor) / FLIGHT_VELOCITY
                new_cost = new_node.get_cost() + additional_time + neighbor_weight
                if new_cost < neighbor.get_cost():
                    old_parent = neighbor.parent
                    neighbor.parent = new_node
                    cost_difference = new_cost - neighbor.get_cost()
                    time_difference = new_node.get_time() + additional_time - neighbor.get_time()
                    self.update_descendants(neighbor, cost_difference, time_difference)

    def update_descendants(self, node, cost_difference, time_difference):
        node.set_cost(node.get_cost() + cost_difference)
        node.set_time(node.get_time() + time_difference)
        for descendant in self.tree:
            if descendant.parent == node:
                self.update_descendants(descendant, cost_difference, time_difference)

    def find_path(self):
        #start_time = time.time()
        for i in range(self.max_iter):
            random_node = self.get_random_node()
            nearest_node = self.get_nearest_node(random_node)
            new_node = self.steer(nearest_node, random_node)

            new_node_weight, is_collision_free = self.collision_weight_check(nearest_node, new_node)
            new_node.set_cost(new_node.get_cost() + new_node_weight)
            if is_collision_free:
                neighbor_nodes = [n for n in self.tree if self.distance(n, new_node) <= RRT_MAX_STEP]
                min_cost_node = nearest_node
                min_cost = new_node.get_cost()
                min_cost_node_additional_time = self.distance(nearest_node, new_node) / FLIGHT_VELOCITY
                for neighbor in neighbor_nodes:
                    new_node_weight, is_collision_free = self.collision_weight_check(neighbor, new_node)
                    additional_time = self.distance(neighbor, new_node) / FLIGHT_VELOCITY
                    new_cost = neighbor.get_cost() + additional_time + new_node_weight
                    if is_collision_free and new_cost < min_cost:
                        min_cost = new_cost
                        min_cost_node = neighbor
                        min_cost_node_additional_time = additional_time

                new_node.parent = min_cost_node
                new_node.set_cost(min_cost)
                new_node.set_time(min_cost_node.get_time() + min_cost_node_additional_time)
                self.tree.append(new_node)
                self.rewire(new_node, neighbor_nodes)

                if self.distance_2d(new_node, self.goal) < RRT_MAX_STEP + BASE_AREA:
                    goal_weight, is_collision_free = self.collision_weight_check(new_node, self.goal)
                    if not is_collision_free:
                        continue
                    additional_time = self.distance_2d(new_node, self.goal) / FLIGHT_VELOCITY
                    new_cost = new_node.get_cost() + additional_time + goal_weight
                    if new_cost < self.goal.get_cost():
                        self.goal.parent = new_node
                        self.goal.coords[2] = new_node.coords[2]
                        self.goal.set_time(new_node.get_time() + additional_time)
                        self.goal.set_cost(new_cost)

            if (i % 1000 == 0):
               visualize_weight_map(new_node.get_time(), None, self.tree)
        if self.goal.parent is not None:
            #print(f"elapsed_time: {start_time - time.time()}")
            self.tree.append(self.goal)
            visualize_weight_map(self.goal.get_time(), self.reconstruct_path())
            return self.reconstruct_path()
        #print()
        return None

    def reconstruct_path(self):
        path = []
        node = self.goal
        while node:
            path.append(node.coords)
            node = node.parent
        return path[::-1]
