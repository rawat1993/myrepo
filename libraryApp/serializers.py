from rest_framework import serializers
from libraryApp.models import *
from studentApp.serializers import Student_on_Issue_BookSerializer
from employeeApp.serializers import Employee_General_Serializer
class Library_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Library
		fields = ('library_name','school_name')

'''********** this serializer for Librarian_Mangement Model*********************'''

class Librarian_Mangement_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Librarian_Mangement
		fields = ('id','school_name','Librian_Id')





'''********** this serializer for Books_Type Model*********************'''

class Books_Type_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Books_Type
		fields = ('id','book_type_name','other_info','is_active')


class Books_Type_Name_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Books_Type
		fields = ('book_type_name',)


'''********** this serializer for Library_Rules Model*********************'''

class Library_Rules_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Library_Rules
		fields = ('id','employee_category','student_category','book_type','max_days_for_issue','after_due_date_fine','no_of_maximum_reissue','tear_book_fine_in_percentage_of_book_Rate','missing_book_fine_in_percentage_of_book_Rate','discription_about_rules','is_active')




'''********** this serializer for Book_Detail Model*********************'''

class Book_Detail_Serializer(serializers.ModelSerializer):
	book_type=Books_Type_Name_Serializer()
	class Meta:
		model = Book_Detail
		fields = ('id','book_type','book_ISBN','book_name','book_author','book_price','book_language','edition','is_active','select_book_cover_image')


class Book_Detail_For_Active_Inactive_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Book_Detail
		fields = ('id','book_id','is_active','select_book_cover_image')


class Book_General_Detail_Serializer(serializers.ModelSerializer):
	# book_type=Books_Type_Serializer(read_only=True)
	class Meta:
		model = Book_Detail
		fields = ('id','book_id','book_ISBN','book_name','book_author','edition','select_book_cover_image')
class Book_Detail_Name_Serializer(serializers.ModelSerializer):
	# book_type=Books_Type_Serializer(read_only=True)
	class Meta:
		model = Book_Detail
		fields = ('book_name',)

'''********** this serializer for Issue_Book Model*********************'''

class Issue_Book_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Issue_Book
		fields = ('id','student_id','employee_id','book_detail')


class Issue_Book_with_Book_Detail_Serializer(serializers.ModelSerializer):
	book_detail = Book_General_Detail_Serializer()
	class Meta:
		model = Issue_Book
	 	fields = ('id','book_detail','date_of_issue','due_date')

class Issue_Book_with_Book_Name_Serializer(serializers.ModelSerializer):
	book_detail = Book_Detail_Name_Serializer()
	class Meta:
		model = Issue_Book
	 	fields = ('id','book_detail','date_of_issue','due_date')

class Issue_Book_with_Book_Detail_And_Return_Date_Serializer(serializers.ModelSerializer):
	book_detail = Book_Detail_Serializer()
	class Meta:
		model = Issue_Book
	 	fields = ('id','book_detail','date_of_issue','due_date','date_of_return')


class Issue_Book_Detail_with_Stu_Emp_Serializer(serializers.ModelSerializer):
	student_id =  Student_on_Issue_BookSerializer()
	employee_id = Employee_General_Serializer()
	book_detail = Book_General_Detail_Serializer()
	class Meta:
		model = Issue_Book
		fields = ('student_id','employee_id','book_detail')


'''********** this serializer for Fine_History Model*********************'''

class Fine_History_Serializer(serializers.ModelSerializer):
	issue_book = Issue_Book_Detail_with_Stu_Emp_Serializer()
	class Meta:
		model = Fine_History
		fields = ('id','issue_book','is_pending','fine_type')


class Fine_History_with_Book_Detail_Serializer(serializers.ModelSerializer):
	issue_book = Issue_Book_with_Book_Detail_And_Return_Date_Serializer()
	class Meta:
		model = Fine_History
		fields = ('id','issue_book','is_pending','fine_type')



"""####################### now we start Serializer for Inventory ###################"""

'''********** this serializer for Product_Type Model*********************'''

class Product_Type_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Product_Type
		fields = ('product_type','now_is_active')



'''********** this serializer for Product_Detail Model*********************'''

class Product_Detail_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Product_Detail
		fields = ('product_type','total_available','is_active')



'''********** this serializer for Break_product_Detail Model*********************'''

class Break_product_Detail_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Break_product_Detail
		fields = ('product_detail','total_break_product','discription','now_is_active')



'''********** this serializer for Product_Request Model*********************'''

class Product_Request_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Product_Request
		fields = ('product_detail','requirment','assignee','no_of_product_issue','request_date','accepted_request_date','is_accepted','is_requested')


