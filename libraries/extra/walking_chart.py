__author__ = ['Migyeong Gwak']
__credit__ = ['Migyeong Gwak']
__email__ = ['mgwak@ucla.edu']
__date__ = ['2019_05_10']

# 1 when Toe walking
# 2 when normal sitting
# 3 when Toe sitting and Toe standing
# 4 when Heel standing and heel sitting
# 5 when normal standing
# 6 when Flat walking
# 7 when normal walking

import json
import os
import numpy as np
import matplotlib.pyplot as plt


def step_counter(data_directory, sid, cdate):
    toe_walking = 0
    flat_walking = 0
    normal_walking = 0
    plt.figure()
    with open(data_directory) as json_file:
        data = json.load(json_file)
        for p in data:
            flat_walking += int(p['FlatCount'])
            normal_walking += int(p['NormalCount'])
            toe_walking += int(p['ToeCount'])

    print("Toe_walking = ", toe_walking)
    print("Flat_walking = ", flat_walking)
    print("Normal_walking = ", normal_walking)

    walking_type = [toe_walking, flat_walking, normal_walking]
    objects = ('Toe', 'Flat', 'Normal')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, walking_type, align='center', alpha=0.8, color=['red', 'yellow', 'green'])
    plt.xticks(y_pos, objects)
    plt.ylabel('Counts')
    plt.title(sid + '-' + cdate)
    for i, v in enumerate(walking_type):
        plt.text(i, v, " " + str(v), color='blue', horizontalalignment='center', va='bottom', fontweight='bold')

    plt.savefig(data_directory[:-4] + 'png', dpi=100)


def step_counter_by_log(dataDirectory, sid, cdate):
    Toe_walking = 0
    Normal_sitting = 0
    Toe_sitstand = 0
    Heel_sitstand = 0
    Normal_standing = 0
    Flat_walking = 0
    Normal_walking = 0
    with open(dataDirectory) as json_file:
        data = json.load(json_file)
        list_shoeState = []
        for p in data:
            list_shoeState.extend(p['shoeState'])

    clean_shoeState = []
    for n in list_shoeState:
        if n > 10:
            multiState = [int(d) for d in str(n)]
            clean_shoeState.extend(multiState)
        else:
            clean_shoeState.append(n)

    for n in clean_shoeState:
        if n == 1:
            Toe_walking += 1
        elif n == 2:
            Normal_sitting += 1
        elif n == 3:
            Toe_sitstand += 1
        elif n == 4:
            Heel_sitstand += 1
        elif n == 5:
            Normal_standing += 1
        elif n == 6:
            Flat_walking += 1
        elif n == 7:
            Normal_walking += 1

    print("Toe_walking = ", Toe_walking)
    print("Normal_sitting = ", Normal_sitting)
    print("Toe_sitstand = ", Toe_sitstand)
    print("Heel_sitstand = ", Heel_sitstand)
    print("Normal_standing = ", Normal_standing)
    print("Flat_walking = ", Flat_walking)
    print("Normal_walking = ", Normal_walking)
    print("Total detected shoe states = ", Toe_walking + Normal_sitting + Toe_sitstand + Heel_sitstand + Normal_standing + Flat_walking + Normal_walking)

    walking_type = [Toe_walking, Flat_walking, Normal_walking]
    objects = ('Toe', 'Flat', 'Normal')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, walking_type, align='center', alpha=0.8, color=['red', 'yellow', 'green'])
    plt.xticks(y_pos, objects)
    plt.ylabel('Counts')
    plt.title(sid + '-' + cdate)
    for i, v in enumerate(walking_type):
        plt.text(i, v, " " + str(v), color='blue', horizontalalignment='center', va='bottom', fontweight='bold')

    plt.show()





