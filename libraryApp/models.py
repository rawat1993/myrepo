from django.db import models
from employeeApp.models import Employee,Designation,Category
from userAuthentication.models import MyUser
from school.models import School
from studentApp.models import Student,Batch,Student_Category
from time import gmtime, strftime
from  datetime import date


class Library(models.Model):

	"""This Model **Library** is use for creation purpose of library"""
	school_name=models.ForeignKey(School,null=True,blank=True)

	library_name =models.CharField(max_length=128, blank = True, null = True)
	
	total_books=models.IntegerField(default=0)
	total_issue_books=models.IntegerField(default=0)


	def __str__(self):
		return self.library_name
		# return self.library_name

class Librarian_Mangement(models.Model):

	school_name=models.ForeignKey(School,null=True,blank=True)

	Librian_Id=models.ManyToManyField(Employee,blank=True)



	def __str__(self):
		return self.school_name.school_name
		# return self.library_name




"""**********Books_Type model***********"""


class Books_Type(models.Model):

	"""This Model **Books_Type** contains a discription of a book type like text book and magzine etc"""

	school_name        =    models.ForeignKey(School,null=True,blank=True)
	book_type_name     =    models.CharField(max_length=50,null=False,blank = True)
	other_info         =    models.TextField(max_length=128,null=True,blank=True)
	is_active          =    models.BooleanField(default=True)

	total_books        =    models.IntegerField(default=0)
	total_issue_books  =    models.IntegerField(default=0)

	created_by         =    models.ForeignKey(MyUser,related_name="books_type_created_by",null=True,default=None,blank=True)
	create_at          =    models.DateField(auto_now_add=True)
	updated_at         =    models.DateField(auto_now=True)
	updated_by         =    models.ForeignKey(MyUser,related_name="books_type_updated_by",null=True,default=None,blank=True)
	is_deleted         =    models.BooleanField(default=False)


	def __str__(self):
		return self.book_type_name	


"""this is use by anmol Member_Category Table"""

class Library_Rules(models.Model):

	"""This Model **Library_Rules** make a rules for Library"""

	# category=models.ForeignKey(Category,default=None)
	employee_category  =  models.ForeignKey(Category,null=True,blank=True)
	student_category   =  models.ForeignKey(Student_Category,null=True,blank=True)

	# library=models.ForeignKey(Library,null=True,blank=True)
	book_type          =  models.ForeignKey(Books_Type)
	
	

	max_days_for_issue      =     models.PositiveIntegerField(default=0)
	after_due_date_fine     =     models.PositiveIntegerField(default=0)
	no_of_maximum_reissue   =     models.PositiveIntegerField(default=0)

	tear_book_fine_in_percentage_of_book_Rate      =    models.PositiveIntegerField(default=0)
	missing_book_fine_in_percentage_of_book_Rate   =     models.PositiveIntegerField(default=0)

	is_active    =   models.BooleanField(default=True)	
	created_by   =   models.ForeignKey(MyUser,related_name="lib_rules_created_by",null=True,default=None,blank=True)
	create_at    =   models.DateField(auto_now_add=True)
	updated_at   =   models.DateField(auto_now=True)
	updated_by   =   models.ForeignKey(MyUser,related_name="lib_rules_updated_by",null=True,default=None,blank=True)
	is_deleted   =   models.BooleanField(default=False)
	discription_about_rules  =   models.TextField(max_length=128,null=True,blank=True)

	def __str__(self):
		return self.book_type.book_type_name



class Book_Detail(models.Model):

	"""This Model **Book_Detail** have a detail of perticular book like book name, book author, book language etc"""

	book_type  =  models.ForeignKey(Books_Type,null=True,blank=True, default=None)
	school_name  =  models.ForeignKey(School,null=True,blank=True)

	book_id         =      models.CharField(max_length=128,unique=True,null=True,blank=True)
	book_ISBN       =      models.CharField(max_length=128,null=True,blank=True)
	book_name       =      models.CharField(max_length=128,null=True,blank=True)
	book_author     =      models.CharField(max_length=128,null=True,blank=True)
	book_price      =      models.CharField(max_length=128,null=True,blank=True)
	book_language   =      models.CharField(max_length=128,null=True,blank=True)
	edition         =      models.CharField(max_length=128,null=True,blank=True)


	is_active=models.BooleanField(default=False)
	select_book_cover_image=models.ImageField(blank=True,null=True)

	is_issue=models.BooleanField(default=False)
	created_by=models.ForeignKey(MyUser,related_name="book_detail_created_by",null=True,default=None,blank=True)
	create_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	updated_by=models.ForeignKey(MyUser,related_name="book_detail_updated_by",null=True,default=None,blank=True)
	is_deleted=models.BooleanField(default=False)

	



	def __str__(self):
		return self.book_name


"""this is use by anmol Member_Category Table"""

