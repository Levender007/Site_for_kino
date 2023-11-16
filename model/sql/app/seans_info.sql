select seans.Date as Date, seans.Time as Time, zal.Name as zal_Name from seans
join zal on zal.ID = seans.zal_ID
where (seans.Date > curdate() or (seans.Date = curdate() and seans.Time >= curtime())) and
seans.film_ID = $title
order by Date, Time, zal_Name