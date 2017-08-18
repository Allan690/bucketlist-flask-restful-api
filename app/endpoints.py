from app.app import api
from app.app import UserLogin, UserLogout, UserRegistration, BucketList, SingleBucketList, BucketListItems, \
                    SingleBucketListItem

"""Authentication endpoints"""
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogout, '/auth/logout')
api.add_resource(UserRegistration, '/auth/register')

"""Bucketlist endpoints"""
api.add_resource(BucketList, '/bucketlist')
api.add_resource(SingleBucketList, '/bucketlist/<int:id>')

"""Bucketlist items endpoints"""
api.add_resource(BucketListItems, '/bucketlist/<int:id>/items')
api.add_resource(SingleBucketListItem, '/bucketlist/<int:id>/items/<int:item_id>')


