import streamlit as st
from datetime import datetime
import random

# --- ページ設定（頭に必ず） ---
st.set_page_config(page_title="介護職員・適性診断", layout="centered")

# --- CSSでちょっとおしゃれに ---
st.markdown("""
<style>
/* ここから */
@media (max-width: 600px) {
  .stMarkdown, .stButton, .stText, .stContainer, .stTitle, .stHeader, .stSubheader {
    font-size: 1.1em !important;
    margin-bottom: 0.5em !important;
    line-height: 1.5 !important;
    word-break: break-all !important;
    white-space: normal !important;
  }
  .element-container { margin-top: 0.2em !important; margin-bottom: 0.2em !important; }
}
body { background: #eaf5ff; }
section.main { background: #fff9f2; border-radius: 20px;}
div.stButton > button {
    color: white;
    background: linear-gradient(90deg, #32b8e8, #e8e7ff);
    border-radius: 20px;
    font-size: 1.2em;
    margin: 6px 0;
    font-weight: bold;
}
/* ここまで */
</style>
""", unsafe_allow_html=True)

st.title("👩‍⚕️介護職員・シチュエーション適性診断 ＆ 性格＋今日の運勢アプリ🌟")

# --- セッションで質問管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# --- 最初にプロフィール ---
if st.session_state.step == 0:
    st.subheader("まずはあなたの基本プロフィールを教えてください！")
    blood = st.selectbox("あなたの血液型は？", ("A型", "B型", "O型", "AB型"))
    year = st.number_input("生まれた年（西暦）", 1940, 2025, 1990)
    month = st.number_input("生まれた月", 1, 12, 1)
    day = st.number_input("生まれた日", 1, 31, 1)
    if st.button("診断スタート！🚀"):
        st.session_state.blood = blood
        st.session_state.year = year
        st.session_state.month = month
        st.session_state.day = day
        st.session_state.step = 1

# --- 設問リスト ---
questions = [
    {
        "q": "トイレに行った利用者様が、またすぐ“トイレに行きたい”と言われました。あなたなら？",
        "a": ["A. さっき行きましたよ、と説明する",
              "B. わかりました、行きましょう",
              "C. まず気持ちを聞いてみる、理由を尋ねてみる"]
    },
    {
        "q": "利用者様が食事を拒否。あなたは？",
        "a": ["A. そうですよね。もう少ししたらまた声かけますね",
              "B. これだけでも食べられますか？とスプーンで口まで運ぶ",
              "C. 早く食べてください、と声をかける"]
    },
    {
        "q": "夜勤のある仕事にはどんなイメージ？",
        "a": ["A. 体調管理が難しそう、できれば避けたい",
              "B. 慣れれば大丈夫。どちらでも構わない",
              "C. 夜勤も全然苦じゃないし積極的にやりたい"]
    },
    {
        "q": "あなたが重視したい働き方は？",
        "a": ["A. 規則正しい生活リズムで働きたい",
              "B. 不規則でもいろんな経験したい",
              "C. 夜勤手当や収入アップのためなら夜勤も積極的にやりたい"]
    },
    {
        "q": "同僚とケア方法で意見が食い違った時は？",
        "a": ["A. 自分の意見をはっきり伝えて話し合う",
              "B. 相手の意見をまず聞く",
              "C. お互いの意見をまとめて妥協点を探す"]
    },
    {
        "q": "夜勤中、2つの対応が重なったら？",
        "a": ["A. 片方に待っててと言い、すぐもう一方へ",
              "B. ひとつずつ慎重に対応",
              "C. 柔軟に両方を見ながら動く"]
    },
]

result_patterns = {
    "デイサービス向き": "あなたは柔軟性とコミュニケーション力が高く、明るい雰囲気作りや利用者様との信頼関係を築くのが得意なタイプです。特に、急な変更や多様な要望にも柔軟に対応できるため、日中の活発な現場やレクリエーションの場面で力を発揮できます。デイサービスのような、利用者様との交流や個別ケアが重視される環境が最も向いています。",
    "特養・グループホーム向き": "あなたは落ち着きと体力に自信があり、忙しい現場や長時間の勤務にも冷静に対応できるタイプです。複数の利用者様を同時にケアする場面でも動じず、観察力や安全管理の意識が高い点が強みです。特養やグループホームのような、チームワークと継続的なケアが必要な現場で活躍できるでしょう。",
    "訪問・定期巡回向き": "あなたは計画性や自己管理能力が高く、1対1の関わりや利用者様の生活をじっくり支える現場に適性があります。急なイレギュラーにも冷静に対応でき、限られた時間の中で的確なケアができる点も評価ポイントです。定期巡回や訪問介護など、少人数でじっくりケアする仕事でやりがいを感じるでしょう。"
}

