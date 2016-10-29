import numpy as np
import pandas as pd
import sqlite3

# Create a connection and create the db
conn = sqlite3.connect('IPF_data.db')

# Create the cursor for use
c = conn.cursor()

# Create table ipf
c.execute('''CREATE TABLE ipf (lifter text, birth_year integer, team text,
                                body_weight real, best_squat real, best_bench real,
                                best_deadlift real, total real, year integer,
                                sex text, division text)''')

# Insert data into ipf
for i in np.array(pd.read_csv('Data_Total_Table_1.csv')):
    sql_insert = "INSERT INTO ipf VALUES ('{}',{},'{}',{},{},{},{},{},{},'{}','{}')".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10])
    c.execute(sql_insert)

'''Some feature engeneering'''
df = pd.read_csv('Data_Total_Table_1.csv')
df = df[:1369]
df['bench/squat'] = df['Best Bench'] / df['Best Squat']

weight_class = []
for _, lifter in df.iterrows():
    weights = [(0.0,50.0),(50.0,60.0),(60.0,70.0),(70.0,80.0),(80.0,90.0),(90.0,100.0),\
                                                                           (100.0,110.0),(110.0,120.0),(120.0,200.0)]
    for w_class in weights:
        bottom = w_class[0]
        top = w_class[1]
        if (lifter['Body Weight'] > bottom) and (lifter['Body Weight'] <= top):
            weight_class.append(top)
df['weight_class'] = pd.Series(weight_class)

squat_class = []
for _, lifter in df.iterrows():
    squat_range =[(0.0,50.0),(50.0,60.0),(60.0,70.0),(70.0,80.0),(80.0,90.0),(90.0,100.0),(100.0,110.0),(110.0,120.0),\
               (120.0,130.0),(130.0,140.0),(140.0,150.0),(150.0,160.0),(160.0,170.0),(170.0,180.0),(180.0,190.0),\
               (190.0,200.0),(200.0,210.0),(210.0,220.0),(220.0,230.0),(230.0,240.0),(240.0,250.0),(250.0,260.0),\
               (260.0,270.0),(270.0,280.0),(280.0,290.0),(290.0,300.0),(300.0,310.0),(310.0,320.0),(320.0,330.0),\
               (330.0,340.0),(340.0,350.0),(350.0,360.0),(360.0,370.0),(370.0,380.0),(380.0,390.0),(390.0,400.0),\
               (400.0,410.0),(410.0,420.0),(420.0,430.0),(430.0,440.0),(440.0,450.0),(450.0,460.0),(460.0,470.0),\
               (470.0,480.0),(480.0,490.0)]

    for s_range in squat_range:
        bottom = s_range[0]
        top = s_range[1]
        if (lifter['Best Squat'] > bottom) and (lifter['Best Squat'] <= top):
            squat_class.append(top)
df['squat_class'] = pd.Series(squat_class)

df_Open = df[df.Division == 'Open']
df_Classic = df[df.Division == 'Classic']
'''---------------------------------------------------------------------'''

# Create table open
c.execute('''CREATE TABLE open (lifter text, birth_year integer, team text,
                                body_weight real, best_squat real, best_bench real,
                                best_deadlift real, total real, year integer,
                                sex text, division text, bench_squat_ratio real,
                                weight_class integer, squat_class integer)''')

# Insert data into open
for i in np.array(df_Open):
    sql_insert = "INSERT INTO open VALUES ('{}',{},'{}',{},{},{},{},{},{},'{}','{}',{},{},{})".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13])
    c.execute(sql_insert)


# Create table classic
c.execute('''CREATE TABLE classic (lifter text, birth_year integer, team text,
                                body_weight real, best_squat real, best_bench real,
                                best_deadlift real, total real, year integer,
                                sex text, division text, bench_squat_ratio real,
                                weight_class integer, squat_class integer)''')

# Insert data into classic
for i in np.array(df_Classic):
    sql_insert = "INSERT INTO classic VALUES ('{}',{},'{}',{},{},{},{},{},{},'{}','{}',{},{},{})".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13])
    c.execute(sql_insert)

# Save (commit) the changes
conn.commit()

# Close the connection to sql db
# Just be sure any changes have been committed or they will be lost.
conn.close()
