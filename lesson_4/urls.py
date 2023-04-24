from views import About, ContactUs, CopyProduct, CreateCategory, CreateProduct, Index, ProductList

routes = {
    "/": Index(),
    "/contact/": ContactUs(),
    "/about/": About(),
    "/create-category/": CreateCategory(),
    "/product-list/": ProductList(),
    "/create-product/": CreateProduct(),
    "/copy-product/": CopyProduct(),
}
