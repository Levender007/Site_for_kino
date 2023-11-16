select zal.Name as Name, seans.Time as Time, sum(tickets.Price) as Income from seans
join zal on zal.ID = seans.zal_ID
left join tickets on tickets.seans_ID = seans.ID and tickets.Sold = True
where seans.Date = $y$m$d
group by seans.ID
order by Time, Name;