'''
Author: Mengfei Xi
Date: 2022-07-30 10:53:16
LastEditors: Mengfei Xi
LastEditTime: 2022-07-30 15:41:21
FilePath: \GDAL地学分析\Extract grid values.py
Description: null

Copyright (c) 2022 by Mengfei Xi, All Rights Reserved. 
'''
from osgeo import ogr
from osgeo import gdal
import numpy as np
def get_vector_coordinates(filepath):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    #打开矢量
    ds = driver.Open(filepath, 0)
    if ds is None:
        print('Could not open ' +'stations.shp')
    layer = ds.GetLayer()
    #获取要素及要素地理位置
    xValues = []
    yValues = []
    feature = layer.GetNextFeature()
    while feature:
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()
        xValues.append(x)
        yValues.append(y)  
        feature = layer.GetNextFeature()
    coordinates_list = np.array([x for x in zip(xValues,yValues)])
    return coordinates_list

def Set_GridDataTemplate(grid_size = (5,5), scale = 0.1):
    # 默认生成5*5的格网,scale为栅格数据的分辨率，单位是度
    grid = [[None] * grid_size[1] for i in range(grid_size[0])]
    start_coordinate = -(grid_size[1] - 1) / 2 * scale
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            grid[i][j] = (start_coordinate + j * scale,-start_coordinate - i * scale)
            template = np.array(grid,dtype=object)
    return template

def get_grid_coordinates(vector_coordinates,grid_template):
    grid_coordinates_list = []
    for  i in vector_coordinates:
        lon_lat_grid = [[i] * grid_template.shape[1] for j in range(grid_template.shape[0])]
        grid_coordinates = lon_lat_grid + grid_template
        grid_coordinates_list.append(grid_coordinates)
    return grid_coordinates_list

def Extract_value(raster_path,grid_coordinates):
    ds = gdal.Open(raster_path)
    if ds is None:
        print('Could not open image')
    #获取行列、波段
    rows = ds.RasterYSize
    cols = ds.RasterXSize
    bands = ds.RasterCount
    #获取仿射变换信息
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    all_feature = []
    for i in grid_coordinates:
        feature = []
        count = 0
        lon = 0
        lat = 0
        for j in i:
            count += 1
            for z in range(len(j)):
                if (z + 1) == (len(grid_coordinates[0]) + 1)/2 and count == (len(grid_coordinates[0]) + 1)/2:
                    lon = j[z][0]
                    lat = j[z][1]
                x = j[z][0]
                y = j[z][1]
                #获取点位所在栅格的位置
                xOffset = int((x-xOrigin)/pixelWidth)
                yOffset = int((y-yOrigin)/pixelHeight)
                #提取每个波段上对应的像元值
                for n in range(bands):
                    band = ds.GetRasterBand(n+1)                     
                    data = band.ReadAsArray(xOffset, yOffset,1,1)
                    if data != None:
                        value = int(data[0,0])
                        feature.append(value)
                    else:
                        feature.append(-999)
        feature.append(lon)
        feature.append(lat)
        all_feature.append(feature)
    return all_feature

if __name__ == "__main__":
    vector_coordinates = get_vector_coordinates('./台站数据/stations.shp')
    grid_template = Set_GridDataTemplate(grid_size = (5,5), scale = 0.1)
    grid_coordinates = get_grid_coordinates(vector_coordinates,grid_template)
    all_feature = Extract_value('./重采样数据/dem.tif',grid_coordinates)
    print(len(all_feature))
    print(all_feature)