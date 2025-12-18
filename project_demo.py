from matplotlib import patheffects
import streamlit as st
import time as time_module
from sympy import randprime, mod_inverse
import numpy as np
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import seaborn as sns
import math

# Set page config
st.set_page_config(
    page_title="Cryptography Demos: RSA & Quantum BB84",
    layout="wide",
    page_icon="🔐"
)

# Sidebar menu
st.sidebar.title("🔐 Cryptography Demos")
st.sidebar.markdown("---")

# Menu selection
demo_selection = st.sidebar.radio(
    "Select Demo:",
    ["🏠 Home", "🔐 RSA Encryption", "⚛️ Quantum BB84", "📊 Comparison"]
)

# -------------------------------
# COMMON STYLING
# -------------------------------
def apply_custom_styles():
    st.markdown("""
    <style>
    /* --- Existing styles (unchanged) --- */
    .main-header {
        color: #1E3A8A;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-section {
        background-color: #F8FAFC;
        color: #1E3A8A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #3B82F6;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        color: #1E3A8A;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .info-box {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        color: #1E3A8A;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }

    .qubit-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 14px;
        border: 1.5px solid #BFDBFE;
        color: #1E3A8A;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        font-size: 0.9rem;
    }

    .qubit-card h4 {
        margin-bottom: 8px;
        font-size: 1.05rem;
    }

    .qubit-card:hover {
        transform: translateY(-3px);
    }

    .qubit-safe {
        border-left: 6px solid #3B82F6;
    }

    .qubit-eve {
        border-left: 6px solid #EF4444;
        background-color: #FEF2F2;
    }

    .basis-pill {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 0.8rem;
        margin-left: 5px;
        background-color: #DBEAFE;
        color: #1E3A8A;
        font-weight: 600;
    }

    .eve-pill {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


apply_custom_styles()

# -------------------------------
# HOME PAGE
# -------------------------------
if demo_selection == "🏠 Home":
    st.markdown("<h1 class='main-header'>Cryptography Demos: Classical vs Quantum</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='demo-section'>
        <h2>🔐 RSA Encryption</h2>
        <p><strong>Classical Public-Key Cryptography</strong></p>
        <ul>
        <li>Based on prime factorization</li>
        <li>Asymmetric encryption</li>
        <li>Vulnerable to quantum computers (Shor's algorithm)</li>
        <li>Key size vs security trade-off</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='demo-section'>
        <h2>⚛️ Quantum BB84</h2>
        <p><strong>Quantum Key Distribution</strong></p>
        <ul>
        <li>Unconditional security (quantum physics)</li>
        <li>Detects eavesdropping attempts</li>
        <li>No computational assumptions</li>
        <li>Quantum bit error rate (QBER) monitoring</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comparison table
    st.subheader("📊 Quick Comparison")
    comparison_data = {
        "Property": ["Security Basis", "Eavesdropping Detection", "Quantum Safe", "Key Distribution"],
        "RSA": ["Computational Hardness", "No", "No (broken by Shor)", "Public/Private Key"],
        "BB84": ["Quantum Mechanics", "Yes (via QBER)", "Yes", "Symmetric Key"]
    }
    
    st.table(pd.DataFrame(comparison_data))
    
    # Security timeline
    st.subheader("🛡️ Security Timeline")
    timeline_data = {
        "Year": ["1977", "1984", "1994", "1996", "2020s"],
        "Event": ["RSA Invented", "BB84 Proposed", "Shor's Algorithm", "First QKD Demo", "Post-Quantum Crypto"],
        "Impact": ["Revolutionized secure communication", "First quantum cryptography protocol", "Showed RSA is quantum-vulnerable", "Practical quantum key distribution", "Transition to quantum-safe algorithms"]
    }
    st.table(pd.DataFrame(timeline_data))

# -------------------------------
# RSA ENCRYPTION DEMO
# -------------------------------
elif demo_selection == "🔐 RSA Encryption":
    st.title("🔐 RSA Encryption Demo")
    st.markdown("Classical public-key cryptography based on prime factorization")
    
    # RSA Functions
    def generate_keys(bits):
        start = time_module.time()
        
        half = bits // 2
        p = randprime(2**(half-1), 2**half)
        q = randprime(2**(half-1), 2**half)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        d = mod_inverse(e, phi)
        
        end = time_module.time()
        return n, e, d, p, q, end - start
    
    def encrypt(message, e, n):
        start = time_module.time()
        # Split into chunks for large messages
        chunk_size = (n.bit_length() // 8) - 1
        cipher_chunks = []
        
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i+chunk_size]
            numeric = int.from_bytes(chunk.encode('utf-8'), 'big')
            cipher_chunks.append(pow(numeric, e, n))
        
        end = time_module.time()
        return cipher_chunks, end - start
    
    def decrypt(cipher_chunks, d, n):
        start = time_module.time()
        message_parts = []
        
        for cipher in cipher_chunks:
            numeric = pow(cipher, d, n)
            # Convert back to bytes then to string
            byte_length = (numeric.bit_length() + 7) // 8
            bytes_data = numeric.to_bytes(byte_length, 'big')
            message_parts.append(bytes_data.decode('utf-8', errors='ignore'))
        
        end = time_module.time()
        return ''.join(message_parts), end - start
    
    def get_grovers_time(bits):
        """Grover's algorithm time for symmetric key search (simplified)"""
        # Grover's provides quadratic speedup: O(√N) instead of O(N)
        key_space = 2 ** bits
        
        # Classical brute force
        classical_operations = key_space / 2
        classical_time_seconds = classical_operations / (1e12)
        
        # Grover's quantum speedup
        quantum_operations = math.sqrt(key_space)
        quantum_time_seconds = quantum_operations / (1e6)
        
        return {
            "classical_years": classical_time_seconds / (365 * 24 * 3600),
            "quantum_seconds": quantum_time_seconds,
            "quantum_ms": quantum_time_seconds * 1000,
            "speedup_factor": classical_time_seconds / quantum_time_seconds
        }
    
    def get_shors_time(bits):
        """Realistic Shor's algorithm time estimates"""
        if bits <= 1024:
            time_ms = 500
        elif bits <= 2048:
            time_ms = 8000
        elif bits <= 3072:
            time_ms = 30000
        elif bits <= 4096:
            time_ms = 120000
        else:
            time_ms = bits * 100
        
        if bits <= 1024:
            qubits = "~2,000 logical qubits"
        elif bits <= 2048:
            qubits = "~20 million physical qubits"
        elif bits <= 4096:
            qubits = "~100 million physical qubits"
        else:
            qubits = ">500 million physical qubits"
        
        return {
            "time_ms": time_ms,
            "time_seconds": time_ms / 1000,
            "readable": f"{time_ms} ms" if time_ms < 1000 else f"{time_ms/1000:.1f} s",
            "hardware": qubits,
            "note": "Requires fault-tolerant quantum computer"
        }
    
    def estimate_classical_attack_time(bits, algorithm="GNFS"):
        """Estimate classical attack times"""
        n = 2 ** bits
        
        if algorithm == "trial_division":
            operations = math.isqrt(n)
            time_seconds = operations / 1e15
        elif algorithm == "GNFS":
            log_n = math.log(n)
            log_log_n = math.log(log_n)
            exponent = (64/9) ** (1/3) * (log_n ** (1/3)) * (log_log_n ** (2/3))
            operations = math.exp(exponent)
            time_seconds = operations / 1e12
        
        if time_seconds < 1:
            readable = f"{time_seconds*1000:.0f} ms"
        elif time_seconds < 60:
            readable = f"{time_seconds:.1f} seconds"
        elif time_seconds < 3600:
            readable = f"{time_seconds/60:.1f} minutes"
        elif time_seconds < 86400:
            readable = f"{time_seconds/3600:.1f} hours"
        elif time_seconds < 31536000:
            readable = f"{time_seconds/86400:.1f} days"
        elif time_seconds < 3.1536e9:
            readable = f"{time_seconds/31536000:.1f} years"
        else:
            readable = f"{time_seconds/3.1536e12:.0f} trillion years"
        
        return {
            "operations": f"{operations:.2e}",
            "time_seconds": time_seconds,
            "readable": readable,
            "algorithm": algorithm
        }

    # ============================================
    # SIDEBAR CONTROLS ONLY
    # ============================================
    st.sidebar.header("🔧 RSA Controls")
    
    # Key Generation Section in Sidebar
    st.sidebar.subheader("1. Key Generation")
    
    # Single key generation mode
    generation_mode = st.sidebar.radio(
        "Generation Mode:",
        ["Single Key", "Multiple Keys"],
        key="gen_mode"
    )
    
    if generation_mode == "Single Key":
        # Single key selection
        key_size = st.sidebar.selectbox(
            "Select RSA Key Size (bits):",
            [256, 512, 1024, 2048, 3072, 4096],
            index=2,  # Default to 1024
            key="rsa_single_size"
        )
        
        if st.sidebar.button("🎯 Generate Single Key", type="primary", key="generate_single"):
            with st.spinner(f"Generating {key_size}-bit RSA key..."):
                n, e, d, p, q, keygen_time = generate_keys(key_size)
            
            # Store in session state
            st.session_state.current_key = {
                'size': key_size,
                'n': n, 'e': e, 'd': d, 'p': p, 'q': q,
                'keygen_time': keygen_time,
                'bit_length': n.bit_length()
            }
            st.session_state.rsa_keys_generated = True
            st.session_state.mode = "single"
            st.sidebar.success(f"{key_size}-bit key generated!")
            
    else:  # Multiple Keys
        st.sidebar.markdown("Select multiple key sizes to generate:")
        
        # Multi-select for multiple keys
        selected_sizes = st.sidebar.multiselect(
            "Choose key sizes:",
            [256, 512, 1024, 2048, 3072, 4096],
            default=[1024, 2048, 4096],
            key="rsa_multi_sizes"
        )
        
        if st.sidebar.button("🚀 Generate All Selected Keys", type="primary", key="generate_multi"):
            if not selected_sizes:
                st.sidebar.warning("Please select at least one key size!")
            else:
                with st.spinner(f"Generating {len(selected_sizes)} RSA keys..."):
                    generated_keys = {}
                    for size in selected_sizes:
                        n, e, d, p, q, keygen_time = generate_keys(size)
                        generated_keys[size] = {
                            'n': n, 'e': e, 'd': d, 'p': p, 'q': q,
                            'keygen_time': keygen_time,
                            'bit_length': n.bit_length()
                        }
                
                st.session_state.generated_keys = generated_keys
                st.session_state.rsa_keys_generated = True
                st.session_state.mode = "multiple"
                st.session_state.current_key_size = selected_sizes[0]
                st.sidebar.success(f"Generated {len(selected_sizes)} keys!")
    
    st.sidebar.markdown("---")
    
    # Encryption/Decryption Controls
    if 'rsa_keys_generated' in st.session_state and st.session_state.rsa_keys_generated:
        st.sidebar.subheader("2. Encryption/Decryption")
        
        if st.session_state.mode == "multiple":
            # Let user select which key to use from generated ones
            available_keys = list(st.session_state.generated_keys.keys())
            selected_key = st.sidebar.selectbox(
                "Select key to use:",
                available_keys,
                key="key_selector"
            )
            st.session_state.current_key_size = selected_key
            current_key_data = st.session_state.generated_keys[selected_key]
        else:
            current_key_data = st.session_state.current_key
        
        # Message input in sidebar
        message = st.sidebar.text_area(
            "Message to encrypt:",
            "Hello Quantum World!",
            height=100,
            key="message_input"
        )
        
        col_enc, col_dec = st.sidebar.columns(2)
        
        with col_enc:
            if st.sidebar.button("🔒 Encrypt", key="encrypt_btn"):
                cipher, enc_time = encrypt(message, current_key_data['e'], current_key_data['n'])
                st.session_state.cipher = cipher
                st.session_state.enc_time = enc_time
                st.session_state.original_message = message
                st.session_state.encrypted = True
                st.sidebar.success("Encrypted!")
        
        with col_dec:
            if 'encrypted' in st.session_state and st.session_state.encrypted:
                if st.sidebar.button("🔓 Decrypt", key="decrypt_btn"):
                    decrypted, dec_time = decrypt(
                        st.session_state.cipher,
                        current_key_data['d'],
                        current_key_data['n']
                    )
                    st.session_state.decrypted = decrypted
                    st.session_state.dec_time = dec_time
                    st.sidebar.success("Decrypted!")
        
        st.sidebar.markdown("---")
        
        # Performance Comparison Controls
        if st.session_state.mode == "multiple":
            st.sidebar.subheader("3. Performance Analysis")
            
            compare_count = st.sidebar.slider(
                "Keys to compare:",
                min_value=2,
                max_value=min(6, len(st.session_state.generated_keys)),
                value=min(3, len(st.session_state.generated_keys)),
                key="compare_slider"
            )
            
            # Let user select which keys to compare
            available_keys = list(st.session_state.generated_keys.keys())
            keys_to_compare = st.sidebar.multiselect(
                f"Select keys to compare (max {compare_count}):",
                available_keys,
                default=available_keys[:min(compare_count, len(available_keys))],
                max_selections=compare_count,
                key="compare_select"
            )
            
            st.session_state.keys_to_compare = keys_to_compare
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Controls moved to sidebar for better organization")
    
    # ============================================
    # MAIN CONTENT AREA (DISPLAY ONLY)
    # ============================================
    
    # Introduction
    st.markdown("""
    <div class='info-box'>
    <h4>📖 How to Use This Demo:</h4>
    <ol>
    <li>Use the <strong>sidebar controls on the left</strong> to generate RSA keys</li>
    <li>Choose between single key or multiple keys generation</li>
    <li>Results will appear automatically in this main area</li>
    <li>Use encryption/decryption controls in the sidebar</li>
    <li>Performance comparisons will update automatically</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Display generated key(s) information
    if 'rsa_keys_generated' in st.session_state and st.session_state.rsa_keys_generated:
        
        if st.session_state.mode == "single":
            # Display single key information
            current_key = st.session_state.current_key
            key_size = current_key['size']
            
            st.subheader(f"🔑 Generated {key_size}-bit RSA Key")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Key Size", f"{key_size} bits")
            with col2:
                st.metric("Generation Time", f"{current_key['keygen_time']:.4f}s")
            
            # Security analysis
            classical = estimate_classical_attack_time(key_size, "GNFS")
            quantum = get_shors_time(key_size)
            
            with col3:
                st.metric("Classical Security", 
                         classical['readable'],
                         delta="GNFS Algorithm",
                         delta_color="off")
            with col4:
                st.metric("Quantum Attack", 
                         f"{quantum['time_ms']:.0f} ms",
                         delta="Shor's Algorithm",
                         delta_color="inverse")
            
            # Security warning
            security_status = "✅ Secure" if key_size >= 2048 else "⚠️ Weak" if key_size >= 1024 else "❌ Insecure"
            status_color = "green" if key_size >= 2048 else "orange" if key_size >= 1024 else "red"
            
            st.markdown(f"""
            <div class='warning-box'>
            <h4>🛡️ Security Analysis: {security_status}</h4>
            <p><strong>{key_size}-bit RSA Key Analysis:</strong></p>
            <ul>
            <li><strong>Classical Attack Time</strong>: {classical['readable']} using {classical['algorithm']}</li>
            <li><strong>Quantum Attack Time</strong>: {quantum['readable']} using Shor's algorithm</li>
            <li><strong>Hardware Required</strong>: {quantum['hardware']}</li>
            <li><strong>Status</strong>: <span style='color:{status_color}; font-weight:bold;'>{security_status}</span></li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Key details
            with st.expander("🔍 View Key Details & Verification"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**Public Key:**")
                    st.code(f"e = {current_key['e']}")
                    st.code(f"n = {current_key['n']}")
                    
                    st.write("**Private Key:**")
                    st.code(f"d = {current_key['d']}")
                
                with col_b:
                    st.write("**Prime Factors:**")
                    st.code(f"p = {current_key['p']}")
                    st.code(f"q = {current_key['q']}")
                    
                    # Verification
                    st.write("**Verification Tests:**")
                    
                    # Test 1: Factorization
                    n_calculated = current_key['p'] * current_key['q']
                    if n_calculated == current_key['n']:
                        st.success("✓ Factorization: p × q = n")
                    else:
                        st.error("✗ Factorization failed")
                    
                    # Test 2: Encryption/Decryption
                    test_value = 12345
                    encrypted = pow(test_value, current_key['e'], current_key['n'])
                    decrypted = pow(encrypted, current_key['d'], current_key['n'])
                    if test_value == decrypted:
                        st.success(f"✓ Crypto test: {test_value} → {encrypted} → {decrypted}")
                    else:
                        st.error(f"✗ Crypto test failed")
        
        else:  # Multiple keys mode
            st.subheader("📊 Multiple RSA Keys Generated")
            
            # Summary table of all generated keys
            summary_data = []
            for size, data in st.session_state.generated_keys.items():
                classical = estimate_classical_attack_time(size, "GNFS")
                quantum = get_shors_time(size)
                
                summary_data.append({
                    'Size': f"{size}-bit",
                    'Gen Time': f"{data['keygen_time']:.4f}s",
                    'Modulus Bits': data['bit_length'],
                    'Classical Security': classical['readable'],
                    'Quantum Attack': f"{quantum['time_ms']:.0f} ms",
                    'Status': '✅ Secure' if size >= 2048 else '⚠️ Weak' if size >= 1024 else '❌ Insecure'
                })
            
            # Display summary table
            st.table(pd.DataFrame(summary_data))
            
            # Currently selected key details
            if 'current_key_size' in st.session_state:
                current_size = st.session_state.current_key_size
                current_data = st.session_state.generated_keys[current_size]
                
                st.markdown(f"""
                <div class='info-box'>
                <h4>🎯 Currently Selected: {current_size}-bit Key</h4>
                <p>Using this key for encryption/decryption operations.</p>
                <p>Generation time: {current_data['keygen_time']:.4f} seconds</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Encryption/Decryption Results Display
        st.markdown("---")
        st.subheader("✉️ Encryption & Decryption")
        
        if 'encrypted' in st.session_state and st.session_state.encrypted:
            col_enc, col_dec = st.columns(2)
            
            with col_enc:
                st.write("**🔒 Encryption Results**")
                st.write(f"Original message: `{st.session_state.original_message}`")
                st.write(f"Encryption time: {st.session_state.enc_time:.6f} seconds")
                st.write(f"Number of ciphertext chunks: {len(st.session_state.cipher)}")
                
                if st.session_state.cipher:
                    with st.expander("View Ciphertext"):
                        for i, chunk in enumerate(st.session_state.cipher[:5]):
                            st.code(f"Chunk {i}: {chunk}")
                        if len(st.session_state.cipher) > 5:
                            st.caption(f"... and {len(st.session_state.cipher)-5} more chunks")
            
            with col_dec:
                if 'decrypted' in st.session_state:
                    st.write("**🔓 Decryption Results**")
                    st.write(f"Decryption time: {st.session_state.dec_time:.6f} seconds")
                    
                    # Verification
                    if st.session_state.decrypted == st.session_state.original_message:
                        st.success(f"✅ Decryption successful!")
                        st.write(f"Decrypted message: `{st.session_state.decrypted}`")
                        st.balloons()
                    else:
                        st.error(f"❌ Decryption failed!")
                        st.write(f"Expected: `{st.session_state.original_message}`")
                        st.write(f"Got: `{st.session_state.decrypted}`")
        else:
            st.info("👈 Use the sidebar controls to encrypt a message")
        
        # Performance Analysis (only for multiple keys mode)
        if st.session_state.mode == "multiple" and 'keys_to_compare' in st.session_state:
            st.markdown("---")
            st.subheader("📈 Performance Analysis")
            
            keys_to_compare = st.session_state.keys_to_compare
            
            if len(keys_to_compare) >= 2:
                # Prepare data for visualization
                sizes = []
                gen_times = []
                classical_times = []
                quantum_times = []
                security_scores = []
                
                for size in keys_to_compare:
                    data = st.session_state.generated_keys[size]
                    sizes.append(size)
                    gen_times.append(data['keygen_time'])
                    
                    classical = estimate_classical_attack_time(size, "GNFS")
                    quantum = get_shors_time(size)
                    
                    classical_times.append(math.log10(max(1, classical['time_seconds'])))
                    quantum_times.append(math.log10(max(1, quantum['time_seconds'])))
                    
                    # Security score
                    if size < 1024:
                        score = 1
                    elif size < 2048:
                        score = 3
                    elif size < 3072:
                        score = 7
                    else:
                        score = 9
                    security_scores.append(score)
                
                # Create visualizations
                sns.set_style("whitegrid")
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                
                # 1. Generation Time
                colors = ['red' if s < 2048 else 'orange' if s < 3072 else 'green' for s in sizes]
                bars = axes[0, 0].bar([str(s) for s in sizes], gen_times, color=colors, alpha=0.7)
                axes[0, 0].set_xlabel('Key Size (bits)')
                axes[0, 0].set_ylabel('Generation Time (seconds)')
                axes[0, 0].set_title('Key Generation Performance')
                axes[0, 0].tick_params(axis='x', rotation=45)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                                   f'{height:.3f}s', ha='center', va='bottom', fontsize=9)
                
                # 2. Attack Time Comparison
                axes[0, 1].plot(sizes, classical_times, 'o-', linewidth=2, markersize=8, label='Classical (GNFS)')
                axes[0, 1].plot(sizes, quantum_times, 's-', linewidth=2, markersize=8, label='Quantum (Shor)')
                axes[0, 1].set_xlabel('Key Size (bits)')
                axes[0, 1].set_ylabel('Log₁₀(Attack Time in seconds)')
                axes[0, 1].set_title('Attack Time Scaling')
                axes[0, 1].legend()
                axes[0, 1].grid(True, alpha=0.3)
                
                # 3. Security Score
                scatter = axes[1, 0].scatter(sizes, security_scores, 
                                           c=security_scores, cmap='RdYlGn', 
                                           s=200, alpha=0.7, edgecolors='black')
                axes[1, 0].set_xlabel('Key Size (bits)')
                axes[1, 0].set_ylabel('Security Score (1-10)')
                axes[1, 0].set_title('Security Level')
                axes[1, 0].set_yticks(range(1, 11))
                axes[1, 0].grid(True, alpha=0.3)
                
                # Add labels
                for i, (size, score) in enumerate(zip(sizes, security_scores)):
                    status = 'Insecure' if score <= 3 else 'Weak' if score <= 5 else 'Secure' if score <= 7 else 'Strong'
                    axes[1, 0].annotate(status, (size, score), 
                                       xytext=(5, 5), textcoords='offset points',
                                       fontsize=9, fontweight='bold')
                
                # 4. Time vs Security Trade-off
                axes[1, 1].scatter(gen_times, security_scores, s=150, alpha=0.7, c=colors, edgecolors='black')
                axes[1, 1].set_xlabel('Generation Time (seconds)')
                axes[1, 1].set_ylabel('Security Score (1-10)')
                axes[1, 1].set_title('Time vs Security Trade-off')
                axes[1, 1].grid(True, alpha=0.3)
                
                # Add labels
                for i, (gen_time, score, size) in enumerate(zip(gen_times, security_scores, sizes)):
                    axes[1, 1].annotate(f'{size}-bit', (gen_time, score), 
                                       xytext=(5, 5), textcoords='offset points',
                                       fontsize=9)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Recommendations
                st.markdown("""
                <div class='info-box'>
                <h4>🎯 Recommendations Based on Comparison</h4>
                
                **Best Choices:**
                - **For testing/learning**: Smallest key for fastest generation
                - **For production**: RSA-2048 (balance of speed & security)
                - **For long-term security**: RSA-3072 or RSA-4096
                
                **Key Insights:**
                - Generation time increases ~2x when doubling key size
                - Security increases exponentially with key size
                - Quantum attacks reduce security by polynomial factor
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Select at least 2 keys in the sidebar to compare performance")
    
    else:
        # Initial state - no keys generated yet
        st.markdown("---")
        st.subheader("🚀 Getting Started")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='demo-section'>
            <h4>🎯 Quick Start</h4>
            <ol>
            <li>Go to the <strong>sidebar on the left</strong></li>
            <li>Select <strong>"Single Key"</strong> or <strong>"Multiple Keys"</strong> mode</li>
            <li>Choose your key size(s)</li>
            <li>Click the <strong>Generate</strong> button</li>
            <li>Results will appear here automatically</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='demo-section'>
            <h4>🔐 RSA Key Size Guide</h4>
            
            **Recommended Sizes:**
            - **1024-bit**: For testing only (insecure)
            - **2048-bit**: Minimum for production
            - **3072-bit**: Recommended for new systems
            - **4096-bit**: Maximum practical size
            
            **Generation Time Estimates:**
            - RSA-1024: ~0.01-0.05 seconds
            - RSA-2048: ~0.05-0.15 seconds
            - RSA-3072: ~0.15-0.30 seconds
            - RSA-4096: ~0.30-0.60 seconds
            </div>
            """, unsafe_allow_html=True)
        
        # Show example of what will be displayed
        st.markdown("---")
        st.subheader("📊 Example Output (After Generation)")
        
        with st.expander("Click to see what will be displayed"):
            st.write("""
            **After generating keys, you'll see:**
            
            1. **Key Information**: Size, generation time, security metrics
            2. **Security Analysis**: Classical vs quantum attack times
            3. **Key Details**: Public/private keys and prime factors
            4. **Encryption/Decryption**: Test messages and verification
            5. **Performance Charts**: Comparison of different key sizes
            
            **Example Metrics:**
            - Key Size: 2048 bits
            - Generation Time: 0.125 seconds
            - Classical Security: 10⁸⁰ operations (centuries)
            - Quantum Attack: 8,000 ms (8 seconds)
            """)

# -------------------------------
# QUANTUM BB84 DEMO
# -------------------------------
elif demo_selection == "⚛️ Quantum BB84":
    st.title("⚛️ Quantum BB84 Key Distribution")
    st.markdown("Quantum cryptography with unconditional security")
    
    # BB84 Functions
    def encode_qubit(bit, basis):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)
        return qc
    
    def measure_qubit(qc, basis):
        if basis == 1:
            qc.h(0)
        qc.measure(0, 0)
        backend = AerSimulator()
        job = backend.run(qc, shots=1, memory=True, noise_model=None)
        return int(job.result().get_memory()[0])
    
    def draw_bloch_sphere(bit, basis, title="Qubit State"):
        fig, ax = plt.subplots(figsize=(5, 5))
        circle = Circle((0, 0), 1, fill=False, linewidth=2, color='black')
        ax.add_patch(circle)
        
        if basis == 0:
            ax.quiver(0, 0, 0, 0.8, color='red', scale=1, scale_units='xy', angles='xy')
            ax.quiver(0, 0, 0, -0.8, color='red', scale=1, scale_units='xy', angles='xy')
            ax.text(0, 0.9, '|0⟩', color='red', ha='center', fontsize=12)
            ax.text(0, -0.9, '|1⟩', color='red', ha='center', fontsize=12)
            x, y = (0, 0.8) if bit == 0 else (0, -0.8)
        else:
            ax.quiver(0, 0, 0.566, 0.566, color='blue', scale=1, scale_units='xy', angles='xy')
            ax.quiver(0, 0, -0.566, -0.566, color='blue', scale=1, scale_units='xy', angles='xy')
            ax.text(0.7, 0.7, '|+⟩', color='blue', ha='center', fontsize=12)
            ax.text(-0.7, -0.7, '|-⟩', color='blue', ha='center', fontsize=12)
            x, y = (0.566, 0.566) if bit == 0 else (-0.566, -0.566)
        
        ax.scatter(x, y, s=150, color='green', edgecolors='black', zorder=5)
        state_name = '|0⟩' if (basis==0 and bit==0) else '|1⟩' if (basis==0 and bit==1) else '|+⟩' if (basis==1 and bit==0) else '|-⟩'
        ax.text(x, y+0.1, state_name, color='green', ha='center', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=12)
        ax.axis('off')
        return fig
    
    # Sidebar controls for BB84
    st.sidebar.header("BB84 Parameters")
    num_bits = st.sidebar.slider("Number of Qubits", 10, 50, 30, 5, key="bb84_bits")

    # Change from decimal to percentage
    eve_rate_percent = st.sidebar.slider("Eavesdropping Rate", 0, 100, 30, 10, key="bb84_eve")
    eve_rate = eve_rate_percent / 100  # Convert to decimal for calculations

    show_bloch = st.sidebar.checkbox("Show Bloch Spheres", True, key="bb84_bloch")
    
    # Initialize session state
    if 'bb84_run' not in st.session_state:
        st.session_state.bb84_run = False
    
    # Run BB84 simulation
    if st.sidebar.button("▶️ Run BB84 Simulation", type="primary", key="bb84_run_btn"):
        with st.spinner("Running quantum simulation..."):
            # Generate random bits and bases
            alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
            alice_bases = [random.randint(0, 1) for _ in range(num_bits)]
            bob_bases = [random.randint(0, 1) for _ in range(num_bits)]
            bob_results = []
            eve_intercepted = []
            
            # Process each qubit - use eve_rate (already converted from percentage)
            for i in range(num_bits):
                qc = encode_qubit(alice_bits[i], alice_bases[i])
                intercepted = False
                
                if random.random() < eve_rate:  # eve_rate is now decimal (0.3 for 30%)
                    intercepted = True
                    eve_basis = random.randint(0, 1)
                    eve_bit = measure_qubit(qc.copy(), eve_basis)
                    qc = encode_qubit(eve_bit, eve_basis)
                
                eve_intercepted.append(intercepted)
                bob_results.append(measure_qubit(qc, bob_bases[i]))
            
            # Sifting
            sifted_alice = []
            sifted_bob = []
            matching_indices = []
            
            for i in range(num_bits):
                if alice_bases[i] == bob_bases[i]:
                    sifted_alice.append(alice_bits[i])
                    sifted_bob.append(bob_results[i])
                    matching_indices.append(i)
            
            # Calculate QBER
            errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
            qber = errors / len(sifted_alice) if sifted_alice else 0
            
            # Store results
            st.session_state.update({
                'bb84_alice_bits': alice_bits,
                'bb84_alice_bases': alice_bases,
                'bb84_bob_bases': bob_bases,
                'bb84_bob_results': bob_results,
                'bb84_sifted_alice': sifted_alice,
                'bb84_sifted_bob': sifted_bob,
                'bb84_qber': qber,
                'bb84_eve_intercepted': eve_intercepted,
                'bb84_matching_indices': matching_indices,
                'bb84_run': True
            })
    
    # Display results
    if st.session_state.bb84_run:
        apply_custom_styles()

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Qubits", num_bits)
        with col2:
            st.metric("Matching Bases", len(st.session_state.bb84_sifted_alice))
        with col3:
            key_length = len(st.session_state.bb84_sifted_alice) // 2
            st.metric("Key Length", key_length)
        with col4:
            st.metric("QBER", f"{st.session_state.bb84_qber:.2%}")
            # Display Eve Rate as percentage
            st.caption(f"Eve Rate: {eve_rate_percent}%")
            if st.session_state.bb84_qber > 0.11:
                st.error("Eavesdropping likely!")
        
        # Generated key
        if st.session_state.bb84_sifted_alice:
            key = st.session_state.bb84_sifted_alice[:key_length]
            st.subheader("🔑 Generated Quantum Key")
            key_str = ''.join(str(bit) for bit in key)
            st.code(key_str)

        # Transmission Legends
        st.subheader("🧾 Legend")

        st.markdown(f"""
        <div style="display:flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
        <div style="display:flex; align-items: center; gap: 8px;"><b>✅ Match</b>: Alice & Bob used same basis</div>
        <div style="display:flex; align-items: center; gap: 8px;"><b>❌ Mismatch</b>: Different bases (discarded)</div>
        <div style="display:flex; align-items: center; gap: 8px;"><b>⚠️ Eve</b>: Qubit intercepted ({eve_rate_percent}% rate)</div>
        </div>
        """, unsafe_allow_html=True)

        # Transmission Visualization
        st.subheader("📡 Qubit Transmission Visualization")

        # Show ALL qubits
        display_bits = num_bits

        table_data = []
        for i in range(display_bits):
            alice_basis = st.session_state.bb84_alice_bases[i]
            bob_basis = st.session_state.bb84_bob_bases[i]
            alice_bit = st.session_state.bb84_alice_bits[i]
            bob_result = st.session_state.bb84_bob_results[i]
            basis_match = alice_basis == bob_basis
            eve = st.session_state.bb84_eve_intercepted[i]
            
            # Check for errors
            has_error = basis_match and alice_bit != bob_result
            
            # Simplify the status icons
            if eve:
                status = "⚠️ Eve"
            elif not basis_match:
                status = "❌ Mismatch"
            elif has_error:
                status = "❌ Error"
            else:
                status = "✅ Good"
            
            # Simplify the display format
            table_data.append({
                "Qubit": i + 1,
                "Alice": f"{alice_bit} ({'Z' if alice_basis == 0 else 'X'})",
                "Bob": f"{bob_result} ({'Z' if bob_basis == 0 else 'X'})",
                "Match": "✅" if basis_match else "❌",
                "Eve": "⚠️" if eve else "—",
                "Status": status
            })

        # Create dataframe
        df = pd.DataFrame(table_data)

        # Display as a clean table
        st.dataframe(
            df,
            column_config={
                "Qubit": st.column_config.NumberColumn(width="small"),
                "Alice": "Alice (bit, basis)",
                "Bob": "Bob (bit, basis)",
                "Match": "Bases Match",
                "Eve": "Eve Intercept",
                "Status": "Status"
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )

        # Add summary statistics below the table
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            eve_count = sum(st.session_state.bb84_eve_intercepted)
            st.metric("Eve Interceptions", f"{eve_count}/{num_bits}", f"{eve_count/num_bits:.0%}")

        with col2:
            match_count = sum(st.session_state.bb84_alice_bases[i] == st.session_state.bb84_bob_bases[i] 
                            for i in range(num_bits))
            st.metric("Matching Bases", f"{match_count}/{num_bits}", f"{match_count/num_bits:.0%}")

        with col3:
            if match_count > 0:
                error_count = 0
                for i in range(num_bits):
                    if (st.session_state.bb84_alice_bases[i] == st.session_state.bb84_bob_bases[i] and
                        st.session_state.bb84_alice_bits[i] != st.session_state.bb84_bob_results[i]):
                        error_count += 1
                st.metric("Errors", f"{error_count}/{match_count}", 
                        f"{error_count/match_count:.0%}" if match_count > 0 else "0%")
            else:
                st.metric("Errors", "0/0", "N/A")
        
        # Bloch sphere visualization
        if show_bloch and st.session_state.bb84_run:
            st.subheader("🎯 Qubit State Visualization")
            qubit_idx = st.selectbox("Select qubit:", range(1, min(10, num_bits)+1)) - 1
            
            col_a, col_b = st.columns(2)
            with col_a:
                fig = draw_bloch_sphere(
                    st.session_state.bb84_alice_bits[qubit_idx],
                    st.session_state.bb84_alice_bases[qubit_idx],
                    "Alice's Encoding"
                )
                st.pyplot(fig)
            with col_b:
                fig = draw_bloch_sphere(
                    st.session_state.bb84_bob_results[qubit_idx],
                    st.session_state.bb84_bob_bases[qubit_idx],
                    "Bob's Measurement"
                )
                st.pyplot(fig)
            
            if st.session_state.bb84_eve_intercepted[qubit_idx]:
                st.warning(f"⚠️ Eve intercepted Qubit {qubit_idx+1}!")
        
        # -------------------------------
        # Qubit Disturbance Visualization
        # -------------------------------
        st.subheader("🧬 Qubit Disturbance Analysis")

        # Modern dark-themed scatter plot
        errors = []
        categories = []  # 0=Correct, 1=Error, 2=Eve Error, 3=Mismatch

        for i in range(num_bits):
            if st.session_state.bb84_alice_bases[i] == st.session_state.bb84_bob_bases[i]:
                if st.session_state.bb84_eve_intercepted[i]:
                    # Eve intercepted and caused error
                    categories.append(2)
                else:
                    # No eve, check if bits match
                    if st.session_state.bb84_alice_bits[i] == st.session_state.bb84_bob_results[i]:
                        categories.append(0)  # Correct
                    else:
                        categories.append(1)  # Natural error
            else:
                categories.append(3)  # Basis mismatch

        # Create dark-themed plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={'width_ratios': [3, 1]})

        # Set dark theme
        fig.patch.set_facecolor('#0F172A')
        ax1.set_facecolor('#0F172A')
        ax2.set_facecolor('#0F172A')

        # Modern color palette for dark theme
        colors = ['#10B981', '#3B82F6', '#EF4444', '#6B7280']
        labels = ['Correct', 'Natural Error', 'Eve Error', 'Basis Mismatch']

        # Create scatter plot with modern styling
        for i in range(num_bits):
            color = colors[categories[i]]
            ax1.scatter(i+1, categories[i], color=color, s=100, 
                        alpha=0.9, edgecolor='white', linewidth=1.5, zorder=2)

        # Customize main plot
        ax1.set_xlim(0, num_bits+1)
        ax1.set_ylim(-0.5, 3.5)
        ax1.set_yticks([0, 1, 2, 3])
        ax1.set_yticklabels(labels, fontsize=11, fontweight='medium', color='#E5E7EB')
        ax1.set_xlabel('Qubit Index', fontsize=12, fontweight='medium', color='#9CA3AF', labelpad=10)
        ax1.set_title('Quantum Transmission Error Analysis', 
                    fontsize=15, fontweight='bold', color='#FFFFFF', pad=20)

        # Customize grid and spines
        ax1.grid(True, alpha=0.1, color='#374151', linestyle='--', linewidth=0.5)
        ax1.spines['top'].set_color('#374151')
        ax1.spines['right'].set_color('#374151')
        ax1.spines['left'].set_color('#374151')
        ax1.spines['bottom'].set_color('#374151')

        # Set tick colors
        ax1.tick_params(colors='#9CA3AF', labelsize=10)

        # Add subtle gradient background
        ax1.axhspan(0, 0.5, alpha=0.05, color='#10B981', zorder=0)
        ax1.axhspan(1, 1.5, alpha=0.05, color='#3B82F6', zorder=0)
        ax1.axhspan(2, 2.5, alpha=0.05, color='#EF4444', zorder=0)
        ax1.axhspan(3, 3.5, alpha=0.05, color='#6B7280', zorder=0)

        # Create modern legend plot
        ax2.axis('off')

        # Add legend title
        ax2.text(0.5, 0.95, 'LEGEND', transform=ax2.transAxes,
                fontsize=14, fontweight='bold', color='#FFFFFF',
                ha='center', va='center')

        # Add legend items
        legend_y = 0.8
        legend_height = 0.12
        spacing = 0.14

        for i, (color, label) in enumerate(zip(colors, labels)):
            y_pos = legend_y - (i * spacing)
            
            # Add colored circle
            circle = plt.Circle((0.2, y_pos), 0.04, color=color, transform=ax2.transAxes)
            ax2.add_patch(circle)
            
            # Add white edge to circle
            circle_edge = plt.Circle((0.2, y_pos), 0.04, color='white', fill=False, 
                                linewidth=1, transform=ax2.transAxes, alpha=0.5)
            ax2.add_patch(circle_edge)
            
            # Add label
            ax2.text(0.35, y_pos, label, transform=ax2.transAxes,
                    fontsize=11, fontweight='medium', color='#E5E7EB',
                    va='center')

        # Add counts for each category
        counts = [categories.count(0), categories.count(1), 
                categories.count(2), categories.count(3)]

        for i, count in enumerate(counts):
            y_pos = legend_y - (i * spacing)
            ax2.text(0.85, y_pos, f'{count}', transform=ax2.transAxes,
                    fontsize=11, fontweight='bold', color=colors[i],
                    ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#1E293B", 
                            edgecolor=colors[i], alpha=0.7, linewidth=1.5))

        # Add summary text
        summary_text = f"Total Qubits: {num_bits}\n"
        summary_text += f"Secure Bits: {counts[0]} ({counts[0]/num_bits:.1%})\n"
        summary_text += f"Eve Errors: {counts[2]} ({counts[2]/num_bits:.1%})"

        ax2.text(0.5, 0.25, summary_text, transform=ax2.transAxes,
                fontsize=10, color='#9CA3AF', ha='center', va='top',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#1E293B", 
                        edgecolor="#374151", alpha=0.8))

        plt.tight_layout()
        st.pyplot(fig)

        # -------------------------------
        # QBER vs Eavesdropping Rate (Dark Theme)
        # -------------------------------
        st.subheader("🔍 Eavesdropping Detection Analysis")

        # Generate data for the visualization (simulated data for the trend line)
        rates_percent = [i * 10 for i in range(11)]  # 0%, 10%, 20%, ..., 100%
        rates_decimal = [r/100 for r in rates_percent]  # Convert to decimal for simulation
        qbers_simulated = []  # Renamed for clarity

        # Run simulations for trend line
        for rate in rates_decimal:
            test_bits = 80
            alice_b = [random.randint(0, 1) for _ in range(test_bits)]
            alice_bs = [random.randint(0, 1) for _ in range(test_bits)]
            bob_bs = [random.randint(0, 1) for _ in range(test_bits)]
            bob_r = []

            for i in range(test_bits):
                qc = encode_qubit(alice_b[i], alice_bs[i])
                if random.random() < rate:
                    eve_b = random.randint(0, 1)
                    eve_bit = measure_qubit(qc.copy(), eve_b)
                    qc = encode_qubit(eve_bit, eve_b)
                bob_r.append(measure_qubit(qc, bob_bs[i]))

            sifted_a = [alice_b[i] for i in range(test_bits) if alice_bs[i] == bob_bs[i]]
            sifted_b = [bob_r[i] for i in range(test_bits) if alice_bs[i] == bob_bs[i]]
            err = sum(a != b for a, b in zip(sifted_a, sifted_b))
            qbers_simulated.append(err / len(sifted_a) if sifted_a else 0)

        # Get ACTUAL QBER from your simulation
        current_qber_value = st.session_state.bb84_qber  # This is your actual simulation's QBER

        # Create modern dark-themed visualization
        fig, ax = plt.subplots(figsize=(11, 6))

        # Set dark theme
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')

        # Create smooth gradient line - use percentage for x-axis
        x_smooth = np.linspace(0, 100, 100)  # Now 0-100%
        x_original = rates_percent
        y_original = qbers_simulated
        y_smooth = np.interp(x_smooth, x_original, y_original)

        # Plot gradient line with neon effect (using percentage x-axis)
        line = ax.plot(x_smooth, y_smooth, color='#3B82F6', linewidth=4, alpha=0.9, zorder=2,
                    label='Simulated QBER Trend')[0]
        line.set_path_effects([
            patheffects.Stroke(linewidth=6, foreground='#1D4ED8', alpha=0.3),
            patheffects.Stroke(linewidth=8, foreground='#1E40AF', alpha=0.1),
            patheffects.Normal()
        ])

        # Add scatter points with glow effect (using percentage x-axis)
        for x, y in zip(rates_percent, qbers_simulated):
            ax.scatter(x, y, s=200, color='#60A5FA', edgecolor='white', 
                    linewidth=2, zorder=3, alpha=0.9)

        # Add glow effect around points
        for x, y in zip(rates_percent, qbers_simulated):
            ax.scatter(x, y, s=400, color='#60A5FA', alpha=0.1, zorder=1)

        # Add security threshold with modern styling
        ax.axhline(0.11, color='#EF4444', linestyle='--', linewidth=2.5, 
                alpha=0.9, label='Security Threshold (11%)', zorder=1)

        # Calculate expected QBER for current Eve rate based on trend
        # Find the nearest simulated point to get expected QBER
        expected_qber_idx = min(int(eve_rate_percent / 10), len(qbers_simulated)-1)
        expected_qber = qbers_simulated[expected_qber_idx]

        # Use ACTUAL QBER from your simulation for the marker
        actual_qber = current_qber_value  # This is from st.session_state.bb84_qber

        # Glow effect for current marker
        for size, alpha in [(400, 0.2), (300, 0.3), (200, 0.4)]:
            ax.scatter(eve_rate_percent, actual_qber, s=size, color='#10B981', 
                    alpha=alpha, zorder=2)

        # Main current marker - use ACTUAL QBER
        current_marker = ax.scatter(eve_rate_percent, actual_qber, s=150, color='#10B981', 
                edgecolor='white', linewidth=3, zorder=4,
                label=f'Current: {eve_rate_percent}% Eve, {actual_qber:.1%} QBER')

        # Add annotation with ACTUAL QBER
        ax.annotate(f'Your Simulation\n{eve_rate_percent}% Eve → {actual_qber:.1%} QBER', 
                    xy=(eve_rate_percent, actual_qber), 
                    xytext=(eve_rate_percent + 10, actual_qber + 0.05),
                    fontsize=11, fontweight='bold', color='#FFFFFF',
                    arrowprops=dict(arrowstyle='->', color='#10B981', 
                                linewidth=2, alpha=0.8),
                    bbox=dict(boxstyle="round,pad=0.4", 
                            facecolor="#1E293B", 
                            edgecolor="#10B981", alpha=0.9))

        # Fill insecure region (using percentage x-axis)
        ax.fill_between(x_smooth, 0.11, y_smooth, where=(y_smooth >= 0.11), 
                        alpha=0.15, color='#EF4444', zorder=0, label='Insecure Region')

        # Also highlight if actual QBER is in insecure region
        if actual_qber > 0.11:
            # Add a vertical line to show actual QBER position
            ax.axvspan(eve_rate_percent - 2, eve_rate_percent + 2, alpha=0.2, 
                    color='#EF4444', zorder=0)

        # Customize axes with dark theme
        ax.set_xlim(-5, 105)
        ax.set_ylim(0, max(qbers_simulated) * 1.15)
        ax.set_xlabel('Eavesdropping Rate (%)', fontsize=13, fontweight='medium', 
                    color='#9CA3AF', labelpad=10)
        ax.set_ylabel('Quantum Bit Error Rate (QBER)', fontsize=13, fontweight='medium', 
                    color='#9CA3AF', labelpad=10)

        # Customize ticks
        ax.tick_params(colors='#9CA3AF', labelsize=11)
        ax.set_xticks(np.arange(0, 101, 10))
        ax.set_xticklabels([f'{int(x)}%' for x in np.arange(0, 101, 10)])
        # Format y-axis as percentage
        ax.set_yticks(np.arange(0, 0.51, 0.05))
        ax.set_yticklabels([f'{int(y*100)}%' for y in np.arange(0, 0.51, 0.05)])

        # Customize spines
        for spine in ax.spines.values():
            spine.set_color('#374151')
            spine.set_linewidth(1)

        # Add title
        ax.set_title('Quantum Security: Eavesdropping Detection via QBER', 
                    fontsize=16, fontweight='bold', color='#FFFFFF', pad=20)

        # Create custom legend handles
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D

        legend_elements = [
            Line2D([0], [0], color='#3B82F6', linewidth=4, label='Simulated QBER Trend'),
            Line2D([0], [0], color='#EF4444', linestyle='--', linewidth=2.5, 
                label='Security Threshold (11%)'),
            Line2D([0], [0], color='none', marker='o', markerfacecolor='#10B981', 
                markersize=10, markeredgecolor='white', markeredgewidth=2,
                label=f'Current: {eve_rate_percent}% Eve, {actual_qber:.1%} QBER'),
            Patch(facecolor='#EF4444', alpha=0.15, edgecolor='#EF4444', 
                label='Insecure Region (QBER > 11%)')
        ]

        # Add legend with dark theme
        legend = ax.legend(handles=legend_elements, loc='upper left', frameon=True, 
                        framealpha=0.95, edgecolor='#374151', fontsize=11, 
                        facecolor='#1E293B', title='Legend', title_fontsize=12)
        legend.get_frame().set_linewidth(1)
        for text in legend.get_texts():
            text.set_color('#E5E7EB')
        legend.get_title().set_color('#FFFFFF')

        # Add subtle grid
        ax.grid(True, alpha=0.1, linestyle='--', linewidth=0.7, color='#374151')

        # Add security status indicators
        status_y = max(qbers_simulated) * 1.05
        if actual_qber < 0.11:
            status_color = '#10B981'
            status_text = '🔒 SECURE COMMUNICATION'
            # Add explanation for secure status
            ax.text(eve_rate_percent + 12, actual_qber - 0.02, 
                    f"QBER ({actual_qber:.1%}) < 11%\nEavesdropping not detected",
                    fontsize=10, color='#10B981', alpha=0.8,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#1E293B", 
                            edgecolor='#10B981', alpha=0.5))
        else:
            status_color = '#EF4444'
            status_text = '⚠️ EAVESDROPPING DETECTED'
            # Add explanation for compromised status
            ax.text(eve_rate_percent + 12, actual_qber + 0.02, 
                    f"QBER ({actual_qber:.1%}) > 11%\nEavesdropping likely!",
                    fontsize=10, color='#EF4444', alpha=0.8,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#1E293B", 
                            edgecolor='#EF4444', alpha=0.5))

        ax.text(0.5, status_y, status_text, transform=ax.transAxes,
                fontsize=12, fontweight='bold', color=status_color,
                ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#1E293B", 
                        edgecolor=status_color, alpha=0.8, linewidth=2))

        # Add comparison text
        if abs(actual_qber - expected_qber) > 0.02:  # If difference is significant
            diff = actual_qber - expected_qber
            if diff > 0:
                diff_text = f"Your QBER is {abs(diff):.1%} higher than expected"
                diff_color = '#EF4444'
            else:
                diff_text = f"Your QBER is {abs(diff):.1%} lower than expected"
                diff_color = '#10B981'
            
            ax.text(0.02, 0.95, diff_text, transform=ax.transAxes,
                    fontsize=10, color=diff_color, alpha=0.8,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="#1E293B", 
                            edgecolor=diff_color, alpha=0.5))

        plt.tight_layout()
        st.pyplot(fig)

        # Add explanation about the QBER values
        with st.expander("📈 Understanding Your QBER Value", expanded=False):
            st.markdown(f"""
            **Your Simulation Results:**
            
            | Metric | Value | Explanation |
            |--------|-------|-------------|
            | **Eve Rate** | {eve_rate_percent}% | Percentage of qubits intercepted by Eve |
            | **Actual QBER** | {actual_qber:.1%} | Quantum Bit Error Rate from your simulation |
            | **Expected QBER** | {expected_qber:.1%} | Theoretical QBER for {eve_rate_percent}% Eve rate |
            | **Difference** | {actual_qber - expected_qber:+.1%} | How your result compares to expectation |
            | **Security Status** | {'✅ SECURE' if actual_qber < 0.11 else '⚠️ COMPROMISED'} | Based on 11% threshold |
            
            **Why your QBER might differ from the trend line:**
            1. **Statistical variation**: With {num_bits} qubits, random fluctuations are expected
            2. **Basis selection**: Random basis choices affect which qubits Eve intercepts
            3. **Measurement outcomes**: Quantum measurement is probabilistic
            
            **Key Insight**: Even with the same Eve rate ({eve_rate_percent}%), different runs can produce 
            slightly different QBER values due to quantum randomness and statistical variation.
            """)

# -------------------------------
# COMPARISON PAGE
# -------------------------------
elif demo_selection == "📊 Comparison":
    st.title("📊 RSA vs Quantum BB84 Comparison")
    
    tab1, tab2, tab3 = st.tabs(["Security", "Performance", "Future Outlook"])
    
    with tab1:
        st.subheader("Security Level vs Computing Power: The Quantum Cliff")

        fig, ax = plt.subplots(figsize=(10, 5))

        # RSA security curve (High security until critical point)
        comp_power = np.linspace(1, 100, 100)
        # Use a sigmoid-like or sharp drop function to simulate the "cliff"
        rsa_security = np.where(comp_power < 50, 2, 0.2) 
        bb84_security = np.ones_like(comp_power) * 2.5 # Constant high security

        ax.plot(comp_power, rsa_security, label='RSA Security (Computational)', linewidth=3, color='red')
        ax.plot(comp_power, bb84_security, label='BB84 Security (Information-Theoretic)', linewidth=3, color='green', linestyle='--')

        # Mark quantum computing threshold (the cliff)
        ax.axvline(50, color='blue', linestyle=':', label="Shor's Algorithm Threshold (Quantum Cliff)")
        ax.text(50, 1.0, 'Collapse', color='red', ha='left', fontsize=12, fontweight='bold')
        ax.fill_between([45, 55], 0, 3, alpha=0.2, color='blue')

        ax.set_xlabel('Computational Power / Quantum Capability')
        ax.set_ylabel('Security Level (Arbitrary)')
        ax.set_title('Security Foundations: Computational Cliff vs. Unconditional Security')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 3)

        st.pyplot(fig)
    
    with tab2:
        st.subheader("Key Distribution and Size Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### RSA Key Exchange
            * **Primary Key:** Asymmetric 2048/4096-bit key used for security foundation.
            * **Final Secure Key:** The RSA private key **encrypts a small symmetric session key** (e.g., 256 bits) used for the bulk data transfer (AES).
            * **Security Dependency:** If the 2048-bit key is broken by Shor's, the 256-bit session key is instantly revealed.
            """)
            
        with col2:
            st.markdown("""
            ### BB84 Key Generation
            * **Primary Key:** Ephemeral quantum states (photons) used for security foundation.
            * **Final Secure Key:** The BB84 protocol **generates a symmetric key** (e.g., up to 256 bits) bit-by-bit, guaranteed by physics.
            * **Security Dependency:** The key is **Information-Theoretically Secure**. No amount of computational power can reconstruct the key without leaving a detectable error (QBER).
            """)
        
        # Performance chart
        st.subheader("Key Generation Rate Comparison")
        
        categories = ['Key Generation', 'Encryption', 'Max Distance', 'Infrastructure Cost']
        rsa_scores = [8, 9, 1000, 6]  # Distance in km, others 1-10
        bb84_scores = [4, 5, 100, 2]   # Distance in km, others 1-10
        
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 5))
        bars1 = ax.bar(x - width/2, rsa_scores, width, label='RSA', color='red', alpha=0.7)
        bars2 = ax.bar(x + width/2, bb84_scores, width, label='BB84', color='green', alpha=0.7)
        
        ax.set_xlabel('Performance Metric')
        ax.set_ylabel('Score (1-10, except distance in km)')
        ax.set_title('Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom')
        
        st.pyplot(fig)
    
    with tab3:
        st.subheader("🚀 Future Outlook")
        
        st.markdown("""
        ### The Post-Quantum Cryptography Era
        
        **Timeline:**
        
        1. **Current State (2020s)**
           - RSA still dominant (2048-4096 bit)
           - BB84 in specialized applications
           - Quantum computers: 50-100 qubits
        
        2. **Near Future (2030s)**
           - Hybrid systems (RSA + Post-quantum)
           - Satellite QKD networks
           - NIST post-quantum standards deployed
        
        3. **Quantum Era (2040s+)**
           - Large-scale quantum computers
           - RSA deprecated
           - Quantum internet with QKD
        """)
        
        # Timeline visualization
        years = [2020, 2025, 2030, 2035, 2040, 2045]
        rsa_usage = [95, 80, 50, 20, 5, 1]
        bb84_usage = [1, 5, 15, 30, 50, 70]
        quantum_comp = [1, 10, 30, 60, 90, 100]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        ax1.plot(years, rsa_usage, marker='o', label='RSA Usage', linewidth=2, color='red')
        ax1.plot(years, bb84_usage, marker='s', label='QKD Usage', linewidth=2, color='green')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Adoption Rate (%)')
        ax1.set_title('Cryptography Adoption Timeline')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(years, quantum_comp, marker='^', label='Quantum Computer Power', linewidth=2, color='blue')
        ax2.fill_between(years, 0, quantum_comp, alpha=0.3, color='blue')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Relative Quantum Power (%)')
        ax2.set_title('Quantum Computing Advancement')
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        st.markdown("""
        ### Recommendations
        
        **For Current Applications:**
        - Use RSA-2048 or higher for classical systems
        - Plan migration to post-quantum algorithms
        - Consider hybrid approaches
        
        **For Long-term Security:**
        - Invest in QKD infrastructure
        - Develop quantum-resistant algorithms
        - Train quantum-safe cybersecurity teams
        """)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("🔐 Cryptography Demos | RSA & Quantum BB84 | Quantum Computing Educational Project")