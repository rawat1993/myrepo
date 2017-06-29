from django.utils.formats import get_format
from rest_framework import viewsets
from rest_framework.response import Response
from libraryApp.serializers import *
from libraryApp.models import *
from school.models import School
from django.db.models import Max
from rest_framework import status
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from datetime import datetime,timedelta
from libraryApp.permissions import *
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope,TokenHasScope
import json
from userAuthentication.models import MyUser
from django.core.paginator import Paginator
from  datetime import date



'''********** This ViewSets for Library Model ***************************'''
class Library_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Library_ViewSet** is use for creation of library id"""

	queryset        = Library.objects.all()
	serializer_class= Library_Serializer





'''********** This ViewSets for Librarian_Mangement Model ***************************'''
class Librarian_Mangement_ViewSet(viewsets.ModelViewSet):


	queryset        = Librarian_Mangement.objects.all()
	serializer_class= Librarian_Mangement_Serializer

	# def update(self, request, pk):


 #        try:
 #            emp_boj = Employee.objects.get(pk=pk)
 #            print "aaa",emp_boj

 #        except:
 #            return Response(status=status.HTTP_400_BAD_REQUEST)







'''********** This ViewSets for Books_Type Model ***************************'''
class Books_Type_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Books_Type_ViewSet** is use for creation Book Type"""

	queryset        = Books_Type.objects.all()
	serializer_class = Books_Type_Serializer



	def create(self,request):


		request_user  =   request.user 

		emp_school    =   request_user.school

		data          =   json.loads(request.body)

		try:

			library_obj=Library.objects.get(school_name=emp_school)

		except:
			print 'yahhhhh'

			return Response( status=status.HTTP_400_BAD_REQUEST)
		
		book_type_obj =   Books_Type.objects.create(school_name = emp_school, created_by = request_user)

		serializer    =   Books_Type_Serializer(book_type_obj,data = data)

		if serializer.is_valid():

			serializer.save()

			return Response(status=status.HTTP_201_CREATED)

		else:
			print 'oooooo'

			return Response( status=status.HTTP_400_BAD_REQUEST)



	def list(self, request,*args):
				
		request_user = request.user
		emp_school = request_user.school


		book_type_obj = Books_Type.objects.filter(Q(school_name=emp_school)  & Q(is_deleted=False))

		serializer = Books_Type_Serializer(book_type_obj, many = True) 

		return Response(serializer.data,status=status.HTTP_200_OK)


	def retrieve(self, request,pk):

		try:

			request_user = request.user
			emp_school = request_user.school
			
			book_type_obj = Books_Type.objects.get(Q(school_name=emp_school) & Q(pk=pk) & Q(is_deleted=False))

			serializer = Books_Type_Serializer(book_type_obj) 
			return Response(serializer.data,status=status.HTTP_200_OK)

		except Exception as e:
			print e
			return Response(status=status.HTTP_204_NO_CONTENT)



	def update(self, request, pk):

		request_user          =   request.user
		emp_school            =   request_user.school
		data                  =   json.loads(request.body)

		book_type_name        =   data.get('book_type_name')
		other_info            =   data.get('other_info')
		is_active             =   data.get('is_active')

		try:
			book_type_obj = Books_Type.objects.get(Q(pk=pk) & Q(school_name=emp_school))
			book_type_obj.book_type_name = book_type_name
			book_type_obj.other_info = other_info


			if (is_active == False and book_type_obj.is_active == True) or (is_active == True and book_type_obj.is_active == False) :
				
				book_objects = Book_Detail.objects.filter(Q(book_type=book_type_obj) & Q(school_name=emp_school) & Q(is_deleted=False)).update(is_active=is_active)
				book_type_obj.is_active = is_active

			book_type_obj.save()	
			return Response(status=status.HTTP_205_RESET_CONTENT)

		except Exception as e:
			print e
			return Response(status=status.HTTP_400_BAD_REQUEST)



	def destroy(self, request, pk=None):

		request_user          =   request.user
		emp_school            =   request_user.school

		try:
 	 		book_type_obj = Books_Type.objects.get(Q(pk=pk) & Q(school_name=emp_school) & Q(is_deleted=False))
 	 		book_type_obj.is_deleted = True
 	 		book_type_obj.is_active = False

			book_objects = Book_Detail.objects.filter(Q(book_type=book_type_obj) & Q(school_name=emp_school) & Q(is_deleted=False)).update(is_active=False,is_deleted=True)

 	 		book_type_obj.save()
			return Response(status=status.HTTP_205_RESET_CONTENT)

		except Exception as e:
			print e
		 	return Response(status=status.HTTP_204_NO_CONTENT)




			

