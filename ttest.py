import pandas as pd
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
          'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    """Returns a DataFrame of towns and the states they are in from the university_towns.txt list."""
    with open('university_towns.txt') as file:
        data = []
        for line in file:
            data.append(line[:-1])
    state_town = []
    for line in data:
        if line[-6:] == '[edit]':
            state = line[:-6]
        elif '(' in line:
            town = line[:line.index('(') - 1]
            state_town.append([state, town])
        else:
            town = line.rstrip()
            state_town.append([state, town])
    return pd.DataFrame(state_town, columns=["State", "RegionName"])


def get_recession_start():
    """Returns the year and quarter of the recession start time as a string value in a format such as 2005q3"""
    gdp = pd.read_excel('gdplev.xls', skiprows=7)
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.iloc[212:]
    gdp.columns = ['Quarter', 'GDP']

    recession_start = []
    for year in range(len(gdp) - 2):
        if (gdp.iloc[year][1] > gdp.iloc[year + 1][1]) & (gdp.iloc[year + 1][1] > gdp.iloc[year + 2][1]):
            recession_start.append(gdp.iloc[year][0])
    return recession_start[0]


def get_recession_end():
    """Returns the year and quarter of the recession end time as a string value in a format such as 2005q3"""
    gdp = pd.read_excel('gdplev.xls', skiprows=7)
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.iloc[212:]
    gdp.columns = ['Quarter', 'GDP']

    recession_end = []
    for year in range(len(gdp) - 4):
        if (gdp.iloc[year][1] > gdp.iloc[year + 1][1]) & (gdp.iloc[year + 1][1] > gdp.iloc[year + 2][1]) & (
                gdp.iloc[year + 2][1] < gdp.iloc[year + 3][1]) & (gdp.iloc[year + 3][1] < gdp.iloc[year + 4][1]):
            recession_end.append(gdp.iloc[year + 4][0])
    return recession_end[0]


def get_recession_bottom():
    """Returns the year and quarter of the recession bottom time as a string value in a format such as 2005q3"""
    start = get_recession_start()
    end = get_recession_end()
    gdp = pd.read_excel('gdplev.xls', skiprows=7)
    gdp = gdp[['Unnamed: 4', 'Unnamed: 5']]
    gdp = gdp.iloc[212:]
    gdp.columns = ['Quarter', 'GDP']
    gdp = gdp.set_index('Quarter')
    gdp = gdp.loc[start:end]
    return gdp['GDP'].idxmin()


def convert_housing_data_to_quarters():
    """Converts the housing data to quarters and returns it as mean values in a dataframe. This dataframe has columns
    from 2000q1 through 2016q3, and a multi-index in the shape of ["State","RegionName"]."""
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing = housing.drop(housing.columns[[0] + list(range(3, 51))], axis=1)
    qhouse = pd.DataFrame(housing[['State', 'RegionName']])
    for year in range(2000, 2017):
        qhouse[str(year) + 'q1'] = housing[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis=1)
        qhouse[str(year) + 'q2'] = housing[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis=1)
        if year == 2016:
            qhouse[str(year) + 'q3'] = housing[[str(year) + '-07', str(year) + '-08']].mean(axis=1)
        else:
            qhouse[str(year) + 'q3'] = housing[[str(year) + '-07', str(year) + '-08', str(year) + '-09']].mean(axis=1)
            qhouse[str(year) + 'q4'] = housing[[str(year) + '-10', str(year) + '-11', str(year) + '-12']].mean(axis=1)
    qhouse['State'] = [states[state] for state in qhouse['State']]
    qhouse = qhouse.set_index(['State', 'RegionName'])
    return qhouse


def run_ttest():
    """First creates new data showing the decline or growth of housing prices between the recession start and the
    recession bottom. Then runs a ttest comparing the university town values to the non-university towns values, return
    whether the alternative hypothesis (that the two groups are the same) is true or not as well as the p-value of the
    confidence.

    Returns the tuple (different, p, better) where different=True if the t-test is True at a p<0.01 (we reject the null
    hypothesis), or different=False if otherwise (we cannot reject the null hypothesis). The value for better is either
    "university town" or "non-university town" depending on which has a lower mean price ratio (which is equivalent to a
    reduced market loss)."""

    unitowns = get_list_of_university_towns()
    bottom = get_recession_bottom()
    start = get_recession_start()
    house = convert_housing_data_to_quarters()
    before_start = house.columns[house.columns.get_loc(start) - 1]

    house['ratio'] = house[before_start] / house[bottom]
    house = house[[bottom, before_start, 'ratio']]
    house = house.reset_index()

    house_unitown = pd.merge(house, unitowns, how='inner', on=['State', 'RegionName'])
    house_unitown['University Town'] = True
    house_unitown2 = pd.merge(house, house_unitown, how='outer',
                              on=['State', 'RegionName', before_start, bottom, 'ratio'])
    house_unitown2['University Town'] = house_unitown2['University Town'].fillna(False)

    university_towns = house_unitown2[house_unitown2['University Town'] == True]
    non_university_towns = house_unitown2[house_unitown2['University Town'] == False]
    t, p = ttest_ind(university_towns['ratio'].dropna(), non_university_towns['ratio'].dropna())
    different = True if p < 0.01 else False
    better = "university town" if university_towns['ratio'].mean() < non_university_towns[
        'ratio'].mean() else "non-university town"
    return different, p, better


if __name__ == '__main__':
    print(run_ttest())
