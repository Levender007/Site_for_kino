select Name, sum(price * (LastSeat - FirstSeat + 1)) as Base from sheme
join zal on sheme.zal_ID = zal.ID
group by zal_ID
order by zal_ID;