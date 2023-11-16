select Date, Time, Title as Film, Name as Zal, Ratio from seans
left join films on seans.film_ID = films.ID
left join zal on seans.zal_ID = zal.ID
where datediff(curdate(), Date) <= $d and datediff(curdate(), Date) >= 0
order by Date DESC, Time, Zal;