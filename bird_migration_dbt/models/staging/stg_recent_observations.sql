{{ config(materialized='table') }}

with final as (
    select *
    from read_csv_auto('data/recent_bird_obs.csv')
)

select *
from final
