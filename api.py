from flask_pymongo import PyMongo
from flask import Flask, jsonify, request

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'movies'
app.config['MONGO_URI'] = 'mongodb+srv://<username>:<password>@trialcluster.spns5qz.mongodb.net/<database_name>?retryWrites=true&w=majority'
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
    output = {'name': q['name'], 'img': q['img'], 'summary': q['summary']}

    return jsonify(output)

# READ


@app.route('/movies/read', methods=['GET'])
def get_all_movies():
    newPosts = mongo.db.newPosts
    output = []

    for q in newPosts.find():
        # print('objectID ', q['_id'])
        output.append(
            {'name': q['name'], 'img': q['img'], 'summary': q['summary']})

    return jsonify(output)

# READ SPECIFIC


@app.route('/movies/read/<name>', methods=['GET'])
def get_specific_movie(name):
    newPosts = mongo.db.newPosts

    q = newPosts.find_one({"name": name})
    if q:
        output = {'name': q['name'], 'img': q['img'], 'summary': q['summary']}
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

    q = newPosts.update_one(
        {"name": nameKEY}, {'$set': {'name': name, 'img': img, 'summary': summary}})

    q = newPosts.find_one({"name": name})
    output = {'name': q['name'], 'img': q['img'], 'summary': q['summary']}
    return jsonify(output)

# DELETE


@app.route('/movies/delete/<name>', methods=['PATCH'])
def delete_movie(name):
    newPosts = mongo.db.newPosts
    q = newPosts.find_one({"name": name})
    output = {'name': q['name']}
    q = newPosts.delete_one({"name": name})
    return jsonify({'Movie Deleted': output})


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
