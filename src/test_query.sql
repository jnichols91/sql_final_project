-- select f.*, r.eco_id, r.eco_region
-- from fires as f, regions as r
-- where f.fpa_id = r.fpa_id;


select f.state, r.eco_region, count(*)
from fires as f, regions as r
where f.fpa_id = r.fpa_id
group by f.state, r.eco_region;
