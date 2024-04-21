CREATE OR REPLACE PROCEDURE RemoveDuplicateSimulator()

AS 
$$
 DECLARE
 begin
drop table IF EXISTS tickers;
drop table IF EXISTS SimualtorToInsert;

CREATE TEMP TABLE tickers AS
select ticker,dateprice,database
from public.simulator
group by ticker,dateprice,database
having count(*) > 1;

CREATE TEMP TABLE SimualtorToInsert AS
select  distinct s.dateprice,	s.openprice	,s.highprice	,s.lowprice,	s.closeprice	,s.adjprice	,s.volume	,s.database,s.ticker
from simulator s
inner join tickers t 
on t.ticker = s.ticker and t.database = s.database and t.dateprice = s.dateprice;

delete 
from simulator s
USING tickers t 
where t.ticker = s.ticker and t.database = s.database and t.dateprice = s.dateprice;

insert into simulator
select * from SimualtorToInsert;

  END;
$$ LANGUAGE plpgsql;