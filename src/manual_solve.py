#!/usr/bin/python


###### NAME: JOSHUA O'CURRY
######   ID: 20235838

###### GitHub URL : https://github.com/joshocurry


import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.
########## SUMMARY & REFLECTION
# The only library I used in the solve_* functions was numpy. I only used this in one instance and the function I used was numpy.flip()
# The rest of the time I just used pure python as this is where I believe my strengths are. I used many common methods when writing the solve functions.
# In every function I iterate through the array using a nested for loop in which I use (for i in range(len(array.shape(0))):) I used this as it allowed me
# to always have access to the coordinates of the elements I was dealing with as i would be the row and j would be the column.
# Fancy indexing was also very helpful as there were certain solutions in which I needed access to chunks of the array.

# There were many commonalities in these solutions however I believe these were a consequence of my personal ways of working and coding process.
# As I mentioned above I repeatedly used a nested for loop to iterate and access elements in the arrays. Another process which I found myself repeating in a number
# of functions was that in which I needed to assess what cells were touching other cells of certain colours I could cgeck surrounding cells by adding/subtracting
# 1 from the column/row value. Because of this I often first had to ensure I was not at the edge of an array or I would receive an IndexError for attempting to
# check a cell out of range. There were not many differences that I noticed other that the tasks themselves being inherently different in their own right. 
# One difference I found was that some tasks required me to manipulate the input array and return it others in contrast required me to create a new array 
# using characteristics of the input array and return that new array. This was mainly the case when the dimensions of the input differed from that of the output.
################################################################################################

def solve_484b58aa(x):

        #   OUTLINE OF TRANSFORMATION AND APPROACH 
# The transformation in this task was simple (by eye) fill in the the gaps (black spaces) with the relevant part of the pattern.
# The issue was that this pattern was not consistent across all arrays but they were all the same shape
# From too much time spent looking at these arrays I could see that they all repeated but at different times.
# I started to solve the pattern by looking at the test array, I could see that the row pattern repeated after 9 rows
# Then I saw that the column pattern repeated after 18 cols, which seemed like a coincidence
# This is when I began to have a theory of a key_array ie array[0:9, 0:18]
# This was validated by looking at the next 9 rows below this key_array
# The same was not true for the other arrays so I knew 9 was a variable that depended on the array and 18 was double it.
# I took the amount of unique colours in hopes that it would be 9 but it was in fact 7 but by printing this set of colours
# I noticed that the max 'colour' was 9!
# I repeated this process of looking for a key_array for all datasets using this max(colour) concept and it worked!
# The rest of the thoery behind this function was some array maniupulation etc to obtain this key_array and 
# then use it to populate the remainder of the original array.

### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###

#   Getting a list of all colours in the array
    colours = []
    for i in x:
        for j in i:
            colours.append(j)
            
#   length in this case is how many rows are in the pattern whic is equal to the max colour as stated above
#   This was the key to the whole function
    length = max(set(colours))
    
#   I defined repeater as the pattern would repeat a different amount of times as a pattern with 9 rows would repeat
#   3.(something) times in 29 rows but a pattern with 7 rows would repeat just over 4 times
    repeator = int(x.shape[0]/length)
    p = 0
    q = 0
    
#   I seperated these into key_array candidates and arrays on the right that contained the left and sometimes the whole key_array
    array_dict = {}
    right_dict = {}

#   A while loop to capture the necessary number of patterns based on the inputs 'repeatpr' value
    while p <= repeator:
        array_dict[p] = x[length * p: length * (p+1), 0:length * 2]
        p += 1

    while q <= repeator:
        right_dict[q] = x[length * q: length * (q+1), length * 2:]
        q += 1
#   defining 2 lists to hold all key array candidates and right arrays
    key_arrays = []
    right_arrays = []

#   Appending the relevant arrays to their list
#   In this case if it did not have the shape (length, length * 2) it must be the left over array at the bottom
    for i in array_dict:
        if array_dict[i].shape == (length, length * 2):
            key_arrays.append(array_dict[i]) 
        else:
            bottom_array = array_dict[i]
            
#   Similar process as above  
    for i in right_dict:
        if right_dict[i].shape[0] == length and 0 not in right_dict[i]:
            right_array = right_dict[i]
            
#   the right bottom array is essentially the array with the same cols as the right arrays and same rows as the bottom array
    right_bottom = right_array[0:bottom_array.shape[0], :]

