select  DISTINCT database
from public.simulator


select  ticker
from public.simulator
ORDER BY ticker DESC
limit 1
drop

-- drop table public.simulator
select  count(*)
from public.simulator
limit 1


truncate table simulator

select  *
from public.simulator
limit 1000