# ガイド付き質問: ステアリングベクトルの理解

このドキュメントは、ステアリングベクトルを完全に理解するための実験ガイドです。
各質問に対して、**あなた自身が仮説を立て、実験で確認**してください。

---

## 使い方

1. **質問を1つ選ぶ**
2. **仮説を立てる**（「〇〇だと思う」）
3. **実験コードを書く**（テンプレートを参考に）
4. **結果を観察**
5. **学びを記録**（experiment_log.mdに記載）
6. **AIに答え合わせを依頼**

---

## Phase 1: 複素数の内積の基礎

### Q1: なぜ複素数を使うのか？

**深層学習との対比**:
- 深層学習では実数ベクトルの内積 `<a, b> = Σ(a_i × b_i)` を使います
- レーダーでは複素数ベクトルの内積を使います

**質問**:
実数ベクトルの内積と複素数ベクトルの内積で、**何が違う**のでしょうか？

**実験の方向性**:
1. 実数信号と複素信号を用意
2. それぞれステアリングベクトルとの内積を計算
3. 位相を変えたときの挙動を比較

**実験テンプレート**:
```python
# notebooks/q01_why_complex.ipynb

import numpy as np
import matplotlib.pyplot as plt

# パラメータ
freq = 5
M = 8  # アンテナ素子数
n = np.arange(M)  # アンテナインデックス

# ステアリングベクトル（複素数）
steering_complex = np.exp(-1j * 2 * np.pi * freq * n / M)

# 実験1: 実数信号
signal_real = np.cos(2 * np.pi * freq * n / M)

# 実験2: 複素信号
signal_complex = np.exp(1j * 2 * np.pi * freq * n / M)

# 位相を変化させて内積を計算
phases = np.linspace(0, 2*np.pi, 100)

# TODO: 実数と複素数でそれぞれ位相を振って内積を計算
# TODO: 結果をプロット
# TODO: 何が違うか観察
```

**期待される学び**（実験後に開く）:
<details>
<summary>クリックして答えを見る</summary>

- 実数では位相情報が失われる
- 複素数では振幅と位相の両方を保持
- レーダーでは「どの方向から来たか」を位相で判定するため、複素数が必須

</details>

---

### Q2: 共役転置はなぜ必要？

**あなたの実験での発見**:
- `complex_barrel_roll.ipynb`で、共役を取らないと内積がゼロになった
- 共役を取ると正しい値が出た

**質問**:
なぜ共役を取る必要があるのでしょうか？数学的・物理的な意味は？

**実験の方向性**:
1. 同じ信号同士の内積（共役あり vs なし）
2. 異なる信号の内積（共役あり vs なし）
3. 位相を変えたときの挙動（共役あり vs なし）

**実験テンプレート**:
```python
# notebooks/q02_why_conjugate.ipynb

# 同じ周波数の2つの複素信号
a = np.exp(1j * 2 * np.pi * freq * n / M)
b = np.exp(1j * 2 * np.pi * freq * n / M + 1j * phase)

# パターン1: 共役なし
inner_no_conj = np.sum(a * b)

# パターン2: 共役あり（正しい複素内積）
inner_with_conj = np.vdot(a, b)  # または np.sum(np.conj(a) * b)

# TODO: 位相を変化させて両方を計算
# TODO: 複素平面上にプロット
# TODO: 絶対値の変化を観察
```

**ヒント**:
- 共役を取ると「位相の差」が取れる
- 共役を取らないと「位相の和」になる

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 共役転置により「位相差」を計算できる
- `conj(a) * b = |a||b|·e^(j(φ_b - φ_a))`
- 物理的には「どれだけ位相がずれているか」を測定

</details>

---

### Q3: 位相普遍性とは何か？

**今回の実験で学んだこと**:
- 正しい複素指数関数と共役内積を使うと、位相を変えても内積は一定

**質問**:
この「位相普遍性」は、レーダー信号処理でなぜ重要なのでしょうか？

