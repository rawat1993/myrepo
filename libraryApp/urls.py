from django.conf.urls import include, url,patterns
from libraryApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'lib', views.Library_ViewSet)
router.register(r'Librarian', views.Librarian_Mangement_ViewSet)
router.register(r'Library_Rules', views.Library_Rules_ViewSet)
router.register(r'Books_Type', views.Books_Type_ViewSet)
router.register(r'Book_Detail', views.Book_Detail_ViewSet)

# router.register(r'Book_Detail/(?P<pk>\d+)/?$', views.Book_Detail_ViewSet)
# router.register(r'Book_Detail/(?P<>[^/w.]+)/$', views.Book_Detail_ViewSet)

router.register(r'Issue_Book', views.Issue_Book_ViewSet)
router.register(r'Fine_History', views.Fine_History_ViewSet)
router.register(r'Product_Type', views.Product_Type_ViewSet)
router.register(r'Product_Detail', views.Product_Detail_ViewSet)
router.register(r'Break_product_Detail', views.Break_product_Detail_ViewSet)
router.register(r'Product_Request', views.Product_Request_ViewSet)
# router.register(r'return_book/(?P<pk>[0-9]+)/$', views.ReturnBookView.as_view())

# router.register(r'return_book', views.ReturnBookView)


urlpatterns=patterns('',

	url(r'^',include(router.urls)),
	

	)
