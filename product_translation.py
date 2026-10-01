"""Automatic storefront translations, stored with each saved product."""
import json
from pathlib import Path
import requests


def translate_product(name, description, previous=None):
    catalog = json.loads((Path(__file__).with_name('demo_catalog.json')).read_text(encoding='utf-8'))
    result = {locale: {} for locale in ('en', 'ru', 'uk')}
    for field, text in [('name', name), ('description', description)]:
        known = next((item for item in catalog if text in [item.get(field)] + [v.get(field) for v in item.get('translations', {}).values()]), None)
        if known:
            for locale in result:
                result[locale][field] = known.get('translations', {}).get(locale, {}).get(field, known[field])
            continue
        if previous and any(values.get(field) == text for values in previous.values()):
            for locale in result:
                result[locale][field] = previous.get(locale, {}).get(field, text)
            continue
        source = 'uk' if any(c in text.lower() for c in 'іїєґ') else 'ru' if any('\u0400' <= c <= '\u04ff' for c in text) else 'en'
        for locale in result:
            if locale == source:
                result[locale][field] = text
                continue
            # MyMemory free tier limits each query to 500 UTF-8 bytes.
            chunks, chunk = [], ''
            for character in text:
                if len((chunk + character).encode('utf-8')) > 450:
                    chunks.append(chunk); chunk = ''
                chunk += character
            if chunk: chunks.append(chunk)
            translated = []
            for chunk in chunks:
                try:
                    response = requests.get('https://api.mymemory.translated.net/get', params={'q': chunk, 'langpair': source + '|' + locale}, timeout=8)
                    response.raise_for_status()
                    payload = response.json()
                    value = payload.get('responseData', {}).get('translatedText')
                    if payload.get('responseStatus') != 200 or not isinstance(value, str) or not value.strip():
                        raise ValueError('Translation service unavailable. Please retry saving the product.')
                    translated.append(value.strip())
                except (requests.RequestException, KeyError, TypeError) as exc:
                    raise ValueError('Translation service unavailable. Please retry saving the product.') from exc
            result[locale][field] = ' '.join(translated)
    return result