**実験の方向性**:
1. 同じ到来角の信号に全体位相回転を加える
2. ステアリングベクトルとの内積を計算
3. 異なる到来角の場合と比較

**実験テンプレート**:
```python
# notebooks/q03_phase_invariance.ipynb

# 到来角30度のステアリングベクトル
theta = 30  # degrees
d = 0.5  # 素子間隔（波長で正規化）
steering = np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta)))

# 受信信号（同じ到来角）+ 全体位相回転
global_phases = np.linspace(0, 2*np.pi, 100)
inner_products = []

for phi in global_phases:
    signal = np.exp(1j * phi) * steering  # 全体に位相回転
    inner = np.abs(np.vdot(steering, signal))
    inner_products.append(inner)

# TODO: プロット
# TODO: 異なる到来角でも試す
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 全体位相回転は物理的に意味がない（基準位相のずれ）
- ステアリングベクトルマッチングでは相対位相のみが重要
- これにより、受信機の基準発振器のずれを無視できる

</details>

---

## Phase 2: 空間周波数の理解

### Q4: 「空間周波数」とは何か？

**深層学習との対比**:
- 時間信号: `e^(j2πft)` → `f` が周波数（Hz）
- 空間信号: `e^(jnΔφ)` → `Δφ` が空間周波数（？）

**質問**:
ステアリングベクトルの「周波数が異なる」とは、具体的に何が異なるのでしょうか？

**実験の方向性**:
1. 異なる到来角のステアリングベクトルを生成
2. 実部・虚部をアンテナインデックスに対してプロット
3. 「波」の周期を観察

**実験テンプレート**:
```python
# notebooks/q04_spatial_frequency.ipynb

# 3つの異なる到来角
thetas = [10, 30, 60]  # degrees

fig, axes = plt.subplots(len(thetas), 1, figsize=(10, 8))

for i, theta in enumerate(thetas):
    steering = np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta)))

    axes[i].plot(n, np.real(steering), 'o-', label='Real')
    axes[i].plot(n, np.imag(steering), 's-', label='Imag')
    axes[i].set_title(f'θ = {theta}°')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.show()

# TODO: 各角度での「波の周期」を観察
# TODO: 角度と周期の関係を考察
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 到来角が異なると、アンテナ間の位相差が異なる
- アンテナインデックスに対する位相変化率 = 空間周波数
- 時間のFFT ↔ 空間のビームフォーミング（アナロジー）

</details>

---

### Q5: アンテナ素子数が変わると何が変わる？

**あなたの質問**:
「1周期分でも5周期分でも同じように扱える？」

**質問**:
アンテナ素子数（M=8 vs M=100）で、内積の値や分解能は変わるのでしょうか？

**実験の方向性**:
1. 同じ到来角で素子数を変える（M=8, 16, 32, 64）
2. ステアリングベクトルとの内積を計算
3. 正規化あり・なしで比較

**実験テンプレート**:
```python
# notebooks/q05_antenna_count.ipynb

theta = 30
d = 0.5
Ms = [8, 16, 32, 64]

for M in Ms:
    n = np.arange(M)

    # 正規化なし
    steering_unnorm = np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta)))
    signal_unnorm = steering_unnorm  # 同じ信号
    inner_unnorm = np.abs(np.vdot(steering_unnorm, signal_unnorm))

    # 正規化あり
    steering_norm = steering_unnorm / np.sqrt(M)
    signal_norm = signal_unnorm / np.sqrt(M)
    inner_norm = np.abs(np.vdot(steering_norm, signal_norm))

    print(f"M={M}: 正規化なし={inner_unnorm:.2f}, 正規化あり={inner_norm:.2f}")

# TODO: 素子数と内積の関係をプロット
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 正規化なしでは内積がMに比例
- 正規化すれば素子数によらず比較可能
- 素子数が多いほど角度分解能が向上（後の質問で実験）

</details>

---

## Phase 3: ビームフォーミングの基礎

### Q6: 内積で方向推定ができる理由は？

**質問**:
なぜステアリングベクトルとの内積で、物体の方向が分かるのでしょうか？

**実験の方向性**:
1. 特定角度から信号が到来（シミュレーション）
2. 全角度のステアリングベクトルとの内積を計算
3. スペクトルをプロット

**実験テンプレート**:
```python
# notebooks/q06_direction_estimation.ipynb

