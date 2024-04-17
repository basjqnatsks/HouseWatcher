drop table IF EXISTS mytable;
drop table IF EXISTS lasts;
drop table IF EXISTS lastsfinal;


CREATE TEMP TABLE mytable AS
select z.ticker,t.dateprice--,
from (
select distinct s.ticker
from simulator s
) z
cross join public.marketcalender t;


CREATE TEMP TABLE lasts AS
select distinct ticker from simulator s;

CREATE TEMP TABLE lastsfinal AS
select *,
(select st.dateprice from simulator st where st.ticker = l.ticker order by st.dateprice desc limit 1) as top,
(select st.dateprice from simulator st where st.ticker = l.ticker order by st.dateprice asc limit 1)as bottom
 from lasts l;


select *
from simulator s
full join mytable t on  s.dateprice = t.dateprice and s.ticker = t.ticker
left join lastsfinal lf on t.ticker = lf.ticker
 where
s.dateprice is NULL and s.ticker is NULL
and t.dateprice >= bottom and t.dateprice <= top

--  t.database = s.database and s.ticker=t.ticker and

;





