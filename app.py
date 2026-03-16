import streamlit as st
from bank import (
    create_account,
    deposit,
    withdraw,
    get_details,
    update_details,
    delete_account,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --ink:   #0d0d0d;
    --paper: #f5f0e8;
    --gold:  #c9a84c;
    --rust:  #b84a2e;
    --mist:  #d6cfbf;
    --white: #fefcf8;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--paper) !important;
    font-family: 'DM Mono', monospace;
    color: var(--ink);
}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(circle at 15% 10%, rgba(201,168,76,0.08) 0%, transparent 45%),
        radial-gradient(circle at 85% 90%, rgba(184,74,46,0.07) 0%, transparent 40%);
}
[data-testid="stHeader"] { display: none; }

.hero { text-align:center; padding:2.5rem 0 1.5rem; border-bottom:2px solid var(--ink); margin-bottom:2rem; }
.hero-bank { font-family:'DM Serif Display',serif; font-size:3.4rem; letter-spacing:-1px; line-height:1; color:var(--ink); }
.hero-bank span { color:var(--gold); font-style:italic; }
.hero-tagline { font-size:0.72rem; letter-spacing:0.25em; text-transform:uppercase; color:#666; margin-top:0.4rem; }

.card { background:var(--white); border:1.5px solid var(--ink); border-radius:2px; padding:1.8rem 2rem; box-shadow:4px 4px 0 var(--ink); margin-bottom:1.5rem; }
.card-title { font-family:'DM Serif Display',serif; font-size:1.4rem; margin-bottom:1.2rem; border-bottom:1px solid var(--mist); padding-bottom:0.6rem; display:flex; align-items:center; gap:0.5rem; }

.alert-success { background:#e8f5e2; border-left:4px solid #4caf50; padding:0.8rem 1rem; border-radius:2px; font-size:0.88rem; margin-top:1rem; }
.alert-error   { background:#fce8e4; border-left:4px solid var(--rust); padding:0.8rem 1rem; border-radius:2px; font-size:0.88rem; margin-top:1rem; }
.alert-info    { background:#fff8e6; border-left:4px solid var(--gold); padding:0.8rem 1rem; border-radius:2px; font-size:0.88rem; margin-top:1rem; }

.detail-row   { display:flex; justify-content:space-between; padding:0.45rem 0; border-bottom:1px dashed var(--mist); font-size:0.88rem; }
.detail-label { color:#777; text-transform:uppercase; font-size:0.7rem; letter-spacing:0.1em; }
.detail-value { font-weight:500; }
.balance-big  { font-family:'DM Serif Display',serif; font-size:2.2rem; color:var(--ink); text-align:center; padding:0.5rem 0 0.2rem; }
.balance-label{ text-align:center; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; color:#999; }

.stButton > button {
    font-family:'DM Mono',monospace !important; font-size:0.78rem !important;
    letter-spacing:0.08em; text-transform:uppercase;
    border:1.5px solid var(--ink) !important; border-radius:2px !important;
    background:var(--white) !important; color:var(--ink) !important;
    padding:0.45rem 1rem !important; transition:all 0.15s;
}
.stButton > button:hover { background:var(--ink) !important; color:var(--paper) !important; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border:1.5px solid var(--mist) !important; border-radius:2px !important;
    background:var(--white) !important; font-family:'DM Mono',monospace !important;
    font-size:0.9rem !important; color:var(--ink) !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color:var(--ink) !important; box-shadow:2px 2px 0 var(--ink) !important;
}
label { font-size:0.75rem !important; letter-spacing:0.05em; text-transform:uppercase; color:#555 !important; }

hr { border:none; border-top:1px solid var(--mist); margin:1rem 0; }
.footer { text-align:center; font-size:0.68rem; color:#aaa; letter-spacing:0.12em; padding:2rem 0 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-bank">Nov<span>Bank</span></div>
    <div class="hero-tagline">Private Banking · Est. 2025</div>
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
pages = ["🏠 Home", "➕ Open Account", "💰 Deposit", "🏧 Withdraw",
         "📋 My Details", "✏️ Update", "🗑️ Close Account"]
cols = st.columns(len(pages))
for i, (col, pg) in enumerate(zip(cols, pages)):
    if col.button(pg, key=f"nav_{i}"):
        st.session_state.page = pg.split(" ", 1)[1]

st.markdown("<hr>", unsafe_allow_html=True)
page = st.session_state.page

# ── Home ──────────────────────────────────────────────────────────────────────
if "Home" in page:
    st.markdown("""
    <div class="card">
        <div class="card-title">🏦 Welcome to NovBank</div>
        <p style="font-size:0.9rem;line-height:1.7;color:#444;">
            A secure, streamlined personal banking experience.
            Open an account in seconds, manage your funds, and stay in control — all from one place.
        </p>
        <div style="margin-top:1.2rem;display:flex;gap:2rem;flex-wrap:wrap;">
            <div style="flex:1;min-width:120px;">
                <div style="font-size:1.8rem;font-family:'DM Serif Display',serif;">03</div>
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#888;">Simple Steps to Open</div>
            </div>
            <div style="flex:1;min-width:120px;">
                <div style="font-size:1.8rem;font-family:'DM Serif Display',serif;">₹10k</div>
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#888;">Daily Deposit Limit</div>
            </div>
            <div style="flex:1;min-width:120px;">
                <div style="font-size:1.8rem;font-family:'DM Serif Display',serif;">18+</div>
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#888;">Minimum Age</div>
            </div>
        </div>
    </div>
    <div class="alert-info">ℹ️ Use the navigation above to access all banking services.</div>
    """, unsafe_allow_html=True)

# ── Open Account ──────────────────────────────────────────────────────────────
elif "Open Account" in page:
    st.markdown('<div class="card"><div class="card-title">➕ Open New Account</div>', unsafe_allow_html=True)
    name  = st.text_input("Full Name")
    age   = st.number_input("Age", min_value=1, max_value=120, step=1)
    email = st.text_input("Email Address")
    pin   = st.text_input("4-Digit PIN", type="password", max_chars=4)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Create Account"):
        if not name or not email or not pin:
            st.markdown('<div class="alert-error">❌ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            ok, msg, info = create_account(name, int(age), email, pin)
            if not ok:
                st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-success">✅ {msg}</div>
                <div class="card" style="margin-top:1rem;">
                    <div class="card-title">Your Account Details</div>
                    <div class="detail-row"><span class="detail-label">Name</span><span class="detail-value">{info['Name']}</span></div>
                    <div class="detail-row"><span class="detail-label">Account No</span><span class="detail-value">{info['AccountNo']}</span></div>
                    <div class="detail-row"><span class="detail-label">Email</span><span class="detail-value">{info['Email']}</span></div>
                    <div class="detail-row"><span class="detail-label">Age</span><span class="detail-value">{info['Age']}</span></div>
                </div>
                <div class="alert-info">📌 Note your Account Number: <strong>{info['AccountNo']}</strong></div>
                """, unsafe_allow_html=True)

# ── Deposit ───────────────────────────────────────────────────────────────────
elif "Deposit" in page:
    st.markdown('<div class="card"><div class="card-title">💰 Deposit Money</div>', unsafe_allow_html=True)
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amt = st.number_input("Amount (₹)", min_value=1, step=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Deposit"):
        ok, msg, balance = deposit(acc, int(pin) if pin.isdigit() else -1, int(amt))
        if not ok:
            st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-success">✅ {msg}</div>
            <div class="card" style="margin-top:1rem;">
                <div class="balance-label">Current Balance</div>
                <div class="balance-big">₹{balance:,}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Withdraw ──────────────────────────────────────────────────────────────────
elif "Withdraw" in page:
    st.markdown('<div class="card"><div class="card-title">🏧 Withdraw Money</div>', unsafe_allow_html=True)
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amt = st.number_input("Amount (₹)", min_value=1, step=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Withdraw"):
        ok, msg, balance = withdraw(acc, int(pin) if pin.isdigit() else -1, int(amt))
        if not ok:
            st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-success">✅ {msg}</div>
            <div class="card" style="margin-top:1rem;">
                <div class="balance-label">Remaining Balance</div>
                <div class="balance-big">₹{balance:,}</div>
            </div>
            """, unsafe_allow_html=True)

# ── My Details ────────────────────────────────────────────────────────────────
elif "Details" in page:
    st.markdown('<div class="card"><div class="card-title">📋 Account Details</div>', unsafe_allow_html=True)
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("View Details"):
        ok, msg, u = get_details(acc, int(pin) if pin.isdigit() else -1)
        if not ok:
            st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card" style="margin-top:1rem;">
                <div class="balance-label">Available Balance</div>
                <div class="balance-big">₹{u['Balance']:,}</div>
                <hr>
                <div class="detail-row"><span class="detail-label">Name</span><span class="detail-value">{u['Name']}</span></div>
                <div class="detail-row"><span class="detail-label">Account No</span><span class="detail-value">{u['AccountNo']}</span></div>
                <div class="detail-row"><span class="detail-label">Email</span><span class="detail-value">{u['Email']}</span></div>
                <div class="detail-row"><span class="detail-label">Age</span><span class="detail-value">{u['Age']}</span></div>
            </div>
            """, unsafe_allow_html=True)

# ── Update Details ────────────────────────────────────────────────────────────
elif "Update" in page:
    st.markdown('<div class="card"><div class="card-title">✏️ Update Account Details</div>', unsafe_allow_html=True)
    acc = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password", max_chars=4)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Load Account"):
        ok, msg, _ = get_details(acc, int(pin) if pin.isdigit() else -1)
        if not ok:
            st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            st.session_state["edit_acc"] = acc
            st.session_state["edit_pin"] = pin

    if "edit_acc" in st.session_state:
        _, _, u = get_details(
            st.session_state["edit_acc"],
            int(st.session_state["edit_pin"]) if st.session_state["edit_pin"].isdigit() else -1,
        )
        if u:
            st.markdown('<div class="card"><div class="card-title">New Values (leave blank to keep current)</div>', unsafe_allow_html=True)
            new_name  = st.text_input("New Name",  placeholder=u["Name"])
            new_email = st.text_input("New Email", placeholder=u["Email"])
            new_pin   = st.text_input("New PIN",   type="password", max_chars=4)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Save Changes"):
                ok, msg = update_details(
                    st.session_state["edit_acc"],
                    int(st.session_state["edit_pin"]),
                    new_name  or None,
                    new_email or None,
                    new_pin   or None,
                )
                if not ok:
                    st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
                else:
                    del st.session_state["edit_acc"]
                    del st.session_state["edit_pin"]
                    st.markdown(f'<div class="alert-success">✅ {msg}</div>', unsafe_allow_html=True)

# ── Close Account ─────────────────────────────────────────────────────────────
elif "Close Account" in page:
    st.markdown('<div class="card"><div class="card-title">🗑️ Close Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-error" style="margin-bottom:1rem;">⚠️ This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)
    acc     = st.text_input("Account Number")
    pin     = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will permanently delete my account")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Delete Account"):
        if not confirm:
            st.markdown('<div class="alert-error">❌ Please check the confirmation box.</div>', unsafe_allow_html=True)
        else:
            ok, msg = delete_account(acc, int(pin) if pin.isdigit() else -1)
            if not ok:
                st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-success">✅ {msg}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    NOVBANK · PRIVATE & SECURE · ALL TRANSACTIONS LOCALLY STORED<br>
    © 2025 NovBank. For demonstration purposes only.
</div>
""", unsafe_allow_html=True)