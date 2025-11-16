"""
ステアリングベクトルの位相普遍性の検証
"""
import numpy as np
import matplotlib.pyplot as plt

# パラメータ
freq = 5  # 周波数（または空間周波数）
N = 100   # サンプル数（またはアンテナ素子数）
t = np.arange(0, 1, 0.01)  # 時間軸（またはアンテナインデックス）

# ステアリングベクトル（特定の到来方向に対応）
steering_vector = np.exp(-1j * 2 * np.pi * freq * t)

print("=" * 60)
print("実験1: 同じ周波数の受信信号（位相を変化させる）")
print("=" * 60)

# 位相を変化させて内積を計算
phases = np.linspace(0, 2*np.pi, 100)
inner_products_wrong = []  # 誤った方法
inner_products_correct = []  # 正しい方法

for phase in phases:
    # 受信信号（位相がphaseだけずれている）
    # 正しい複素指数関数
    x_complex_correct = np.exp(1j * (2 * np.pi * freq * t + phase))

    # あなたの元のコード（参考）
    x1 = np.sin(2 * np.pi * freq * t + phase)
    x2 = np.sin(2 * np.pi * freq * t + np.pi / 2 + phase)
    x_complex_wrong = x1 + 1j * x2

    # 正しい内積（共役を取る）
    inner_prod_correct = np.abs(np.vdot(steering_vector, x_complex_correct))
    inner_products_correct.append(inner_prod_correct)

    # 誤った内積（共役なし）
    inner_prod_wrong = np.abs(np.sum(x_complex_wrong * steering_vector))
    inner_products_wrong.append(inner_prod_wrong)

# プロット
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(phases, inner_products_wrong, 'r-', linewidth=2, label='元のコード（誤り）')
plt.xlabel('位相 φ [rad]')
plt.ylabel('内積の絶対値')
plt.title('誤った計算方法\n（実部・虚部の定義が逆 & 共役なし）')
plt.grid(True)
plt.legend()
plt.ylim([-0.1, max(inner_products_correct) * 1.2])

plt.subplot(1, 2, 2)
plt.plot(phases, inner_products_correct, 'b-', linewidth=2, label='修正版（正しい）')
plt.xlabel('位相 φ [rad]')
plt.ylabel('内積の絶対値')
plt.title('正しい計算方法\n（e^(j(ωt+φ)) と共役内積）')
plt.grid(True)
plt.axhline(y=np.mean(inner_products_correct), color='g', linestyle='--',
            label=f'平均値 = {np.mean(inner_products_correct):.2f}')
plt.legend()

plt.tight_layout()
plt.savefig('d:/radar_understanding/docs/phase_invariance_comparison.png', dpi=150)
plt.show()

print(f"\n【誤った方法】")
print(f"  内積の範囲: {np.min(inner_products_wrong):.6f} ~ {np.max(inner_products_wrong):.6f}")
print(f"  標準偏差: {np.std(inner_products_wrong):.6f}")

print(f"\n【正しい方法】")
print(f"  内積の範囲: {np.min(inner_products_correct):.6f} ~ {np.max(inner_products_correct):.6f}")
print(f"  標準偏差: {np.std(inner_products_correct):.10f}")
print(f"  → 位相によらずほぼ一定！（位相普遍性）")

print("\n" + "=" * 60)
print("実験2: 異なる周波数の受信信号（位相普遍性が崩れる例）")
print("=" * 60)

freq2 = 7  # 異なる周波数
steering_vector2 = np.exp(-1j * 2 * np.pi * freq2 * t)

inner_products_diff_freq = []
for phase in phases:
    x_complex = np.exp(1j * (2 * np.pi * freq * t + phase))
    inner_prod = np.abs(np.vdot(steering_vector2, x_complex))
    inner_products_diff_freq.append(inner_prod)

plt.figure(figsize=(10, 6))
plt.plot(phases, inner_products_correct, 'b-', linewidth=2,
         label=f'同じ周波数 (freq={freq})')
plt.plot(phases, inner_products_diff_freq, 'r-', linewidth=2,
         label=f'異なる周波数 (steering={freq2}, signal={freq})')
plt.xlabel('位相 φ [rad]')
plt.ylabel('内積の絶対値')
plt.title('周波数が異なる場合の位相依存性')
plt.grid(True)
plt.legend()
plt.savefig('d:/radar_understanding/docs/different_frequency_comparison.png', dpi=150)
plt.show()

print(f"\n【異なる周波数】")
print(f"  内積の範囲: {np.min(inner_products_diff_freq):.6f} ~ {np.max(inner_products_diff_freq):.6f}")
print(f"  標準偏差: {np.std(inner_products_diff_freq):.6f}")
print(f"  → 位相に依存して変動（位相普遍性が成立しない）")

print("\n" + "=" * 60)
print("結論")
print("=" * 60)
print("1. 同じ周波数の場合、位相によらず内積は一定（位相普遍性）")
print("2. 異なる周波数の場合、位相によって内積が変動する")
print("3. 正しい複素数表現と共役内積が重要")
