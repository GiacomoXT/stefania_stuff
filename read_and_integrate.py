#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Tool to make wonderful calculations for Stefania.'''

__author__ = 'Giacomo De Pietro'
__copyright__ = 'stocazzo'


import argparse
import matplotlib.pyplot as plot


def argument_parser():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input_prima',
                        required=True,
                        type=str,
                        help='input file name for "prima"',
                        metavar='FILE')
    parser.add_argument('--input_dopo',
                        required=True,
                        type=str,
                        help='input file name for "dopo"',
                        metavar='FILE')
    parser.add_argument('--min',
                        default=-1,
                        type=float,
                        help='minimum value for "X" range',
                        metavar='MIN')
    parser.add_argument('--max',
                        default=-1,
                        type=float,
                        help='maximum value for "X" range',
                        metavar='MAX')
    parser.add_argument('--offset_x_prima',
                        default=0,
                        type=float,
                        help='offset on "X" for "prima"',
                        metavar='OFFSET_X')
    parser.add_argument('--offset_x_dopo',
                        default=0,
                        type=float,
                        help='offset on "X" for "dopo"',
                        metavar='OFFSET_X')
    parser.add_argument('--offset_y_prima',
                        default=0,
                        type=float,
                        help='offset on "Y" for "prima"',
                        metavar='OFFSET_Y')
    parser.add_argument('--offset_y_dopo',
                        default=0,
                        type=float,
                        help='offset on "Y" for "dopo"',
                        metavar='OFFSET_Y')
    parser.add_argument('--plot',
                        default=False,
                        action='store_true',
                        help='flag for saving the plot')
    parser.add_argument('--plot_name',
                        default='plot_prima_dopo.png',
                        type=str,
                        help='name of output plot',
                        metavar='PLOT_NAME')
    return parser


if __name__ == "__main__":

    args = argument_parser().parse_args()
    file_name_prima = args.input_prima
    file_name_dopo = args.input_dopo
    x_min = args.min
    x_max = args.max
    offset_x_prima = args.offset_x_prima
    offset_x_dopo = args.offset_x_dopo
    offset_y_prima = args.offset_y_prima
    offset_y_dopo = args.offset_y_dopo
    do_plot = args.plot
    plot_name = args.plot_name
    
    list_x_prima = []
    list_x_dopo = []
    list_y_prima = []
    list_y_dopo = []

    with open(file_name_prima) as file_prima, open(file_name_dopo) as file_dopo:
        for line_prima, line_dopo in zip(file_prima, file_dopo):
            values_prima = line_prima.rsplit()
            values_dopo = line_dopo.rsplit()
            if len(values_prima) == 2 and len(values_dopo) == 2:
                list_x_prima.append(float(values_prima[0]) + offset_x_prima)
                list_x_dopo.append(float(values_dopo[0]) + offset_x_dopo)
                list_y_prima.append(float(values_prima[1]) + offset_y_prima)
                list_y_dopo.append(float(values_dopo[1]) + offset_y_dopo)

    integral_prima = 0
    integral_dopo = 0
    points = len(list_x_prima)
    if x_min == -1:
        x_min = min([list_x_prima[0], list_x_dopo[0]])
    if x_max == -1:
        x_max = max([list_x_prima[points-1], list_x_dopo[points-1]])
    for i in range(points):
        x_prima = list_x_prima[i]
        x_dopo = list_x_dopo[i]
        if (i > 0):
            if (x_prima > x_min) and (x_prima < x_max):
                delta = list_x_prima[i] - list_x_prima[i-1]
                integral_prima += delta * (list_y_prima[i-1] + list_y_prima[i])
            if (x_dopo > x_min) and (x_dopo < x_max):
                delta = list_x_dopo[i] - list_x_dopo[i-1]
                integral_dopo += delta * (list_y_dopo[i-1] + list_y_dopo[i])
    integral_prima *= 0.5
    integral_dopo *= 0.5

    print(f'Integral before = {integral_prima}')
    print(f'Integral after = {integral_dopo}')
    print(f'Difference = {integral_prima - integral_dopo}')
    print(f'Depth = {(integral_prima - integral_dopo)/(x_max - x_min)}')

    if do_plot:
        plot.style.use("belle2")
        plot.figure(figsize=[16,10])
        plot.plot(list_x_prima, list_y_prima, color='blue', label='Before')
        plot.plot(list_x_dopo, list_y_dopo, color='red', label='After')
        plot.legend()
        plot.xlabel('Length [nm]')
        plot.xlim(x_min-20, x_max+20)
        plot.ylabel('Depth [nm]')
        plot.show()
        plot.savefig(plot_name)
