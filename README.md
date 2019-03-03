# fruit-sales-management-console
Djangoを使った、果物の販売管理を行うシンプルなWebアプリ。

## 実行環境
* python==3.6
* django==2.1.7
* dateutil

## インストール
`pipenv install`

## 特長
* 果物マスタデータの登録・表示・管理
* 販売情報の登録・管理・表示・管理
* 過去一定期間の販売統計情報の表示

## プロジェクト構成
* fsmc_project: djangoプロジェクトのメインapp
* fruits: 果物マスタapp
* fruitsales: 販売情報app
* stats: 統計統計情報app
* pages: トップページなどを扱うapp
* static: 静的コンテンツ用ディレクトリ
* templates: テンプレート用ディレクトリ
