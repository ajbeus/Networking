from flask import Flask, request, render_template_string
import pyautogui

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head>
            <title>Remote Mouse</title>
            <style>
                body {
                    font-family: sans-serif;
                    background: #111;
                    color: white;
                    text-align: center;
                    padding: 20px;
                }
                button {
                    font-size: 24px;
                    padding: 15px;
                    margin: 10px;
                    background: #444;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                input {
                    font-size: 20px;
                    padding: 10px;
                    width: 80%;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h1>Remote Mouse</h1>
            <div>
                <button onclick="move(0, -30)">⬆️</button><br>
                <button onclick="move(-30, 0)">⬅️</button>
                <button onclick="move(30, 0)">➡️</button><br>
                <button onclick="move(0, 30)">⬇️</button>
            </div>
            <br>
            <div>
                <button onclick="mouseClick('left')">🖱️ Left Click</button>
                <button onclick="mouseClick('right')">👉 Right Click</button>
            </div>
            <br>
            <div>
                <input id="text" placeholder="Type something..." />
                <button onclick="sendText()">Type</button>
            </div>

            <script>
                function move(dx, dy) {
                    fetch(`/move?dx=${dx}&dy=${dy}`);
                }
                function mouseClick(button) {
                    fetch(`/click?button=${button}`);
                }
                function sendText() {
                    const text = document.getElementById('text').value;
                    fetch(`/type?text=${encodeURIComponent(text)}`);
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/move')
def move():
    dx = float(request.args.get('dx', 0))
    dy = float(request.args.get('dy', 0))
    pyautogui.moveRel(dx, dy)
    return 'Moved'

@app.route('/click')
def click():
    button = request.args.get('button', 'left')
    if button not in ['left', 'right', 'middle']:
        return 'Invalid button', 400
    pyautogui.click(button=button)
    return f'{button.capitalize()} clicked'


@app.route('/type')
def type_text():
    text = request.args.get('text', '')
    pyautogui.write(text)
    return f"Typed: {text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
