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
    
    def get_shors_time(bits):
        # Highly simplified theoretical model demonstrating polynomial time speed-up
        if bits <= 1024:
            return 1
        elif bits <= 2048:
            return 10
        elif bits <= 4096:
            return 100
        else:
            return bits * 0.05 # Scaling up for larger keys

    # Sidebar controls for RSA
    st.sidebar.header("RSA Parameters")
    key_size = st.sidebar.selectbox(
        "Select RSA Key Size (bits)",
        [256, 512, 1024, 2048, 4096],
        key="rsa_key_size"
    )
    
    # Initialize session state
    if "rsa_keys_generated" not in st.session_state:
        st.session_state.rsa_keys_generated = False
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Key Generation")
        
        if st.button("Generate RSA Keys", type="primary", key="rsa_generate"):
            with st.spinner(f"Generating {key_size}-bit RSA keys..."):
                n, e, d, p, q, keygen_time = generate_keys(key_size)
            
            st.session_state.rsa_n = n
            st.session_state.rsa_e = e
            st.session_state.rsa_d = d
            st.session_state.rsa_p = p
            st.session_state.rsa_q = q
            st.session_state.rsa_keygen_time = keygen_time
            st.session_state.rsa_keys_generated = True
            st.success("Keys generated successfully!")
        
        if st.session_state.rsa_keys_generated:
            st.markdown("---")
            
            # Calculate Shor's time
            shors_time = get_shors_time(key_size)
            
            # --- MODIFIED METRICS (col_c replaced) ---
            col_a, col_b, col_c, col_d = st.columns(4) # Added a 4th column
            with col_a:
                st.metric("Key Size", f"{key_size} bits")
            with col_b:
                st.metric("Generation Time", f"{st.session_state.rsa_keygen_time:.4f}s")
            with col_c:
                # Classical security message
                st.metric("Classical Security", "Centuries") 
            with col_d:
                # Quantum vulnerability message
                st.metric("Quantum Attack Time", f"{shors_time} seconds", delta="Existence Threat", delta_color="inverse")

            st.markdown(f"""
            <div class='warning-box'>
            ⚠️ **Quantum Vulnerability**
            The {key_size}-bit key is only computationally secure. A hypothetical, large-scale quantum computer running **Shor's Algorithm** could break this key in approximately **{shors_time} seconds**, rendering all encrypted data compromised.
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.rsa_keys_generated:
            st.markdown("---")
            
            # Metrics
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Key Size", f"{key_size} bits")
            with col_b:
                st.metric("Generation Time", f"{st.session_state.rsa_keygen_time:.4f}s")
            with col_c:
                key_security = "⚠️ Insecure" if key_size < 2048 else "✅ Secure"
                st.metric("Security Level", key_security)
            
            # Key details
            with st.expander("🔍 View Key Details"):
                st.write(f"**Public Key (e, n):**")
                st.code(f"e = {st.session_state.rsa_e}\nn = {st.session_state.rsa_n}")
                
                st.write(f"**Private Key (d, n):**")
                st.code(f"d = {st.session_state.rsa_d}")
                
                st.write(f"**Prime Numbers:**")
                st.code(f"p = {st.session_state.rsa_p}\nq = {st.session_state.rsa_q}")
    
    with col2:
        st.subheader("Quick Info")
        st.markdown("""
        <div class='info-box'>
        <h4>⚡ RSA Facts</h4>
        <ul>
        <li>Invented in 1977 (Rivest, Shamir, Adleman)</li>
        <li>Security relies on factoring large numbers</li>
        <li>2048-bit RSA: ~10²⁰ operations to break</li>
        <li>Vulnerable to quantum computers</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if key_size < 2048:
            st.markdown("""
            <div class='warning-box'>
            ⚠️ **Security Warning**
            Keys smaller than 2048 bits are considered insecure for modern applications.
            </div>
            """, unsafe_allow_html=True)
    
    # Encryption/Decryption section
    if st.session_state.rsa_keys_generated:
        st.markdown("---")
        st.subheader("Encryption & Decryption")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("**Encrypt Message**")
            message = st.text_area("Enter message:", "Hello Quantum World!", height=100)
            
            if st.button("Encrypt", key="rsa_encrypt"):
                cipher, enc_time = encrypt(message, st.session_state.rsa_e, st.session_state.rsa_n)
                st.session_state.rsa_cipher = cipher
                st.session_state.rsa_enc_time = enc_time
                
                st.write(f"**Encryption Time:** {enc_time:.6f} seconds")
                st.write("**Ciphertext:**")
                st.code(str(cipher[:3]) + ("..." if len(cipher) > 3 else ""))
        
        with col4:
            if "rsa_cipher" in st.session_state:
                st.write("**Decrypt Message**")
                
                if st.button("Decrypt", key="rsa_decrypt"):
                    decrypted, dec_time = decrypt(
                        st.session_state.rsa_cipher,
                        st.session_state.rsa_d,
                        st.session_state.rsa_n
                    )
                    
                    st.write(f"**Decryption Time:** {dec_time:.6f} seconds")
                    st.write("**Decrypted Message:**")
                    st.success(decrypted)
        
        # Performance chart
        st.markdown("---")
        st.subheader("Performance Analysis")
        
        # Simulate different key sizes
        sizes = [256, 512, 1024, 2048, 4096]
        gen_times = []
        
        for size in sizes:
            if size == key_size and st.session_state.rsa_keys_generated:
                gen_times.append(st.session_state.rsa_keygen_time)
            else:
                # Estimate based on size
                gen_times.append(size * 0.0001 + random.uniform(0.001, 0.01))
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar([str(s) for s in sizes], gen_times, color=['red' if s < 2048 else 'green' for s in sizes])
        ax.set_xlabel('Key Size (bits)')
        ax.set_ylabel('Generation Time (seconds)')
        ax.set_title('RSA Key Generation Time vs Key Size')
        ax.axhline(y=1.0, color='orange', linestyle='--', alpha=0.5, label='1 second')
        ax.legend()
        st.pyplot(fig)

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
        job = backend.run(qc, shots=1, memory=True)
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
    num_bits = st.sidebar.slider("Number of Qubits", 10, 100, 30, 5, key="bb84_bits")
    eve_rate = st.sidebar.slider("Eavesdropping Rate", 0.0, 1.0, 0.3, 0.1, key="bb84_eve")
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
            
            # Process each qubit
            for i in range(num_bits):
                qc = encode_qubit(alice_bits[i], alice_bases[i])
                intercepted = False
                
                if random.random() < eve_rate:
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
            if st.session_state.bb84_qber > 0.11:
                st.error("Eavesdropping likely!")
        
        # Generated key
        if st.session_state.bb84_sifted_alice:
            key = st.session_state.bb84_sifted_alice[:key_length]
            st.subheader("🔑 Generated Quantum Key")
            key_str = ''.join(str(bit) for bit in key)
            st.code(key_str)
        
        # Transmission table
        st.subheader("📊 Transmission Details")
        display_bits = min(20, num_bits)
        df_data = []
        
        for i in range(display_bits):
            df_data.append({
                'Qubit': i+1,
                'Alice Bit': st.session_state.bb84_alice_bits[i],
                'Alice Basis': 'Z' if st.session_state.bb84_alice_bases[i] == 0 else 'X',
                'Bob Basis': 'Z' if st.session_state.bb84_bob_bases[i] == 0 else 'X',
                'Bob Result': st.session_state.bb84_bob_results[i],
                'Match': '✓' if st.session_state.bb84_alice_bases[i] == st.session_state.bb84_bob_bases[i] else '✗',
                'Eve': '✓' if st.session_state.bb84_eve_intercepted[i] else '✗'
            })
        
        st.dataframe(pd.DataFrame(df_data), use_container_width=True)
        
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
        
        # QBER Analysis
        st.subheader("📈 QBER vs Eavesdropping Rate")
        rates = [i/10 for i in range(11)]
        qbers = []
        
        for rate in rates:
            # Quick simulation
            test_bits = 50
            alice_b = [random.randint(0,1) for _ in range(test_bits)]
            alice_bs = [random.randint(0,1) for _ in range(test_bits)]
            bob_bs = [random.randint(0,1) for _ in range(test_bits)]
            bob_r = []
            
            for i in range(test_bits):
                qc = encode_qubit(alice_b[i], alice_bs[i])
                if random.random() < rate:
                    eve_b = random.randint(0,1)
                    eve_bit = measure_qubit(qc.copy(), eve_b)
                    qc = encode_qubit(eve_bit, eve_b)
                bob_r.append(measure_qubit(qc, bob_bs[i]))
            
            sifted_a = [alice_b[i] for i in range(test_bits) if alice_bs[i] == bob_bs[i]]
            sifted_b = [bob_r[i] for i in range(test_bits) if alice_bs[i] == bob_bs[i]]
            err = sum(a != b for a,b in zip(sifted_a, sifted_b))
            qbers.append(err/len(sifted_a) if sifted_a else 0)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(rates, qbers, marker='o', linewidth=2)
        ax.axhline(0.11, color='red', linestyle='--', label='Security Threshold (11%)')
        ax.axvline(eve_rate, color='green', linestyle=':', label=f'Current Eve Rate ({eve_rate:.1f})')
        ax.fill_between(rates, 0.11, 0.5, alpha=0.2, color='red', label='Insecure Region')
        ax.set_xlabel('Eavesdropping Rate')
        ax.set_ylabel('QBER')
        ax.set_title('BB84: Eavesdropping Detection via QBER')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0, 0.5)
        st.pyplot(fig)
    
    else:
        # Instructions
        st.info("👈 Configure parameters and click 'Run BB84 Simulation' to start!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='info-box'>
            <h4>⚛️ BB84 Protocol</h4>
            <ul>
            <li>First quantum cryptography protocol (1984)</li>
            <li>Unconditional security via quantum mechanics</li>
            <li>Detects eavesdropping via QBER</li>
            <li>Information-theoretically secure</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='info-box'>
            <h4>🎯 How It Works</h4>
            <ol>
            <li>Alice sends qubits in random bases</li>
            <li>Bob measures in random bases</li>
            <li>Public discussion to keep matching bases</li>
            <li>Check QBER for eavesdropping</li>
            <li>Generate secure key</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)

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