import datetime
import uuid
import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import api, app, Resource, User, db, Session, Bucketlist, models, BucketlistItems
from app.decorators import token_required

login_parser = api.parser()
login_parser.add_argument('name', type=str, help='Username', location='form', required=True)
login_parser.add_argument('password', type=str, help='Password', location='form', required=True)


class UserLogin(Resource):
    '''Allow a user to login to the Bucketlist application'''

    @api.doc(parser=login_parser)
    def post(self):
        '''Login a user.'''
        args = parser.parse_args()
        name = args['name']
        passwd = args['password']

        if not name or not passwd:
            return {
                       "message": "Fill all fields!!"
                   }, 400

        user = User.query.filter_by(name=name).first()

        if not user:
            return {
                       "message": "Wrong credentials!!"
                   }, 403

        if check_password_hash(user.password, passwd):
            token = jwt.encode(
                {'public_id': user.public_id,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                 },
                app.config['SECRET']
            )

            session = Session(user_id=user.public_id, token=token.decode('UTF-8'))
            db.session.add(session)
            db.session.commit()

            return {
                       'name': user.name,
                       'id': user.id,
                       'token': token.decode('UTF-8'),
                       'created_date': str(user.date_created),
                   }, 200


parser = api.parser()
parser.add_argument('name', type=str, help='Username', location='form')
parser.add_argument('password', type=str, help='Password', location='form')


class UserLogout(Resource):
    '''Allow a user to logout from the the Bucketlist application.'''

    method_decorators = [token_required]

    def get(self, current_user):
        '''Logout a user.'''
        token = request.headers['token']
        session_exist = Session.query.filter_by(user_id=current_user.public_id, token=token).first()

        if session_exist:
            db.session.delete(session_exist)
            db.session.commit()

            return {
                       "message": "You have successfully logged out.",
                   }, 200


