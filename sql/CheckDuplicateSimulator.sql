CREATE OR REPLACE FUNCTION GetDuplicateSimulator()

AS 
$$
 DECLARE
 begin
drop table IF EXISTS tickers;



CREATE TEMP TABLE tickers AS
select ticker,dateprice,database
from public.simulator
group by ticker,dateprice,database
having count(*) > 1;


select * 
from simulator s
inner join tickers t 
on t.ticker = s.ticker and t.database = s.database and t.dateprice = s.dateprice;



  END;
$$ LANGUAGE plpgsql;