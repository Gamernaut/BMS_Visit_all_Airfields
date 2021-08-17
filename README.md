Interesting alternative to the Travelling Salesman Problem

Inspiration:  Whilst playing the F16 flight simulator game, Falcon BMS, I wondered if it was possible to find the quickest route to visit every airfield once (airbase, airstrip etc.).
              There is no need to return to the starting airfield so basically start at one airfiled and fly all over the map visiting all the others.
              This is a learning exerice for me to implement a number of classical and non-classic algorithms and to understand the strengths and weaknesses.

Techqiues used: Haversine formula to calculate the distance in miles between 2 pairs of Latitude/Longditude location (formula accounts for the curvature of the Earth).
                Greedy Algorithm (minimum continous route) - Simple algorithm that looks for next closest airfield in a continous route
                Genetic Algorithm - Alternative, more complex algorithm whichi may avoid getting stuck in a local minimum (i.e the greedy algorithm)

Languages/Packages: Python with Pandas and NumPy.

