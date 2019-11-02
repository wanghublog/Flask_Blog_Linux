'''1.定义解析器'''
from flask_restful import reqparse

post_get_parser = reqparse.RequestParser()
post_post_parser = reqparse.RequestParser()
user_post_parser = reqparse.RequestParser()
post_put_parser = reqparse.RequestParser()
post_delete_parser = reqparse.RequestParser()
#get
post_get_parser.add_argument(
    'page',
    type=int,
    location=['json', 'args', 'headers'],
    required=False)

post_get_parser.add_argument(
    'user',
    type=str,
    location=['json', 'args', 'headers'])


#post
post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Title is required!')

post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help='Text is required!')

post_post_parser.add_argument(
    'tags',
    type=str,
    action='append')#action指定了传入的参数会转换为以字典为元素的列表数据类型. 这是为了便于创建 post.tags 对象.

post_post_parser.add_argument(
    'token',#定义 token 参数是为了后期的身份认证做准备
    type=str,
    required=True,
    help='Auth Token is required to create posts.')


# User's HTTP Request Parser
user_post_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='Username is required!')

user_post_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='Password is required!')


#put 
post_put_parser.add_argument(
    'title',
    type=str)
 
post_put_parser.add_argument(
    'text',
    type=str)
 
post_put_parser.add_argument(
    'tags',
    type=str,
    action='append')
 
post_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to update the posts.')

#delete
post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to update the posts.')