#   This set of statements helps to find the key_array or build it from the other arrays we have
    for array in key_arrays:
        if 0 not in array:
            key_array = array
        elif 0 not in bottom_array:
            for array in key_arrays:
                if 0 in array[0:bottom_array.shape[0], 0:bottom_array.shape[1]] and 0 not in array[bottom_array.shape[0]:, bottom_array.shape[1]:]:
                    array[0:bottom_array.shape[0], 0:bottom_array.shape[1]] = bottom_array
                    key_array = array
        else:
            array[0:length, 0:length * 2] = right_array[0:length, 0:length * 2]
            key_array = array


#   Using this repeator logic once again we are putting in the key_array where necessary
    r = 0
    while r < repeator:
        x[length * r: length * (r+1), 0 : length * 2] = key_array
        r += 1

#   Same as above for the right_array
    r = 0
    while r < repeator:
        x[length * r: length * (r+1), length * 2 :] = right_array
        r += 1

#   I can use repeator here as the (amount of rows in a pattern) * repetitions is where the bottom array begins    
    
#   Putting the bottom array into place
    x[repeator * length:, 0:length * 2] = bottom_array
        
#   Putting the bottom right array into place
    x[repeator * length:, length * 2:] = right_bottom

    return x

def solve_3631a71a(x):

    #   OUTLINE OF TRANSFORMATION AND APPROACH 
# First thing I noticed is that each pattern is symmetrical across the origin in all directions ie all quadrants are 'mirrored'
# Next I saw that this is only true for a grid of size (28,28) leaving out top and leftmost 2 rows
# First step was to solve this 28x28 grid.
# I split this grid into 4 quadrants in which 1 was always complete (no maroon squares)
# I then used np.flip() on the complete quadrant to 'mirror' it and replace the other three
# I then put those quadrants back into the original array
# Next was to adress remaining maroon squares
# These could only be on the left 2 cols or the top two cols
# I then thought about what would make a puzzle 'unsolvable' :
#   - If there were maroon spots in the top left 2x2 grid as these were found nowhere else
#   - If there were maroon spots on the left 2 cols that stretched across top and bottom half as one is needed to solve the other
#   - Similar to above but for the top two rows.   
#
### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###
#
#   SEPERATING THE 4 QUADRANTS OF (28,28) GRID
    top_left = x[2:int((x.shape[0]/2) + 1),2:int((x.shape[1]/2) + 1) ]
    top_right = x[2:int(x.shape[0]/2) + 1,int(x.shape[1]/2) + 1 : ]
    bottom_left = x[int(x.shape[0]/2 ) + 1 :,2:int(x.shape[1]/2) + 1 ]
    bottom_right = x[int(x.shape[0]/2) + 1 : ,int(x.shape[1]/2) + 1 : ]

#   SEARCHING EACH QUADRANT FOR 9's (MAROON) AND USING GRID WITH NONE
    if 9 not in top_left:
        #print('using top left quadrant')
        top_right = np.flip(top_left,1)
        bottom_left = np.flip(top_left,0)
        bottom_right = np.flip(top_left)

    elif 9 not in top_right:
        #print('using top right quadrant')
        top_left = np.flip(top_right,1)
        bottom_right = np.flip(top_right,0)
        bottom_left = np.flip(top_right)

    elif 9 not in bottom_left:
        #print('using bottom left quadrant')
        bottom_right = np.flip(bottom_left,1)
        top_left = np.flip(bottom_left,0)
        top_right = np.flip(bottom_left)

    elif 9 not in bottom_right:
        #print('using bottom right quadrant')
        bottom_left = np.flip(bottom_right,1)
        top_right = np.flip(bottom_right,0)
        top_left = np.flip(bottom_right)

#   PUTTING THE NOW COMPLETE QUADRANTS BACK INTO ORIGINAL ARRAY (STILL ACCOUTING FOR 28,28 SHAPE)  
    x[2:int((x.shape[0]/2) + 1),2:int((x.shape[1]/2) + 1) ] = top_left
    x[2:int(x.shape[0]/2) + 1,int(x.shape[1]/2) + 1 : ] = top_right
    x[int(x.shape[0]/2 ) + 1 :,2:int(x.shape[1]/2) + 1 ] = bottom_left
    x[int(x.shape[0]/2) + 1 : ,int(x.shape[1]/2) + 1 : ] = bottom_right

#   SEPERATING THE ONLY AREAS FOR POSSIBLE 9's
    left_upper = x[2:int(x.shape[0]/2) + 1,0:2]
    left_lower = x[int(x.shape[0]/2) + 1 :,0:2]
    top_left =   x[0:2, 2:int(x.shape[1]/2) +1]
    top_right =  x[0:2, int(x.shape[1]/2) +1 :]

    
