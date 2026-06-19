select
	c.first_name,
	c.last_name,
	a.address,
	ci.city
from customer c
join address a on c.address_id = a.address_id 
join city ci on a.city_id = ci.city_id 
limit 10;

select
	f.title,
	count(r.rental_id) as times_rented
from film f
join inventory i on f.film_id = i.film_id 
join rental r on i.inventory_id = r.inventory_id 
group by f.title 
order by times_rented desc
limit 10;

select
	c.first_name,
	c.last_name,
	p.amount,
	sum(p.amount) over (partition by c.customer_id) as total_spent
from customer c
join payment p on c.customer_id = p.customer_id
order by total_spent desc
limit 20;

select
	first_name,
	last_name,
	total_spent,
	rank() over (order by total_spent desc) as spend_rank
from (
	select
		c.customer_id,
		c.first_name,
		c.last_name,
		sum(p.amount) as total_spent
	from customer c
	join payment p on c.customer_id = p.customer_id 
	group by c.customer_id, c.first_name, c.last_name 
) as customer_totals
limit 20;