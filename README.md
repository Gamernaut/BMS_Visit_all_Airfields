<h2>Interesting alternative to the Travelling Salesman Problem</h2>

<h3>Inspiration:</h3>
Whilst playing Falcon BMS, an F16 flight simulator, I wondered if it was possible to find the quickest/shortest route to visit every airfield in the sim once (i.e. every airbase, airstrip etc.). There would be no need to return to the starting airfield so it was more of a linear route than a circular route. <BR><BR> 

<h3>Techniques used:</h3>
<ul>
<li>Haversine formula to calculate the distance, in miles, between 2 pairs of Latitude/Longitude coordinates (formula accounts for the curvature of the Earth) </li>
<li>Greedy Algorithm (minimum continuous route) - Simple algorithm that looks for next closest airfield in a continuous route</li>
<li>Genetic Algorithm - Alternative, more complex algorithm which may avoid getting stuck in the same local minimum as the Greedy Minimum Continuous Route Algorithm </li>
</ul>

<h3>Languages/Packages:</h3>
<ul>
<li>Python 3.9 (PyCharm 2021 Community Editon IDE from JetBrains)</li>
<li>Pandas</li>
<li>NumPy</li>
</ul>
  
<BR><i>This is a learning exercise for me to implement a number of classical and non-classic algorithms to understand the strengths and weaknesses. </i><BR>
