/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) 
	[time]
		      ,[event]
      ,[t:applicationname]
      ,[t:computername]

      ,[method]
      ,[body]
      ,[clientid]
      ,[interface]
      ,[iname]

      ,[mname]


      ,[usr]

      ,[dbms]
      ,[database]
      ,[trans]
      ,[sdbl]
      ,[rows]
      ,[context]
      ,[sql]
      ,[dbpid]
      ,[rowsaffected]
      ,[func]

      ,[status]
      ,[phrase]
      ,[tablename]
      ,[callwait]
      ,[memory]
      ,[memorypeak]
      ,[inbytes]
      ,[outbytes]
      ,[cputime]


  FROM [tempdb].[dbo].[tjpy2]
  where sql<>''