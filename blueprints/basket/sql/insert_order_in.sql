insert orders(inner_user_id, date_time, Sum) values ($id, now(), $sum);
set @$us$id = (select ID from orders where ID not in (select distinct order_id from order_details) and inner_user_id = $id);
