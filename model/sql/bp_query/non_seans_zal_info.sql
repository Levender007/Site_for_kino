select zal.Name as Name, zal.SeatsCount as SeatsCount from zal
left join seans on seans.zal_ID = zal.ID
where seans.zal_ID is NULL;