#Импортируйте библиотеку pandas как pd
import pandas as pd

#Загрузите датасет bookings.csv с разделителем ;
file_path = r'C:\Users\tvoya\Desktop\Python Projects\CSV\bookings.csv'
booking = pd.read_csv(file_path, sep = ';')

#Приведите названия колонок к нижнему регистру и замените пробелы на знак нижнего подчеркивания
booking.columns = booking.columns.str.lower().str.replace(' ', '_')

#Проверьте размер таблицы
rows, columns = booking.shape
# print(f'В таблице Bookings {columns} столбцов и  {rows} строк.')

#Проверьте типы переменных
types = booking.dtypes

#выведите первые 7 строк, чтобы посмотреть на данные
rows_7 = booking.head(7)

# Вывести DataFrame с обновленными названиями колонок
#print(Types)

#Пользователи из каких стран совершили наибольшее число успешных бронирований? Укажите топ-5.
top_5_country = booking.query('is_canceled == 0') \
    .groupby(['country']) \
    .aggregate({'is_canceled': 'count'})\
    .sort_values('is_canceled', ascending=False)\
    .head(5)

top_5_country_2 = booking.loc[booking.is_canceled == 0].country.value_counts().head(5)

#На сколько ночей (stays_total_nights)  в среднем бронируют отели типа City Hotel? Resort Hotel?
# Запишите полученные значения в пропуски с точностью до 2 знаков после точки.
stays_mean_nights_by_city_hotel, stays_mean_nights_by_resort_hotel  = booking.groupby(['hotel']).stays_total_nights.mean()

#
# print(f'Среднее число забронированных ночей в отелях типа city hotel: {round(stays_mean_nights_by_city_hotel,2)} 'f'. В resort hotel: {round(stays_mean_nights_by_resort_hotel, 2)}')

#Иногда тип номера, полученного клиентом (assigned_room_type), отличается от изначально забронированного (reserved_room_type).
# Такое может произойти, например, по причине овербукинга.
room_type_checks = booking.query('assigned_room_type != reserved_room_type').shape[0]
room_type_checks_2 = len(booking.loc[booking.assigned_room_type != booking.reserved_room_type])

#Теперь проанализируйте даты запланированного прибытия (arrival_date_year).
#На какой месяц чаще всего оформляли бронь в 2016 году? Изменился ли самый популярный месяц в 2017 году?
anal_arrival_date = booking.query('arrival_date_year == 2016 | arrival_date_year == 2017').groupby(['arrival_date_year']).value_counts(['arrival_date_month'])
anal_arrival_date_2 = booking.groupby('arrival_date_year').arrival_date_month.agg(pd.Series.mode)

# Сгруппируйте данные по годам, а затем проверьте, на какой месяц (arrival_date_month) бронирования отеля типа City Hotel отменялись чаще всего в 2015? 2016? 2017?
canceled_booking = booking.query('is_canceled == 1').groupby('arrival_date_year')['arrival_date_month'].value_counts()
canceled_booking_2 = booking.groupby(['arrival_date_year','arrival_date_month']).is_canceled.sum().groupby(['arrival_date_year']).nlargest(1)

#Посмотрите на числовые характеристики трёх колонок: adults, children и babies. Какая из них имеет наибольшее среднее значение?
the_mean = booking[['adults', 'children', 'babies']].mean()

#Создайте колонку total_kids, объединив столбцы children и babies. Для отелей какого типа среднее значение переменной оказалось наибольшим?
booking['total_kids'] = booking.children + booking.babies
bookin_kids = booking.groupby('hotel').agg({'total_kids' : 'mean'}).round(2)

#Не все бронирования завершились успешно (is_canceled), поэтому можно посчитать, сколько клиентов было потеряно в процессе.
# Иными словами, посчитать метрику под названием Churn Rate.


#Не все бронирования завершились успешно (is_canceled), поэтому можно посчитать, сколько клиентов было потеряно в процессе.
#Иными словами, посчитать метрику под названием Churn Rate.
#Churn rate (отток, коэффициент оттока) – это процент подписчиков (например, на push-уведомления от сайта), которые отписались от канала коммуникации, отказались от услуг сервиса в течение определенного периода времени.
#Иными словами, представляет собой отношение количества ушедших пользователей к общему количеству пользователей, выраженное в процентах.
#В нашем случае Churn Rate - это процент клиентов, которые отменили бронирование. Давайте посмотрим, как эта метрика связана с наличием детей у клиентов!
#Создайте переменную has_kids, которая принимает значение True, если клиент при бронировании указал хотя бы одного ребенка (total_kids), в противном случае – False.
#Далее проверьте, среди какой группы пользователей показатель оттока выше.
booking['has_kids'] = booking.total_kids > 0
churn_rate = booking.query('is_canceled == 1 and has_kids == False').shape[0] / booking.query(' has_kids == False').shape[0]




