from yt_dlp.extractor.neteasemusic import NetEaseMusicProgramIE
from yt_dlp.utils import ExtractorError, determine_ext, int_or_none, traverse_obj, url_or_none


__all__ = []


class _NetEaseProgramQualityIE(NetEaseMusicProgramIE, plugin_name='netease-program-quality'):
    def _extract_formats(self, info):
        formats = []
        seen_urls = set()
        seen_streams = set()
        first_error = None

        for level in self._LEVELS:
            try:
                response = self._call_player_api(info['id'], level)
            except ExtractorError as error:
                if first_error is None:
                    first_error = error
                self.report_warning(f'Unable to check NetEase audio level {level}: {error.msg}')
                continue

            song = traverse_obj(response, ('data', lambda _, item: url_or_none(item['url']), any))
            if not song or song.get('freeTrialInfo'):
                continue

            media_url = song['url']
            actual_level = song.get('level')
            extension = traverse_obj(song, ('type', {str})) or determine_ext(media_url, default_ext=None)
            bitrate = int_or_none(song.get('br'))
            abr = int_or_none(bitrate, scale=1000) if bitrate and bitrate > 0 else None
            filesize = int_or_none(song.get('size'))
            checksum = traverse_obj(song, ('md5', {str}))
            encoding = (extension, bitrate, filesize)
            stream_key = None
            if checksum:
                stream_key = ('md5', checksum.lower())
            elif all(encoding):
                stream_key = ('encoding', *encoding)
            if media_url in seen_urls or stream_key in seen_streams:
                continue
            seen_urls.add(media_url)
            if stream_key is not None:
                seen_streams.add(stream_key)

            # A request can return a lower tier or omit the level entirely.
            if actual_level in self._LEVELS:
                format_id = actual_level
            elif extension == 'flac':
                format_id = f'flac-{abr}' if abr else 'flac'
            else:
                format_id = f'abr-{abr}' if abr else extension or 'audio'
            formats.append({
                'url': media_url,
                'format_id': format_id,
                'vcodec': 'none',
                'ext': extension,
                'abr': abr,
                'filesize': filesize,
            })

        if not formats:
            if first_error is not None:
                raise first_error
            self.raise_no_formats('NetEase returned no full audio URLs for this program', expected=True)
        return formats
