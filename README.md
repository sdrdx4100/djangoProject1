# Django Project 1

## プロジェクト概要

このプロジェクトは、Djangoの習熟およびAdminの使用方法、テーブルの連携などを検証するためのプロジェクトです。

## 環境構築方法

1. リポジトリをクローンします。
    ```sh
    git clone https://github.com/sdrdx4100/djangoProject1.git
    cd djangoProject1
    ```

2. 仮想環境を作成し、アクティベートします。
    ```sh
    python -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
    ```

3. 必要なパッケージをインストールします。
    ```sh
    pip install -r requirements.txt
    ```

4. マイグレーションを実行します。
    ```sh
    python manage.py migrate
    ```

5. 開発サーバーを起動します。
    ```sh
    python manage.py runserver
    ```

## 使用方法

1. ブラウザで `http://127.0.0.1:8000/` にアクセスします。
2. 管理画面にアクセスするには、`http://127.0.0.1:8000/admin/` にアクセスします。
3. メモの作成、編集、削除が可能です。
4. 定数マスターを使用して、挨拶文やシステムメッセージを管理します。
