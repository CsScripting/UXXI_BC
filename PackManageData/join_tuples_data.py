from PackLibrary.librarys import (	
  DataFrame,
  where,
  to_datetime,
  datetime,
  timedelta,
  Series
)


from mod_variables import *

def group_entities(df, list_series, sep = ',', sort_flag = True):
    
    #Por vezes valores numericos tem o . (No entanto não se pode tratar aqui, pode haver campos com o .)
    # df = df.applymap(str).replace('\.0', '', regex=True)
    df.set_index (list_series, inplace=True)
    df = df.groupby (level = list_series, sort = sort_flag).agg(sep.join)
    df.reset_index(inplace=True)
    return df


def weekly_date (df, series_dates):

	for val in series_dates:
	
		df[val] = to_datetime(df[val], dayfirst = True)
		df['week_day_temp'] = df[val].apply(lambda x: x.weekday())
		df[val] = df[val] - df['week_day_temp'] * timedelta(days=1) 
		df.drop (['week_day_temp'], axis = 1,inplace = True)
    
	return df

def asign_weeks (df, begin_date, end_date, name_new_serie = 'WEEKS_EVENT'):
    
    for ind, row in df.iterrows():
        valuesWeeks = []
        valuesNew_str = {}
        weekly_begin = row[begin_date].date()
        weekly_end = row[end_date].date()
        
        if weekly_begin <= weekly_end:
            while weekly_begin <= weekly_end:
                
                if weekly_begin == weekly_end:
                    add_week = weekly_begin.strftime("%Y-%m-%d")
                    valuesWeeks.append(add_week)
                    valuesNew_str = ','.join(valuesWeeks)
                    weekly_begin = weekly_begin + datetime.timedelta(days=7)
                    df.loc[ind,name_new_serie] = valuesNew_str
                else:
                    add_week = weekly_begin.strftime("%Y-%m-%d")
                    valuesWeeks.append(add_week)
                    weekly_begin = weekly_begin + datetime.timedelta(days=7)
                    valuesNew_str = ','.join(valuesWeeks)
                    df.loc[ind,name_new_serie] = valuesNew_str
        else:
            df.loc[ind,name_new_serie] = 'BeginDate > EndDate'
    
    df_valid = df[df[name_new_serie] != 'BeginDate > EndDate']
    df_invalid = df[df[name_new_serie] == 'BeginDate > EndDate']
    df_valid.drop([begin_date, end_date], axis = 1,inplace = True)
    
    return (df_valid, df_invalid)

def manage_weeks (df: DataFrame):

    series_dates = [v_week_begin, v_week_end]
    df = weekly_date (df, series_dates)
    df_valid_weeks, df_invalid = asign_weeks(df, v_week_begin, v_week_end)

    df_valid_weeks.sort_values(by = [v_course_name, v_year, v_mod_code,v_mod_typologie, 'WEEKS_EVENT'], inplace=True)

    df = df_valid_weeks.copy()

    df['Split_Weeks'] = where (df['WEEKS_EVENT'].str.contains(','), '0', '1')

    series_grouped = [v_course_name,v_course_code, v_year, v_mod_code,v_mod_name,v_mod_typologie, v_student_group, v_activity_code,v_student_group_code, v_day,
                      v_duration, v_hourBegin_split, v_hourEnd_split,v_minute_begin_split, v_minute_end_split, v_students_number]

    df = group_entities(df, series_grouped, sep=',')

    return(df, df_invalid)


def split_by_column(column,sep):
    
	return Series(column.str.cat(sep=sep).split(sep=sep))
	
	
def split_by_rows(df, name_serie, sep):	
    
	df= df.applymap(str)
	df_new = (df.groupby(df.columns.drop(name_serie).tolist()) 
	[name_serie]
	.apply(split_by_column,sep=sep) 
	.reset_index(drop=True,level=-1).reset_index()) 
	

	return (df_new)