#   I THEN SEARCHED FOR 9's IN THESE AREAS AND REPLACED THEM WITH THEIR COUNTERPART
    if 9 in left_lower:
        x[int(x.shape[0]/2) + 1 :,0:2] = np.flip(left_upper, 0)
    elif 9 in left_upper:
        x[2:int(x.shape[0]/2) + 1,0:2] = np.flip(left_lower, 0)

#   SIMILAR TO ABOVE
    if 9 in top_left:
        x[0:2, 2:int(x.shape[1]/2) +1] = np.flip(top_right, 1)
    elif 9 in top_right:
        x[0:2, int(x.shape[1]/2) +1 :] = np.flip(top_left, 1)

#   RETURNING NOW SOLVED ARRAY
# One addition I would make is that although this solves all the arrays I just noticed however in contradiction to an original
# statement the puzzle would not be unsolvable if for example there were 9s in x[2:, 0:2] as this pattern would exist as
# a 2,28 row at the top of the array and could be leveraged to get this left hand side however this was not required for
# this specific set of arrays
    return x

def solve_469497ad(x):
# TRANSFORMATION AND APPROACH
# This pattern was also not straight forward but after some tie I could finally find it:
# Every cell/square was turned into a (n,n) where n was the amount of colours in the right & bottom border (or either one)
# plus 1
# Then once that ransofrmation was complete , at each corner of this new main array (main square) red cells would go diagonally
# until they reachanother colour or the end of the overall array

### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###
### ERROR IN SECOND TRAINING ARRAY OUTPUT ###

#   First I began to get my n + 1 value by gettin the number of unique colours in the bottom row.
    for i in x:
        for j in i:
            if j not in x[-1] and j != 0:
            #   It will become clear later why I needed this value
                square_col = j

#   I then added one to this number of unique colour to get what I called it the 'multiplier'
    n = len(set(x[-1]))
    mult = n + 1

    new_list = []

#   I then created a new array 
#   The plan for this was to create every row (mult) times and repeat every value in each row (mult) times
#   eg if mult = 2 and orig row = [1,2,3,4], new list would be [[1,1,2,2,3,3,4,4],[1,1,2,2,3,3,4,4]]
    for row in x:
        new_row = []
        for j in row:
            for i in range(mult):
                new_row.append(j)
        for i in range(mult):
            new_list.append(new_row)
    new_array = np.array(new_list)
    
#   The next step was finding wach corner of my 'main square' of which I new the colour from above

    top_right = 0
    top_left = 0
    bottom_right = 0
    bottom_left =  0

#   I chose to use a series of if statements to locate the four corners of the main square
#   By iterating through each cell and stopping only when we find a square the was the correct colour
#   I also set each of the diagonal square to red if it was not at a border in which cass the corner value would = 0
    for i in range(new_array.shape[0]):
        for j in range(new_array.shape[1]):
            if new_array[i, j] == square_col:
                if i != 0 and i != new_array.shape[0] - 1 and j != 0 and j != new_array.shape[1] - 1:
                    # TOP RIGHT
                    if new_array[i, j + 1] == 0 and new_array[i - 1, j + 1] == 0 and new_array[i - 1, j ] == 0:
                        top_right = i, j
                        new_array[i - 1, j + 1] = 2
                    # TOP LEFT
                    if new_array[i, j - 1] == 0 and new_array[i - 1, j - 1] == 0 and new_array[i - 1, j ] == 0:
                        top_left = i, j
                        new_array[i - 1, j - 1] = 2
                    # BOTTOM RIGHT
                    if new_array[i, j + 1] == 0 and new_array[i + 1, j + 1] == 0 and new_array[i + 1, j ] == 0:
                        bottom_right = i, j
                        new_array[i + 1, j + 1] = 2
                    # BOTTOM LEFT 
                    if new_array[i, j - 1] == 0 and new_array[i + 1, j - 1] == 0 and new_array[i + 1, j ] == 0:
                        bottom_left = i, j
                        new_array[i + 1, j - 1] = 2

#   Then I then continued to add a red square diagonally untilthe red squares were at the edge of the grid
    c = 2
    while 2 not in new_array[0] and 2 not in [i[0] for i in new_array]:
        if top_right != 0:
            new_array[top_right[0] - c, top_right[1] + c] = 2
        if top_left != 0:
            new_array[top_left[0] - c, top_left[1] - c] = 2
        if bottom_right != 0:
            new_array[bottom_right[0] + c, bottom_right[1] + c] = 2
        if bottom_left != 0:
            new_array[bottom_left[0] + c, bottom_left[1] - c] = 2
        c += 1



    return new_array

