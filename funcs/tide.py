import re

import pandas as pd


def get_lunch_times(df: pd.DataFrame):
    dt0 = df.index[0]
    dt0_str = str(dt0)
    pattern = re.compile(r'.+([+\-][0-9]{2}:[0-9]{2})$')
    m = pattern.match(dt0_str)
    if m:
        tz = m.group(1)
    else:
        tz = ''
    date_str = str(dt0.date())
    dt_noon1 = pd.to_datetime('%s 11:30:00%s' % (date_str, tz))
    dt_noon2 = pd.to_datetime('%s 12:30:00%s' % (date_str, tz))
    return dt_noon1, dt_noon2
