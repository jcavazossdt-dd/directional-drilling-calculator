import streamlit as st
import math

st.set_page_config(page_title="Oilfield Directional Drilling Calculator", layout="wide")
st.title("🛢️ Directional Drilling Formula Solver")
st.markdown("**Full app for ALL formulas in your Directional_Drilling_Formulas.docx** • Enter values • Click Calculate • Results appear instantly")
st.caption("Built by Grok • Zero extra setup beyond: `pip install streamlit` then `streamlit run directional_drilling_app.py`")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📐 1. Survey Calculations",
    "📈 2. Build/Drop/Turn Rate",
    "🔧 3. Hydraulics",
    "🔄 4. Torque & Drag",
    "🌀 5. Bit & Motor Performance",
    "🛤️ 6. Wellpath Planning",
    "⚖️ 7. Miscellaneous"
])

# ===================== TAB 1: SURVEY =====================
with tab1:
    st.subheader("Dogleg Severity (DLS °/100ft)")
    col1, col2 = st.columns(2)
    with col1:
        dmd = st.number_input("ΔMD (ft)", value=100.0, step=1.0)
        i1 = st.number_input("Inc1 (°) [I₁]", value=0.0, step=0.1)
        az1 = st.number_input("Az1 (°) [Az₁]", value=0.0, step=0.1)
    with col2:
        i2 = st.number_input("Inc2 (°) [I₂]", value=3.0, step=0.1)
        az2 = st.number_input("Az2 (°) [Az₂]", value=10.0, step=0.1)
    
    if st.button("Calculate DLS", type="primary"):
        try:
            cos_term = math.cos(math.radians(i1)) * math.cos(math.radians(i2)) + \
                       math.sin(math.radians(i1)) * math.sin(math.radians(i2)) * math.cos(math.radians(az2 - az1))
            cos_term = max(min(cos_term, 1.0), -1.0)
            dls = (57.3 / dmd) * math.degrees(math.acos(cos_term))
            st.success(f"**Dogleg Severity = {dls:.3f} °/100ft**")
        except:
            st.error("Invalid input (check angles)")

    st.divider()
    st.subheader("Minimum Curvature Method (one survey interval)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        mc_dmd = st.number_input("ΔMD (ft)", value=100.0, key="mc_dmd")
        mc_i1 = st.number_input("I₁ (°)", value=0.0, key="mc_i1")
        mc_az1 = st.number_input("Az₁ (°)", value=0.0, key="mc_az1")
    with col_b:
        mc_i2 = st.number_input("I₂ (°)", value=3.0, key="mc_i2")
        mc_az2 = st.number_input("Az₂ (°)", value=10.0, key="mc_az2")
        prev_n = st.number_input("Previous Northing (ft)", value=0.0)
        prev_e = st.number_input("Previous Easting (ft)", value=0.0)
    with col_c:
        prev_tvd = st.number_input("Previous TVD (ft)", value=0.0)
        if st.button("Calculate Min Curvature", type="primary", key="mc_btn"):
            try:
                delta_theta_rad = math.acos(
                    math.cos(math.radians(mc_i1)) * math.cos(math.radians(mc_i2)) +
                    math.sin(math.radians(mc_i1)) * math.sin(math.radians(mc_i2)) * math.cos(math.radians(mc_az2 - mc_az1))
                )
                rf = (2 / delta_theta_rad) * math.tan(delta_theta_rad / 2) if delta_theta_rad != 0 else 1.0
                
                delta_n = (mc_dmd / 2) * (math.sin(math.radians(mc_i1)) * math.cos(math.radians(mc_az1)) +
                                         math.sin(math.radians(mc_i2)) * math.cos(math.radians(mc_az2))) * rf
                delta_e = (mc_dmd / 2) * (math.sin(math.radians(mc_i1)) * math.sin(math.radians(mc_az1)) +
                                         math.sin(math.radians(mc_i2)) * math.sin(math.radians(mc_az2))) * rf
                delta_v = (mc_dmd / 2) * (math.cos(math.radians(mc_i1)) + math.cos(math.radians(mc_i2))) * rf
                
                new_n = prev_n + delta_n
                new_e = prev_e + delta_e
                new_tvd = prev_tvd + delta_v
                hd = math.sqrt(new_n**2 + new_e**2)
                
                st.success(f"""
                **ΔNorth = {delta_n:.2f} ft** **ΔEast = {delta_e:.2f} ft** **ΔTVD = {delta_v:.2f} ft**  
                **New TVD = {new_tvd:.1f} ft** **Horizontal Departure = {hd:.1f} ft**
                """)
            except:
                st.error("Check inputs")

# ===================== TAB 2: BUILD/DROP/TURN =====================
with tab2:
    st.subheader("Build Rate & Turn Rate")
    c1, c2, c3 = st.columns(3)
    with c1:
        inc1 = st.number_input("Inc₁ (°)", value=0.0)
        inc2 = st.number_input("Inc₂ (°)", value=5.0)
        dmd_br = st.number_input("ΔMD (ft)", value=100.0, key="dmd_br")
    with c2:
        az1_br = st.number_input("Az₁ (°)", value=0.0)
        az2_br = st.number_input("Az₂ (°)", value=15.0)
        if st.button("Calculate BR & TR", type="primary"):
            br = (inc2 - inc1) / dmd_br * 100
            tr = (az2_br - az1_br) / dmd_br * 100
            st.success(f"**Build Rate = {br:.2f} °/100ft** **Turn Rate = {tr:.2f} °/100ft**")
    with c3:
        st.info("Use negative values for Drop Rate")

# ===================== TAB 3: HYDRAULICS =====================
with tab3:
    st.subheader("Annular Velocity • Jet Impact • Hydraulic HP")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        q = st.number_input("Flow Rate Q (gpm)", value=500.0)
        dh = st.number_input("Hole Diameter Dh (in)", value=12.25)
        dp = st.number_input("Pipe OD Dp (in)", value=5.0)
        if st.button("AV", key="av_btn"):
            av = (24.5 * q) / (dh**2 - dp**2)
            st.success(f"**Annular Velocity = {av:.1f} ft/min**")
        
        delta_p = st.number_input("Pressure Drop ΔP (psi)", value=1200.0, key="dp")
        q_jet = st.number_input("Q (gpm) for Jet", value=500.0)
        if st.button("Jet Impact Force"):
            f = 0.01823 * q_jet * delta_p
            st.success(f"**Jet Impact Force = {f:.1f} lbf**")
    
    with col_h2:
        p_hhp = st.number_input("Standpipe Pressure P (psi)", value=3000.0)
        q_hhp = st.number_input("Q (gpm) for HHP", value=500.0)
        if st.button("Hydraulic Horsepower"):
            hhp = (p_hhp * q_hhp) / 1714
            st.success(f"**HHP = {hhp:.1f}**")

# ===================== TAB 4: TORQUE & DRAG =====================
with tab4:
    st.subheader("Drag Force & Torque")
    w = st.number_input("Weight W (lbf)", value=50000.0)
    mu = st.number_input("Friction μ", value=0.25)
    theta = st.number_input("Inclination θ (°)", value=60.0)
    r = st.number_input("Radius r (ft) – usually pipe radius", value=0.208)  # 5" pipe example
    
    if st.button("Calculate Drag & Torque", type="primary"):
        fd = w * mu * math.cos(math.radians(theta))
        t = fd * r
        st.success(f"**Drag Force Fd = {fd:,.0f} lbf** **Torque T = {t:.1f} ft-lbf**")

# ===================== TAB 5: BIT & MOTOR =====================
with tab5:
    st.subheader("RPM & Power")
    c5a, c5b = st.columns(2)
    with c5a:
        rpm_rot = st.number_input("Rotary RPM", value=60.0)
        rpm_rev = st.number_input("Motor Revs/1000 psi (spec)", value=4.5)
        delta_p_motor = st.number_input("Motor ΔP (psi)", value=800.0)
        rpm_motor = (rpm_rev * delta_p_motor) / 1000   # as per doc
        bit_rpm = rpm_rot + rpm_motor
        st.success(f"**Motor RPM = {rpm_motor:.1f}** **Bit RPM = {bit_rpm:.1f}**")
    
    with c5b:
        eff = st.number_input("Motor Efficiency (decimal)", value=0.85)
        q_motor = st.number_input("Flow Q (gpm)", value=400.0)
        hp = (delta_p_motor * q_motor * eff) / 1714
        st.success(f"**Motor Power = {hp:.1f} HP**")

# ===================== TAB 6: WELLPATH PLANNING =====================
with tab6:
    st.subheader("Radius • Build Length • Turn Length")
    dls_r = st.number_input("DLS (°/100ft)", value=3.0)
    if st.button("Radius of Curvature"):
        r_curv = (180 * 100) / (math.pi * dls_r)
        st.success(f"**Radius R = {r_curv:,.0f} ft**")
    
    col6a, col6b = st.columns(2)
    with col6a:
        delta_inc = st.number_input("ΔInc (°)", value=30.0)
        br_l = st.number_input("Build Rate (°/100ft)", value=3.0)
        lbuild = (delta_inc / br_l) * 100
        st.success(f"**Build-Up Length = {lbuild:.0f} ft**")
    with col6b:
        delta_az = st.number_input("ΔAz (°)", value=90.0)
        tr_l = st.number_input("Turn Rate (°/100ft)", value=2.0)
        lturn = (delta_az / tr_l) * 100
        st.success(f"**Turn Length = {lturn:.0f} ft**")

# ===================== TAB 7: MISCELLANEOUS =====================
with tab7:
    st.subheader("Kill Mud Weight & Pressure Gradient")
    p_shut = st.number_input("Shut-in Pressure (psi)", value=1200.0)
    tvd_kill = st.number_input("TVD (ft)", value=10000.0)
    mw_curr = st.number_input("Current MW (ppg)", value=9.5)
    if st.button("Kill Mud Weight"):
        mw_kill = (p_shut * 0.052) / tvd_kill + mw_curr
        st.success(f"**Kill MW = {mw_kill:.2f} ppg**")
    
    mw_pg = st.number_input("Mud Weight for Gradient (ppg)", value=10.0)
    pg = 0.052 * mw_pg
    st.success(f"**Pressure Gradient = {pg:.3f} psi/ft**")
