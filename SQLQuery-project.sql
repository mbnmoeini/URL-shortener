create table links(
    link_id int primary key identity(1,1),
    original_link nvarchar(100) not null,
    shortened_link nvarchar(50) not null,
    created_date datetime default GETDATE(),
    references_count int default 0,
    expired bit default 0
)

CREATE TABLE references_link(
    references_id int primary key identity(100,1),
    shortened_link nvarchar(50) not null,
    reference_date datetime default GETDATE()
)

--Triggers
--this is a trigger for counting referced links 
create trigger count_references
on references_link
after INSERT
as
begin
update links
set references_count = references_count + 1
from links inner join inserted on links.shortened_link = inserted.shortened_link
end


--peocedures
--this is a procedure for finding the top 3 referred links
create procedure top_links
as
begin
select top 3
shortened_link,
references_count
from links
where expired = 0
order by references_count desc;
end

--functions
--this is a function to fetch links with its expiration and reference count
create function link_maps()
returns table
as
return(
select shortened_link, DATEDIFF(DAY, GETDATE(), DATEADD(WEEK, 1, created_date)) as remaining_time, references_count
from links
where expired = 0
)

select * from links
select * from references_link