# 真の到来角
true_theta = 35  # degrees

# 受信信号（真の方向から）
M = 16
n = np.arange(M)
d = 0.5
signal = np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(true_theta)))

# 全角度を試す
test_thetas = np.linspace(-90, 90, 180)
spectrum = []

for theta in test_thetas:
    steering = np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta)))
    steering_norm = steering / np.sqrt(M)
    signal_norm = signal / np.sqrt(M)
    power = np.abs(np.vdot(steering_norm, signal_norm))**2
    spectrum.append(power)

plt.plot(test_thetas, spectrum)
plt.axvline(true_theta, color='r', linestyle='--', label='True angle')
plt.xlabel('Angle [deg]')
plt.ylabel('Power')
plt.title('Beamforming Spectrum')
plt.legend()
plt.grid(True)
plt.show()

# TODO: ピーク位置を確認
# TODO: 複数の物体がある場合も試す
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 真の角度でステアリングベクトルが一致 → 内積最大
- フーリエ変換と類似（周波数マッチング vs 角度マッチング）
- これがビームフォーミングの基本原理

</details>

---

### Q7: 2つの物体を区別できるか？

**質問**:
2つの近い角度から信号が来た場合、ビームフォーミングで区別できるでしょうか？

**実験の方向性**:
1. 2つの物体（θ1=30°, θ2=35°）からの信号を合成
2. ビームフォーミングスペクトルを計算
3. 角度差を変えて分離可能な限界を探る

**実験テンプレート**:
```python
# notebooks/q07_resolution.ipynb

# 2つの物体
theta1 = 30
theta2 = 35  # 5度の差
A1 = 1.0
A2 = 1.0

# 受信信号（2つの信号の重ね合わせ）
signal1 = A1 * np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta1)))
signal2 = A2 * np.exp(-1j * 2 * np.pi * d * n * np.sin(np.deg2rad(theta2)))
signal = signal1 + signal2

# ビームフォーミング
# （Q6と同じコード）

# TODO: 角度差を変えて実験（10度, 5度, 2度, 1度）
# TODO: どこまで分離できるか確認
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- ビームフォーミングには角度分解能の限界がある
- レイリー限界: Δθ ≈ λ/(M·d)
- これを超えるにはCapon, MUSICが必要

</details>

---

## Phase 4: 深層学習との対比

### Q8: Embeddingとの類似点は？

**質問**:
深層学習のembedding空間での類似度計算と、ステアリングベクトルの内積は似ていますか？

**考察の方向性**:
1. Embeddingベクトルの内積 → 意味的類似度
2. ステアリングベクトルの内積 → 角度の一致度
3. 両者の数学的構造を比較

**実験テンプレート**:
```python
# notebooks/q08_embedding_analogy.ipynb

# 深層学習のembedding（例）
embedding_dim = 16
word1_embed = np.random.randn(embedding_dim)
word2_embed = np.random.randn(embedding_dim)

# 正規化
word1_norm = word1_embed / np.linalg.norm(word1_embed)
word2_norm = word2_embed / np.linalg.norm(word2_embed)

# コサイン類似度
similarity = np.dot(word1_norm, word2_norm)

# ステアリングベクトル（同じ次元）
theta1 = 30
theta2 = 35
steering1 = np.exp(-1j * 2 * np.pi * d * np.arange(embedding_dim) * np.sin(np.deg2rad(theta1)))
steering2 = np.exp(-1j * 2 * np.pi * d * np.arange(embedding_dim) * np.sin(np.deg2rad(theta2)))

