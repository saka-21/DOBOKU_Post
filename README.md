# DOBOKU_Post
## URL
https://doboku-post.site

## イメージ図
![スクリーンショット 2020-10-10 18 56 39](https://user-images.githubusercontent.com/62042131/95652190-56ef7e00-0b2a-11eb-9c95-798d9c5476dc.png)

## 概要
主に土木、建築に関する写真を投稿し、共有できるアプリです。  
今まで知らなかった土木構造物、建築物及びその技術を知ることができます。

## 制作背景
　自分は大学で４年間土木工学を学ぶ上で、土木という分野は日常を支える大きな役割を果たしているのにもかかわらず、現場の３K（きつい、きたない、危険）というイメージがいまだのこっており、なかなか興味を持ってもらえないと感じていました。実際に土木学科は年々減少し、さらに土木学科を専攻した人も最終的に土木以外の仕事につく人が多い印象が受けます。土木・建築業界の人不足から建設現場の環境を改善、IT化が必要となっていますが、それと同時にまずは少しでも土木・建築に興味を持ってもらうことが必要だと感じ、このアプリケーションを制作しました。今後は写真のみではなく土木・建築に関する書籍や記事に関しても投稿できるよう機能を拡張しようと思っています。
 
## 使用技術
### フロントエンド
* Vue.js: 2.6.11
* Vue CLI: 4.4.6
* HTML/CSS
### バックエンド
* Python: 3.8.3
* Django: 3.0
* Django REST Framework: 3.10
* poetry: 1.0.10

## 主な機能
### SPA
* VueとDjango REST Frameworkを使用することでフロントエンドとバックエンドを分離
* Vue CLIでbuildした静的ファイルをS3へデプロイ、CloudFrontで配信

### 投稿一覧
#### 新着投稿・人気投稿ページ
* 投稿日・いいねの数でソート
#### カテゴリページ
* 橋やダムなどカテゴリによって投稿を絞り込む
#### マップページ
*マップ表示機能
  * 位置情報が登録されている場合はマップ画面で位置を確認できる。
  * 吹き出しから詳細ページへ遷移が可能。
#### 検索ページ
* 検索機能
  * タイトル、カテゴリ、投稿日、都道府県によって投稿を絞り込む（複数の条件を指定可能）
#### 無限スクロール
　vue-infinite-loadingを用いて実装

### 投稿詳細
#### コメント機能
* コメントの投稿・削除
#### いいね機能

### 新規投稿
* 名前（タイトル）から住所及び緯度経度を検索「GoogleMapAPI」
### ユーザー周り
* ログイン機能
* 新規登録機能
