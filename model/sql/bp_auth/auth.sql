select users.ID as user_id, user_groups.Name as user_group from users
left join user_groups on users.user_group = user_groups.ID
where users.Login = '$login' and users.Pass = '$password';