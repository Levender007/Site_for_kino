select films.Title as Title, zal.Name as Name, seans.Date as Date, seans.Time as Time from seans
join films on films.ID = seans.film_ID
join zal on zal.ID = seans.zal_ID
where seans.ID = $id;