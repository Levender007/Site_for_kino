select Date, Time, Title as Film, Name as Zal, Ratio from seans
left join films on seans.film_ID = films.ID
left join zal on seans.zal_ID = zal.ID
where extract(year_month from seans.Date) = $y$m
order by Date, Time, Zal;