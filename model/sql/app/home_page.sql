select ID, Title, Duration, PosterURL from films
where ID in (select distinct film_ID from seans where Date > curdate() or (Date = curdate() and Time >= curtime()))