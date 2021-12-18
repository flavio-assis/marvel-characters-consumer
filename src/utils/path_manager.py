import os


def construct_path(path):
    curr_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(curr_path)

    final_path = os.path.join(dir_name, '../..', path)

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    return final_path
