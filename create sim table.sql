drop INDEX simulator_ticker_dateprice_idx;
drop INDEX  idx_simulator_ticker;
drop INDEX idx_all_simulator;






CREATE INDEX IF NOT EXISTS idx_all_simulator
    ON public.simulator USING btree
    (dateprice ASC NULLS LAST, openprice ASC NULLS LAST, highprice ASC NULLS LAST, lowprice ASC NULLS LAST, closeprice ASC NULLS LAST, adjprice ASC NULLS LAST, volume ASC NULLS LAST, database COLLATE pg_catalog."default" ASC NULLS LAST, ticker COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: public.idx_simulator_ticker
CREATE INDEX IF NOT EXISTS idx_simulator_ticker
    ON public.simulator USING btree
    (ticker COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: public.simulator_ticker_dateprice_idx
CREATE INDEX IF NOT EXISTS simulator_ticker_dateprice_idx
    ON public.simulator USING btree                                      
    (ticker COLLATE pg_catalog."default" ASC NULLS LAST, dateprice ASC NULLS LAST)
    TABLESPACE pg_default;