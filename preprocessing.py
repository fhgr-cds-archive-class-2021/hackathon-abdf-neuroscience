import numpy as np
import scipy.stats as linregress

window = 12

alpha_queue = np.array([])
beta_queue = np.array([])
gamma_queue = np.array([])
delta_queue = np.array([])
theta_queue = np.array([])
sigma_queue = np.array([])

def preprocessing_pipeline(alpha, beta, gamma, delta, theta, sigma):
    global alpha_queue, beta_queue, gamma_queue, delta_queue, theta_queue, sigma_queue, window
    #print(f"Alpha: {alpha}, Beta: {beta}, Gamma: {gamma}, Delta: {delta}, Theta: {theta}, Sigma: {sigma}")

    if not alpha or not beta or not gamma or not delta or not theta or not sigma:
        return None

    alpha_queue = np.append(alpha_queue, alpha)
    beta_queue = np.append(beta_queue, beta)
    gamma_queue = np.append(gamma_queue, gamma)
    delta_queue = np.append(delta_queue, delta)
    theta_queue = np.append(theta_queue, theta)
    sigma_queue = np.append(sigma_queue, sigma)
    
    mean_freq = []
    if len(alpha_queue) >= window:     
        mean_freq.append(np.mean(alpha_queue[:-window]))
        mean_freq.append(np.mean(beta_queue[:-window]))
        mean_freq.append(np.mean(gamma_queue[:-window]))
        mean_freq.append(np.mean(delta_queue[:-window]))
        mean_freq.append(np.mean(theta_queue[:-window]))
        mean_freq.append(np.mean(sigma_queue[:-window]))

        print(f"Mean freq: {mean_freq}")
        
        max_freq = np.argmax(mean_freq)
        print(f"Max freq Index: {max_freq}")
        # 0: alpha, 1: beta, 2: gamma, 3: delta, 4: theta, 5: sigma

        return max_freq

    return None

def map_index_to_brain_wave(index):
    brain_waves = ['alpha', 'beta', 'gamma', 'delta', 'theta', 'sigma']
    return brain_waves[index]

def gamma_trend():
    global gamma_queue, window
    if len(gamma_queue) < window:
        return None  # Not enough data points for trend analysis
    y = gamma_queue[-window:]
    x = np.arange(window)
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return slope