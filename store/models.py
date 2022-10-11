from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL


class Product(models.Model):
    ROMANS = "ROM"
    MANGAS = "MAN"
    SCOLAIRES = "SCO"
    VOYAGES = "VOY"
    BD = "BDD"
    ENFANTS = "ENF"
    COMICS = "COM"

    CATEGORY = [
        (ROMANS, "Romans"),
        (MANGAS, "Mangas"),
        (SCOLAIRES, "Livres scolaires"),
        (VOYAGES, "Livres de voyages"),
        (BD, "BD"),
        (ENFANTS, "Livres enfants"),
        (COMICS, "Comics"),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, )
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY, verbose_name="categories")
    type_gender = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    number_page = models.IntegerField(blank=True)
    stock = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    price = models.FloatField(default=0.0, blank=True)
    stripe_id = models.CharField(max_length=90, blank=True)

    class Meta:
        verbose_name = "Les livre"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    class Meta:
        verbose_name = "Article"


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Panier"