class Issue_Book(models.Model):




	"""This Model **Issue_Book** have a detail of issued book """

	# is_employee = models.BooleanField(default=False)
	# category=models.ForeignKey(Category)

	library_rules      =    models.ForeignKey(Library_Rules,null=True,default=None,blank=True)

	student_id         =    models.ForeignKey(Student,null=True,default=None,blank=True)
	employee_id        =    models.ForeignKey(Employee,null=True,default=None,blank=True)
	# book_id            =    models.CharField(max_length=128,null=True,blank=True)
	book_detail        =    models.ForeignKey(Book_Detail,null=True,blank=True)
	# is_reissue         =    models.BooleanField(default=False)


	date_of_issue      =    models.DateField(null=True,blank=True,default=date.today)
	no_times_reissue   =    models.PositiveIntegerField(default=0)
	due_date           =    models.DateField(null=True,blank=True,default='2015-09-08')
	date_of_return     =    models.DateField(null=True,blank=True)
	reissue_date       =    models.DateField(null=True,blank=True)



	updated_by         =     models.ForeignKey(MyUser,related_name="issue_book_updated_by",null=True,default=None,blank=True)
	created_by         =     models.ForeignKey(MyUser,related_name="issue_book_created_by",null=True,default=None,blank=True)
	create_at          =     models.DateField(auto_now_add=True)

	def __str__(self):
		return self.book_detail.book_name



class Fine_History(models.Model):

	# student_id         =    models.ForeignKey(Student,null=True,default=None,blank=True)
	# employee_id        =    models.ForeignKey(Employee,null=True,default=None,blank=True)
	# book_detail        =    models.ForeignKey(Book_Detail,null=True,blank=True)
	issue_book         =    models.ForeignKey(Issue_Book,null=True,blank=True)

	fine_type          =    models.TextField(null=True,blank=True)
	total_fine         =    models.IntegerField(default=0)
	is_paid    = models.BooleanField(default=False)
	is_pending = models.IntegerField(default=0)

	created_by = models.ForeignKey(MyUser,related_name="Fine_History_created_by",null=True,default=None,blank=True)
	updated_by = models.ForeignKey(MyUser,related_name="Fine_History_updated_by",null=True,default=None,blank=True)
	create_at  =  models.DateField(auto_now_add=True)
	updated_at  =  models.DateField(auto_now=True)   

	def __str__(self):
		return self.issue_book.book_detail.book_name



"""************now we start Iventory for Library*********************"""


class Product_Type(models.Model):


	"""This Model **Product_Type** have a detail of product_type like chairs, tables, ac etc"""

	# library=models.ForeignKey(Library)
	

	product_type=models.CharField(max_length=128,unique=True,null=False)
	now_is_active=models.BooleanField(default=False)

	created_by=models.ForeignKey(Employee,related_name="product_type_created_by",null=True,default=None,blank=True)
	create_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	updated_by=models.ForeignKey(Employee,related_name="product_type_updated_by")


	
	def __str__(self):
		return self.product_type


class Product_Detail(models.Model):


	"""This Model **Product_Detail** have a detail of product like chairs no, price , etc"""	


	product_type=models.ForeignKey(Product_Type)
	

	

	total_available=models.IntegerField()
	
	created_by=models.ForeignKey(Employee,related_name="product_detail_created_by",null=True,default=None,blank=True)
	create_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	updated_by=models.ForeignKey(Employee,related_name="product_detail_updated_by")
	
	
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.product_type.product_type



class Break_product_Detail(models.Model):


	"""This Model **Break_product_Detail** have a detail of break products"""	

	product_detail=models.ForeignKey(Product_Detail)
	

	total_break_product=models.IntegerField()
	discription=models.TextField(max_length=500,blank=True)

	created_by=models.ForeignKey(Employee,related_name="break_product_detail_crated_by",null=True,default=None,blank=True)
	create_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	updated_by=models.ForeignKey(Employee,related_name="break_product_detail_updated_by")

	now_is_active=models.BooleanField(default=False)

	def __str__(self):
		return self.product_detail.product_type.product_type

class Product_Request(models.Model):


	"""This Model **Product_Request** contains requirments of product. how much product are requirments for library """

	assignee=models.ForeignKey(Employee, related_name="product_request_assignee")
	product_detail=models.ForeignKey(Product_Detail)

	# this is use by anmol
	created_by=models.ForeignKey(Employee,related_name="product_request_created_by")
	updated_by=models.ForeignKey(Employee,related_name="product_request_updated_by")
	
	requirment=models.IntegerField()
	no_of_product_issue=models.IntegerField()

	request_date=models.DateField(auto_now_add=True)
	

	accepted_request_date=models.DateField(null=True,blank=True)
	
	is_accepted=models.BooleanField(default=False)
	is_requested=models.BooleanField(default=False)

	def __str__(self):
		return self.product_detail.product_type