# --- 診断フロー ---
if 1 <= st.session_state.step <= len(questions):
    q_idx = st.session_state.step - 1
    st.subheader(f"Q{q_idx+1}. {questions[q_idx]['q']}")
    btns = questions[q_idx]['a']
    cols = st.columns(3)
    pressed = [cols[i].button(btns[i]) for i in range(3)]
    for idx, p in enumerate(pressed):
        if p:
            st.session_state.answers.append(idx)
            st.session_state.step += 1
            st.rerun()

# --- 結果表示 ---
if st.session_state.step > len(questions):
    # ▼診断ロジック（シンプルな例：最多の回答タイプ）
    counts = [0,0,0]
    for a in st.session_state.answers:
        counts[a] += 1
    result_type = ["デイサービス向き", "特養・グループホーム向き", "訪問・定期巡回向き"][counts.index(max(counts))]
    apt_text = result_patterns[result_type]

    # ▼性格診断
    blood = st.session_state.blood
    year = st.session_state.year
    month = st.session_state.month
    day = st.session_state.day

    # 星座
    def get_zodiac(month, day):
        zodiac_dates = [
            ((1, 20), (2, 18), "水瓶座"),
            ((2, 19), (3, 20), "魚座"),
            ((3, 21), (4, 19), "牡羊座"),
            ((4, 20), (5, 20), "牡牛座"),
            ((5, 21), (6, 21), "双子座"),
            ((6, 22), (7, 22), "蟹座"),
            ((7, 23), (8, 22), "獅子座"),
            ((8, 23), (9, 22), "乙女座"),
            ((9, 23), (10, 23), "天秤座"),
            ((10, 24), (11, 22), "蠍座"),
            ((11, 23), (12, 21), "射手座"),
            ((12, 22), (1, 19), "山羊座"),
        ]
        for (start, end, name) in zodiac_dates:
            if ((month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1])):
                return name
        return "不明"
    zodiac = get_zodiac(month, day)

    blood_dict = {
        "A型": "A型はストレスマネジメントが得意。まじめで協調性もバツグン！",
        "B型": "B型は自由な発想と切り替えの早さが強み。変化にも強い！",
        "O型": "O型はおおらかで包容力があり、チームの潤滑油的存在。",
        "AB型": "AB型は分析力とバランス感覚が優秀。冷静な対応で信頼されます。"
    }
    zodiac_dict = {
        "牡羊座": "チャレンジ精神が旺盛で行動力抜群！",
        "牡牛座": "堅実で粘り強いタイプ。じっくり信頼を築きます。",
        "双子座": "コミュ力と情報収集力が武器。柔軟性も◎",
        "蟹座": "面倒見が良く、家族的な温かさ。共感力バツグン。",
        "獅子座": "明るくリーダーシップを発揮！存在感抜群。",
        "乙女座": "きめ細やかで真面目。分析力とサポート力が強み。",
        "天秤座": "バランス感覚が絶妙。調和を生み出せる。",
        "蠍座": "情熱的で探究心が強い。信念を貫きます。",
        "射手座": "好奇心旺盛で前向き。新しい挑戦を楽しめる。",
        "山羊座": "責任感が強く努力家。着実に目標達成！",
        "水瓶座": "独創的で未来志向。仲間を大切にする。",
        "魚座": "やさしく感受性豊か。癒しの存在です。"
    }

    # ▼運勢ランダム生成
    def default_fortune():
        stars = ["⭐️", "⭐️⭐️", "⭐️⭐️⭐️"]
        msgs = [
            "普段通り過ごして吉。小さな変化に幸運あり。",
            "柔軟な対応が運気UPのカギ。",
            "思い切った行動がラッキーを呼びそう。"
        ]
        return (random.choice(stars), random.choice(msgs))

    random.seed(str(datetime.now()) + str(blood) + str(zodiac))
    love = default_fortune()
    money = default_fortune()
    work = default_fortune()
    lucky_colors = ["ブルー", "ピンク", "イエロー", "グリーン", "オレンジ", "パープル", "レッド", "ホワイト"]
    color = random.choice(lucky_colors)

    # ▼結果
    st.success(f"## 診断結果：{result_type}\n\n{apt_text}")
    st.markdown("---")
    st.markdown(f"""
**性格診断**
- 血液型：{blood} … {blood_dict[blood]}
- 星座：{zodiac} … {zodiac_dict.get(zodiac, "")}

---

**今日の運勢**
- 恋愛運：{love[0]} {love[1]}
- 金銭運：{money[0]} {money[1]}
- 仕事運：{work[0]} {work[1]}
- ラッキーカラー：{color}
    """)

    st.markdown("---")
    if st.button("もう一度診断する🔄"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
