select tickets.RowOfSeat as RowOfSeat, tickets.Seat as Seat, tickets.Price as Price from tickets
join seans on seans.ID = tickets.seans_ID
where tickets.ID = $prod_id;