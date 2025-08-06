from flask import Flask, render_template, request, redirect, url_for, session
import uuid
from flask import jsonify
app = Flask(__name__)
app.secret_key = 'a-very-secret-key'  # 用于启用 session，必须添加！

# 模拟作品信息
artworks = [
    {"id": 1, "filename": "example1.jpg", "title": "素描艺术像 1"},
    {"id": 2, "filename": "example2.jpg", "title": "素描艺术像 2"},
    {"id": 3, "filename": "example3.jpg", "title": "成都熊猫 3"},
    {"id": 4, "filename": "example4.jpg", "title": "太乙真人 4"},
]

# 评论：每条是 dict(id, text)
comments = {art['id']: [] for art in artworks}

# 点赞数（每个作品）
likes = {art['id']: 0 for art in artworks}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        artwork_id = int(request.form['artwork_id'])
        comment_text = request.form['comment'].strip()
        if comment_text:
            comment_id = str(uuid.uuid4())
            comments[artwork_id].append({'id': comment_id, 'text': comment_text})
        return redirect(url_for('home'))

    # 获取当前用户点赞记录（从 session 读取）
    liked_ids = session.get('liked', [])
    return render_template('index.html', artworks=artworks, comments=comments, likes=likes, liked_ids=liked_ids)


@app.route('/like/<int:artwork_id>', methods=['POST'])
def like(artwork_id):
    liked = session.get('liked', [])

    if artwork_id in liked:
        likes[artwork_id] -= 1
        liked.remove(artwork_id)
        liked_flag = False
    else:
        likes[artwork_id] += 1
        liked.append(artwork_id)
        liked_flag = True

    session['liked'] = liked

    return jsonify({
        'liked': liked_flag,
        'likes_count': likes[artwork_id]
    })


@app.route('/delete_comment/<int:artwork_id>/<comment_id>', methods=['POST'])
def delete_comment(artwork_id, comment_id):
    comments[artwork_id] = [c for c in comments[artwork_id] if c['id'] != comment_id]
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)