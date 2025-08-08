{{ config(
    materialized='incremental',
    unique_key='observation_id'
) }}

with final as (
    select 
        speciesCode as species_code,
        comName as common_name,
        sciName as scientific_name,
        locId as location_id,
        locName as location_name,
        obsDt as observation_datetime,
        howMany as observation_count,
        lat as latitude,
        lng as longitude,
        obsValid as observation__is_valid,
        obsReviewed as observation__is_reviewed,
        locationPrivate as location__is_private,
        subId as submitted_by_id,
        exoticCategory as exotic_category,
        fetch_timestamp as fetch_datetime,
        md5(
            concat_ws('||',
                submitted_by_id,
                observation_datetime,
                species_code,
                location_id
            )
        ) as observation_id

    from read_csv_auto('data/recent_bird_obs.csv')
)

select *
from final

{% if is_incremental() %}

where observation_datetime > (select max(observation_datetime) from {{ this }})

{% endif %}
