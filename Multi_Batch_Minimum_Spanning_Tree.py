import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

# Given information from Problem Set
####################################
home = np.array([0.5, 0.5]) 
max_charge = 3.0
####################################
N = 5000
pts = np.vstack((home, np.random.rand(N,2)))


class Travel:
    """
    A class to computer the correct order of indices in which the points
    should be accessed.

    Attributes:
    -----------
    pts : array
        (N by 2) array of all points
    pts_batch : array
        (N/batch_size by 2) array i.e. points in a batch
    visited_map : dict
		dictionary of all points in array
	max_charge : int
		maximum charge of the robot

	Methods:
	--------
	distance():
		To get distance between points
	cal_indices():
		To get dictionary of points according to the index value
	cal_center_distance_map():
		To get dictionary with distances of all points from center
	cal_curr_distance_map():
		To get dictionary with distances of points from current point
	sort_dict():
		To sort the given dictionary
	get_sort_list():
		To convert key_list from string to array
	make_grid():
		To create grid of all points
	generate_path():
		To travel along the points and get order of indices
	"""
    def __init__(self, pts, pts_batch, visited_map, max_charge=3):
        """
        Construct all necesarry attributes of Travel object

        Parameters:
        -----------
            pts : array
                (N by 2) array of all points
            pts_batch : array
                (N/batch_size by 2) array i.e. points in a batch
            visited_map : dict
		        dictionary of all points in array
	        max_charge : int
		        maximum charge of the robot
        """
        self.max_charge = max_charge  #
        self.curr_charge = self.max_charge
        self.min_charge = self.max_charge*0.25  # 25% of max charge of Robot
        self.pts = pts  # Total number of points to be covered
        self.home = pts[0]  # home
        self.pts_batch = pts_batch  # points in every batch
        self.center_dis = {}  # dict of distance of points from home
        self.indices = {}  # Indices for all points in points array
        self.visited_map = visited_map  # to check if the point is visited
        self.order = []
        self.grid = {}

    def distance(self, point_1, point_2):
        """
        Will calculate distance from point 1 to point 2

        Parameters:
        -----------
            point_1 : array
                point of dimension (2,)
            point_2 : array
                point of dimension (2,)

        Returns:
        --------
            distance between point_1 and point_2
        """
        return np.sqrt((point_1[0]-point_2[0])**2 + (point_1[1]-point_2[1])**2)

    def cal_indices(self):
        """
        Will get indices for all points in the point list and store it
        in self.indices dictionary with points as keys and indices as
        values.

        Parameters:
        -----------
            None

        Returns:
        --------
            None
        """
        for i in range(0, len(self.pts)):
            key = str(self.pts[i])
            self.indices[key] = i

    def cal_center_distance_map(self):
        """
        Will get distance of every point in the batch of points from
        the center/home and store it as dictionary.

        Parameters:
        -----------
            None

        Returns:
        --------
            self.center_dis : dictionary
                Dictionary with points as keys and distance as the values
        """
        for i in range(0, len(self.pts_batch)):
            key = str(self.pts_batch[i])
            self.center_dis[key] = self.distance(self.home, self.pts_batch[i])
        return self.center_dis

    def cal_curr_distance_map(self, curr_point):
        """
        Will get distance of every point in the batch of points from
        the current point and create a dictionary of this information.

        Parameters:
        -----------
            curr_point : array
                selected current point of dimension (2,)

        Returns:
        --------
            self.curr_point_map : dictionary
                Dictionary with points as keys and distance as the values
        """
        self.curr_point_map = {}  # dictionary created
        for i in range(0, len(self.pts_batch)):
            if self.pts_batch[i][0] == curr_point[0] and \
            self.pts_batch[i][1] == curr_point[1]:  # self distance is ignored
                pass
            else:
                key = str(self.pts_batch[i])
                self.curr_point_map[key] = self.distance(
                                            curr_point, self.pts_batch[i])
        return self.curr_point_map

    def sort_dict(self, tar_dict):
        """
        Sorts the target dictionary based on values and creates
        a new dictionary

        Parameters:
        -----------
            tar_dict : dictionary
                target dictionary that needs to be sorted

        Returns:
        --------
            self.sorted_distance : dictionary
                Sorted target dictionary
        """
        self.sorted_distance = {}  # dictionary created
        sorted_keys = sorted(tar_dict, key=tar_dict.get)
        for w in sorted_keys:
            self.sorted_distance[w] = tar_dict[w]
        return self.sorted_distance

    def get_sort_list(self, key_list):
        """
        Convert the sorted list of strings of points to the
        array of points to create appropriate key list

        Parameters:
        -----------
            key_list : list of strings
                sorted list of strings of points

        Returns:
        --------
            data_set : array
                array of points in the given list
        """
        data = []
        for i in range(0, len(key_list)):  # for all elemenst in key list
            a = key_list[i].split()  # split string parameters
            a_new = []
            for j in range(0, len(a)):
                element = a[j]
                new_elem = []
                for el in element:
                    if el == '[' or el == ']':  # remove brackets
                        pass
                    else:
                        new_elem.append(el)
                new_elem = ''.join(new_elem)
                if len(new_elem) > 0:
                    f_new = float(new_elem)
                    a_new.append(f_new)
            cur = np.asarray(a_new)
            data.append(cur)
        data_set = np.array(data)
        return data_set

    def make_grid(self):
        """
        Create a grid (N by N) which will have distances of all
        points from every other point

        Structure of Grid:

                | point 1   |  point 2 |   point 3 | ......... | point N
        ------------------------------------------------------------
        point 1 | distance    distance    distance
        point 2 |    .            .           .
        point 3 |    .            .           .
            .
            .
        point N |    .            .           .

        Parameters:
        -----------
            None

        Returns:
        --------
            sorted_center_dict : dictionary
                sorted dictionary with points arraged by distance from center
            self.grid : dictionary
                grid of all points
            key_list : array
                sorted keys as per distance from center
        """
        center_dis = self.cal_center_distance_map()
        sorted_center_dict = self.sort_dict(center_dis)
        old_keys = np.array(list(sorted_center_dict))
        key_list = self.get_sort_list(old_keys)
        for key in key_list:
            key_dis = self.cal_curr_distance_map(key)
            sorted_key_dis = self.sort_dict(key_dis)
            self.grid[str(key)] = sorted_key_dis
        return sorted_center_dict, self.grid, key_list

    def generate_path(self):
        """
        The main algorithm to move from one point to another point.

        We start by setting out home as previous point and append its
        index value to final order list and look for the closest point
        from there and set it to be our current point. for evry point
        from here out approach is to check of the next closest point
        from there and append index value for curent point.

        To check the closest point, if the previous point is home,
        we check distance from self.center_dis dictionary, where as
        for other points we check from the self.grid dictionary.

        We also make sure that current points are selected only if
        they are not visited

        Parameters:
        -----------
            None

        Returns:
        --------
            final_order : list
                Order of indices for a batch of points
            self.visited_map : dictionary
                Updated visited map from current batch of points
        """

        self.cal_indices()  # establish index dictionary
        prev_pt = self.home  # set previous point to home in the beginning
        center_dis, grid, key_list = self.make_grid()

        final_order = []  # list with index order for every batch of points
        final_order.append(0)
        curr_point = key_list[0]
        for elem in range(0, len(self.pts)-1):  # No home
            curr_dict = grid[str(curr_point)]

            # keys from sorted current point map in string format
            old_keys_sub = np.array(list(curr_dict))

            # keys converted in array format
            key_list_sub = self.get_sort_list(old_keys_sub)

            # We will enter the loop only if the current point is not visted
            if not self.visited_map[str(curr_point)]:
                # when last point is home
                if prev_pt[0] == self.home[0] and prev_pt[1] == self.home[1]:
                    curr_dis = center_dis[str(curr_point)]
                    self.curr_charge -= curr_dis  # updating current charge
                    self.visited_map[str(curr_point)] = 1  # marking visited
                    final_order.append(self.indices[str(curr_point)])  # order
                    prev_pt = curr_point
                    count = 0
                    for k in key_list_sub:
                        if not self.visited_map[str(k)] and count == 0:
                            curr_point = k
                            count += 1
                        else:
                            pass
                # monitoring current charge
                elif self.max_charge \
                >= (self.curr_charge - self.distance(prev_pt, curr_point)) \
                >= self.min_charge:
                    curr_dis = self.distance(prev_pt, curr_point)
                    self.curr_charge -= curr_dis
                    self.visited_map[str(curr_point)] = 1
                    final_order.append(self.indices[str(curr_point)])
                    prev_pt = curr_point
                    count = 0
                    for k in key_list_sub:
                        if not self.visited_map[str(k)] and count == 0:
                            curr_point = k
                            count += 1
                        else:
                            pass
                else:
                    final_order.append(0)
                    self.curr_charge = 3
                    self.visited_map[str(self.home)] += 1
                    prev_pt = self.home
                    count = 0
                    for k in key_list_sub:
                        if not self.visited_map[str(k)] and count == 0:
                            curr_point = k
                            count += 1
                        else:
                            pass
        final_order.append(0)
        return final_order, self.visited_map


