from app.app import app

if __name__ == "__main__":
    app.run()

#変更後の反映
#次にデプロイします。 Heroku へのデプロイは、ほとんどの場合、このパターンで行います。 まず、変更したファイルをローカルの git リポジトリに追加します。
#$ git add .
#次に、変更内容をリポジトリにコミットします。
#$ git commit -m "Demo"
#前と同じ方法でデプロイします。
#$ git push heroku main
#最後に、すべて正常に動作しているかどうかを確認します。
#$ heroku open