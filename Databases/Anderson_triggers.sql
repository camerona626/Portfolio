/*
If games started in greater than games played on insert or delete,
games started is changed to games played
 */
delimiter //
CREATE TRIGGER games_started_update
BEFORE update ON Seasons
FOR EACH ROW
BEGIN
	IF New.games < New.games_started THEN
			SET New.games_started = New.games;
	END IF;
END //

CREATE TRIGGER games_started_insert
BEFORE insert ON Seasons
FOR EACH ROW
BEGIN
	IF New.games < New.games_started THEN
			SET New.games_started = New.games;
	END IF;
END //
delimiter ;

/*
When a player is removed from the Players table,
that players games and seasons are removed as well.
*/
delimiter // 
create trigger delete_player
before delete on Players
for each row
begin
	delete from Seasons where id = OLD.id;
	delete from Games where id = OLD.id;
END //
delimiter ;

/*
Given a player id and a year, calculates the qb rating for
that player for that year
*/
delimiter //
CREATE FUNCTION qb_rating_season (pid varchar(8), pyear year) RETURNS float
begin
	declare rating float;
	declare comp float;
	declare att float;
	declare td float;
	declare ints float;
	declare yards float;
	declare a float;
	declare b float;
	declare c float;
	declare d float;

	select completions into comp from Seasons where pid = id and `year` = pyear;
	select pass_attempts into att from Seasons where pid = id and `year` = pyear;
	select pass_td into td from Seasons where pid = id and `year` = pyear;
	select interceptions into ints from Seasons where pid = id and `year` = pyear;
	select pass_yards into yards from Seasons where pid = id and `year` = pyear; 
	
	set a = ((comp / att) - .3) * 5;
	if a < 0 THEN
		SET a = 0;
	ELSEIF a > 2.375 THEN
		SET a = 2.375;
	END if; 

	set b = ((yards / att) - 3) * .25;
	if b < 0 THEN
		set b = 0;
	ELSEIF b > 2.375 THEN
		SET b = 2.375;
	END IF;

	set c = (td / att) * 20;
	IF c > 2.375 THEN
		SET c = 2.375;
	END IF;

	set d = 2.375 - ((ints / att) * 25);
	IF d < 0 THEN
		SET d = 0; 
	END IF;

	set rating = ((a + b + c + d) / 6) * 100;
	RETURN rating;

END //
delimiter ;