class UserRegistration(Resource):
    '''Allow a user to register.'''

    @api.doc(parser=parser)
    def post(self):
        '''Create new user.'''
        args = parser.parse_args()
        name = args['name']
        passwd = args['password']

        if not name or not passwd:
            return {
                       "message": "Provide your name and password!!"
                   }, 400

        hashed_password = generate_password_hash(passwd, method='sha256')

        if User.query.filter_by(name=name).first():
            return {
                       "message": "Username taken!!"
                   }, 409

        new_user = User(public_id=str(uuid.uuid4()), name=name, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        response = jsonify({
            "message": "Registration successful."
        })

        response.status_code = 201

        return response


bucket_get_parser = api.parser()
bucket_post_parser = api.parser()

bucket_get_parser.add_argument('page', type=int, help='Page number, default=1')
bucket_get_parser.add_argument('limit', type=int, help='Limit per page, default=5')
bucket_get_parser.add_argument('q', type=str, help='Search')
bucket_post_parser.add_argument('desc', type=str, help='Bucketlist Description', location='form')


class BucketList(Resource):
    '''Shows a list of all user bucketlist, and lets you POST to add new bucketlists.'''
    method_decorators = [token_required]

    @api.doc(parser=bucket_get_parser)
    def get(self, current_user):
        '''List all user's bucketlists.'''
        args = bucket_get_parser.parse_args()
        page = args['page']
        limit = args['limit']
        q = args['q']

        if page:
            try:
                page = int(page)
                if page < 1:
                    return {
                               "message": "Page number must be a positive integer!! "
                           }, 400
            except Exception:
                return {
                           "message": "Invalid page value!!"
                       }, 400
        else:
            page = 1

        if limit:
            try:
                limit = int(limit)
                if limit < 1:
                    return {
                               "message": "Limit number must be a positive integer!! "
                           }, 400
            except Exception:
                return {
                           "message": "Invalid limit value!!"
                       }, 400
        else:
            limit = 5

        output = []
        bucketlists = Bucketlist.query.filter_by(user_id=current_user.id).paginate(page, limit, error_out=False)
        if q:
            bucketlists = models.Bucketlist.query. \
                filter(models.Bucketlist.desc.ilike('%' + q + '%')).paginate(page, limit)
            if bucketlists:
                for bucketlist in bucketlists.items:

                    bucketlist_item = BucketlistItems.query.filter_by(bucket_id=bucketlist.id)
                    bucketlist_items = []
                    for bucket_items in bucketlist_item:
                        bucket_item = {
                            "id": bucket_items.id,
                            "goal": bucket_items.goal,
                            "completed": bucket_items.status,
                            "bucket list id": bucket_items.bucket_id,
                            'created_date': str(bucket_items.date_created),
                            'modified_date': str(bucket_items.date_modified),
                        }
                        bucketlist_items.append(bucket_item)

                    if not bucketlist_items:
                        bucketlist_items = "Not available at the moment."

                    buckets = {
                        'id': bucketlist.id,
                        'description': bucketlist.desc,
                        'user id': bucketlist.user_id,
                        'created_date': str(bucketlist.date_created),
                        'modified_date': str(bucketlist.date_modified),
                        'items': bucketlist_items
                    }
                    output.append(buckets)

                if output:
                    return {
                               "Bucket lists": output
                           }, 200
            return {
                       "message": "No results found!!"
                   }, 404

        if not bucketlists:
            return jsonify({
                "message": "You don't have any bucket list at the moment!"
            }), 404

        for bucketlist in bucketlists.items:
            bucketlist_item = BucketlistItems.query.filter_by(bucket_id=bucketlist.id)
            bucketlist_items = []
            for bucket_items in bucketlist_item:
                bucket_item = {
                    "id": bucket_items.id,
                    "goal": bucket_items.goal,
                    "completed": bucket_items.status,
                    "bucket list id": bucket_items.bucket_id,
                    'created_date': str(bucket_items.date_created),
                    'modified_date': str(bucket_items.date_modified),
                }
                bucketlist_items.append(bucket_item)

            if not bucketlist_items:
                bucketlist_items = "Not available at the moment."

            buckets = {
                'id': bucketlist.id,
                'description': bucketlist.desc,
                'user id': bucketlist.user_id,
                'created_date': str(bucketlist.date_created),
                'modified_date': str(bucketlist.date_modified),
                'items': bucketlist_items
            }
            output.append(buckets)

        if not output:
            return {
                       "message": "You don't have any bucket list at the moment!"
                   }, 404

        return {
                   "Bucket lists": output
               }, 200

    @api.doc(parser=bucket_post_parser)
    def post(self, current_user):
        '''Create a new bucketlist.'''
        args = bucket_post_parser.parse_args()
        desc = args['desc']

        if not desc:
            return {
                       'message': "Bucket list description cannot be empty!!."
                   }, 400

        bucketlist = Bucketlist.query.filter_by(desc=desc).all()

        if bucketlist:
            return {
                       'message': "Bucket list already exists!!."
                   }, 409

        new_bucket = Bucketlist(desc=desc, status=False, user_id=current_user.id)
        db.session.add(new_bucket)
        db.session.commit()

        return {
                   'message': "Bucket list added successfully."
               }, 201


bucket_put_parser = api.parser()
bucket_put_parser.add_argument('desc', type=str, help='Bucketlist Description', location='form')

class SingleBucketList(Resource):
    '''Show a single bucketlist and lets you update or delete them.'''

    method_decorators = [token_required]

    def get(self, current_user, id=None):
        '''Fetch a single bucketlist given its identifier.'''
        if id:
            bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

            if not bucketlist:
                return {
                           'message': "Bucketlist does not exist!!"
                       }, 404

            bucketlist_item = BucketlistItems.query.filter_by(bucket_id=bucketlist.id)
            bucketlist_items = []
            for bucket_items in bucketlist_item:
                bucket_item = {
                    "id": bucket_items.id,
                    "goal": bucket_items.goal,
                    "completed": bucket_items.status,
                    "bucket list id": bucket_items.bucket_id,
                    'created_date': str(bucket_items.date_created),
                    'modified_date': str(bucket_items.date_modified),
                }
                bucketlist_items.append(bucket_item)

            if not bucketlist_items:
                bucketlist_items = "Not available at the moment."

            return {
                       "id": bucketlist.id,
                       "description": bucketlist.desc,
                       "completed": bucketlist.status,
                       "user id": bucketlist.user_id,
                       'created_date': str(bucketlist.date_created),
                       'modified_date': str(bucketlist.date_modified),
                        'items': bucketlist_items
                   }, 200

    @api.doc(parser=bucket_put_parser)
    def put(self, current_user, id=None):
        '''Update a single bucketlist given its identifier.'''
        if id:
            args = bucket_put_parser.parse_args()
            desc = args['desc']

            bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

            if not bucketlist:
                return {
                           "message": "Bucketlist does not exist!!"
                       }, 404

            if not desc:
                return {
                           "message": "Description cannot be empty!!"
                       }, 400

            bucketlist.desc = desc
            bucketlist.user_id = current_user.id
            db.session.commit()
            return {
                       'message': "Bucket list changes made successfully."
                   }, 200
        return {
                   "message": "404 page not found."
               }, 404

    def delete(self, current_user, id=None):
        '''Delete a single bucketlist given its identifier.'''
        if id:
            bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

            if bucketlist:
                db.session.delete(bucketlist)
                db.session.commit()
                return {
                           "message": "Bucket list deleted successfully!!"
                       }, 200
            return {
                       "message": "Sorry, the bucket list you want to delete does not exist."
                   }, 404
        return {
                   "message": "404 page not found."
               }, 404


bucket_item_get_parser = api.parser()
bucket_item_post_parser = api.parser()

bucket_item_get_parser.add_argument('page', type=int, help='Page number, default=1')
bucket_item_get_parser.add_argument('limit', type=int, help='Limit per page, default=5')
bucket_item_get_parser.add_argument('q', type=str, help='Search')

bucket_item_post_parser.add_argument('goal', type=str, help='Bucketlist Item name', location='form')


class BucketListItems(Resource):
    '''Shows a list of all bucketlist items belonging to a bucketlist, and lets you POST to add bucketlist items.'''

    method_decorators = [token_required]

    @api.doc(parser=bucket_item_get_parser)
    def get(self, current_user, id):
        '''List all user's bucketlist items.'''
        args = bucket_item_get_parser.parse_args()
        page = args['page']
        limit = args['limit']
        q = args['q']

        bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

        if not bucketlist:
            return {
                       'message': "Bucketlist does not exist!!"
                   }, 404

        output = []


        if page:
            try:
                page = int(page)
            except Exception:
                return {
                           "message": "Invalid page value!!"
                       }, 400
        else:
            page = 1

        if limit:
            try:
                limit = int(limit)
            except Exception:
                return {
                           "message": "Invalid limit value!!"
                       }, 400
        else:
            limit = 5

        if q:
            bucketlist_items = models.BucketlistItems.query. \
                filter(models.BucketlistItems.goal.ilike('%' + q + '%')).paginate(page, limit)
            if bucketlist_items:
                for item in bucketlist_items.items:
                    if str(id) == str(item.bucket_id):
                        buckets = {
                            'id': item.id,
                            'goal': item.goal,
                            "completed": item.status,
                            "bucket list id": item.bucket_id,
                            'date_created': str(item.date_created),
                            'date_modified': str(item.date_modified),
                        }
                        output.append(buckets)

                if output:
                    return {
                               "Bucket lists": output
                           }, 200
            return {
                       "message": "No results found!!"
                   }, 404

        bucketlist_item = BucketlistItems.query.filter_by(bucket_id=id).paginate(page, limit)

        message = {
                      "message": "No bucket list items available at this time."
                  }, 404
        if not bucketlist_item:
            return message
        bucketlist_items = []
        for bucket_items in bucketlist_item.items:
            bucket_item = {
                "id": bucket_items.id,
                "goal": bucket_items.goal,
                "completed": bucket_items.status,
                "bucket list id": bucket_items.bucket_id,
                'created_date': str(bucket_items.date_created),
                'modified_date': str(bucket_items.date_modified),
            }
            bucketlist_items.append(bucket_item)

        if not bucketlist_items:
            return message
        return {
                   "Bucket list items": bucketlist_items
               }, 200

    @api.doc(parser=bucket_item_post_parser)
    def post(self, current_user, id):
        '''Create a new bucketlist item.'''

        args = bucket_item_post_parser.parse_args()
        goal = args['goal']

        bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

        if not bucketlist:
            return {
                       'message': "Bucketlist does not exist!!"
                   }, 404

        bucketlist_item = BucketlistItems.query.filter_by(goal=goal).all()

        if bucketlist_item:
            return {
                       "message": "Bucket list item already exists!!"
                   }, 409

        if not goal:
            return {
                       "message": "goal cannot be empty!!"
                   }, 400

        new_goal = BucketlistItems(goal=goal, status=False, bucket_id=id)
        db.session.add(new_goal)
        db.session.commit()

        return {
                   "message": "Bucket list item added successfully!!"
               }, 201


class SingleBucketListItem(Resource):
    '''Show a single bucketlist item and lets you update or delete them.'''

    method_decorators = [token_required]

    def get(self, current_user, id, item_id):
        '''Fetch a given bucketlist item given its identifier.'''

        if item_id:
            bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

            if not bucketlist:
                return {
                           'message': "Bucketlist does not exist!!"
                       }, 404
            bucket_item = BucketlistItems.query.filter_by(id=item_id, bucket_id=id).first()

            if not bucket_item:
                return {
                           "message": "Bucketlist item does not exists!!"
                       }, 404

            return {
                "id": bucket_item.id,
                "goal": bucket_item.goal,
                "completed": bucket_item.status,
                "bucket list id": bucket_item.bucket_id,
                'created_date': str(bucket_item.date_created),
                'modified_date': str(bucket_item.date_modified),
            }

    def put(self, current_user, id, item_id=None):
        '''Update a given bucketlist item given its identifier.'''

        bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

        if not bucketlist:
            return {
                       'message': "Bucketlist does not exist!!"
                   }, 404

        if item_id:
            bucket_item = BucketlistItems.query.filter_by(id=item_id, bucket_id=id).first()
            if bucket_item:
                bucket_item.status = True
                db.session.commit()
                return {
                           "message": "Goal completed."
                       }, 201
            return {
                       "message": "404 Page not found."
                   }, 404
        return {
                   "message": "Item id cannot be null."
               }, 400

    def delete(self, current_user, id, item_id=None):
        '''Delete a given bucketlist item given its identifier.'''

        bucketlist = Bucketlist.query.filter_by(id=id, user_id=current_user.id).first()

        if not bucketlist:
            return {
                       'message': "Bucketlist does not exist!!"
                   }, 404

        if item_id:
            bucket_item = BucketlistItems.query.filter_by(id=item_id, bucket_id=id).first()
            if bucket_item:
                db.session.delete(bucket_item)
                db.session.commit()
                return {
                           "message": "Bucket list item deleted successfully"
                       }, 200
            return {
                       "message": "Sorry, Bucket list item does not exist."
                   }, 404
        return {
                   "message": "404 Page not found."
               }, 404
