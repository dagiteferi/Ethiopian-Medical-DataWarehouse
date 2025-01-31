-- models/example/transform_messages.sql

with cleaned_data as (
    select
        id,
        channel_title,
        channel_username,
        message_id,
        message,
        message_date,
        media_path,
        emoji_used,
        youtube_links,
        case 
            when emoji_used = 'No emoji' then false
            else true
        end as has_emoji,
        case 
            when youtube_links = 'No YouTube link' then false
            else true
        end as has_youtube_links
    from {{ source('telegram_data', 'telegram_messages') }}
)

select
    *,
    current_timestamp as transformed_at
from cleaned_data
