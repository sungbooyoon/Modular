import math
import openpyxl
import random


def read_location(filename):
    wb = openpyxl.load_workbook(filename)
    wb = wb.active

    list_type =[]
    list_grid =[]

    for r in wb.rows:
        type = r[0].value
        grid_x = r[1].value
        grid_y = r[2].value

        list_type.append(type)
        list_grid.append([grid_x, grid_y])

    index_crane = list_type.index('크레인')
    index_trailer = list_type.index('트레일러')
    index_unit = list_type.index('유닛')

    list_crane = list_grid[:index_trailer] #1 ~ index_trailer-1
    list_trailer = list_grid[index_trailer:index_unit] #index-trailer ~ index_unit-1
    list_unit = list_grid[index_unit:] #index_unit ~ end

    return list_crane, list_trailer, list_unit, list_grid, index_crane, index_trailer, index_unit