CREATE OR REPLACE PROCEDURE RemoveDuplicateSimulator()

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


delete 
from simulator s
USING tickers t 
where t.ticker = s.ticker and t.database = s.database and t.dateprice = s.dateprice;



  END;
$$ LANGUAGE plpgsql;