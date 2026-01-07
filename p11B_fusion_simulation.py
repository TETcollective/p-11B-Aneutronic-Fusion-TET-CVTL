"""
Topological Catalysis of p-¹¹B Aneutronic Fusion
TET–CVTL Framework – January 2026
Simon Soliman, TET Collective, Rome, Italy
License: CC BY-NC 4.0 (non-commercial)

QuTiP simulation of anyonic phase enhancement for p-¹¹B fusion
Generates: p11B_fusion_enhancement.pdf and .png
"""

!pip install qutip -q  # Solo per Colab, rimuovi se usi locale

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# Primordial trefoil anyonic phase
theta = 6 * np.pi / 5

# Effective Z amplification for boron (Z=5 vs proton Z=1)
Z_factor = 5.0

# Base Hamiltonian with stronger Coulomb proxy for p-¹¹B
H0 = Z_factor * qt.tensor(qt.sigmax(), qt.sigmax())

# Topological catalysis phase (amplified for higher Z)
phase = np.exp(1j * theta * Z_factor)
phase_op = qt.tensor(qt.qeye(2), qt.qdiags([1.0, phase], offsets=0))

# Effective Hamiltonian with catalysis
H_eff = H0 + phase_op

# Initial entangled state
psi0 = (qt.tensor(qt.basis(2,0), qt.basis(2,1)) + 
        qt.tensor(qt.basis(2,1), qt.basis(2,0))).unit()

# Proxy fused state (3α channel)
fused = qt.tensor(qt.basis(2,0), qt.basis(2,0))

# Time evolution
times = np.linspace(0, 15, 500)

# With catalysis
result_with = qt.mesolve(H_eff, psi0, times)
overlap_with = [abs(fused.overlap(state))**2 for state in result_with.states]

# Without catalysis
result_without = qt.mesolve(H0, psi0, times)
overlap_without = [abs(fused.overlap(state))**2 for state in result_without.states]

# Enhancement factor
enhancement = np.max(overlap_with) / np.max(overlap_without)
print(f"p-¹¹B fusion enhancement factor: {enhancement:.1f}x")

# Plot
plt.figure(figsize=(10,6))
plt.plot(times, overlap_with, label=f'With trefoil catalysis (enhancement {enhancement:.1f}x)', color='gold', linewidth=3)
plt.plot(times, overlap_without, '--', label='Standard p-¹¹B (high Z=5 barrier)', color='red', linewidth=2.5)
plt.title('TET–CVTL Topological Catalysis of p-¹¹B Aneutronic Fusion')
plt.xlabel('Time (arbitrary units)')
plt.ylabel('Fusion channel overlap probability')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig('p11B_fusion_enhancement.pdf', dpi=300)
plt.savefig('p11B_fusion_enhancement.png', dpi=300)
print("Figures saved: p11B_fusion_enhancement.pdf and .png")
