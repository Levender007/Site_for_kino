select zal.Name as "Название зала", rep.Revenu as "Доход" from kino.report_monthzalrev as rep
join kino.zal as zal on zal.ID = rep.zal_ID
where rep.month ='$date-01'
order by zal.Name