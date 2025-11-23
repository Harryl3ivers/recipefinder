import pytest
from main.validate_ingredients import validate_ingredients

def test_valid_ingredients():
    result = validate_ingredients("chicken, rice, carrots")
    assert result == ["chicken", "rice", "carrots"]

def test_ingredients_with_extra_spaces():
   
    result = validate_ingredients("  chicken  ,  rice  ,  carrots  ")
    assert result == ["chicken", "rice", "carrots"]

def test_empty_ingredients_raises_error():
    with pytest.raises(ValueError, match="No ingredients provided"):
        validate_ingredients("")

def test_invalid_characters_raises_error():
    with pytest.raises(ValueError, match="Invalid ingredient"):
        validate_ingredients("chicken478, rice")

def test_single_ingredient():
    result = validate_ingredients("carrots")
    assert result == ["carrots"]

def test_ingredients_with_hyphens():
    result = validate_ingredients("Greek-style salad")
    assert result == ["Greek-style salad"]