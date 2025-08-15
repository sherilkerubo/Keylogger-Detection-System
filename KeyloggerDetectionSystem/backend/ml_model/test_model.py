from predict import is_malicious  # No need for 'ml_model.'

sample = [0.1] * 81
result = is_malicious(sample)
print("Malicious" if result else "Benign")
