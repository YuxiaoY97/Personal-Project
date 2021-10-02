# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 20:52:15 2020

@author: Yuxiao Yang
"""
# %%%
import csv
import numpy as np
def read_file(filename,date_index,field_index,has_header=True):
    time_series = []
    with open(filename) as csvfile:
        reader= csv.reader(csvfile,delimiter=',' )
        if has_header:
            next(reader, None)
        for row in reader :
            time_series.append((row[date_index] , float(row[field_index])))
    return time_series
    
    
def valid_input(date_range):
    while True:
        window = input('Please enter a rolling window size between 0 - ' + str(date_range) + ': ')
        if 0 < int(window) < date_range:
            return window
            break
    
def main():
    filename = 'GOOG.csv '
    ts = read_file(filename, 0, 5)
    ts = np.array(ts)
    print (f'{filename} has been read with {len(ts)} daily prices')
    window = int(valid_input(len(ts)))
    wid = 0
    print("\n{:^10}|{:^23}|{:^10}|{:^10}|{:^10}|{:^10}".format('Window','Date', 'Range','Mean','Median','Std Dev'))
    for i in range(0,len(ts)-window+1):
        wid +=1
        price_range = np.array(ts[i:(i + window-1),1],dtype = float)
        date_range = str(ts[i,0])+' - ' + str(ts[i+window-1, 0])
        ran = max(price_range) - min(price_range)        
        avg = np.mean(price_range)
        med = np.percentile(price_range,50)
        std = np.std(price_range)
        print("{:^10}|{:^10}|{:^10.2f}|{:^10.2f}|{:^10.2f}|{:^10.2f}".format(wid, date_range, ran, avg, med, std))
                

if __name__ == '__main__':
    main()
    
    
    


