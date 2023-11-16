select Name, SeatsCount from zal
where SeatsCount = (select max(SeatsCount) from zal);