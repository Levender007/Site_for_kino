select product.Name as "Продукт", report_test1.revenu as "Доход" from supermarket.report_test1 as report_test1
join supermarket.product as product on product.ID = report_test1.prod_id
where report_test1.month = '$date-01'