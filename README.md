# Statistical Testing of the effect of Recession on the Housing Prices in University Towns

### Hypothesis: University towns have their mean housing prices less effected by recessions.

Performs a Student's t-test to validate the statistical significance of this hypothesis using real world data.

#### Files in the repository
* City_Zhvi_AllHomes.csv - Median home sale prices at a fine grained level for all homes at a city level from the [Zillow research data site](https://www.zillow.com/research/data/) for housing data in the United States.
* university_towns.txt - A list of university towns in the United States which has been copy pasted from the [Wikipedia page on college towns](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States)
* gdplev.xls - The [GDP over time](http://www.bea.gov/data/gdp/gross-domestic-product#gdp) of the United States in current dollars (using the chained value in 2009 dollars), in quarterly intervals from the Bureau of Economic Analysis, US Department of Commerce.
* ttest.py - Contains code for appropriate cleaning and pre-processing the data before performing the t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom.

#### Definitions of the terms used in the repository
* A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
* A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
* A recession bottom is the quarter within a recession which had the lowest GDP.
* A university town is a city which has a high percentage of university students compared to the total population of the city.
