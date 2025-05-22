from datetime import datetime, time
from .models import Constant

def greeting_context(request):
    """
    現在時刻に応じた挨拶文をコンテキストとして返すDjangoコンテキストプロセッサ。

    Parameters
    ----------
    request : HttpRequest
        Djangoのリクエストオブジェクト。

    Returns
    -------
    dict
        'navbar_greeting'キーに挨拶文を格納した辞書。
    
    Notes
    -----
    - 7:00〜11:59は「greeting_1」、12:00〜17:00は「greeting_2」としてConstantモデルから挨拶文を取得。
    - Constantモデルに該当データがなければデフォルトで"Hello"を返す。
    """
    now = datetime.now().time()  # 現在時刻（時刻のみ）を取得
    category_key = None  # 挨拶カテゴリのキーを初期化

    # 時間帯でキーを決定
    if time(7, 0) <= now <= time(11, 59):
        category_key = 'greeting_1'  # 朝〜午前の挨拶
    elif time(12, 0) <= now <= time(17, 0):
        category_key = 'greeting_2'  # 昼〜夕方の挨拶
        
    print(f"Current time: {now}, Greeting key: {category_key}")

    greeting = None  # 挨拶文の初期化
    if category_key:
        # Constantモデルから該当する挨拶文を取得
        greeting_obj = Constant.objects.filter(category_key='greeting', name_key=category_key).first()
        if greeting_obj:
            greeting = greeting_obj.name  # モデルから取得できた場合はその挨拶文を使用
            
    # デフォルトの挨拶を設定
    if not greeting:
        greeting = "Hello"
    
    print(f"Greeting: {greeting}")

    # テンプレートで利用するための辞書を返す
    return {'navbar_greeting': greeting}


def system_message_context(request):
    """
    Constantモデルからsystem_messageカテゴリのname_keyとnameを取得し、リストで返す。

    Returns
    -------
    dict
        'system_messages'キーに[{name_key, name}, ...]のリストを格納
    """
    messages = list(Constant.objects.filter(category_key='system_message').values('name_key', 'name'))
    # DEBUG用のログ出力
    print(f"System messages: {messages}")
    return {'system_messages': messages}