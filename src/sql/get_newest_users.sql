select distinct on (id) * 
from twitter_user 
order by id, version desc;