def cal_visited_map(pts):
    """
    Create visited Map dictionary

    Parameters:
    -----------
        pts: array
            array of shape (N+1,2) (points stacked with home/charging point)

    Returns:
    --------
        visited_map : Dictionary
            A dictionary with points as keys and 0 as values to create
            an unvisited map of all points
    """
    visited_map = {}
    for i in range(0, len(pts)):
        key = str(pts[i])
        visited_map[key] = 0
    return visited_map


def clean_order(order_stack):
    """
    Combine order from all batches of point and create one order list

    Parameters:
    -----------
        order_stack: array
            order list from every batch of points

    Returns:
    --------
        new_order : list
            final order list
    """
    new_order = [0]
    for i in range(0, len(order_stack)):
        for j in range(1, len(order_stack[i])):
            new_order.append(order_stack[i][j])
    return new_order


def make_a_path(pts, max_limit=500):
    """
    We send in visited map which has all the points and in every
    loop it will mark the points covered in that batch and return
    the updated visisted map which is used in next batch of points.

    Then we seperate the points from home/charging point to create
    batches of point based on the total number of points and the
    max_limit. This variable can also be set by user, but by
    default it will be 500.

    For every Batch of points, Travel class is defined to get the
    order list.

    Parameters:
    -----------
        order_stack: array
            order list from every batch of points

    Returns:
    --------
        new_order : list
            final order list
    """
    visited_map = cal_visited_map(pts)
    points = pts[1:]
    batches = len(points)/max_limit
    pts_stack = np.array_split(points, batches)
    order_stack = []
    for i in range(0, len(pts_stack)):
        process = Travel(pts, pts_stack[i], visited_map)
        order, visited_map = process.generate_path()
        order_stack.append(order)
    path_order = clean_order(order_stack)
    return path_order


def draw_path(pts, order):
	"""Draw the path to the screen"""
	path = pts[order, :]

	plt.plot(path[:,0], path[:,1])
	plt.show()

if __name__ == "__main__":
    # Rounding the points to 4th decimal place to better processing
    points = np.around(pts[1:], 4)
    pts = np.vstack((home, points))

    # print(maxx_limit)
    visited_map = cal_visited_map(pts)  # Created the visited Map

	## pass arg 2 to make_a_path(arg1, arg2) to give custom batch_size
    maxx_limit = int(len(points)/10)  

    order = make_a_path(pts, maxx_limit)  # get order list for all points

    draw_path(pts, order)
	