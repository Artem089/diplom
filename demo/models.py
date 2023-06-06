from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.


class User(AbstractUser):
    name = models.CharField(verbose_name='Имя', max_length=254, blank=False)
    surname = models.CharField(verbose_name='Фамилия', max_length=254, blank=False)
    patromymic = models.CharField(verbose_name='Отчество', max_length=254, blank=True)
    username = models.CharField(verbose_name='Логин', max_length=254, blank=False, unique=True)
    email = models.CharField(verbose_name='Почта', max_length=254, blank=False)
    password = models.CharField(verbose_name='Пароль', max_length=254, blank=False)
    rules = models.CharField(verbose_name='Роль', max_length=254, blank=False,
                             choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FILD = 'username'

    def full_name(self):
        return self.surname + ' ' + self.name + ' ' + self.patromymic

    def __str__(self):
        return self.full_name()


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    date = models.DateTimeField(verbose_name='Дата обновления', auto_now_add=True)
    photo_file = models.ImageField(max_length=254, upload_to='demo/files',
                                   blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    year = models.IntegerField(verbose_name='Год производства', blank=True, null=True)
    coutry = models.CharField(max_length=254, verbose_name='Страна производства', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False,
                                default=0.00)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование', blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Cart(models.Model):
    count = models.IntegerField(verbose_name='Кол-во', blank=False, default=0)
    product = models.ForeignKey('Product', verbose_name='Продукта', on_delete=models.CASCADE)
    user = models.ForeignKey('User', verbose_name='Пользователя', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product) + " " + str(self.count)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждённый'),
        ('new', 'Новый'),
        ('canseled', 'Отменённый')
    ]
    date = models.DateTimeField(verbose_name='дата заказа', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES, default='new')
    rejectreason = models.TextField(verbose_name='Причина отказа', blank=True)
    user = models.ForeignKey('User', verbose_name='Пользователя', on_delete=models.CASCADE)
    product = models.ManyToManyField('Product', through='ItemInOrder', related_name='order')

    def count_product(self):
        count_product = 0
        for iteminorder in self.iteminorder_set.all():
            count_product += iteminorder.count
        return count_product

    def __str__(self):
        return str(self.date.ctime()) + ' | ' + self.user.full_name() + \
            ' | Количество: ' + str(self.count_product()) + ' | ' + self.user.username

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ItemInOrder(models.Model):
    count = models.IntegerField(verbose_name='Кол-во', blank=False, default=0)
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)

    def __str__(self):
        return str(self.product) + " " + str(self.count) + '(' + str(self.price) + ')'


class Application(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

# Create your models here.
