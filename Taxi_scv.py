import pandas as pd
taxi = pd.read_csv(r'C:\Users\tvoya\Desktop\Python Projects\CSV\2_taxi_nyc.csv')

# сколько всего строк и столбцов имеется в датасете
rows_colums = taxi.shape

#Давайте посмотрим на типы колонок. Все ли из них считались правильно? В качестве ответа выберите тип, преобладающий в датасете.
types = taxi.dtypes

taxi = taxi.rename(columns={'pcp 01': 'pcp_01',
               'pcp 06' : 'pcp_06',
               'pcp 24' : 'pcp_24',
               })

#Вас попросили узнать, сколько записей (строк) в датафрейме относятся к району Манхэттен (Manhattan).\
# Получить ответ на данный вопрос можно было бы, например, с помощью следующей команды:
Brooklyn = taxi.query("borough == 'Brooklyn'").shape[0]

#выяснить, из какого района было совершено наибольшее количество поездок за весь период.
pickups = taxi.aggregate({'pickups' : 'sum'}) #общее количество поездок (pickups) без группировки
pickups_borough = taxi.groupby(['borough']).aggregate({'pickups' : 'sum'}) #по району (borough)

#Ускорить данный процесс в дальнейшем помогут методы idxmin() и idxmax(),
# которые возвращают индекс минимального или максимального значения.
min_pickups = pickups_borough.idxmin()
max_pickups = pickups_borough.idxmax()

#Сгруппируйте данные по двум признакам: району города и является ли день выходным
#hday – является ли день праздничным/выходным; Y – да, N – нет
pickups_weekends = taxi.groupby(['borough', 'hday']).pickups.mean()

#Для каждого района посчитайте число поездок по месяцам. Отсортируйте полученные значения по убыванию
pickups_by_mon_bor = taxi.groupby(['pickup_month', 'borough'], as_index = False).aggregate({'pickups' : 'sum'}).sort_values('pickups', ascending=False)

#получает на вход колонку с температурой в °F и возвращает значения, переведённые в градусы Цельсия
def temp_to_celcius(temp):
    temp = ((temp -32) * 5.0) / 9.0
    return temp

#команда примения функции
taxi.temp.apply(temp_to_celcius))