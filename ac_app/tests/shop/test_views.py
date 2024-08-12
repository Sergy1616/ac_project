from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, resolve

from shop.forms import ProductSortForm
from shop.models import Category, Brand, ProductImage, WishList
from shop.views import ProductListView, ProductDetailView
from tests.base_test import BaseTest


class ProductListViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.second_category = Category.objects.create(
            name="Second Category", slug="second-category"
        )
        self.second_brand = Brand.objects.create(
            name="Second Brand", slug="second-brand"
        )
        self.product3 = self.create_product(
            category=self.second_category,
            brand=self.second_brand,
            name="Second Category Product",
            slug="second-category-product",
            price=150,
            discount=20,
        )
        self.url = reverse("products")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/shop/products/")
        self.assertEqual(view.func.view_class, ProductListView)

    def test_products_view_with_authenticated_user(self):
        self.client.login(username=self.existing_user, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # print(response.context['user'])

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "shop/products.html")
        self.assertIsInstance(self.response.context["login_form"], AuthenticationForm)
        self.assertIsInstance(self.response.context["form"], ProductSortForm)
        self.assertTrue("product_list" in self.response.context)
        self.assertTrue("categories" in self.response.context)
        self.assertTrue("brands" in self.response.context)
        self.assertTrue("sale_product_list" in self.response.context)

    def test_selected_category_in_context(self):
        url_with_category = reverse("products_by_category", args=[self.category.slug])
        response = self.client.get(url_with_category)
        self.assertIn("selected_category", response.context)
        self.assertEqual(response.context["selected_category"], self.category)

    def test_selected_brand_in_context(self):
        url_with_brand = reverse("products_by_brand", args=[self.brand.slug])
        response = self.client.get(url_with_brand)
        self.assertIn("selected_brand", response.context)
        self.assertEqual(response.context["selected_brand"], self.brand)

    def test_categories_with_products_only_in_context(self):
        unused_category = Category.objects.create(
            name="Unused Category", slug="unused-category"
        )
        response = self.client.get(self.url)

        categories_in_context = response.context["categories"]
        self.assertNotIn(unused_category, categories_in_context)
        self.assertIn(self.category, categories_in_context)
        self.assertIn(self.second_category, categories_in_context)

    def test_brands_with_products_only_in_context(self):
        unused_brand = Brand.objects.create(name="Unused Brand", slug="unused-brand")
        response = self.client.get(self.url)
        brands_in_context = response.context["brands"]
        self.assertNotIn(unused_brand, brands_in_context)
        self.assertIn(self.brand, brands_in_context)
        self.assertIn(self.second_brand, brands_in_context)

    def test_category_filter(self):
        response = self.client.get(
            reverse("products_by_category", args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product1, response.context["product_list"])
        self.assertIn(self.product2, response.context["product_list"])
        self.assertNotIn(self.product3, response.context["product_list"])

    def test_brand_filter(self):
        response = self.client.get(reverse("products_by_brand", args=[self.brand.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product1, response.context["product_list"])
        self.assertIn(self.product2, response.context["product_list"])
        self.assertNotIn(self.product3, response.context["product_list"])

    def test_nonexistent_category(self):
        url_with_invalid_category = reverse(
            "products_by_category", args=["nonexistent-category"]
        )
        response = self.client.get(url_with_invalid_category)
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_brand(self):
        url_with_invalid_brand = reverse(
            "products_by_brand", args=["nonexistent-brand"]
        )
        response = self.client.get(url_with_invalid_brand)
        self.assertEqual(response.status_code, 404)

    def test_sale_product_list_contains_only_discounted_products(self):
        sale_product_list = self.response.context["sale_product_list"]
        for product in sale_product_list:
            self.assertGreater(product.discount, 0)
        self.assertIn(self.product3, sale_product_list)
        self.assertNotIn(self.product1, sale_product_list)

    def test_products_view_pagination(self):
        products_per_page = 6
        for product_number in range(products_per_page):
            self.create_product(
                name=f"Product {product_number}",
                slug=f"product-{product_number}",
            )
        response = self.client.get(self.url)
        self.assertTrue(len(response.context["product_list"]) == products_per_page)

        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(len(response.context["product_list"]), 3)
        self.assertTrue(response.context["is_paginated"])

        response = self.client.get(f"{self.url}?sort=price_asc&page=2")
        self.assertEqual(len(response.context["product_list"]), 3)

        response = self.client.get(f"{self.url}?page=1000")
        self.assertEqual(response.status_code, 404)

    def test_sorting_by_creation_date_descending(self):
        response = self.client.get(f"{self.url}?sort=date_desc")
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product3, self.product2, self.product1]
        )

    def test_sorting_price_ascending(self):
        response = self.client.get(f"{self.url}?sort=price_asc")
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product1, self.product3, self.product2]
        )

    def test_sorting_price_descending(self):
        response = self.client.get(f"{self.url}?sort=price_desc")
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product2, self.product3, self.product1]
        )

    def test_sorting_by_name_ascending(self):
        response = self.client.get(f"{self.url}?sort=name_asc")
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product3, self.product1, self.product2]
        )

    def test_sorting_by_name_descending(self):
        response = self.client.get(f"{self.url}?sort=name_desc")
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product2, self.product1, self.product3]
        )

    def test_invalid_sort_parameter(self):
        response = self.client.get(f"{self.url}?sort=unknown_parameter")
        self.assertEqual(response.status_code, 200)
        products_page = response.context["product_list"]
        self.assertEqual(
            list(products_page), [self.product3, self.product2, self.product1]
        )


class ProductDetailTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.image = ProductImage.objects.create(
            product=self.product1, image="test_image.jpg", is_for_slider=False
        )
        self.url = reverse(
            "product_detail", kwargs={"product_slug": self.product1.slug}
        )
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/shop/products/{}/".format(self.product1.slug))
        self.assertEqual(view.func.view_class, ProductDetailView)

    def test_products_view_with_authenticated_user(self):
        self.client.login(username=self.existing_user, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # print(response.context['user'])

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "shop/product_detail.html")
        self.assertIsInstance(self.response.context["login_form"], AuthenticationForm)
        self.assertTrue("product" in self.response.context)
        self.assertTrue("images" in self.response.context)
        self.assertTrue("in_wishlist" in self.response.context)
        self.assertFalse(self.response.context["in_wishlist"])
        images_in_context = self.response.context["images"]
        self.assertIn(self.image, images_in_context)

    def test_in_wishlist_for_authenticated_user(self):
        self.client.force_login(self.user)
        self.wishlist.products.add(self.product1)
        response = self.client.get(self.url)
        self.assertTrue(response.context["in_wishlist"])


class WishListUpdateViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("wishlist", kwargs={"product_slug": self.product1.slug})

    def test_add_product_to_wishlist(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], "added")
        self.assertEqual(WishList.objects.get(user=self.user).products.count(), 1)

    def test_remove_product_from_wishlist(self):
        self.wishlist.products.add(self.product1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], "removed")
        self.assertEqual(self.wishlist.products.count(), 0)

    def test_wishlist_update_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["error"],
            "You must be logged in to add an item to your wishlist",
        )
