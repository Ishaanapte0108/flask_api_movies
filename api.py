
from bson import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

load_dotenv()
app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.getenv('DB_NAME')  # your database name
app.config['MONGO_URI'] = os.getenv(
    'DB_CONNECTION')  # your database url string
mongo = PyMongo(app)

# CREATE


@app.route('/movies/create', methods=['POST'])
def create_new_movie():

    newPosts = mongo.db.newPosts
    name = request.json['name']
    img = request.json['img']
    summary = request.json['summary']

    q = newPosts.insert_one({'name': name, 'img': img, 'summary': summary})

    q = newPosts.find_one({"name": name})

    id = str(q['_id'])

    output = {'_id': id, 'name': q['name'],
              'img': q['img'], 'summary': q['summary']}

    return jsonify(output)

# READ ALL


@app.route('/movies/read', methods=['GET'])
def get_all_movies():
    newPosts = mongo.db.newPosts
    output = []

    if newPosts.find():

        for q in newPosts.find():

            output.append({"_id": str(
                q['_id']), 'name': q['name'], 'img': q['img'], 'summary': q['summary']})

    else:
        output = 'Database Empty..Add something...'

    return jsonify(output)


# READ SPECIFIC


@app.route('/movies/read/<name>', methods=['GET'])
def get_specific_movie(name):

    newPosts = mongo.db.newPosts
    output = {}

    try:
        objectInstance = ObjectId(name)
        q = newPosts.find_one({"_id": objectInstance})

        if q:
            output = {"_id": str(q['_id']), 'name': q['name'],
                      'img': q['img'], 'summary': q['summary']}
        else:
            output = 'no result found'

    except:

        q = newPosts.find_one({"name": name})
        if q:
            output = {"_id": str(q['_id']), 'name': q['name'],
                      'img': q['img'], 'summary': q['summary']}
        else:
            output = 'No results found'

    return jsonify(output)

# UPDATE


@app.route('/movies/update/<nameKEY>', methods=['PATCH'])
def update_movie(nameKEY):

    newPosts = mongo.db.newPosts
    name = request.json['name']
    img = request.json['img']
    summary = request.json['summary']

    try:
        # check if movie exists

        objectInstance = ObjectId(nameKEY)
        q = newPosts.find_one({"_id": objectInstance})

        if q:

            q = newPosts.update_one(
                {"_id": objectInstance}, {'$set': {'name': name, 'img': img, 'summary': summary}})

            q = newPosts.find_one({"_id": objectInstance})
            output = {"_id": str(q['_id']), 'name': q['name'],
                      'img': q['img'], 'summary': q['summary']}

            return jsonify(output)
        else:
            return jsonify('Movie does not exist')

    except:
        # check if movie exists
        q = newPosts.find_one({"name": nameKEY})

        if q:

            q = newPosts.update_one(
                {"name": nameKEY}, {'$set': {'name': name, 'img': img, 'summary': summary}})

            q = newPosts.find_one({"name": nameKEY})
            output = {"_id": str(q['_id']), "name": q['name'],
                      "img": q["img"], "summary": q['summary']}

            return jsonify(output)

        else:
            return jsonify('This movie does not exist in db')

# DELETE


@app.route('/movies/delete/<name>', methods=['DELETE'])
def delete_movie(name):
    newPosts = mongo.db.newPosts

    try:

        # check if movie exists

        objectInstance = ObjectId(name)
        q = newPosts.find_one({"_id": objectInstance})

        if q:

            # delete movie
            q = newPosts.delete_one({"_id": ObjectId(name)})
            return jsonify('Movie Deleted')

        else:
            return jsonify('Movie does not exist')

    except:

        # check if movie exists
        q = newPosts.find_one({"name": name})
        if q:
            q = newPosts.delete_one({"name": name})
            return jsonify('Movie Deleted')
        else:
            return jsonify('Movie Does not exist')


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
