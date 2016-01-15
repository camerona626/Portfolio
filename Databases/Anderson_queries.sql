/*
Returns all players who rushed for at least 1000 yards
during the 1987 season
*/
select p.lastname, p.firstname, s.rush_attempts, s.rush_yards, s.rush_td
from Players as p, Seasons as s
where p.id = s.id and s.rush_yards >= 1000 and s.`year` = 1987;

/*
Returns all players who rushed for a 1000 yards in a season
at least twice.
*/
select p.lastname, p.firstname, count(*)
from Players as p, Seasons as s
where p.id = s.id and s.rush_yards >= 1000
group by p.id
having count(*) >= 2
order by count(*) desc;

/*
Returns the 10 highest qb ratings for an individual in any season.
*/
select p.lastname, p.firstname, (qb_rating_season(p.id, s.`year`)) as rating, s.`year`, s.team
from Players as p, Seasons as s 
where s.id = p.id and s.position = 'qb' and p.id not in 
(select id from Seasons group by id, `year` having count(*) > 1)
and ((s.pass_attempts >= 191 and s.`year` < 1978) or 
(s.pass_attempts >= 255 and s.`year` >= 1978))
order by rating desc
limit 0, 10;

/*
Returns the 10 highest td totals in any game for and individual
*/
select p.lastname, p.firstname, g.total_td
from Players as p, Games as g
where p.id = g.id
order by g.total_td desc
limit 0, 10;