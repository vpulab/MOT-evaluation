
import os
import numpy as np

def frame_number(file, plus=1):

    file[:, 0] = file[:, 0] + 1

    return file



def change_order(file):

    file[:, [2, 3, 4, 5]] = file[:, [3, 2, 5, 4]]

    return file

def resize_detections(file):

    file[:, [2, 4]] = file[:, [2, 4]] * 4
    file[:, [3, 5]] = file[:, [3, 5]] * 2

    return file


def center2xy(file):

    file[:, 2] = file[:, 2] - file[:, 4] / 2
    file[:, 3] = file[:, 3] - file[:, 5] / 2

    return file



if __name__ == '__main__':

    # detector = 'efficientdet-d7x'
    # detector = 'yolo4'
    sets = ['MOT17']
    # sets = ['MOT20']


    for set_name in sets:

        list_subsets = os.listdir( os.path.join('outputs/detections', detector, set_name) )

        print(set_name)

        for subset in list_subsets:

            if not os.path.isdir(os.path.join('outputs/detections', detector, set_name, subset)): continue

            print('->', subset)

            path = os.path.join('outputs/detections', detector, set_name, subset, 'det/det.txt')

            file = np.loadtxt(path, delimiter=',')




            # file = frame_number(file)
            # file = change_order(file)
            # file = resize_detections(file)
            file = center2xy(file)




            np.savetxt(path, file, delimiter=',', fmt=['%d', '%d', '%.0f', '%.0f', '%.0f', '%.0f', '%.4f', '%d', '%d', '%d'])


        print()