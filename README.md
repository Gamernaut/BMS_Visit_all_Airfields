# Interesting alternative to the Travelling Salesman Problem

### Inspiration:
Whilst playing Falcon BMS, an F16 flight simulator, I wondered if it was possible to find the quickest/shortest route to visit every airfield in the sim once (i.e. every airbase, airstrip etc.). There would be no need to return to the starting airfield so it was more of a linear route than a circular route. 

The idea is to use this as a platform to "plug-in" different algorithms to understand the performance versus accuracy of different approaches and to gain experience implementing different types of algorithms for this problem.

_This is a learning exercise for me to implement a number of classical and non-classic algorithms to understand the strengths and weaknesses and is still a work in progress._

### Techniques used/Learnings:
- Haversine formula to calculate the distance, in miles, between 2 pairs of Latitude/Longitude coordinates (formula accounts for the curvature of the Earth)
- Greedy Algorithm (minimum continuous route) - Simple algorithm that looks for next closest airfield in a continuous route
- Genetic Algorithm - Alternative, more complex algorithm which may avoid getting stuck in the same local minimum as the Greedy Minimum Continuous Route Algorithm

### Languages/Packages:
- Python 3.9 (PyCharm 2021 Community Edition)
- Pandas
- NumPy
