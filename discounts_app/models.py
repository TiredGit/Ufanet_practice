from django.db import models


class DiscountCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=100)
    image = models.ImageField(verbose_name='Картинка категории', upload_to='category_images',
                                      blank=True, null=True)

    class Meta:
        verbose_name='Раздел'
        verbose_name_plural='Разделы'

    def __str__(self):
        return self.name

    def cards_number(self):
        return self.discount_cards.count()


class Company(models.Model):
    company_name = models.CharField(verbose_name='Название компании', max_length=100)
    company_image = models.ImageField(verbose_name='Аватарка компании', upload_to='company_images',
                                      blank=True, null=True)

    class Meta:
        verbose_name='Компания'
        verbose_name_plural='Компании'

    def __str__(self):
        return self.company_name


class City(models.Model):
    name = models.CharField(verbose_name='Название города', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name


class DiscountCard(models.Model):
    name = models.CharField(verbose_name='Название предложения', max_length=100)
    small_name = models.CharField(verbose_name='Название предложения (продолжение)', max_length=100)
    how_to_get = models.TextField(verbose_name='Как получить', blank=True, null=True)
    about = models.TextField(verbose_name='О партнере', blank=True, null=True)
    start_date = models.DateField(verbose_name='Стартовая дата')
    end_date = models.DateField(verbose_name='Конечная дата')
    address = models.URLField(verbose_name='Ссылка', max_length=500)
    bonus_code = models.CharField(verbose_name='Промокод',max_length=100, blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение карточки', upload_to='discounts_images', blank=True, null=True)
    offers_category = models.CharField(verbose_name='Категория предложения', max_length=100, blank=True, null=True)
    categories = models.ManyToManyField(
        DiscountCategory,
        related_name='discount_cards',
        verbose_name='Категории'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='discount_cards',
        verbose_name='Компания'
    )
    cities = models.ManyToManyField(
        City,
        related_name='discount_cards',
        verbose_name='Города',
    )

    class Meta:
        verbose_name='Предложение'
        verbose_name_plural='Предложения'

    def __str__(self):
        return self.name
