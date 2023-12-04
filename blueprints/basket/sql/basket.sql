select tickets.ID as ID, tickets.RowOfSeat as RowOfSeat, tickets.Seat as Seat, tickets.Price as Price from tickets
join seans on seans.ID = tickets.seans_ID
where seans.ID = $id and tickets.Sold = False and tickets.ID not in $bas
order by RowOfSeat, Seat;