from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

from discounts_app.models import *
import pytest
from datetime import date


@pytest.fixture()
def category():
    category1 = DiscountCategory.objects.create(name="Продукты")
    category2 = DiscountCategory.objects.create(name="Услуги")
    return [category1, category2]


@pytest.fixture(autouse=True)
def temporary_media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture()
def company():
    image = Image.new("RGB", (32, 32), color="blue")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    test_image = SimpleUploadedFile(
        name="test_image.png",
        content=buffer.read(),
        content_type="image/png"
    )
    company1 = Company.objects.create(company_name="Фарфор", company_image=test_image)
    company2 = Company.objects.create(company_name="ДоДо")
    return [company1, company2]


@pytest.fixture()
def city_no_ufa():
    city1 = City.objects.create(name="Самара")
    city2 = City.objects.create(name="Ялта")
    return [city1, city2]


@pytest.fixture()
def discount_no_ufa(category, company, city_no_ufa):
    discount_card1 = DiscountCard.objects.create(
        name="no_ufa",
        small_name="test",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        address="https://example.com",
        company=company[0]
    )
    discount_card1.categories.add(category[0])
    discount_card1.cities.add(city_no_ufa[0])

    return discount_card1


@pytest.fixture()
def city():
    city1 = City.objects.create(name="Уфа")
    city2 = City.objects.create(name="Москва")
    return [city1, city2]


@pytest.fixture()
def discount(category, company, city):
    discount_card1 = DiscountCard.objects.create(
        name="Test Discount",
        small_name="Small Name",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        address="https://example.com",
        company=company[0]
    )
    discount_card1.categories.add(category[0])
    discount_card1.cities.add(city[0])

    discount_card2 = DiscountCard.objects.create(
        name="ДоДо пицца",
        small_name="Скидка",
        start_date=date(2024, 5, 1),
        end_date=date(2024, 12, 31),
        address="https://dodo.com",
        company=company[1]
    )
    discount_card2.categories.add(category[0])
    discount_card2.cities.add(city[0])

    discount_card3 = DiscountCard.objects.create(
        name="Интернет",
        small_name="за 300 руб",
        start_date=date(2024, 1, 1),
        end_date=date(2025, 12, 31),
        address="https://example.com",
        company=company[0]
    )
    discount_card3.categories.add(category[1])
    discount_card3.cities.add(city[0])
    discount_card3.cities.add(city[1])

    return [discount_card1, discount_card2, discount_card3]


@pytest.mark.django_db
def test_discount_category_str(category):
    assert str(category[0]) == "Продукты"


@pytest.mark.django_db
def test_discount_company_str(company):
    assert str(company[0]) == "Фарфор"


@pytest.mark.django_db
def test_discount_city_str(city):
    assert str(city[0]) == "Уфа"


@pytest.mark.django_db
def test_discount_card_str(discount):
    assert str(discount[0]) == "Test Discount"


@pytest.mark.django_db
def test_city_count(city):
    assert len(city) == 2


@pytest.mark.django_db
def test_discount_card_1(discount):
    assert discount[0].company.company_name == "Фарфор"


@pytest.mark.django_db
def test_discount_card_2(discount):
    assert discount[0].cities.first().name == "Уфа"


@pytest.mark.django_db
def test_discount_card_3(discount):
    assert discount[0].small_name == "Small Name"


@pytest.mark.django_db
def test_city_name_required():
    city = City(name=None)
    with pytest.raises(ValidationError):
        city.full_clean()


@pytest.mark.django_db
def test_company_image(company):
    assert company[0].company_image.name.endswith(".png")
