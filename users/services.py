import datetime
def get_years():
    return [(year,year) for year in range(2018, datetime.date.today().year+1)][::-1]