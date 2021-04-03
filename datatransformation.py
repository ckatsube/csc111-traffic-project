import pandas as pd
df = pd.read_csv('trafficdata.csv')
#tf = df['speed'] >= 0
fd = pd.DataFrame(df, columns=['time', 'segment_id', 'speed', 'street', 'direction',
                                'from_street', 'to_street', 'length', 'bus_count',
                                'hour', 'day_of_week', 'month'])
fd_one = fd[fd['speed'] != -1]
# print(fd_one.shape) outputs (1852701, 12), all negative speed values removed
