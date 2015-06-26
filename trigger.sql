ALTER TRIGGER [dbo].[LabelUpdate] ON [dbo].[Label]
AFTER UPDATE
AS
	DECLARE @tmp DATETIME2
	DECLARE @user NVARCHAR(100)
	DECLARE @new NVARCHAR(1000)
	DECLARE @old NVARCHAR(1000)
	SET @tmp = GETDATE()
	SET @user = USER
	select @old = LabelValue from deleted
	select @new =  LabelValue from inserted
	insert into dbo.History(TableName,ColumnName,Operation,OldValue,NewValue,ChangedBy,ChangeDate) values('Label','LabelValue','UPDATE',@old,@new,@user,@tmp);
	
GO

CREATE TRIGGER [dbo].[LabelInsert] ON [dbo].[Label]
AFTER INSERT
AS
	DECLARE @tmp DATETIME2
	DECLARE @user NVARCHAR(100)
	DECLARE @new NVARCHAR(1000)
	DECLARE @old NVARCHAR(1000)
	SET @tmp = GETDATE()
	SET @user = USER
	select @new =  LabelValue from inserted
	insert into dbo.History(TableName,ColumnName,Operation,OldValue,NewValue,ChangedBy,ChangeDate) values('Label','LabelValue','INSERT','-',@new,@user,@tmp);
	
GO

CREATE TRIGGER [dbo].[LabelDelete] ON [dbo].[Label]
AFTER Delete
AS
	DECLARE @tmp DATETIME2
	DECLARE @user NVARCHAR(100)
	DECLARE @new NVARCHAR(1000)
	DECLARE @old NVARCHAR(1000)
	SET @tmp = GETDATE()
	SET @user = USER
	select @old = LabelValue from deleted
	insert into dbo.History(TableName,ColumnName,Operation,OldValue,NewValue,ChangedBy,ChangeDate) values('Label','LabelValue','Delete',@old,'-',@user,@tmp);
	
GO

CREATE TRIGGER [dbo].[MenuUpdate] ON [dbo].[Menu]
AFTER UPDATE
AS
	DECLARE @tmp DATETIME2
	DECLARE @user NVARCHAR(100)
	DECLARE @new NVARCHAR(1000)
	DECLARE @old NVARCHAR(1000)
	SET @tmp = GETDATE()
	SET @user = USER
	select @old = MenuValue from deleted
	select @new =  MenuValue from inserted
	insert into dbo.History(TableName,ColumnName,Operation,OldValue,NewValue,ChangedBy,ChangeDate) values('Menu','MenuValue','UPDATE',@old,@new,@user,@tmp);
	
GO