'''********** This ViewSets for Library_Rules Model ***************************'''
class Library_Rules_ViewSet(viewsets.ModelViewSet):

	queryset        = Library_Rules.objects.all()
	serializer_class=Library_Rules_Serializer


	"""This viewset **Library_Rules_ViewSet** is use for creation rules for library"""

	def create(self,request):


		request_user      =   request.user

		emp_school        =   request_user.school

		data              =   json.loads(request.body)

		book_type_pk      =   data.get('book_type')
		rules_for         =   data.get('rules_for')
		category          =   data.get('category')

		try:
			book_type_obj   =   Books_Type.objects.get(pk=book_type_pk)

			if rules_for == 'student':

				student_cet_obj  =  Student_Category.objects.get(pk=category)
				library_rules_obj =   Library_Rules.objects.filter(Q(book_type=book_type_obj) & Q(student_category=student_cet_obj) & Q(book_type__school_name=emp_school) & Q(is_deleted=False))

				if not library_rules_obj:

					library_rules_obj =   Library_Rules.objects.create(created_by = request_user,book_type=book_type_obj,student_category=student_cet_obj)

				else:
					return Response( status=status.HTTP_409_CONFLICT)

					

			elif rules_for== 'employee':

				emp_cet_obj  =  Category.objects.get(pk=category)
				library_rules_obj =   Library_Rules.objects.filter(Q(book_type=book_type_obj) & Q(employee_category=emp_cet_obj) & Q(book_type__school_name=emp_school) & Q(is_deleted=False))

				if not library_rules_obj:

					library_rules_obj =   Library_Rules.objects.create(created_by = request_user,book_type=book_type_obj,employee_category=emp_cet_obj)

				else:
					return Response( status=status.HTTP_409_CONFLICT)



			serializer        =   Library_Rules_Serializer(library_rules_obj,data = data)
			

			if serializer.is_valid():

				serializer.save()

				return Response(status=status.HTTP_201_CREATED)

			else:
				
				return Response( status=status.HTTP_400_BAD_REQUEST)

		except:
			return Response( status=status.HTTP_400_BAD_REQUEST)


	def list(self, request,*args):
				
		request_user = request.user
		emp_school = request_user.school

		book_type_pk          =   request.GET.get('book_type')
		rules_for             =   request.GET.get('rules_for')
		category              =   request.GET.get('category')

		print category,type(category)
		print rules_for, type(rules_for)

		try:
			if rules_for=='student':

				library_rules_obj = Library_Rules.objects.get(Q(book_type__school_name=emp_school) & Q(is_active=True) & Q(is_deleted=False) & Q(student_category=category) & Q(book_type=book_type_pk))

			if rules_for=='employee':

				library_rules_obj = Library_Rules.objects.get(Q(book_type__school_name=emp_school) & Q(is_active=True) & Q(is_deleted=False) & Q(employee_category=category) & Q(book_type=book_type_pk))

			serializer = Library_Rules_Serializer(library_rules_obj) 

			return Response(serializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			print e
			return Response( status=status.HTTP_204_NO_CONTENT)



	def update(self, request, pk):

		request_user          =   request.user
		emp_school            =   request_user.school
		data                  =   json.loads(request.body)

		max_days_for_issue    =   data.get('max_days_for_issue')
		after_due_date_fine   =   data.get('after_due_date_fine')

		no_of_maximum_reissue                                 =   data.get('no_of_maximum_reissue')
		tear_book_fine_in_percentage_of_book_Rate             =   data.get('tear_book_fine_in_percentage_of_book_Rate')
		missing_book_fine_in_percentage_of_book_Rate          =   data.get('missing_book_fine_in_percentage_of_book_Rate')
		discription_about_rules                               =   data.get('discription_about_rules')

		is_active        =   data.get('is_active')



		try:
			library_rule_obj = Library_Rules.objects.get(Q(pk=pk) & Q(book_type__school_name=emp_school))
			library_rule_obj.max_days_for_issue = max_days_for_issue
			library_rule_obj.after_due_date_fine = after_due_date_fine
			library_rule_obj.no_of_maximum_reissue = no_of_maximum_reissue
			library_rule_obj.tear_book_fine_in_percentage_of_book_Rate = tear_book_fine_in_percentage_of_book_Rate
			library_rule_obj.missing_book_fine_in_percentage_of_book_Rate = missing_book_fine_in_percentage_of_book_Rate
			library_rule_obj.discription_about_rules = discription_about_rules
			library_rule_obj.is_active = is_active			
			library_rule_obj.save()	

			return Response(status=status.HTTP_205_RESET_CONTENT)

		except Exception as e:
			print e
			return Response(status=status.HTTP_400_BAD_REQUEST)



	def destroy(self, request, pk=None):

		request_user          =   request.user
		emp_school            =   request_user.school

		try:
 	 		library_rule_obj = Library_Rules.objects.get(Q(pk=pk) & Q(book_type__school_name=emp_school) & Q(is_deleted=False))
 	 		print type(library_rule_obj)
 	 		library_rule_obj.is_deleted = True
 	 		library_rule_obj.is_active = False
 	 		library_rule_obj.save()
			return Response(status=status.HTTP_205_RESET_CONTENT)

		except Exception as e:
			print e
		 	return Response(status=status.HTTP_204_NO_CONTENT)






'''********** This ViewSets for Book_Detail Model ***************************'''
class Book_Detail_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Book_Detail_ViewSet** is use for create full detail of book"""

	queryset        = Book_Detail.objects.all()
	serializer_class=Book_Detail_Serializer

	# permission_classes= (Book_Detail_Read_and_Write_Permission,TokenHasReadWriteScope)

	

	def create(self,request):


		data                 =     json.loads(request.body)
		request_user         =     request.user
		emp_school           =     request_user.school
		school_code          =     request_user.school.school_code
		

		isbn                 =     data.get('book_ISBN')
		is_existing          =     data.get('is_existing')
		total_no_of_copies   =     data.get('total_no_of_copies')



	
		if not total_no_of_copies:
			total_no_of_copies=1
			total_no_of_copies=int(total_no_of_copies)
		else:
			total_no_of_copies=int(total_no_of_copies)



		if is_existing:

			try:
				detail=Book_Detail.objects.filter(Q(book_ISBN=isbn)& Q(school_name=emp_school)& Q(is_deleted=False))

				if not detail:
					return Response("this isbn or school is not existing")

				else:
				
					for i in detail:
						book_type_name=i.book_type
						t=str(book_type_name)
						break


					prefix=school_code+t[0:3]
					filtr=Book_Detail.objects.filter(book_id__contains=prefix)
					m=filtr.aggregate(Max('book_id'))
					m=m.get('book_id__max')

					book_id=""
					suffix=m[-5:]

					int_suffix=int(suffix)

					if int_suffix<9 :
						suffix="0000"+str(int_suffix+1)
					elif int_suffix>=9 and int_suffix<99:
						suffix="000"+str(int_suffix+1)
					elif int_suffix>=99 and int_suffix<999:
						suffix="00"+str(int_suffix+1)
					elif int_suffix>=999 and int_suffix<9999:
						suffix="0"+str(int_suffix+1)
					elif int_suffix>=9999 and int_suffix<99999:
						suffix=""+str(int_suffix+1)
					book_id=prefix+suffix






					book_detail                 =   Book_Detail()
					book_detail.book_type       =   i.book_type
					book_detail.school_name     =   i.school_name
					book_detail.book_id         =   book_id
					book_detail.book_ISBN       =   i.book_ISBN
					book_detail.book_name       =   i.book_name
					book_detail.book_author     =   i.book_author
					book_detail.book_price      =   i.book_price
					book_detail.book_language   =   i.book_language
					book_detail.is_active       =   data.get('is_active')
					book_detail.created_by      =   request_user
					book_detail.edition         =   i.edition


						
						

					book_detail.save()



					book_type=Books_Type.objects.get(Q(school_name=emp_school) & Q(book_type_name=book_type_name)& Q(is_deleted=False))						
					book_type.total_books=book_type.total_books+1
					book_type.save()

			except Exception as e:
				print e
				return Response(e,status=status.HTTP_400_BAD_REQUEST)


				


									
		else:

			book_type_name    =   data.get('book_type')
			books_Type        =   Books_Type.objects.get(Q(pk=book_type_name) & Q(is_deleted=False)& Q(school_name=emp_school))
			book_type_name    =   books_Type.book_type_name
			book_type_school  =  books_Type.school_name

			isbn  =  data.get('book_ISBN')
			book_isbn_obj = Book_Detail.objects.filter(Q(book_ISBN=isbn)& Q(is_deleted=False)& Q(school_name=emp_school))

			if book_isbn_obj:

				return Response(status=status.HTTP_409_CONFLICT)


			if book_type_school==emp_school:

				prefix = school_code+book_type_name[0:3]

				filtr=Book_Detail.objects.filter(book_id__contains=prefix)
				m=filtr.aggregate(Max('book_id'))
				m=m.get('book_id__max')
			




				book_id=""
				if not m :
					book_id=prefix+"00001"

				else:
												
					suffix=m[-5:]
					int_suffix=int(suffix)

					if int_suffix<9 :
						suffix="0000"+str(int_suffix+1)
					elif int_suffix>=9 and int_suffix<99:
						suffix="000"+str(int_suffix+1)
					elif int_suffix>=99 and int_suffix<999:
						suffix="00"+str(int_suffix+1)
					elif int_suffix>=999 and int_suffix<9999:
						suffix="0"+str(int_suffix+1)
					elif int_suffix>=9999 and int_suffix<99999:
						suffix=""+str(int_suffix+1)

					book_id=prefix+suffix



				'''####### to save created_by only for Employee#########'''




				book_detail                =    Book_Detail()
				book_detail.created_by     =    request_user
				book_detail.book_id        =    book_id
				book_detail.school_name    =    emp_school
				book_detail.book_type      =    books_Type				
				book_detail.book_ISBN      =    data.get('book_ISBN')				
				book_detail.book_name      =    data.get('book_name')
				book_detail.book_title     =    data.get('book_title')
				book_detail.book_author    =    data.get('book_author')
				book_detail.book_price     =    data.get('book_price')
				book_detail.book_language  =    data.get('book_language')
				book_detail.edition        =    data.get('edition')
				book_detail.is_active      =    data.get('is_active')
									
				book_detail.save()			

				Book_type_pk               =    data.get('book_type')
				book_type_obj              =    Books_Type.objects.get(Q(pk=Book_type_pk)& Q(is_deleted=False)& Q(school_name=emp_school))
				book_type_obj.total_books  =    book_type_obj.total_books+1

				book_type_obj.save()
			
			else:
				return Response( status=status.HTTP_400_BAD_REQUEST)


		
		if(total_no_of_copies>1):

			detail=Book_Detail.objects.filter(Q(book_ISBN=isbn)& Q(school_name=emp_school)& Q(is_deleted=False))

			if not detail:
				return Response(status=status.HTTP_400_BAD_REQUEST)


			else:

				for i in detail:
						book_type_name=i.book_type
						t=str(book_type_name)
						break


				for j in range(1,total_no_of_copies):

						prefix  = school_code+t[0:3]
						filtr   = Book_Detail.objects.filter(book_id__contains=prefix)
						m       = filtr.aggregate(Max('book_id'))
						m       = m.get('book_id__max')

						book_id = ""
						suffix  = m[-5:]

						int_suffix=int(suffix)

						if int_suffix<9 :
							suffix = "0000"+str(int_suffix+1)
						elif int_suffix >= 9 and int_suffix<99:
							suffix="000"+str(int_suffix+1)
						elif int_suffix >= 99 and int_suffix<999:
							suffix="00"+str(int_suffix+1)
						elif int_suffix >= 999 and int_suffix<9999:
							suffix="0"+str(int_suffix+1)
						elif int_suffix >= 9999 and int_suffix<99999:
							suffix=""+str(int_suffix+1)
						book_id=prefix+suffix




						book_detail               = Book_Detail()
						book_detail.created_by    = request_user
						book_detail.book_type     = i.book_type
						book_detail.school_name   = i.school_name
						book_detail.book_id       = book_id
						book_detail.book_ISBN     = i.book_ISBN
						book_detail.book_name     = i.book_name
						book_detail.book_author   = i.book_author
						book_detail.book_price    = i.book_price
						book_detail.book_language = i.book_language
						book_detail.is_active     = data.get('is_active')
						book_detail.edition       = i.edition
						
						
						

						book_detail.save()



						book_type = Books_Type.objects.get(Q(school_name=emp_school) & Q(book_type_name=book_type_name)& Q(is_deleted=False))
						
						book_type.total_books = book_type.total_books+1
						book_type.save()
		

		if total_no_of_copies :

			try:
				library_obj=Library.objects.get(school_name=emp_school)
				print library_obj, type(library_obj), "library_obj"
				print library_obj.total_books, "before"
				library_obj.total_books=library_obj.total_books+total_no_of_copies
				library_obj.save()
				print library_obj.total_books,"after"
			except:
				return Response( status=status.HTTP_400_BAD_REQUEST)




		serializer=Book_Detail_Serializer(book_detail)
		
		return Response(status=status.HTTP_201_CREATED)

	'''@@@@@@@@@  Here start Book searching logic  @@@@@@@@@'''

	def list(self, request):

		print 'hi in list of book_detail'

		request_user          =   request.user
		emp_school            =   request_user.school

		# sort                  =   request.GET.get('sort')
		page                  =   request.GET.get('page')
		search                =   request.GET.get('search')
		value                 =   request.GET.get('value')
		book_type_pk          =   request.GET.get('book_type')
		# select_list         =   request.GET.get('select_list')
		# bulk_action         =   request.GET.get('bulk_action')
		recently_added        =   request.GET.get('recently_added')

		book_pk = request.GET.get('book')

		try:

			if not book_pk == "null":

				book_detail_obj = Book_Detail.objects.get(pk=book_pk)
				book_isbn = book_detail_obj.book_ISBN
				book_detail = Book_Detail.objects.filter(Q(book_ISBN=book_isbn) & Q(is_deleted=False))
				total_objects = book_detail.count()

				book_detail = Book_Detail.objects.filter(Q(book_ISBN=book_isbn) & Q(is_issue=False) & Q(is_deleted=False))
				total_available_objects = book_detail.count()


				if  search == 'delete_operation':
					serializer = Book_Detail_For_Active_Inactive_Serializer(book_detail,many=True) 

				else:
					serializer = Book_Detail_Serializer(book_detail_obj) 

				response_json = {'books':serializer.data, 'total_copies':total_objects, 'total_available_copies':total_available_objects}						

				return Response(response_json,status=status.HTTP_200_OK)

			else:

				if search    ==  "all":
					print 'in searching'

					book_detail_obj  =   Book_Detail.objects.filter(Q(school_name=emp_school)  & Q(is_deleted=False) & Q(is_active=True)).distinct('book_ISBN')

				elif search  ==  'book_name':

					book_detail_obj  =   Book_Detail.objects.filter(Q(school_name=emp_school) & Q(book_name__istartswith=value) & Q(is_deleted=False) & Q(is_active=True)).distinct('book_ISBN')

				elif search  ==  'isbn':

					book_detail_obj  =   Book_Detail.objects.filter(Q(school_name=emp_school) & Q(book_ISBN=value) & Q(is_deleted=False) & Q(is_active=True)).distinct('book_ISBN')			

				elif search  ==  'author':

					book_detail_obj  =   Book_Detail.objects.filter(Q(school_name=emp_school) & Q(book_author__istartswith=value) & Q(is_deleted=False) & Q(is_active=True)).distinct('book_ISBN')

				elif search  ==  'book_id':


					book_detail_obj  =   Book_Detail.objects.filter(Q(school_name=emp_school) & Q(book_id=value) & Q(is_deleted=False) & Q(is_active=True)).distinct('book_ISBN')



				else:
					return Response( status =  status.HTTP_400_BAD_REQUEST)



				if not book_type_pk=="null":
					

				 	book_detail_obj = book_detail_obj.filter(book_type__id=book_type_pk).distinct('book_ISBN')


				if recently_added=="true":



					my_objects=[]
					new_list=[]
					for book_obj in book_detail_obj:

						my_objects.append(book_obj.id)


					my_objects.sort()
					new_list=my_objects[-15:]

					book_detail_obj=book_detail_obj.filter(pk__in=new_list)






				p = Paginator(book_detail_obj, 15)
				total_num_pages =  p.num_pages
					
				if page:

					page = int(page)
					if page<1:
						return Response(status = status.HTTP_400_BAD_REQUEST)	
							
					else:
						request_object  =  p.page(page)
								
				else:
						
					request_object  =  p.page(1)
						
						
						
						
				serializer = Book_General_Detail_Serializer(request_object, many = True)
				response_json = {'books':serializer.data, 'total_pages':total_num_pages}

				return Response(response_json,status=status.HTTP_200_OK)

		except Exception as e:		
			return Response(status=status.HTTP_400_BAD_REQUEST)    



	def retrieve(self, request,pk):

		request_user = request.user
		emp_school = request_user.school
		
		book_detail_obj = Book_Detail.objects.get(Q(school_name=emp_school) & Q(pk=pk))

		serializer = Book_Detail_Serializer(book_detail_obj) 
		return Response(serializer.data,status=status.HTTP_200_OK)


	def update(self, request, pk):

		request_user          =   request.user
		emp_school            =   request_user.school
		data                  =   json.loads(request.body)

		book_name   =   data.get('book_name')
		book_author  =   data.get('book_author')
		book_language  =   data.get('book_language')
		select_book_cover_image     =   data.get('select_book_cover_image')
		is_active     =   data.get('is_active')
		urlvalue = data.get('urlvalue')



		try:
			if urlvalue == 'active_inactive':
				book_obj = Book_Detail.objects.get(Q(pk=pk) & Q(school_name=emp_school) & Q(is_deleted=False))

				book_obj.is_active=is_active			
				book_obj.save()	
				return Response(status=status.HTTP_205_RESET_CONTENT)
			else:

				book_obj = Book_Detail.objects.get(Q(pk=pk) & Q(school_name=emp_school))
				book_ISBN = book_obj.book_ISBN 
				total_books_regarding_isbn = Book_Detail.objects.filter(Q(book_ISBN=book_ISBN) & Q(is_deleted=False)).update(book_name=book_name, book_author=book_author, book_language=book_language, is_active=is_active, select_book_cover_image=select_book_cover_image)

				return Response(status=status.HTTP_205_RESET_CONTENT)

		except Exception as e:
			print e
			return Response(status=status.HTTP_400_BAD_REQUEST)



	def destroy(self, request, pk):

		request_user          =   request.user
		emp_school            =   request_user.school

		try:
			print pk ,"hhlkhhlddhdl"
 	 		book_obj = Book_Detail.objects.get(Q(pk=pk) & Q(is_deleted=False))
 	 		book_obj.is_deleted = True
 	 		book_obj.is_active = False
 	 		book_obj.save()

			library_obj=Library.objects.get(school_name=emp_school)

			total_books=library_obj.total_books
			total_books=total_books-1

			library_obj.total_books=total_books
			library_obj.save()

			book_type_obj=book_obj.book_type
			total_book=book_type_obj.total_books
			total_book=total_book-1

			book_type_obj.total_books=total_book
			book_type_obj.save()

			return Response(status=status.HTTP_205_RESET_CONTENT)

		except Book_Detail.DoesNotExist:
		 	return Response(status=status.HTTP_204_NO_CONTENT)



'''********** This ViewSets for Issue_Book Model ***************************'''
class Issue_Book_ViewSet(viewsets.ModelViewSet):

    """This viewset **Issue_Book_ViewSet** is use for issue book by librarian"""

    queryset= Issue_Book.objects.all()
    serializer_class=Issue_Book_Serializer

    # permission_classes= (Issue_Book_Read_and_Write_Permission,TokenHasReadWriteScope)

    def create(self,request):


        request_user          =   request.user
        emp_school            =   request_user.school


        data=json.loads(request.body)
        book_detail=data.get('book_id')


        user_type         =   data.get('user_type')
        user_id           =   data.get('user_id')

# '''################################################'''       
       
        try:

            book_detail_obj=Book_Detail.objects.get(Q(book_id=book_detail) & Q(school_name=emp_school))
            book_detail_school=book_detail_obj.school_name
            is_active=book_detail_obj.is_active
            is_issue=book_detail_obj.is_issue

            book_type=book_detail_obj.book_type



            if user_type=="student":

                user_obj=Student.objects.get(pk=user_id)
                user_school=user_obj.school

            elif user_type=="employee":

        	    emp_boj=Employee.objects.get(pk=user_id)
        	    user_school=emp_boj.school


        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)






        try:

            if (book_detail_school==user_school and is_active==True and is_issue==False) :
              
            

                if user_type=="student":

                    cet=user_obj.student_category
                    lr=Library_Rules.objects.get(Q(student_category=cet)  & Q(book_type__school_name=emp_school) & Q(book_type=book_type) & Q(is_deleted=False))


                elif user_type=="employee":

                    designation_obj=emp_boj.designation.category

                    
                    
                    lr=Library_Rules.objects.get(Q(employee_category=designation_obj)  & Q(book_type__school_name=emp_school) & Q(book_type=book_type) & Q(is_deleted=False))



                   
#                    lr=Library_Rules.objects.get(Q(employee_category=designation_obj)  & Q(book_type__school_name=emp_school) & Q(book_type=book_typ

                  


                md= lr.max_days_for_issue                    	
                d = timedelta(days=md)            
                x=datetime.now().date()+d



                issue_book=Issue_Book()

                if user_type=="student":                          
                    issue_book.student_id=user_obj

                elif user_type=="employee":
                    issue_book.employee_id =emp_boj
  

                issue_book.created_by = request_user
                
                issue_book.book_detail = book_detail_obj
                
                issue_book.library_rules = lr
                
                issue_book.due_date = x
                
                issue_book.is_reissue=data.get('is_reissue')
                
       
                abc=data.get('date_of_return')

                d =None
                if not abc:

                    d='1900-01-01'
                else :

                    d=abc
                    d=datetime.strptime(abc, '%Y-%m-%d').date()

                issue_book.date_of_return=d

                issue_book.save()
 
                book_detail_obj.is_issue=True
                book_detail_obj.save()

                # libobj=Library()
                lib_obj = Library.objects.get(school_name=emp_school)
                lib_obj.total_issue_books=lib_obj.total_issue_books+1
                lib_obj.save()

                book_type.total_issue_books=book_type.total_issue_books+1
                book_type.save()




    
                serializer = Issue_Book_Serializer(issue_book)
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)    
     
        except Exception as e:
            print "hooooooooooo",e
            return Response( status=status.HTTP_400_BAD_REQUEST)

    
                            



    def list(self, request,*args):

		request_user          =   request.user
		emp_school            =   request_user.school

		page                  =   request.GET.get('page')
		start_date            =   request.GET.get('start_date')
		end_date              =   request.GET.get('end_date')		
		issue_book            =   request.GET.get('issue_book')
		due_book              =   request.GET.get('due_book')
		category              =   request.GET.get('category')
		user_id               =   request.GET.get('user_id')
		isuue_book_pk	      =   request.GET.get('isuue_book_pk')
		urlvalue              =   request.GET.get('urlvalue')
		book_loss             =   request.GET.get('book_loss')		
		fine_pk               =   request.GET.get('fine_pk')		
		
		if urlvalue=="return_book":

			try:
				task = Issue_Book.objects.get(pk=isuue_book_pk)
				pk_issue_book = task.pk	

				due_date=task.due_date
				today_date=datetime.now().date()

				book_detail_obj=task.book_detail 
				is_issue=book_detail_obj.is_issue
				book_price=int(book_detail_obj.book_price)				

				if is_issue:

					fine=0
					due_date_fine=0


					if (due_date<today_date):

						total_days=today_date-due_date

						"""convert datetime.timedelta into days"""

						total_days= total_days.days
						total_day=str(total_days)
						total_day=int(total_day)
						print total_day

						rules_fine=task.library_rules.after_due_date_fine
						due_date_fine=rules_fine*total_day

						

						print 'this fine due_date',due_date_fine


					if book_loss=="tearbook":
						rules_fine=task.library_rules.tear_book_fine_in_percentage_of_book_Rate
						fine=(book_price/100)*rules_fine
						print 'tearbook_rules_fine',rules_fine,fine

					elif book_loss=="missingbook":
						rules_fine=task.library_rules.missing_book_fine_in_percentage_of_book_Rate
						fine=(book_price/100)*rules_fine
						print 'missingbook_rules_fine',rules_fine,fine


					
					total_fine =	due_date_fine +  fine

					if (due_date<today_date or book_loss=="tearbook" or book_loss=="missingbook"):

						fine_history=Fine_History.objects.get_or_create(issue_book=task,is_paid=False)

						if fine_history[0]:

							fine_history_object=fine_history[0]

							fine_history_object.total_fine=total_fine
							fine_history_object.save()					


					serializer = Issue_Book_with_Book_Detail_Serializer(task)
					response_json = {'books':serializer.data, 'total_fine':total_fine}						





				return Response(response_json,status=status.HTTP_200_OK)

			except Exception as e:
				print e
				return Response(status=status.HTTP_400_BAD_REQUEST)


		elif urlvalue=="library_fine":

			if not start_date==None:
				print start_date,end_date
				issue_books=Fine_History.objects.filter(Q(create_at__gte=start_date) & Q (create_at__lte=end_date) & Q (is_paid=False) & Q (issue_book__book_detail__school_name=emp_school))
				print issue_books


			elif not fine_pk==None:

				issue_books=Fine_History.objects.filter(pk=fine_pk)

			


		
		elif issue_book=="true":
			print user_id
			
			issue_books=Issue_Book.objects.filter(Q(date_of_issue__gte=start_date) & Q (date_of_issue__lte=end_date) & Q(library_rules__book_type__school_name=emp_school))
			print "issue_books log",issue_books



		elif due_book=="true":
			print "check return date"
			issue_books=Issue_Book.objects.filter(Q(library_rules__book_type__school_name=emp_school) & Q(date_of_issue__gte=start_date) & Q (date_of_issue__lte=end_date) & Q(date_of_return="1900-01-01"))

		elif not user_id=="null":
			print "gyaaaaaaaaaa in user id"

			if category=="student":

				issue_books=Issue_Book.objects.filter(Q(library_rules__book_type__school_name=emp_school) & Q(student_id=user_id) & Q(date_of_return='1900-01-01'))

			elif category=="employee":

			
				issue_books=Issue_Book.objects.filter(Q(library_rules__book_type__school_name=emp_school) & Q(employee_id=user_id) & Q(date_of_return='1900-01-01'))


			if not isuue_book_pk == "null":


				issue_books = issue_books.filter(pk=isuue_book_pk)

		else:
			print 'today_date',date.today
			issue_books=Issue_Book.objects.filter((Q(date_of_issue=date.today()) | Q(reissue_date=date.today())) & Q(library_rules__book_type__school_name=emp_school))




		p = Paginator(issue_books, 15)
		total_num_pages =  p.num_pages
				
		if page:

			page = int(page)

			if page<1:
				return Response(status = status.HTTP_400_BAD_REQUEST)	
						
			else:
					request_object  =  p.page(page)
							
		else:
					
			request_object  =  p.page(1)


		if not user_id=="null":

			serializer = Issue_Book_with_Book_Detail_Serializer(request_object, many= True)

		
		elif urlvalue=="library_fine":

			if not fine_pk==None:

				serializer = Fine_History_with_Book_Detail_Serializer(request_object, many= True)	

			else:

				serializer = Fine_History_Serializer(request_object, many= True)



		else:

			serializer = Issue_Book_Detail_with_Stu_Emp_Serializer(request_object, many= True)


		response_json = {'books':serializer.data, 'total_pages':total_num_pages}

		return Response(response_json,status=status.HTTP_200_OK)




    def update(self, request, pk):

        request_user          =   request.user
        emp_school            =   request_user.school

        try:
            task = Issue_Book.objects.get(pk=pk)
            print "aaa",task

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        data=json.loads(request.body)
        is_reissue=data.get('is_reissue')
        print is_reissue
        return_book=data.get('return_book')
        print return_book

        for_student=data.get('for_student')
        print  "for_student",for_student   

        book_detail_obj=task.book_detail                        
        is_issue=book_detail_obj.is_issue



        no_of_times_reissue=task.no_times_reissue
        print "no_of_times_reissue",no_of_times_reissue
        no_of_maximum_reissue=task.library_rules.no_of_maximum_reissue
        print "no_of_maximum_reissue",no_of_maximum_reissue
        due_date=task.due_date
        today_date=datetime.now().date()
              


        if (is_reissue and no_of_times_reissue<no_of_maximum_reissue and is_issue):
            
                  


            max_days_for_issue=task.library_rules.max_days_for_issue
            print max_days_for_issue
            convert_days = timedelta(days=max_days_for_issue) 
            new_due_Date=today_date+convert_days
            print "new due date",new_due_Date

            task.is_reissue=is_reissue
            task.due_date=new_due_Date
            task.updated_by=request_user
            task.reissue_date=today_date

            task.no_times_reissue=no_of_times_reissue+1 
                
            task.save()              
            return Response(status=status.HTTP_205_RESET_CONTENT)


        
        elif return_book==True:

            if is_issue:

                fine = data.get('fine')
                tearbook = data.get('tearbook')
                missingbook = data.get('missingbook')
                due_date = data.get('due_date')

                fine_type=""

                if tearbook==True:
                    fine_type = fine_type+"  " + "applicable tear book fine"
                
                if missingbook==True:
                    fine_type = fine_type+" & " + "applicable missing book fine"

                if due_date==True:
                    fine_type = fine_type+" & " + "applicable after due date submiting fine"
    
 
                if tearbook or missingbook or due_date:

                   
                    fine_history=Fine_History.objects.get_or_create(issue_book=task,is_paid=False)

                    if fine_history[0]:

                        fine_history_object=fine_history[0]
                        fine_history_object.is_pending = fine

                            
                

                    if fine_history_object.fine_type==None:
                	    fine_history_object.fine_type=""
                    fine_history_object.fine_type = fine_history_object.fine_type+" & "+ fine_type

                    fine_history_object.created_by = request_user

                    fine_history_object.save()                   




                book_detail_obj.is_issue=False
                book_detail_obj.save()

                library=Library.objects.get(school_name=emp_school)
                library.total_issue_books=library.total_issue_books-1
                library.save()

                book_type=book_detail_obj.book_type
                book_type.total_issue_books=book_type.total_issue_books-1
                book_type.save()


                task.date_of_return=today_date
                task.updated_by=request_user
                task.save()

            
                return Response(status=status.HTTP_205_RESET_CONTENT)
        
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:        

            return Response(status=status.HTTP_400_BAD_REQUEST)

'''********** This ViewSets for Fine_History Model ***************************'''
class Fine_History_ViewSet(viewsets.ModelViewSet):


	queryset        = Fine_History.objects.all()
	serializer_class= Fine_History_Serializer


	def list(self, request,*args):

		request_user          =   request.user
		emp_school            =   request_user.school

		urlvalue              =   request.GET.get('urlvalue')
		start_date            =   request.GET.get('start_date')
		end_date              =   request.GET.get('end_date')		
		
		
		if urlvalue=="total_fine":
			fine_objects = Fine_History.objects.filter(Q(create_at__lte=start_date) & Q(create_at__gte=end_date))
			print fine_objects
			return response('suceess')



	



#'''************now we start Viewsets for Iventory *********************'''

#'''********** This ViewSets for Issue_Book Model ***************************'''

class Product_Type_ViewSet(viewsets.ModelViewSet):

    """This viewset **Product_Type_ViewSet** is use for Iventory Purpose and it creates product Type"""

    queryset      = Product_Type.objects.all()    
    serializer_class=Product_Type_Serializer	


'''********** This ViewSets for Product_Detail Model ***************************'''
class Product_Detail_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Product_Detail_ViewSet** is use for Iventory Purpose and it creates product detail"""

	queryset        = Product_Detail.objects.all()
	serializer_class=Product_Detail_Serializer	



'''********** This ViewSets for Break_product_Detail Model ***************************'''
class Break_product_Detail_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Break_product_Detail_ViewSet** is use for Iventory Purpose and it creates detail for break product"""

	queryset        = Break_product_Detail.objects.all()
	serializer_class=Break_product_Detail_Serializer	


'''********** This ViewSets for Product_Request Model ***************************'''
class Product_Request_ViewSet(viewsets.ModelViewSet):

	"""This viewset **Product_Request_ViewSet** is use for Iventory Purpose and it creates detail for Product_Request"""

	queryset        = Product_Request.objects.all()
	serializer_class=Product_Request_Serializer	




















	











