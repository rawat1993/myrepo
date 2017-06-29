# from rest_framework.permissions import BasePermission, SAFE_METHODS
# import json
# # from libraryApp.models import Library
# from userAuthentication.models import MyUser
# from django.db.models import Q


# '''########## This is for Library model permissions'''

# class Library_Read_and_Write_Permission(BasePermission):

#     print "inside Library permission classes"


#     def has_permission(self, request, view):
#         print "has permissions for library"


#         if request.method in SAFE_METHODS:

#             users=MyUser.objects.filter(Q(employee__category__category_name__iexact='admin') & Q(employee__school_id=request.user.school) | Q(employee__category__category_name__iexact='librarian') & Q(employee__school_id=request.user.school))

#             if request.user in users:

#                 return True

#             else:
#                 return False    


#         users=MyUser.objects.filter(Q(employee__category__category_name__iexact='admin') & Q(employee__school_id=request.user.school))       
        
#         if request.user in users:

#             if request.method == 'POST' and request.user.school.id ==json.loads(request.body).get('school_name'):
        
#                 return True 


#             elif request.method == 'PUT' and request.user.school.id ==json.loads(request.body).get('school_name'):

#                 return True          


#             elif request.method == 'DELETE':

#                 return True          


#     def has_object_permission(self, request, view, obj):

#         if request.method == 'PUT' and request.user.school.id==json.loads(request.body).get('school_name'):
#             return True

#         elif request.method == 'GET':
#             return True 

#         elif request.method == 'DELETE' and request.user.school.id==json.loads(request.body).get('school_name'):
#             return True          




# '''########## This is for Book_Detail model permissions'''

# class Book_Detail_Read_and_Write_Permission(BasePermission):

#     print "inside Book_detail permission classes"

#     def has_permission(self, request, view):
#         print "has permissions for Book_detail"
#         print 'request.user.school=>',request.user.school.id
        
#         if request.method in SAFE_METHODS:

#             print 'success'
#             print request.user,type(request.user.user_type)
           
        
#             users=MyUser.objects.filter(Q(employee__category__category_name__iexact='librarian') & Q(employee__school_id=request.user.school) | Q(user_type='student') & Q(student__school_id=request.user.school))

#             if request.user in users:         
#                 print "request.user",request.user
#                 print "students are  allowed"
#                 return True


#         # print Library.objects.get(pk=json.loads(request.body).get('library')).school_name

#         users=MyUser.objects.filter(Q(employee__category__category_name__iexact='librarian') & Q(employee__school_id=request.user.school))
        
#         if request.user in users:

#             if request.method == 'POST' and request.user.school.id == json.loads(request.body).get('school_id'):

#                 print "this is POST"

#                 return True 


#             elif request.method == 'PUT' and request.user.school.id == json.loads(request.body).get('school_id'):

#                 print "in has_objectttttt "
#                 return True          


#             elif request.method == 'DELETE':
#                 print "in has_objectttttt "
#                 return True



                      

#     def has_object_permission(self, request, view, obj):
#         print "has objct permissions"
#         print "request.user",request.user,type(request.user)
#         print "request.user",request.user.user_type,type(request.user.user_type)

#         if request.method == 'PUT':
#             print "in has_object put method "
#             return True

#         elif request.method == 'GET':
#             print "in has_object get method "
#             return True 

#         elif request.method == 'DELETE' and request.user.school.id==json.loads(request.body).get('school_id'):
#             print "in has_object delete method"
#             return True



# class Issue_Book_Read_and_Write_Permission(BasePermission):

#     print "inside issue book permission classes"


#     def has_permission(self, request, view):
#         print "has permissions for issue book"
#         print 'request.user.school=>',request.user.school.id
        
#         if request.method in SAFE_METHODS:


#             users=MyUser.objects.filter(Q(employee__category__category_name__iexact='librarian') & Q(employee__school_id=request.user.school) | Q(user_type='student') & Q(student__school_id=request.user.school))

#             if request.user in users:
#                 print "request.user",request.user
#                 print "students are  allowed"
#                 return True


#         # print Library.objects.get(pk=json.loads(request.body).get('library')).school_name

#         users=MyUser.objects.filter(Q(employee__category__category_name__iexact='librarian') & Q(employee__school_id=request.user.school))

#         if request.user in users:

#             if request.method == 'POST' and request.user.school.id == json.loads(request.body).get('school_id'):

#                 print "this is POST"

#                 return True 


#             elif request.method == 'PUT' and request.user.school.id==json.loads(request.body).get('school_id'):

#                 print "in has_objectttttt "
#                 return True          


#             elif request.method == 'DELETE':
#                 print "in has_objectttttt "
#                 return True



                      

#     def has_object_permission(self, request, view, obj):
#         print "has objct permissions"
#         print "request.user",request.user,type(request.user)
#         print "request.user",request.user.user_type,type(request.user.user_type)

#         if request.method == 'PUT':
#             print "in has_object put method "
#             return True

#         elif request.method == 'GET':
#             print "in has_object get method "
#             return Trues 

#         elif request.method == 'DELETE' and request.user.school.id==json.loads(request.body).get('school_id'):
#             print "in has_object delete method"
#             return True       





