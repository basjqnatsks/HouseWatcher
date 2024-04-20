CREATE TABLE FinancialDisclosure(
FirstName varchar(255), 
LastName varchar(255), 
StateDistrict varchar(10),
FilingType varchar(1), 
Year varchar(10), 
FilingDate TIMESTAMP,
DocID INT
)
CREATE TABLE Transactions(
FirstName varchar(255), 
LastName varchar(255), 
StateDistrict varchar(10),
TranType varchar(1), 
Owner varchar(10), 
Asset varchar(255), 
Ticker varchar(10), 
TransDate date, 
FilingId int ,
FilingDate date,
TradeDate date,
Amount money,
AmountLow int,
AmountHigh int,
NotificationDate date
)
