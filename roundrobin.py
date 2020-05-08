import itertools
import pandas as pd


class Doodle():
    def __init__(self, doodle_fp="Doodle.xls", ipc=2):
        self.filepath = doodle_fp
        self.doodle = {}
        self.robin_cal = {}
        self.int_per_cand = ipc
        self.interviewers = {}

    def read_xls_to_dataframe(self):
        read_file = pd.read_excel(self.filepath, sheet_name='Poll', encoding='utf-8')
        read_file.to_csv(r'Doodle.csv', encoding='utf-8', index=None, header=True)
        self.doodle = pd.read_csv("Doodle.csv",
                             skiprows=3,
                             skip_blank_lines=True,
                             header=None,
                             encoding='utf-8',
                             squeeze=True,
                             keep_default_na=False
                             )[:-1]


    def clean_date_data(self, df):
        patch_date = True
        ym = '' # Stores year/month
        wd = '' # Stores week/day
        for index, row in df.iterrows():
            if index == 0:
                # Get year and month in variables
                year_month = row.to_dict()
                continue
            if index == 1:
                # Get days
                week_day = row.to_dict()
                continue
            if index == 2:
                # If empty match cycle with index 1, to add the date
                hour_segments = row.to_dict()
                continue

            # Patches the date to have the week/day and year/month
            if patch_date:
                for key, value in year_month.items():
                    # Stores the year/month to use later
                    if value != '':
                        ym = value
                    # Stores week/day to use later
                    if week_day[key] != '':
                        wd = week_day[key]
                    else:
                        week_day[key] = wd
                    hour_segments[key] = wd + ' ' + ym + ' ' + hour_segments[key]
                break;
        # Creates new row to add
        new_row = pd.DataFrame(hour_segments, index=[0])
        # Deletes the previous split dates
        df = df.drop([0, 1, 2])
        # Concatenates at the top
        self.doodle = pd.concat([new_row, df]).reset_index(drop=True)


    def get_interviewers_available(self, df):
        interviewers = {}
        for index, row in df.iterrows():
            # Skips empty lines of interviewers
            if row[0].strip() == '':
                continue
            # Stores availabilities for each user
            availabilities = {}
            for key, value in row[1:].to_dict().items():
                if value.strip() == '':
                    continue
                availabilities[key] = df.iloc[0][key]

            availabilities = [(value) for key, value in availabilities.items()]
            interviewers[row[0]] = availabilities
        self.interviewers = interviewers


    def get_cal_robin_dict(self):
        # Doodle needs to be exported to xls
        # Parse xls to csv
        self.read_xls_to_dataframe()
        self.clean_date_data(self.doodle)
        # Matches interviewers with available dates
        # Generate one dict with names as keys and availabilities as values
        self.get_interviewers_available(self.doodle)
        # Number of interviews per candidate
        int_per_cand = 2
        # Pair up the interviewers
        roundrobin = list(itertools.combinations(self.interviewers.keys(),
                                                 self.int_per_cand))
        # Match roundrobin with possible calendar availability
        robin_cal = {}
        for pair in roundrobin:
            calendar_intersect = list(set(self.interviewers[pair[0]])
                                      .intersection(self.interviewers[pair[1]])
                                      )
            robin_cal[pair] = calendar_intersect
        self.robin_cal = robin_cal


if __name__ == "__main__":
    int_per_cand = 2
    rcal = Doodle(r'Doodle.xls', int_per_cand)
    rcal.get_cal_robin_dict()
    for elem in rcal.robin_cal.items():
        print(elem)