def solve_a8d7556c(x):
    
    # TRANSFORMATION AND APPROACH
# This was the transformation is simple by eye, all rectangles (inc squares) are changed to red
# The best way I found to identify was to first create a list of every black cells co-ordinates
# I then  checked to see for every black cell if there was a cell directy to its right and below it and diagonally down and right
# This meant every cell that this condition was true for was the top left corner of a set of 4 black cells
# When looking at the third training array you can see how the error is being caused from my method

### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS EXCEPT FOR THE FINAL TRAINING ARRAY ###

#   Initialising empty list
    black_cells = []

#   Iterating through array to obtain black cell's coordinates
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == 0:
                black_cells.append((i, j))

#   Initialising empty list
    top_corners= []

#   Iterating through black cells to find top lef corners of perfect squares
    for k in range(len(black_cells)):
        i = black_cells[k][0]
        j = black_cells[k][1]
        if (i, j + 1) in black_cells and (i + 1, j + 1) in black_cells and (i + 1, j) in black_cells :
            top_corners.append((i, j))  
    #print(top_corners)
#   changing the perfect square red
    for element in top_corners:
        x[element[0], element[1]] = 2
        x[element[0] + 1, element[1]] = 2
        x[element[0], element[1] + 1] = 2
        x[element[0] + 1, element[1] + 1] = 2

    return x

def solvea_78176bb(x):
    
        # TRANSFORMATION AND APPROACH
# The transforamtion fo this task is:
# For each input there is one diagonal coloured line.
# There are grey cells connected to this diagonal line in a triangle (L ) formation.
# The output must have this same diagonal line repeated at the point of the grey cells.

### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###

#   First step is to find the colour of this main diagonal line we know its the only non black/grey colour
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] != 0 and x[i, j] != 5:
                col_main = x[i, j]

#   Need to iterate through entire array to find a grey 'point' ie a grey cell with a black at the left, below and diagonal below-left
#   I need to cover against all diagonal directions and in a point is found , coulour the next diagonal cell the main line colour
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == 5:
                # TOP RIGHT
                if x[i, j + 1] == 0 and x[i - 1, j + 1] == 0 and x[i - 1, j ] == 0:
                    x[i - 1, j + 1] = col_main
                # TOP LEFT
                if x[i, j -1] == 0 and x[i - 1, j - 1] == 0 and x[i - 1, j ] == 0:
                    x[i - 1, j - 1] = col_main
                # BOTTOM LEFT
                if x[i, j - 1] == 0 and x[i + 1, j - 1] == 0 and x[i + 1, j ] == 0:
                    x[i + 1, j - 1] = col_main
                # BOTTOM RIGHT
                if x[i, j + 1] == 0 and x[i + 1, j + 1] == 0 and x[i + 1, j ] == 0:
                    x[i + 1, j + 1] = col_main

#   Once again I iterated through the array and coloured every cell diagonal from this newly coloured cell the same coulour
#   However this will only colour cells below this cell
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == col_main:
                if i != x.shape[0] - 1 and j != x.shape[1] - 1:
                    x[i + 1, j + 1] = col_main

#   This nested for loop does the same thing however it goes in reverse order allowing me to get cells above
    for i in reversed(range(x.shape[0])):
        for j in reversed(range(x.shape[1])):
            if x[i, j] == col_main:
                if i != 0 and j != 0:
                    x[i - 1, j - 1] = col_main

#   The final step is to remove all grey cells which is simply iterating through the array and changing 5s to 0s
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == 5:
                x[i, j] = 0
                
    return x

def solve_0b148d64(x):
    
            # TRANSFORMATION AND APPROACH
# The transforamtion fo this task is:
# The four corners of each grid are occupied be smaller grids (3 of 1 colour, 1 of another)
# The aim is to isolate this corner grid which is the different colour


### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###

#   getting a list of what colour every non black cell is
    colours = []
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] != 0:
                colours.append(x[i, j])

#   finding the coulour that occupied the least cells
    target_colour = min(set(colours), key = colours.count)
    
#   Creating empty lists
    row_candidates = []
    col_candidates = []

#   Adding all possible row and column indices to the relevant list
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == target_colour:
                row_candidates.append(i)
                col_candidates.append(j)

#   Retruning a slice of the original array using the above lists and their max/min vals
    return x[min(row_candidates):max(row_candidates) + 1,min(col_candidates):max(col_candidates) + 1 ]

