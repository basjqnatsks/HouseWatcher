drop table IF EXISTS crossed;
drop table IF EXISTS tickers;
drop table IF EXISTS lastsfinal;
drop table IF EXISTS SIMTICKDATE;
drop table IF EXISTS INVlastsfinal;
--select all possible cominations ticker | date
CREATE TEMP TABLE tickers AS
select distinct s.ticker
from simulator s;


-- CREATE TEMP TABLE crossed AS
-- select z.ticker,t.dateprice--,
-- from  tickers z
-- cross join public.marketcalender t;


CREATE TEMP TABLE INVlastsfinal AS
select *,
(select st.dateprice from simulator st where st.ticker = l.ticker   order by st.dateprice desc limit 1) as top,
(select st.dateprice from simulator st where st.ticker = l.ticker order by st.dateprice asc limit 1)as bottom
 from tickers l;

CREATE TEMP TABLE SIMTICKDATE AS
select distinct ticker,dateprice
from simulator s;



select * from SIMTICKDATE s
full join mytable t on  s.dateprice = t.dateprice and s.ticker = t.ticker
left join INVlastsfinal lf on t.ticker = lf.ticker
 where
s.dateprice is NULL and s.ticker is NULL
and t.dateprice >= bottom and t.dateprice <= top

--  t.database = s.database and s.ticker=t.ticker and

;





