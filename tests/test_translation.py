from unittest.mock import patch
import pytest
from product_translation import translate_product


def test_known_catalog_translation_needs_no_network():
    with patch('product_translation.requests.get') as remote:
        import json
        from pathlib import Path
        product = json.loads((Path(__file__).parents[1] / 'demo_catalog.json').read_text(encoding='utf-8'))[0]
        result = translate_product(product['name'], product['description'])
        assert result['ru']['name'] == 'Студийные наушники'
        assert not remote.called


def test_new_text_translates_to_other_languages():
    with patch('product_translation.requests.get') as remote:
        remote.return_value.json.return_value = {'responseStatus': 200, 'responseData': {'translatedText': 'Translated text'}}
        result = translate_product('Новый товар', 'Описание нового товара')
        assert result['ru']['name'] == 'Новый товар'
        assert result['en']['name'] == 'Translated text'
        assert result['uk']['description'] == 'Translated text'
        assert remote.call_count == 4


def test_translation_failure_does_not_return_partial_result():
    with patch('product_translation.requests.get') as remote:
        remote.return_value.json.return_value = {'responseStatus': 429}
        with pytest.raises(ValueError, match='Translation service unavailable'):
            translate_product('Новый товар', 'Описание нового товара')
