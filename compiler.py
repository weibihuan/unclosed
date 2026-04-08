[compiler.py](https://github.com/user-attachments/files/26564603/compiler.py)
""" unclosed.compiler ~~~~~~~~~~~~~~~~~ 核心功能：验证数学常数是否符合已知的快速收敛公式（如拉马努金型）。 """
import mpmath as mp
from typing import Dict, Any, Optional, Callable, Union
import warnings

_FORMULA_DB = {
    '1/pi_ramanujan_396': {
        'description': 'Ramanujan 1/π series with base 396 (fastest)',
        'target_constant': lambda: 1 / mp.pi,
        'target_name': '1/π',
        'template': r'\sum_{n=0}^{\infty} \frac{(4n)!}{(n!)^4} \frac{A n + B}{C^{4n}}',
        'params': {'A': 1103, 'B': 26390, 'C': 396},
        'prefactor': lambda: 2 * mp.sqrt(2) / 9801,
        'expected_decay_exponent': 4,
        'convergence_threshold': 1e-15,
    },
}

def check_ramanujan_style(
    target: Union[str, Callable[[], mp.mpf], None] = '1/pi',
    base: Optional[int] = None,
    N: int = 5,
    dps: int = 50
) -> Dict[str, Any]:
    with mp.workdps(dps):
        formulas_to_check = []
        if base is not None:
            for fid, info in _FORMULA_DB.items():
                if info['params'].get('C') == base:
                    formulas_to_check.append((fid, info))
        else:
            formulas_to_check = list(_FORMULA_DB.items())
        if not formulas_to_check:
            warnings.warn(f"No formula found for base {base}")
            return _no_match_result(base)

        if callable(target):
            target_func = target
            target_name = 'user_provided'
        elif isinstance(target, str):
            if target == '1/pi':
                target_func = lambda: 1 / mp.pi
                target_name = '1/π'
            elif target == 'pi':
                target_func = lambda: mp.pi
                target_name = 'π'
            else:
                raise ValueError(f"Unknown target constant: {target}")
        else:
            target_func = formulas_to_check[0][1]['target_constant']
            target_name = formulas_to_check[0][1]['target_name']
        true_value = target_func()

        best_match = None
        best_confidence = 0.0
        for fid, info in formulas_to_check:
            A = info['params']['A']
            B = info['params']['B']
            C = info['params']['C']
            prefactor = info
            alpha = info['expected_decay_exponent']

            partial = mp.mpf('0')
            errors = []
            for n in range(N + 1):
                term = (A * n + B) * (mp.factorial(4 * n) / (mp.factorial(n) ** 4))
                term /= (C ** (alpha * n))
                partial += term
                approx = 1 / (prefactor * partial)
                error = abs(approx - true_value)
                errors.append(float(error))

            final_error = errors[-1]
            confidence = min(1.0, max(0.0, 1 - final_error * (10 ** (dps / 3))))
            observed_base = C
            if len(errors) >= 2 and errors[-2] > 0:
                observed_ratio = errors[-1] / errors[-2]
                if observed_ratio > 0:
                    observed_base = observed_ratio ** (-1 / alpha)
            if abs(observed_base - C) / C < 0.1:
                confidence = min(1.0, confidence * 1.2)

            if confidence > best_confidence:
                best_confidence = confidence
                best_match = {
                    'matched': confidence > 0.9,
                    'confidence': confidence,
                    'observed_base': observed_base,
                    'expected_base': C,
                    'error_sequence': errors,
                    'formula_id': fid,
                    'formula_description': info['description'],
                    'target_name': target_name,
                }
        return best_match if best_match else _no_match_result(base)

def _no_match_result(base):
    return {
        'matched': False,
        'confidence': 0.0,
        'observed_base': None,
        'expected_base': base,
        'error_sequence': [],
        'formula_id': None,
        'formula_description': None,
        'target_name': None,
    }
