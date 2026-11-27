from yt_dlp.extractor.neteasemusic import NetEaseMusicProgramIE
from yt_dlp.utils import ExtractorError, int_or_none, traverse_obj, url_or_none


__all__ = []


class _NetEaseProgramQualityIE(NetEaseMusicProgramIE, plugin_name='netease-program-quality'):
    _FREE_LEVELS = ('standard', 'higher', 'exhigh')

    def _extract_formats(self, info):
        formats = []
        seen_urls = set()
        seen_encodings = set()
        missing_level = False

        for level in self._LEVELS:
            free_level = level in self._FREE_LEVELS
            if not free_level and missing_level:
                break

            try:
                response = self._call_player_api(info['id'], level)
            except ExtractorError as error:
                if not formats:
                    raise
                self.report_warning(f'Unable to check NetEase audio level {level}: {error.msg}')
                continue

            song = traverse_obj(response, ('data', lambda _, item: url_or_none(item['url']), any))
            if not song or song.get('freeTrialInfo'):
                if free_level:
                    continue
                break

            actual_level = song.get('level')
            if actual_level and actual_level != level:
                if level in ('lossless', 'jymaster'):
                    break
                # A later request may return a different free level that we already have.
                if not free_level or actual_level not in self._FREE_LEVELS:
                    continue
            elif not actual_level:
                missing_level = True
                if not free_level:
                    break

            bitrate = int_or_none(song.get('br'))
            abr = int_or_none(bitrate, scale=1000) if bitrate and bitrate > 0 else None
            extension = traverse_obj(song, ('type', {str}))
            filesize = int_or_none(song.get('size'))
            media_url = song['url']
            encoding = (extension, bitrate, filesize)
            if not actual_level and not abr and level != 'standard':
                continue
            if media_url in seen_urls or encoding in seen_encodings:
                continue
            seen_urls.add(media_url)
            if all(encoding):
                seen_encodings.add(encoding)

            formats.append({
                'url': media_url,
                'format_id': actual_level or (f'abr-{abr}' if abr else 'audio'),
                'vcodec': 'none',
                'ext': extension,
                'abr': abr,
                'filesize': filesize,
            })

        if not formats:
            self.raise_no_formats('NetEase returned no full audio URLs for this program', expected=True)
        return formats