# 正規化
steering1_norm = steering1 / np.sqrt(embedding_dim)
steering2_norm = steering2 / np.sqrt(embedding_dim)

# 内積（絶対値）
inner_prod = np.abs(np.vdot(steering1_norm, steering2_norm))

print(f"Embedding similarity: {similarity:.4f}")
print(f"Steering inner product: {inner_prod:.4f}")

# TODO: 類似点と相違点を考察
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

類似点:
- 高次元空間でのベクトルマッチング
- 正規化により次元数に依存しない
- 内積で類似度を測定

相違点:
- Embedding: 実数、学習で獲得
- Steering: 複素数、物理法則で決定
- Steering: 位相情報が重要

</details>

---

### Q9: Transformerの注意機構との関連は？

**質問**:
Transformerのattentionは `Q·K^T` を計算します。これはステアリングベクトルの内積と関連がありますか？

**考察の方向性**:
1. Attention: Query-Keyの内積 → 関連度
2. Beamforming: Signal-Steeringの内積 → 方向一致度
3. 両者の構造的類似性

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- Attentionもビームフォーミングも「内積ベースのマッチング」
- Attentionは学習可能、ビームフォーミングは物理的
- ハイブリッド手法の可能性（学習可能なステアリングベクトル？）

</details>

---

### Q10: 深層学習でビームフォーミングを置き換えられるか？

**質問**:
ステアリングベクトルとの内積を、ニューラルネットワークで学習できるでしょうか？

**実験の方向性**:
1. 古典的ビームフォーミングで学習データ生成
2. 簡単なMLPで角度推定
3. 性能比較

**実験テンプレート**:
```python
# notebooks/q10_dl_beamforming.ipynb

import torch
import torch.nn as nn

# データ生成
def generate_data(n_samples):
    # TODO: ランダムな角度から信号を生成
    # TODO: 受信信号とラベル（角度）のペアを作成
    pass

# 簡単なMLP
class AngleEstimator(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim * 2, 64),  # 実部・虚部で2倍
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)  # 角度出力
        )

    def forward(self, x):
        # TODO: 複素数をreal/imagに分解
        # TODO: MLPに通す
        pass

# TODO: 学習
# TODO: 古典手法と比較
```

**期待される学び**:
<details>
<summary>クリックして答えを見る</summary>

- 単純なMLPでもビームフォーミングは学習可能
- しかし、物理法則を活用した方が効率的
- ハイブリッド（物理モデル + 学習）が有望

</details>

---

## 実験記録の方法

各質問の実験後、以下を記録してください：

### experiment_log.md に記載

```markdown
## Q1: なぜ複素数を使うのか？

### 実験日
2025-11-XX

### 仮説
複素数を使うのは位相情報を保持するため

### 実験内容
- 実数信号と複素信号でステアリングベクトルとの内積を計算
- 位相を0〜2πまで変化させて比較

### 結果
- 実数: 内積が位相に依存して変動
- 複素数: 内積が位相によらず一定

### 学び
複素数では振幅と位相を独立に扱える。レーダーでは位相が方向情報を持つため必須。

### ノートブック
[q01_why_complex.ipynb](../notebooks/q01_why_complex.ipynb)

### 次のアクション
Q2の共役転置の必要性を実験
```

---

## 進捗管理

- [ ] Q1: 複素数の必要性
- [ ] Q2: 共役転置の理由
- [ ] Q3: 位相普遍性の意味
- [ ] Q4: 空間周波数とは
- [ ] Q5: アンテナ素子数の影響
- [ ] Q6: 方向推定の原理
- [ ] Q7: 角度分解能
- [ ] Q8: Embeddingとの類似
- [ ] Q9: Attentionとの関連
- [ ] Q10: 深層学習での置き換え

**推奨順序**: Q1 → Q2 → Q3 → Q4 → Q5 → Q6 → Q7 → Q8 → Q9 → Q10

各質問を完了したら、AIに答え合わせを依頼してください。
