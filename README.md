# Interesting alternative to the Travelling Salesman Problem

### Inspiration:
Whilst playing Falcon BMS, an F16 flight simulator, I wondered if it was possible to find the quickest/shortest route to visit every airfield in the sim once (i.e. every airbase, airstrip etc.). There would be no need to return to the starting airfield so it was more of a linear route than a circular route. <BR> Idea is to try mulitple algorithms to understand the perfroamce versus accuracy of different apporches and to gain experince applying a coupe of different types of algorithms to this problem.

### Techniques used/Learnings:
- Haversine formula to calculate the distance, in miles, between 2 pairs of Latitude/Longitude coordinates (formula accounts for the curvature of the Earth)
- Greedy Algorithm (minimum continuous route) - Simple algorithm that looks for next closest airfield in a continuous route
- Genetic Algorithm - Alternative, more complex algorithm which may avoid getting stuck in the same local minimum as the Greedy Minimum Continuous Route Algorithm

### Languages/Packages:
- Python 3.9 (PyCharm 2021 Community Editon IDE from JetBrains)
- Pandas
- NumPy
  
_This is a learning exercise for me to implement a number of classical and non-classic algorithms to understand the strengths and weaknesses._
