from .models import Media, Album, MediaTag, AlbumTag

class ContentRecommendationAlgorithm:
    def __init__(self, user):
        self.user = user

    def filter_media_by_tags(self, media_list, user_tags):
        if hasattr(self.user, 'tags'):
            user_tags_list = list(self.user.tags.values_list('value', flat=True))
            print(user_tags_list)
            return [media for media in media_list if user_tags_list and any(tag.value in media.tags.values_list('value', flat=True) for tag in user_tags)]
        else:
            return media_list

    def filter_albums_by_tags(self, album_list, user_tags):
        if hasattr(self.user, 'tags'):
            user_tags_list = list(self.user.tags.values_list('value', flat=True))
            return [album for album in album_list if user_tags_list and any(tag.value in album.tags.values_list('value', flat=True) for tag in user_tags)]
        else:
            return album_list

    def sort_media_by_user_engagement(self, media_list):
        # Assuming you have a 'likes' and 'comments' field in your Media model
        return sorted(media_list, key=lambda x: x.likes.count() + x.comments.count(), reverse=True)

    def sort_albums_by_media_count(self, album_list, user_tags):
        sorted_albums = []
        for album in album_list:
            media_count = self.count_media_matching_tags(album.media_set.all(), user_tags)
            sorted_albums.append((album, media_count))

        return [album for album, _ in sorted(sorted_albums, key=lambda x: x[1], reverse=True)]

    def count_media_matching_tags(self, media_list, user_tags):
        return sum(1 for media in media_list if user_tags and any(tag.value in media.tags.values_list('value', flat=True) for tag in user_tags))

    def get_recommendations(self, content_type=None, privacy=None, page=1, per_page=10, start_date=None, end_date=None):
        all_media = Media.objects.all()
        all_albums = Album.objects.all()

        filtered_media = self.filter_media_by_tags(all_media, self.user.tags.all())
        filtered_albums = self.filter_albums_by_tags(all_albums, self.user.tags.all())
        
        recommended_media = self.sort_media_by_user_engagement(filtered_media)
        recommended_albums = self.sort_albums_by_media_count(filtered_albums, self.user.tags.all())

        # Apply additional filtering based on query parameters
        if content_type:
            recommended_media = [media for media in recommended_media if media.content_type == content_type]

        if privacy:
            recommended_media = [media for media in recommended_media if media.privacy == privacy]

        # Apply date filtering
        if start_date and end_date:
            recommended_media = [
                media for media in recommended_media
                if start_date <= media.creation_date <= end_date
            ]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        recommended_media = recommended_media[start_idx:end_idx]
        recommended_albums = recommended_albums[start_idx:end_idx]

        return {
            'recommended_media': recommended_media,
            'recommended_albums': recommended_albums,
        }
