# Alek Westover
# full ai for salesman problem
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random
import numpy as np
import time


def gen_pts(quantity: int, std_deviation: float or int, env_size: list = [250, 250]) -> object:
    #  Two-d visualization uses and graphs these points,
    # the algorithm should work with any valid list of distances like the one generated with genDistances
    pts = []
    for i in range(0, quantity):
        pts.append([random.gauss(env_size[0] / 2, std_deviation), random.gauss(env_size[1] / 2, std_deviation)])
    return pts


def display_pts(pts, picture):
    #  Must have fig = plt.figure \ picture=fig.add_subplot(1,1,1) before this in real code
    #  Also must have plt.tight_layout() \ plt.show() Afterwords in real code
    picture.scatter([pt[0] for pt in pts], [pt[1] for pt in pts], color='red')


def gen_distances(points: list) -> list:  # kinda like an adjacency matrix, really redundant
    return [[np.linalg.norm(np.subtract(pt1, pt2)) for pt2 in points] for pt1 in points]


def combiner(first: list, after: list) -> list:
    if len(after) == 0:
        return first
    out = []
    for i in range(0, len(after)):
        out.append(first+[after[i]])
    return out


def missing(total: list, already: list) -> list:
    missed = []
    for element in total:
        if total.count(element) > already.count(element) + missed.count(element):
            missed.append(element)
    return missed


def permutations(array:  list) -> list:
    arrayed_array = [[array[i]] for i in range(0, len(array))]
    print(arrayed_array)
    out_perms = arrayed_array
    for i in range(0, len(array)-1):
        j_len = len(out_perms)
        for j in range(0, j_len):
            combined = combiner(out_perms[0], missing(array, out_perms[0]))
            for k in range(0, len(combined)):
                out_perms.append(combined[k])
            out_perms.pop(0)
    return out_perms


def cyclic_permutations(array: list) -> list:
    out_perms = [[array[0]]]
    for i in range(0, len(array)-1):
        j_len = len(out_perms)
        for j in range(0, j_len):
            combined = combiner(out_perms[0], missing(array, out_perms[0]))
            for k in range(0, len(combined)):
                out_perms.append(combined[k])
            out_perms.pop(0)
    return out_perms


def pt_dist(pt1, pt2):
    return np.linalg.norm([pt1[i] - pt2[i] for i in range(0, len(pt1))], axis="0")


def slow_path_dist(path: list, points: list) -> float or int:
    total_dist = 0
    for i in range(0, len(path)-1):
        total_dist += pt_dist(points[path[i]], points[path[i+1]])
    total_dist += pt_dist(points[path[-1]], points[path[0]])
    return total_dist


def not_fast_path_dist(path: list, points: list) -> float or int:
    total_dist = 0
    dists = gen_distances(points)
    for i in range(0, len(path)-1):
        total_dist += dists[path[i]][path[i+1]]
    total_dist += dists[path[-1]][path[0]]
    return total_dist


def path_dist(path: list, pt_dists: list) -> float or int:
    total_dist = 0
    for i in range(0, len(path)-1):
        total_dist += pt_dists[path[i]][path[i+1]]
    total_dist += pt_dists[path[-1]][path[0]]
    return total_dist


def smallest_positive(array: list, used: list) -> int:
    min_val = np.inf
    for i in range(0, len(array)):
        if min_val > array[i] > 0 and i not in used:
            min_val = array[i]
    if min_val in array:
        return array.index(min_val)
    else:
        return None


def update_plot(i, pts, figure):
    if i == 0:
        time.sleep(0.5)
    plt.cla()
    figure.set_title("Towns and  Routes")
    figure.set_ylabel("y")
    figure.set_xlabel("x")
    plt.tight_layout()
    display_pts(pts, figure)
    figure.plot([pts[j][0] for j in range(0, i)], [pts[k][1] for k in range(0, i)])


def index_switcher(path, i, j):
    out_path = path[:]
    out_path[i] = path[j]
    out_path[j] = path[i]
    return out_path


def switcher(path, num_towns, pt_dists):
    for i in range(0, num_towns):
        for j in range(0, num_towns):
            seg1 = [path[i], path[i+1]]
            seg2 = [path[j], path[j+1]]
            if seg1[0] != seg2[0] and seg1[0] != seg2[1] and seg2[0] != seg1[1]:
                # no mods necessary because must go back to start, ie len(path) = num_towns +1
                # fix more efficent distance calculations
                # original_dist = pt_dists[seg1[0]][seg1[1]] + pt_dists[seg2[0]][seg2[1]]
                # new_dist = pt_dists[seg1[0]][seg2[1]] + pt_dists[seg2[0]][seg1[1]]
                original_dist_stupid = path_dist(path, pt_dists)
                proposed_path = index_switcher(path, i+1, j+1)
                new_dist_stupid = path_dist(proposed_path, pt_dists)
                if original_dist_stupid > new_dist_stupid:
                    path = proposed_path
    return path


num_towns = 50
towns = [i for i in range(0, num_towns)]
points = gen_pts(num_towns, 30.0)
pt_dists = gen_distances(points)
path = [0]
for i in range(0, num_towns-1):
    path.append(smallest_positive(pt_dists[path[-1]], path))
path.append(0)
print(path_dist(path, pt_dists))
path = switcher(path, num_towns, pt_dists)
greedy_points_order = [points[path[i]] for i in range(0, num_towns)] + [points[path[0]]]
print(path_dist(path, pt_dists))

fig = plt.figure()
picture = fig.add_subplot(1, 1, 1)
anim = animation.FuncAnimation(fig, update_plot, fargs=(greedy_points_order, picture), frames=num_towns + 2, interval=20)
plt.show()
