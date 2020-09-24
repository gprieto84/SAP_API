--delete from SAP_notifications
--delete from SAP_notification_user_status
--delete from SAP_notification_system_status
--delete from SAP_status_log_system
--delete from SAP_status_log_user
--delete from SAP_functional_location
--delete from SAP_user_status
--delete from SAP_notification_type
--delete from SAP_system_status
--delete from SAP_user_status

--delete from SAP_notification_text
--delete from SAP_notification_activities
--delete from SAP_notification_activities_header
--delete from SAP_notification_catalog
--delete from SAP_notification_causes
--delete from SAP_equipments
--delete from SAP_equipment_text
--delete from SAP_work_center
--delete from SAP_functional_location
--delete from SAP_notification_user_status
--delete from SAP_notification_system_status
--delete from SAP_status_log_system
--delete from SAP_status_log_user
--delete from SAP_notification_system_status

--DBCC CHECKIDENT ('SAP_notification_text', RESEED, 0)  
--DBCC CHECKIDENT ('SAP_notification_activities', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_notification_activities_header', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_notification_causes', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_functional_location', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_equipment_text', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_notification_system_status', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_notification_user_status', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_status_log_system', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_status_log_user', RESEED, 0) 
--DBCC CHECKIDENT ('SAP_user_status', RESEED, 0) 

select * from SAP_work_center
select * from SAP_notifications where n_number like '%913068%' --QM000000913068 --QM000000868631
select * from SAP_notifications where obj_nr = 'QM000005423368'
select * from SAP_notification_type
select * from SAP_notification_activities where [group] like '%PARTE4%' and n_number='000000374431'
select * from SAP_notification_activities_header where [group] like '%PARTE4%' and code = '0015'
select * from SAP_notification_catalog where catalog='8'
select distinct(catalog) from SAP_notification_activities_header order by 1
select * from SAP_notification_catalog
select * from SAP_notification_causes
select * from SAP_notification_text
select * from SAP_equipments
select * from SAP_equipment_text
select * from SAP_work_center
select * from SAP_functional_location order by func_location
select * from SAP_system_status where status_id = 'I0072'
select * from SAP_user_status where code = 'GEAM'
--4400014255
select * from SAP_user_status order by status_id, status_schema
select * from SAP_notification_user_status where status_id = 'E0027' and [disabled] = '' and obj_nr in 
(select obj_nr from SAP_notification_system_status where status_id <> 'I0072')
select * from SAP_status_log_system
select * from SAP_status_log_user
--select * from SAP_notification_status where obj_nr = 'QM000005455491'
--QM000005444258

select distinct(created_by), count(0) as cantidad from SAP_notifications group by created_by order by cantidad desc





