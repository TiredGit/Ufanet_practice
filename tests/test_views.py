from django.urls import reverse

from test_models import *

#
# Categories_view (Main)
#


@pytest.mark.django_db
def test_categories_view_default_city_context(client, discount_no_ufa):
    response = client.get(reverse('categories'))
    assert response.status_code == 200
    selected_city = response.context['selected_city']
    assert selected_city.name == 'Самара'


@pytest.mark.django_db
def test_categories_view_default_city_ufa_context(client, discount, city):
    response = client.get(reverse('categories'))
    assert response.status_code == 200
    selected_city = response.context['selected_city']
    assert selected_city.name == 'Уфа'


@pytest.mark.django_db
def test_categories_view_city_switch(client, city, discount):
    response = client.get(reverse('categories'), {'city': city[1].id})
    assert response.status_code == 200

    assert city[1].name in response.content.decode()
    assert client.session['city_id'] == city[1].id

    selected_city = response.context['selected_city']
    assert selected_city.name == 'Москва'


@pytest.mark.django_db
def test_categories_view_context_all(client, city, discount, category):
    response = client.get(reverse('categories'))
    assert response.status_code == 200

    cities = response.context['cities']
    assert city[0] in cities
    assert city[1] in cities
    categories = response.context['categories']
    assert list(category) == list(categories)
    discounts = response.context['discounts']
    assert list(discount) == list(discounts)


@pytest.mark.django_db
def test_categories_view_search1(client, discount):
    response = client.get(reverse('categories'), {'search': 'Small'})
    assert response.status_code == 200
    assert "Small Name" in response.content.decode()
    discounts = response.context['discounts']
    assert "Small Name" in discounts.filter(small_name__icontains='small').get().small_name


@pytest.mark.django_db
def test_categories_view_search2(client, discount):
    response = client.get(reverse('categories'), {'search': 'BigAnimal'})
    assert response.status_code == 200
    assert "BigAnimal" not in response.content.decode()


@pytest.mark.django_db
def test_categories_view_selected_discount(client, discount):
    response = client.get(reverse('categories'), {'selected': discount[0].id})
    assert response.status_code == 200
    assert "https://example.com" in response.content.decode()


@pytest.mark.django_db
def test_category_discounts_number(client, discount, category):
    response = client.get(reverse('categories'))
    assert response.status_code == 200

    categories = response.context['categories']
    our_category1 = next(c for c in categories if c.id == category[0].id)
    assert hasattr(our_category1, 'city_offer_count')
    assert our_category1.city_offer_count == 2

    our_category2 = next(c for c in categories if c.id == category[1].id)
    assert hasattr(our_category2, 'city_offer_count')
    assert our_category2.city_offer_count == 1


@pytest.mark.django_db
def test_categories_view_city_not_exist(client, city, discount):
    response = client.get(reverse('categories'), {'city': 20})
    assert response.status_code == 200

    selected_city = response.context['selected_city']
    assert selected_city.name == 'Уфа'


@pytest.mark.django_db
def test_categories_view_card_not_exist(client, discount):
    response = client.get(reverse('categories'), {'selected': 2200})
    assert response.status_code == 200


@pytest.mark.django_db
def test_categories_view_session(client, city, category, discount):
    session = client.session
    session['city_id'] = city[1].id
    session.save()

    response = client.get(reverse('categories'))
    assert response.status_code == 200

    selected_city = response.context['selected_city']
    assert selected_city.name == 'Москва'

#
# Category_discounts_view
#


@pytest.mark.django_db
def test_category_discounts_view_context_all(client, city, discount, category):
    response = client.get(reverse('category_discounts', args=[category[0].id]))
    assert response.status_code == 200

    cities = response.context['cities']
    assert city[0] in cities
    assert city[1] in cities
    assert 'ДоДо пицца' and 'Test Discount' in response.content.decode()
    page_category = response.context['category']
    assert page_category.name == 'Продукты'


@pytest.mark.django_db
def test_category_discounts_view_default_city_context(client, discount_no_ufa, category):
    response = client.get(reverse('category_discounts', args=[category[0].id]))
    assert response.status_code == 200
    selected_city = response.context['selected_city']
    assert selected_city.name == 'Самара'


@pytest.mark.django_db
def test_category_discounts_view_default_city_ufa_context(client, discount, city, category):
    response = client.get(reverse('category_discounts', args=[category[0].id]))
    assert response.status_code == 200
    selected_city = response.context['selected_city']
    assert selected_city.name == 'Уфа'


@pytest.mark.django_db
def test_category_discounts_view_selected_discount(client, discount, category):
    response = client.get(reverse('category_discounts', args=[category[0].id]), {'selected': discount[0].id})
    assert response.status_code == 200
    assert "https://example.com" in response.content.decode()


@pytest.mark.django_db
def test_category_discounts_view_card_not_exist(client, discount, category):
    response = client.get(reverse('category_discounts', args=[category[0].id]), {'selected': 2200})
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_discounts_view_session(client, city, category, discount):
    session = client.session
    session['city_id'] = city[1].id
    session.save()

    response = client.get(reverse('category_discounts', args=[category[0].id]))
    assert response.status_code == 200

    selected_city = response.context['selected_city']
    assert selected_city.name == 'Москва'

