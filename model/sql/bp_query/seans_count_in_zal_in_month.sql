select zal.Name as Name, count(*) as SeansCount from seans
right join zal on seans.zal_ID = zal.ID
where extract(year_month from seans.Date) = $y$m
group by zal.Name
order by zal.Name;