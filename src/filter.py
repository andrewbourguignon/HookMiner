def filter_videos(videos, min_views=1000000):
    """
    Filters the list of videos, keeping only those with views >= min_views.
    Returns the filtered list.
    """
    filtered = []
    for video in videos:
        # Some platforms might not expose view_count, default to 0
        views = video.get('views') or 0
        if views >= min_views:
            filtered.append(video)
            
    print(f"Filtered {len(videos)} down to {len(filtered)} viral videos (>={min_views} views).")
    return filtered
