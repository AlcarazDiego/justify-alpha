import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def bayes_alpha(test_type, alternative, target_bf10, target_total_n):

    # ==========================================================
    # STEP1: ESTABLISHES RESEARCH PARAMETERS
    # ==========================================================
    CONFIG = {
        'test_type': test_type,      # 'one-sample', 'paired', or 'two-sample'
        'alternative': alternative,     # 'two-sided', 'larger', or 'smaller'
        'target_bf10': target_bf10,             # Target Bayes Factor (e.g., 3 for moderate evidence)
    
        # IMPORTANT: For the BIC approximation, always use the TOTAL sample size.
        # If you have two groups of 175, put 350.
        'target_total_n': target_total_n,          # Specific Total N you want to calculate
        'graph_max_n': 1000   # Upper limit for the X-axis visualization     
    }

    if target_total_n > CONFIG['graph_max_n']:
        CONFIG['graph_max_n'] = target_total_n

    # ==========================================================
    # STEP2: CALCULATION ENGINE (BIC APPROXIMATION)
    # ==========================================================
    def get_alpha_from_bf(target_bf10, total_n, test_type, alternative):
        try:
            # 1. Solve for the critical t-statistic using the BIC approximation
            t_stat_squared = 2 * np.log(target_bf10) + np.log(total_n)

            if t_stat_squared <= 0:
                return "Sample size too small to achieve this Bayes Factor with a valid t-statistic."
            
            critical_t = np.sqrt(t_stat_squared)
        
            # 2. Determine degrees of freedom 
            if test_type == 'two-sample':
                df = total_n - 2
            elif test_type in ['paired', 'one-sample']:
                df = total_n - 1
            else:
                return "Error: test_type must be 'two-sample', 'paired', or 'one-sample'."
            
            # 3. Convert t-statistic to frequentist p-value (alpha)
            # sf = survival function (equivalent to 1 - cdf, finding the right tail)
            if alternative == 'two-sided':
                adjusted_alpha = 2 * stats.t.sf(critical_t, df)
            elif alternative in ['larger', 'smaller']:
                adjusted_alpha = stats.t.sf(critical_t, df)
            else:
                return "Error: alternative must be 'two-sided', 'larger', or 'smaller'."
            
            return float(adjusted_alpha)
        
        except Exception as e:
            return f"Error: {e}"

    # ==========================================================
    # STEP3: ANALYSIS AND VISUALIZATION
    # ==========================================================
    def run_analysis():
        print(f"--- ANALYZING: {CONFIG['test_type']} ({CONFIG['alternative']}) ---")
        print(f"--- TARGET: Bayes Factor (BF10) = {CONFIG['target_bf10']} ---")

        # 3A: Get precise alpha for target_total_n
        target_alpha_result = get_alpha_from_bf(
            CONFIG['target_bf10'], 
            CONFIG['target_total_n'], 
            CONFIG['test_type'],
            CONFIG['alternative']
        )
    
        if isinstance(target_alpha_result, float):
            print(f"✓ Adjusted alpha for target Total N={CONFIG['target_total_n']}: {target_alpha_result:.10e}")
            target_alpha = target_alpha_result
        else:
            print(f"! Could not calculate alpha for Total N={CONFIG['target_total_n']}. {target_alpha_result}")
            target_alpha = None

        # 3B: Generate data for the full graph
        print(f"\nGenerating graph up to Total N={CONFIG['graph_max_n']}...")
        sample_sizes = np.arange(20, CONFIG['graph_max_n'] + 1, 10)
        alphas = []
        valid_ns = []
    
        for n in sample_sizes:
            a = get_alpha_from_bf(
                CONFIG['target_bf10'], 
                n, 
                CONFIG['test_type'],
                CONFIG['alternative']
            )
        
            if isinstance(a, float):
                alphas.append(a)
                valid_ns.append(n)

        # 3C: Plotting
        if alphas:
            plt.figure(figsize=(10, 6))
            plt.plot(valid_ns, alphas, linewidth=2.5, color='#1f77b4', label=f'Equivalent Alpha (BF={CONFIG["target_bf10"]})')
        
            if target_alpha:
                plt.plot(CONFIG['target_total_n'], target_alpha, 'ro', 
                         label=f'Your Target (N={CONFIG["target_total_n"]}, α={target_alpha:.4f})')
        
            plt.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='Traditional α = 0.05')
        
            plt.yscale('log')
            plt.xlabel('Total Sample Size (N)', fontsize=12)
            plt.ylabel('Required Alpha (Log Scale)', fontsize=12)
            plt.title(f"Bayes Factor Equivalence Adjustment (BF10={CONFIG['target_bf10']}, {CONFIG['alternative']})", pad=15)
            plt.grid(True, which="both", ls="--", alpha=0.4)
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            print("No valid data points generated to plot. Target BF might be too high for these sample sizes.")

    if __name__ == "__main__":
        run_analysis()
