select extract(DAY from seans.Date) as Day, sum(tickets.price) as Revenu
from seans
left join tickets
on tickets.seans_ID = seans.ID and tickets.Sold = True
where extract(YEAR_MONTH from seans.Date) = $y$m
group by Day
order by Day;