"""
RAG Web 应用 - 简化版
包含文档上传和问答功能
"""

import os
import shutil
from pathlib import Path
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from simple_demo import SimpleRAGDemo

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './data'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'md', 'json'}

rag_demo = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_documents():
    """获取文档列表"""
    data_dir = Path('./data')
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        return []

    docs = []
    for file in data_dir.iterdir():
        if file.is_file() and file.suffix.lstrip('.') in app.config['ALLOWED_EXTENSIONS']:
            docs.append({
                'name': file.name,
                'size': file.stat().st_size,
                'modified': file.stat().st_mtime
            })
    return docs


def rebuild_rag():
    """重建 RAG 系统"""
    global rag_demo
    rag_demo = SimpleRAGDemo()
    rag_demo.load_documents()
    rag_demo.split_documents(rag_demo.documents)
    return rag_demo


# ========== API 路由 ==========

@app.route('/api/ask', methods=['POST'])
def ask():
    """处理问题"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'error': '请输入问题'})

        rag = rebuild_rag()
        relevant_docs = rag.simple_search(query, top_k=2)
        answer = rag.generate_answer(query, relevant_docs)
        context = [doc.page_content[:150] + '...' for doc in relevant_docs]

        return jsonify({
            'query': query,
            'context': context,
            'context_count': len(context),
            'answer': answer
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """上传文档"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': '没有文件'})

        files = request.files.getlist('files')
        uploaded = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded.append(filename)

        if uploaded:
            return jsonify({'success': True, 'uploaded': uploaded})
        return jsonify({'success': False, 'error': '没有支持的文件类型'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/docs', methods=['GET'])
def list_documents():
    """获取文档列表"""
    try:
        docs = get_documents()
        return jsonify({'docs': docs})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/docs/<filename>', methods=['DELETE'])
def delete_document(filename):
    """删除文档"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': '文件不存在'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/rebuild', methods=['POST'])
def rebuild_index():
    """重建索引"""
    try:
        rebuild_rag()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/')
def index():
    """主页"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>RAG 演示系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .tabs { display: flex; border-bottom: 1px solid #e0e0e0; }
        .tab { flex: 1; padding: 15px; text-align: center; cursor: pointer; background: #f8f9fa; }
        .tab.active { background: white; border-bottom: 3px solid #667eea; font-weight: 600; }
        .tab:hover:not(.active) { background: #e8e8e8; }
        .tab-content { display: none; padding: 30px; }
        .tab-content.active { display: block; }
        .upload-area { border: 2px dashed #667eea; border-radius: 12px; padding: 40px; text-align: center; background: #f8f9fa; cursor: pointer; }
        .upload-area:hover { background: #f0f0f0; }
        .doc-list { margin-top: 20px; }
        .doc-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; background: #f8f9fa; border-radius: 8px; margin-bottom: 10px; }
        .doc-name { font-weight: 600; }
        .doc-meta { font-size: 12px; color: #888; }
        .btn-delete { background: #ff4444; color: white; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; }
        .btn-rebuild { background: #667eea; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; margin-bottom: 20px; }
        .input-group { margin-bottom: 20px; }
        .input-group input { width: 100%; padding: 15px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        .input-group input:focus { outline: none; border-color: #667eea; }
        .btn-group { display: flex; gap: 10px; margin-bottom: 20px; }
        .btn { flex: 1; padding: 12px; border: none; border-radius: 8px; cursor: pointer; }
        .btn-primary { background: #667eea; color: white; }
        .btn-primary:hover { background: #5568d3; }
        .btn-secondary { background: #f0f0f0; color: #333; }
        .result { background: #f8f9fa; border-radius: 8px; padding: 20px; margin-top: 20px; display: none; }
        .result.show { display: block; }
        .result-section h3 { color: #667eea; font-size: 16px; margin-bottom: 10px; }
        .context-item { background: white; padding: 12px; border-radius: 6px; margin-bottom: 10px; font-size: 14px; color: #555; }
        .answer { background: white; padding: 15px; border-radius: 8px; line-height: 1.6; color: #333; }
        .loading { text-align: center; padding: 20px; color: #667eea; }
        .example-btn { background: #f0f0f0; border: none; padding: 8px 12px; border-radius: 20px; font-size: 13px; cursor: pointer; margin-right: 8px; margin-bottom: 8px; }
        .example-btn:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 RAG 检索增强生成演示</h1>
            <p>基于 LangChain 框架的智能问答系统</p>
        </div>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('chat')">💬 问答</div>
            <div class="tab" onclick="switchTab('docs')">📚 知识库管理</div>
        </div>

        <div id="tab-chat" class="tab-content active">
            <div class="input-group">
                <input type="text" id="query" placeholder="请输入你的问题..." />
            </div>
            <div class="btn-group">
                <button class="btn btn-primary" onclick="ask()">🚀 提问</button>
                <button class="btn btn-secondary" onclick="clearResult()">清空</button>
            </div>
            <div id="result" class="result">
                <div id="loading" class="loading" style="display:none">⏳ 正在检索...</div>
                <div id="resultContent"></div>
            </div>
        </div>

        <div id="tab-docs" class="tab-content">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <p style="font-size: 48px;">📁</p>
                <p style="font-size: 16px; color: #666;">点击上传文档</p>
                <input type="file" id="fileInput" style="display:none" accept=".txt,.pdf,.md,.json" multiple>
            </div>
            <button class="btn-rebuild" onclick="rebuildIndex()">🔄 重建索引</button>
            <h3 style="margin-top:20px; color:#667eea;">当前文档</h3>
            <div id="docList" class="doc-list"></div>
        </div>
    </div>

    <script>
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById('tab-' + tab).classList.add('active');
            if (tab === 'docs') loadDocuments();
        }

        function setQuery(q) { document.getElementById('query').value = q; }
        function clearResult() {
            document.getElementById('result').classList.remove('show');
            document.getElementById('resultContent').innerHTML = '';
        }

        async function ask() {
            const query = document.getElementById('query').value.trim();
            if (!query) return alert('请输入问题');

            const resultDiv = document.getElementById('result');
            const loadingDiv = document.getElementById('loading');
            const contentDiv = document.getElementById('resultContent');

            resultDiv.classList.add('show');
            loadingDiv.style.display = 'block';
            contentDiv.innerHTML = '';

            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();
                loadingDiv.style.display = 'none';

                if (data.error) {
                    contentDiv.innerHTML = '<div style="color:red;padding:15px;">❌ ' + data.error + '</div>';
                } else {
                    contentDiv.innerHTML = `
                        <div class="result-section">
                            <h3>📚 检索到 ${data.context_count} 个相关文档</h3>
                            ${data.context.map(c => `<div class="context-item">${c}</div>`).join('')}
                        </div>
                        <div class="result-section">
                            <h3>💡 回答</h3>
                            <div class="answer">${data.answer}</div>
                        </div>
                    `;
                }
            } catch (err) {
                loadingDiv.style.display = 'none';
                contentDiv.innerHTML = '<div style="color:red;padding:15px;">❌ 请求失败</div>';
            }
        }

        document.getElementById('fileInput').addEventListener('change', async function(e) {
            const files = e.target.files;
            if (files.length === 0) return;

            const formData = new FormData();
            for (let file of files) formData.append('files', file);

            try {
                const res = await fetch('/api/upload', { method: 'POST', body: formData });
                const result = await res.json();
                if (result.success) {
                    alert('上传成功！请点击"重建索引"');
                    loadDocuments();
                } else {
                    alert('上传失败: ' + result.error);
                }
            } catch (err) {
                alert('上传失败');
            }
        });

        async function loadDocuments() {
            try {
                const res = await fetch('/api/docs');
                const data = await res.json();
                const listDiv = document.getElementById('docList');

                if (data.docs.length === 0) {
                    listDiv.innerHTML = '<p style="color:#888; text-align:center;">暂无文档</p>';
                    return;
                }

                listDiv.innerHTML = data.docs.map(d => `
                    <div class="doc-item">
                        <div>
                            <div class="doc-name">${d.name}</div>
                            <div class="doc-meta">${(d.size/1024).toFixed(1)} KB</div>
                        </div>
                        <button class="btn-delete" onclick="deleteDoc('${d.name}')">删除</button>
                    </div>
                `).join('');
            } catch (err) {
                console.error(err);
            }
        }

        async function deleteDoc(filename) {
            if (!confirm('确定删除 ' + filename + '?')) return;
            try {
                await fetch('/api/docs/' + filename, { method: 'DELETE' });
                loadDocuments();
            } catch (err) {
                alert('删除失败');
            }
        }

        async function rebuildIndex() {
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = '⏳ 重建中...';
            try {
                await fetch('/api/rebuild', { method: 'POST' });
                btn.textContent = '✓ 完成';
                setTimeout(() => {
                    btn.disabled = false;
                    btn.textContent = '🔄 重建索引';
                }, 1500);
            } catch (err) {
                alert('重建失败');
                btn.disabled = false;
                btn.textContent = '🔄 重建索引';
            }
        }

        document.getElementById('query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') ask();
        });
    </script>
</body>
</html>
    '''


if __name__ == '__main__':
    print("=" * 50)
    print("RAG Web 应用启动中...")
    print("=" * 50)
    print("\n请在浏览器中访问:")
    print("   http://localhost:5000")
    print("\n按 Ctrl+C 停止服务器\n")
    app.run(host='0.0.0.0', port=5000)
