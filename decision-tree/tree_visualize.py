import matplotlib.pyplot as plt
import decision_tree

decision_node = dict(boxstyle = "square", fc = "pink", ec = "yellow")
leaf_node = dict(boxstyle = "round", fc = "pink", ec = "blue")

def plot_node(node_text, center_point, parent_point, node_type):
    create_plot.ax1.annotate(node_text, xy = parent_point, xycoords = "axes fraction", xytext = center_point, textcoords = "axes fraction",va = "center", ha = "center", bbox = node_type, arrowprops = dict(arrowstyle = "<-"))


def get_leaf_num(my_tree):
    leaf_num = 0
    first_key =list(my_tree.keys())[0]    
    second_dict = my_tree[first_key]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            leaf_num += get_leaf_num(second_dict[key])
        else:
            leaf_num += 1
    return leaf_num

def get_tree_depth(my_tree):
    max_tree_depth  = 0
    first_key = list(my_tree.keys())[0]
    second_dict = my_tree[first_key]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            tree_depth = 1 + get_tree_depth(second_dict[key])
        else:
            tree_depth = 1
        if tree_depth > max_tree_depth:
            max_tree_depth = tree_depth
    return max_tree_depth

def anotate(current_point, parent_point, content):
    loc_x = (current_point[0] + parent_point[0]) / 2.0
    loc_y = (current_point[1] + parent_point[1]) / 2.0
    create_plot.ax1.text(loc_x, loc_y, content, ha = "center", va = "center", color = "purple", rotation = 45)

        
def plot_tree(my_tree, parent_point, content):
    cur_leaf_num = float(get_leaf_num(my_tree))
    cur_Tree_depth = float(get_tree_depth(my_tree))
    first_key = list(my_tree.keys())[0]
    current_point = (plot_tree.LOC_LEAF_X + (1.0 + cur_leaf_num)/2.0/plot_tree.TOTAL_WIDTH , plot_tree.LOC_LEAF_Y)
    anotate(current_point, parent_point, content)
    plot_node(first_key, current_point, parent_point, decision_node)
    second_dict = my_tree[first_key]
    plot_tree.LOC_LEAF_Y -= 1 / plot_tree.TOTAL_DEPTH
    for key in list(second_dict.keys()):
        if type(second_dict[key]).__name__ == "dict":
            plot_tree(second_dict[key], current_point, key)
        else:
            plot_tree.LOC_LEAF_X += 1.0 / plot_tree.TOTAL_WIDTH
            plot_node(second_dict[key], (plot_tree.LOC_LEAF_X, plot_tree.LOC_LEAF_Y), current_point, leaf_node)
            anotate((plot_tree.LOC_LEAF_X, plot_tree.LOC_LEAF_Y), current_point, key)
    plot_tree.LOC_LEAF_Y += 1 / plot_tree.TOTAL_DEPTH

def create_plot(in_tree):
    plt.switch_backend("PDF")
    fig = plt.figure(1, facecolor = "white")
    fig.clf()
    hide_axis = dict(xticks = [], yticks = [])  
    plot_tree.TOTAL_WIDTH = float(get_leaf_num(in_tree))
    plot_tree.TOTAL_DEPTH = float(get_tree_depth(in_tree))
    plot_tree.LOC_LEAF_X = -0.5 / plot_tree.TOTAL_WIDTH
    plot_tree.LOC_LEAF_Y = 1.0
    create_plot.ax1 = plt.subplot(111, frameon = False, **hide_axis)
    plot_tree(in_tree, (0.5, 1.0), '')
    plt.savefig("_1_.pdf")

if __name__ == "__main__":
    my_tree = decision_tree.get_tree_dict()
    create_plot(my_tree)
