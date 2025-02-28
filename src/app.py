# filepath: /Users/alexshi/projects/src/app.py
from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_values_followers(data):
    values = []
    for entry in data:
        if isinstance(entry, dict):
            for string_list_entry in entry.get('string_list_data', []):
                values.append(string_list_entry['value'])
    return values

def extract_values_following(data):
    values = []
    for entry in data.get('relationships_following', []):
        if isinstance(entry, dict):
            for string_list_entry in entry.get('string_list_data', []):
                values.append(string_list_entry['value'])
    return values

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        followers_file = request.files['followers']
        following_file = request.files['following']

        followers_path = os.path.join('uploads', followers_file.filename)
        following_path = os.path.join('uploads', following_file.filename)

        followers_file.save(followers_path)
        following_file.save(following_path)

        followers_data = load_json(followers_path)
        following_data = load_json(following_path)

        followers_values = extract_values_followers(followers_data)
        following_values = extract_values_following(following_data)

        unique_followers = set(followers_values) - set(following_values)
        unique_following = set(following_values) - set(followers_values)

        return render_template('result.html', unique_followers=unique_followers, unique_following=unique_following)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)