def solve_543a7ed5(x):

            # TRANSFORMATION AND APPROACH
# The transforamtion fo this task is:
# Each array is a blue background and pink rectangular shapes
# In the output each of these pink rectangles are surrounded by green cells and if the rectangle is not solid
# the centre will change from blue to yellow


### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###

#   I first changed all cells that touch a pink cell green which meant that the indide as well as the outside were are 
#   all green at this point
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == 6:
                # BELOW
                if x[i + 1, j] == 8:
                    x[i + 1, j] = 3
                # ABOVE
                if x[i - 1, j] == 8:
                    x[i - 1, j] = 3
                # LEFT
                if x[i, j - 1] == 8:
                    x[i, j - 1] = 3
                # RIGHT
                if x[i, j + 1] == 8:
                    x[i, j + 1] = 3
                # TOP LEFT
                if x[i - 1, j - 1] == 8:
                    x[i - 1, j - 1] = 3
                # TOP RIGHT
                if x[i - 1, j + 1] == 8:
                    x[i - 1, j + 1] = 3
                # BOTTOM LEFT
                if x[i + 1, j - 1] == 8:
                    x[i + 1, j - 1] = 3
                # BOTTOM RIGHT
                if x[i + 1, j + 1] == 8:
                    x[i + 1, j + 1] = 3
                    
#   Iterating through the array once again, if the green cell is not at the edge of the grid ( as if a green
#   cell is out the edge it must be outside the pink shape) 
#   If a cell is green and touching 3 pink cells in the positions defined below change it to yellow
#   This turns the top left of the inside section to a yellow cell
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if i != 0 and j != 0 and i != x.shape[0] - 1 and j != x.shape[1] - 1:
                if x[i - 1, j] == 6 and x[i, j - 1] == 6 and x[i - 1, j - 1] == 6 and x[i, j] == 3:
                    x[i, j] = 4

#   The same concept as above applies here
#   Any cell that is blue or green and touches a yellow cell will now also turn yellow
#   Since the top left of an inside section is yellow, as we iterate from the top down and left to right
#   This will in turn turn all inside cells yellow.
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if i != 0 and j != 0 and i != x.shape[0] - 1 and j != x.shape[1] - 1:
                if x[i, j] == 3 or x[i, j] == 8:
                    if x[i, j - 1] == 4 or x[i - 1, j] == 4:
                        x[i, j] = 4

    return x

def solve_41e4d17e(x):
    
            # TRANSFORMATION AND APPROACH
# The transforamtion fo this task is:
# In each input there is one or more dark blue sqaures
# After the transformation there are pink lines (horizontal and vertical) that go through the centre point of each square.


### THIS FUNCTION SOLVE ALL TRAINING/TESTING ARRAYS ###

#   The first step I took was to find the centre points for all squares
#   creating an epty list for all x's and y's of all centre points
    xs = []
    ys = []
    
#   for each row initialising a counter c and an initial a value both equal to 0 and an empty list of history
    for i in range(x.shape[0]):
        c = 0
        a = 0
        hist = []
#   for each element in the row if the cell is dark blue increase the counter c and store its coords in hist
        for j in range(x.shape[1]):
            if x[i, j] == 1:
                c += 1
                hist.append(j)
#   if the counter = 2 then the row is one the 3 that contains the centre as the row will only have 2 blue squares
        if c == 2 and x[i+1,int((hist[0] + hist[-1])/2)] != 1 and x[i-1,int((hist[0] + hist[-1])/2)] != 1:
#   set a to the midpoint between the first and last hist element ie the column of the midpoint
            a = int((hist[0] + hist[-1])/2)
#   if a is not 0 , it has been given the column of a midpoint and so append it to the list of x coords
        if a != 0:
            xs.append(a)

#   Similar process to obtain the y coords
    for i in range(x.shape[0]):
        c = 0
        y = 0
        hist = []
        for j in range(x.shape[1]):
            if x[i, j] == 1:
                c += 1
                hist.append(j)
#   This time if c = 5 we are at the top or bottom or the square.
#   This if statement ensures we are at the top and and we then know as all squares are of same dimension that 
#   the y coord is 2 below the top row.
        if c == 5 and x[i+1, hist[0]] == 1 and x[i+1, hist[-1]] == 1:
            y = i + 2
        if y != 0:
            ys.append(y)
    


#   The final step is to turn every cell that has an x coord in x's or a y coord in y's (given it is not dark blue)) pink
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] == 8:
                if j in xs:
                    x[i, j] = 6
                if i in ys:
                    x[i, j] = 6
                    
    return x


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

