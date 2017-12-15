# A Search TSP
Implements the A* Search Algorithm to approximate the Traveling Salesperson Problem.

The Traveling Salesperson Problem is defined as...

"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"
source: Wikipedia - https://en.wikipedia.org/wiki/Travelling_salesman_problem

Given an input text file with list of cities as:

number_of_cities <br/>
city_name_1 x_position y_position <br/>
city_name_2 x_position y_position <br/>
...
  
the program solves the TSP problem by returning the path of the cities to travel in order, the cost to travel this path, and the number of states generated in the State tree.

Usage "python a_search.py example.txt"
