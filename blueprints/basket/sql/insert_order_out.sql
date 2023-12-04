insert orders(outer_user_id, date_time, Sum) values ($id, now(), $sum);
set @$us$id = (select ID from orders where ID not in (select distinct order_id from order_details) and outer_user_id = $id);
